import argparse
import pandas as pd
from utils import merge_dataframes, get_unique_user_count, sample_random_users, filter_users_by_purchase_range, filter_baskets_by_depth_range, filter_users_by_basket_count_range, filter_by_product_assortment, split_history_future


def show_menu():
    print("\n=== NBR Restrictor - Data Limitation Menu ===")
    print("1. Sample random users")
    print("2. Filter by basket count per user (min-max)")
    print("3. Filter by items per basket (min-max)")
    print("4. Show current dataset statistics")
    print("5. Save and exit")
    print("0. Exit without saving")
    return input("Choose an option: ").strip()


def show_stats(df, user_col, basket_col):
    if len(df) == 0:
        print("Dataset is empty!")
        return
    
    users = get_unique_user_count(df, user_col)
    total_records = len(df)
    
    print(f"\n=== Current Dataset Statistics ===")
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


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer")
        except ValueError:
            print("Please enter a valid integer")


def get_range(item_name):
    min_val = get_positive_int(f"Enter minimum {item_name}: ")
    while True:
        max_val = get_positive_int(f"Enter maximum {item_name}: ")
        if max_val >= min_val:
            return min_val, max_val
        else:
            print(f"Maximum must be >= {min_val}")


def main():
    parser = argparse.ArgumentParser(description='NBR Restrictor - Dataset User Sampling Tool')
    parser.add_argument('history_file', help='Path to history dataset file')
    parser.add_argument('future_file', help='Path to future dataset file')
    parser.add_argument('--user-col', default='user_id', help='Name of user column (default: user_id)')
    parser.add_argument('--basket-col', default='order_number', help='Name of basket column (default: order_number)')
    parser.add_argument('--product-col', default='product_id', help='Name of product column (default: product_id)')
    
    args = parser.parse_args()
    
    # Merge the datasets
    print(f"Merging {args.history_file} and {args.future_file}...")
    df = merge_dataframes(args.history_file, args.future_file)
    print(f"Loaded dataset with {len(df)} records and {get_unique_user_count(df, args.user_col)} unique users")
    
    # Menu loop
    while True:
        choice = show_menu()
        
        if choice == '1':  # Sample random users
            current_users = get_unique_user_count(df, args.user_col)
            if current_users == 0:
                print("No users in dataset!")
                continue
                
            print(f"Current users: {current_users}")
            while True:
                try:
                    n_users = int(input(f"How many users to keep? (max {current_users}): "))
                    if 1 <= n_users <= current_users:
                        break
                    else:
                        print(f"Please enter a number between 1 and {current_users}")
                except ValueError:
                    print("Please enter a valid integer")
            
            df = sample_random_users(df, n_users, args.user_col)
            print(f"Sampled {n_users} random users. Dataset now has {len(df)} records.")
            
        elif choice == '2':  # Filter by basket count per user
            if len(df) == 0:
                print("Dataset is empty!")
                continue
            if args.basket_col not in df.columns:
                print(f"Column '{args.basket_col}' not found in dataset!")
                continue
                
            show_stats(df, args.user_col, args.basket_col)
            min_baskets, max_baskets = get_range("baskets per user")
            
            original_users = get_unique_user_count(df, args.user_col)
            df = filter_users_by_basket_count_range(df, min_baskets, max_baskets, args.user_col, args.basket_col)
            new_users = get_unique_user_count(df, args.user_col)
            
            print(f"Filtered from {original_users} to {new_users} users with {min_baskets}-{max_baskets} baskets each")
            
        elif choice == '3':  # Filter by items per basket
            if len(df) == 0:
                print("Dataset is empty!")
                continue
            if args.basket_col not in df.columns:
                print(f"Column '{args.basket_col}' not found in dataset!")
                continue
                
            show_stats(df, args.user_col, args.basket_col)
            min_items, max_items = get_range("items per basket")
            
            # Create temp df to count unique baskets correctly
            df_temp = df.copy()
            df_temp['unique_basket_id'] = df_temp[args.user_col].astype(str) + '_' + df_temp[args.basket_col].astype(str)
            original_baskets = df_temp['unique_basket_id'].nunique()
            
            df = filter_baskets_by_depth_range(df, min_items, max_items, args.basket_col, args.user_col)
            
            df_temp = df.copy()
            df_temp['unique_basket_id'] = df_temp[args.user_col].astype(str) + '_' + df_temp[args.basket_col].astype(str)
            new_baskets = df_temp['unique_basket_id'].nunique()
            
            print(f"Filtered from {original_baskets} to {new_baskets} baskets with {min_items}-{max_items} items each")
            
        elif choice == '4':  # Show statistics
            show_stats(df, args.user_col, args.basket_col)
            
        elif choice == '5':  # Save and exit
            if len(df) == 0:
                print("Cannot save empty dataset!")
                continue
                
            # Get dataset name from user
            dataset_name = input("Enter dataset name (e.g., 'tafeng_few_customers'): ").strip()
            if not dataset_name:
                print("Dataset name cannot be empty!")
                continue
                
            # Split data into history and future
            history_df, future_df = split_history_future(df, args.user_col, args.basket_col)
            
            # Save the results
            history_file = f"output/{dataset_name}_history.csv"
            future_file = f"output/{dataset_name}_future.csv"
            
            history_df.to_csv(history_file, index=False)
            future_df.to_csv(future_file, index=False)
            
            print(f"\nDatasets saved:")
            print(f"History: {history_file} ({len(history_df)} records)")
            print(f"Future: {future_file} ({len(future_df)} records)")
            show_stats(df, args.user_col, args.basket_col)
            print("Done!")
            break
            
        elif choice == '0':  # Exit without saving
            print("Exiting without saving.")
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
