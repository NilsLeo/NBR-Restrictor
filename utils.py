import pandas as pd


def merge_dataframes(history_file_path, future_file_path):
    """
    Merge two dataframes from CSV file paths.
    
    Args:
        history_file_path (str): Path to the history CSV file
        future_file_path (str): Path to the future CSV file
    
    Returns:
        pd.DataFrame: Merged dataframe containing both history and future data
    """
    # Load the CSV files
    history_df = pd.read_csv(history_file_path)
    future_df = pd.read_csv(future_file_path)
    
    # Concatenate the dataframes
    merged_df = pd.concat([history_df, future_df], ignore_index=True)
    
    return merged_df


def sample_random_users(df, n_users, user_col='user_id'):
    """
    Sample n random users from a dataframe and return only their data.
    
    Args:
        df (pd.DataFrame): Input dataframe
        n_users (int): Number of random users to sample
        user_col (str): Name of the user column (default: 'user_id')
    
    Returns:
        pd.DataFrame: Filtered dataframe containing only data from sampled users
    """
    # Get unique users
    unique_users = df[user_col].unique()
    
    # Sample n random users
    sampled_users = pd.Series(unique_users).sample(n=min(n_users, len(unique_users)), random_state=42)
    
    # Filter dataframe to only include sampled users
    filtered_df = df[df[user_col].isin(sampled_users)]
    
    return filtered_df


def get_unique_user_count(df, user_col='user_id'):
    """
    Get the number of unique users in a dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        user_col (str): Name of the user column (default: 'user_id')
    
    Returns:
        int: Number of unique users
    """
    return df[user_col].nunique()


def filter_users_by_purchase_range(df, min_purchases, max_purchases, user_col='user_id'):
    """
    Filter dataframe to keep only users within a specified purchase count range.
    
    Args:
        df (pd.DataFrame): Input dataframe
        min_purchases (int): Minimum number of purchases per user
        max_purchases (int): Maximum number of purchases per user
        user_col (str): Name of the user column (default: 'user_id')
    
    Returns:
        pd.DataFrame: Filtered dataframe containing only users within the purchase range
    """
    # Count purchases per user
    user_purchase_counts = df.groupby(user_col).size()
    
    # Get users within the specified range
    users_in_range = user_purchase_counts[
        (user_purchase_counts >= min_purchases) & 
        (user_purchase_counts <= max_purchases)
    ].index
    
    # Filter dataframe to only include users in range
    filtered_df = df[df[user_col].isin(users_in_range)]
    
    return filtered_df


def filter_baskets_by_depth_range(df, min_items, max_items, basket_col='order_number', user_col='user_id'):
    """
    Filter dataframe to keep only baskets within a specified item count range.
    
    Args:
        df (pd.DataFrame): Input dataframe
        min_items (int): Minimum number of items per basket
        max_items (int): Maximum number of items per basket
        basket_col (str): Name of the basket column (default: 'order_number')
        user_col (str): Name of the user column (default: 'user_id')
    
    Returns:
        pd.DataFrame: Filtered dataframe containing only baskets within the item range
    """
    # Count items per basket (group by both user and order number)
    basket_item_counts = df.groupby([user_col, basket_col]).size()
    
    # Get baskets within the specified range
    baskets_in_range = basket_item_counts[
        (basket_item_counts >= min_items) & 
        (basket_item_counts <= max_items)
    ].index
    
    # Filter dataframe to only include baskets in range
    # Create a mask based on the (user_id, order_number) combinations
    mask = df.set_index([user_col, basket_col]).index.isin(baskets_in_range)
    filtered_df = df[mask].reset_index(drop=True)
    
    return filtered_df


def filter_users_by_basket_count_range(df, min_baskets, max_baskets, user_col='user_id', basket_col='basket_id'):
    """
    Filter dataframe to keep only users within a specified basket count range.
    
    Args:
        df (pd.DataFrame): Input dataframe
        min_baskets (int): Minimum number of baskets per user
        max_baskets (int): Maximum number of baskets per user
        user_col (str): Name of the user column (default: 'user_id')
        basket_col (str): Name of the basket column (default: 'basket_id')
    
    Returns:
        pd.DataFrame: Filtered dataframe containing only users within the basket count range
    """
    # Count baskets per user
    user_basket_counts = df.groupby(user_col)[basket_col].nunique()
    
    # Get users within the specified range
    users_in_range = user_basket_counts[
        (user_basket_counts >= min_baskets) & 
        (user_basket_counts <= max_baskets)
    ].index
    
    # Filter dataframe to only include users in range
    filtered_df = df[df[user_col].isin(users_in_range)]
    
    return filtered_df


def filter_by_product_assortment(df, n_products, product_col='product_id', basket_col='basket_id'):
    """
    Filter dataframe to keep only N randomly sampled products and remove any baskets 
    that contain products not in the sampled set (preserves basket integrity).
    
    Args:
        df (pd.DataFrame): Input dataframe
        n_products (int): Number of products to keep
        product_col (str): Name of the product column (default: 'product_id')
        basket_col (str): Name of the basket column (default: 'basket_id')
    
    Returns:
        pd.DataFrame: Filtered dataframe with complete baskets containing only sampled products
    """
    # Get unique products and sample N random ones
    unique_products = df[product_col].unique()
    sampled_products = pd.Series(unique_products).sample(n=min(n_products, len(unique_products)), random_state=42)
    sampled_products_set = set(sampled_products)
    
    # Find baskets that contain ONLY sampled products
    basket_products = df.groupby(basket_col)[product_col].apply(set)
    valid_baskets = basket_products[basket_products.apply(lambda x: x.issubset(sampled_products_set))].index
    
    # Filter dataframe to only include valid baskets
    filtered_df = df[df[basket_col].isin(valid_baskets)]
    
    return filtered_df


def split_history_future(df, user_col='user_id', basket_col='order_number'):
    """
    Split dataframe into history and future based on most recent order per user.
    Only includes users who have at least 2 orders (so they have both history and future).
    
    Args:
        df (pd.DataFrame): Input dataframe
        user_col (str): Name of the user column (default: 'user_id')
        basket_col (str): Name of the order column (default: 'order_number')
    
    Returns:
        tuple: (history_df, future_df) - history contains all but most recent order per user,
               future contains only the most recent order per user.
               Both datasets contain the same set of users.
    """
    if df.empty:
        return df.copy(), df.copy()
    
    # First, filter to only include users with at least 2 orders
    # This ensures every user has both history and future data
    user_order_counts = df.groupby(user_col)[basket_col].nunique()
    users_with_multiple_orders = user_order_counts[user_order_counts >= 2].index
    
    # Filter out users with only one order
    df_filtered = df[df[user_col].isin(users_with_multiple_orders)].copy()
    
    if df_filtered.empty:
        print("Warning: No users with multiple orders found. Cannot create history/future split.")
        return df.copy(), df.copy()
    
    original_users = df[user_col].nunique()
    filtered_users = df_filtered[user_col].nunique()
    
    if original_users > filtered_users:
        print(f"Filtered out {original_users - filtered_users} users with only 1 order")
        print(f"Remaining users: {filtered_users} (all have ≥2 orders)")
    
    # Find the most recent order for each user (assuming highest order_number is most recent)
    most_recent_orders = df_filtered.groupby(user_col)[basket_col].max()
    
    # Create boolean mask for future orders using vectorized operations
    # Merge the max order info back to the original dataframe
    df_with_max = df_filtered.merge(
        most_recent_orders.reset_index().rename(columns={basket_col: 'max_order'}),
        on=user_col,
        how='left'
    )
    
    # Create mask for future orders (where current order equals max order for the user)
    future_mask = df_with_max[basket_col] == df_with_max['max_order']
    
    # Split data - both datasets will have the same users now
    future_df = df_with_max[future_mask].drop(columns='max_order').reset_index(drop=True)
    history_df = df_with_max[~future_mask].drop(columns='max_order').reset_index(drop=True)
    
    # Verify that both datasets contain the same set of users
    future_users = set(future_df[user_col].unique())
    history_users = set(history_df[user_col].unique())
    
    if history_users != future_users:
        print(f"Warning: User mismatch detected in split_history_future")
        print(f"Future users: {len(future_users)}")
        print(f"History users: {len(history_users)}")
        print(f"Users only in future: {future_users - history_users}")
        print(f"Users only in history: {history_users - future_users}")
    else:
        print(f"Success: Both history and future contain the same {len(future_users)} users")
    
    return history_df, future_df