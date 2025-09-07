import argparse
import pandas as pd
import os
from utils import merge_dataframes, get_unique_user_count, sample_random_users, filter_users_by_purchase_range, filter_baskets_by_depth_range, filter_users_by_basket_count_range, filter_by_product_assortment, split_history_future


def show_stats(df, user_col, basket_col):
    if len(df) == 0:
        print("Dataset is empty!")
        return
    
    users = get_unique_user_count(df, user_col)
    total_records = len(df)
    
    print(f"\n=== Dataset Statistics ===")
    print(f"Total records: {total_records}")
    print(f"Unique users: {users}")
    
    if users > 0:
        avg_purchases = total_records / users
        print(f"Average purchases per user: {avg_purchases:.2f}")
        
        if basket_col in df.columns and df[basket_col].nunique() > 0:
            # Create unique basket identifier by combining user_id and order_number
            df_temp = df.copy()
            df_temp['unique_basket_id'] = df_temp[user_col].astype(str) + '_' + df_temp[basket_col].astype(str)
            unique_baskets = df_temp['unique_basket_id'].nunique()
            avg_baskets_per_user = df.groupby(user_col)[basket_col].nunique().mean()
            avg_items_per_basket = total_records / unique_baskets
            
            print(f"Unique baskets: {unique_baskets}")
            print(f"Average baskets per user: {avg_baskets_per_user:.2f}")
            print(f"Average items per basket: {avg_items_per_basket:.2f}")
        
        # Show product count if there's a product column
        product_cols = ['product_id', 'item_id', 'productId', 'itemId']
        for col in product_cols:
            if col in df.columns:
                unique_products = df[col].nunique()
                print(f"Unique products: {unique_products}")
                break


def main():
    parser = argparse.ArgumentParser(description='NBR Restrictor - Dataset User Sampling Tool')
    parser.add_argument('history_file', help='Path to history dataset file')
    parser.add_argument('future_file', help='Path to future dataset file')
    parser.add_argument('output_name', help='Output dataset name (without extension)')
    
    # Column configuration
    parser.add_argument('--user-col', default='user_id', help='Name of user column (default: user_id)')
    parser.add_argument('--basket-col', default='order_number', help='Name of basket column (default: order_number)')
    parser.add_argument('--product-col', default='product_id', help='Name of product column (default: product_id)')
    
    # Filtering options
    parser.add_argument('--sample-users', type=int, help='Number of random users to sample')
    parser.add_argument('--min-baskets', type=int, help='Minimum baskets per user')
    parser.add_argument('--max-baskets', type=int, help='Maximum baskets per user')
    parser.add_argument('--min-items', type=int, help='Minimum items per basket')
    parser.add_argument('--max-items', type=int, help='Maximum items per basket')
    
    # Options
    parser.add_argument('--stats', action='store_true', help='Show dataset statistics')
    parser.add_argument('--output-dir', default='output', help='Output directory (default: output)')
    
    args = parser.parse_args()
    
    # Merge the datasets
    print(f"Loading datasets...")
    df = merge_dataframes(args.history_file, args.future_file)
    print(f"Loaded dataset with {len(df)} records and {get_unique_user_count(df, args.user_col)} unique users")
    
    # Show initial stats if requested
    if args.stats:
        show_stats(df, args.user_col, args.basket_col)
    
    # Apply filters in order
    
    # 1. Sample random users if specified
    if args.sample_users:
        current_users = get_unique_user_count(df, args.user_col)
        if args.sample_users > current_users:
            print(f"Warning: Requested {args.sample_users} users, but only {current_users} available. Using all users.")
            args.sample_users = current_users
        
        df = sample_random_users(df, args.sample_users, args.user_col)
        print(f"Sampled {args.sample_users} random users. Dataset now has {len(df)} records.")
    
    # 2. Filter by basket count per user
    if args.min_baskets is not None or args.max_baskets is not None:
        if args.basket_col not in df.columns:
            print(f"Error: Column '{args.basket_col}' not found in dataset!")
            return
        
        min_baskets = args.min_baskets if args.min_baskets is not None else 1
        max_baskets = args.max_baskets if args.max_baskets is not None else float('inf')
        
        original_users = get_unique_user_count(df, args.user_col)
        df = filter_users_by_basket_count_range(df, min_baskets, max_baskets, args.user_col, args.basket_col)
        new_users = get_unique_user_count(df, args.user_col)
        
        print(f"Filtered from {original_users} to {new_users} users with {min_baskets}-{max_baskets} baskets each")
    
    # 3. Filter by items per basket
    if args.min_items is not None or args.max_items is not None:
        if args.basket_col not in df.columns:
            print(f"Error: Column '{args.basket_col}' not found in dataset!")
            return
        
        min_items = args.min_items if args.min_items is not None else 1
        max_items = args.max_items if args.max_items is not None else float('inf')
        
        # Create temp df to count unique baskets correctly
        df_temp = df.copy()
        df_temp['unique_basket_id'] = df_temp[args.user_col].astype(str) + '_' + df_temp[args.basket_col].astype(str)
        original_baskets = df_temp['unique_basket_id'].nunique()
        
        df = filter_baskets_by_depth_range(df, min_items, max_items, args.basket_col, args.user_col)
        
        df_temp = df.copy()
        df_temp['unique_basket_id'] = df_temp[args.user_col].astype(str) + '_' + df_temp[args.basket_col].astype(str)
        new_baskets = df_temp['unique_basket_id'].nunique()
        
        print(f"Filtered from {original_baskets} to {new_baskets} baskets with {min_items}-{max_items} items each")
    
    # Show final stats
    if len(df) == 0:
        print("Error: No data remaining after filtering!")
        return
    
    print("\nFinal dataset statistics:")
    show_stats(df, args.user_col, args.basket_col)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Split data into history and future
    history_df, future_df = split_history_future(df, args.user_col, args.basket_col)
    
    # Save the results
    history_file = os.path.join(args.output_dir, f"{args.output_name}_history.csv")
    future_file = os.path.join(args.output_dir, f"{args.output_name}_future.csv")
    
    history_df.to_csv(history_file, index=False)
    future_df.to_csv(future_file, index=False)
    
    print(f"\nDatasets saved:")
    print(f"History: {history_file} ({len(history_df)} records)")
    print(f"Future: {future_file} ({len(future_df)} records)")
    print("Done!")


if __name__ == "__main__":
    main()
