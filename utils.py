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
    
    Args:
        df (pd.DataFrame): Input dataframe
        user_col (str): Name of the user column (default: 'user_id')
        basket_col (str): Name of the order column (default: 'order_number')
    
    Returns:
        tuple: (history_df, future_df) - history contains all but most recent order per user,
               future contains only the most recent order per user
    """
    # Find the most recent order for each user (assuming highest order_number is most recent)
    most_recent_orders = df.groupby(user_col)[basket_col].max()
    
    # Create a function to check if a row is the most recent for its user
    def is_most_recent_order(row):
        user_id = row[user_col]
        order_num = row[basket_col]
        return most_recent_orders[user_id] == order_num
    
    # Apply the function to create a boolean mask
    future_mask = df.apply(is_most_recent_order, axis=1)
    
    # Split data
    future_df = df[future_mask].reset_index(drop=True)
    history_df = df[~future_mask].reset_index(drop=True)
    
    return history_df, future_df