#!/usr/bin/env python3
"""
NBR Restrictor - CLI tool for imposing data limitations on Next Basket Prediction datasets.

This tool analyzes datasets and allows users to apply restrictions based on the data limitations
identified in the thesis: customer count, shopping frequency, basket depth, product variety,
and temporal depth.
"""

import argparse
import json
import os
import sys
from typing import Dict, Tuple, Any
import pandas as pd
from datetime import datetime


class NBRRestrictor:
    """Main class for the NBR Restrictor CLI tool."""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.datasets = ["dunnhumby", "instacart", "tafeng"]
        
    def analyze_dataset(self, dataset_name: str) -> Dict[str, Any]:
        """Analyze a dataset to determine maximum available values for restrictions."""
        history_file = os.path.join(self.input_dir, f"{dataset_name}_history.csv")
        future_file = os.path.join(self.input_dir, f"{dataset_name}_future.csv")
        
        if not os.path.exists(history_file):
            raise FileNotFoundError(f"History file not found: {history_file}")
        
        print(f"\n📊 Analyzing {dataset_name} dataset...")
        
        # Load data
        history_df = pd.read_csv(history_file)
        future_df = pd.read_csv(future_file) if os.path.exists(future_file) else pd.DataFrame()
        
        # Combine for full analysis
        full_df = pd.concat([history_df, future_df], ignore_index=True)
        
        # Calculate metrics
        analysis = {}
        
        # 1. Customer count (Kundenanzahl)
        unique_customers = full_df['user_id'].nunique()
        analysis['max_customers'] = unique_customers
        
        # 2. Shopping frequency (Einkaufsfrequenz) - orders per customer
        orders_per_customer = full_df.groupby('user_id')['order_number'].nunique()
        analysis['max_orders_per_customer'] = orders_per_customer.max()
        analysis['min_orders_per_customer'] = orders_per_customer.min()
        analysis['avg_orders_per_customer'] = round(orders_per_customer.mean(), 2)
        
        # 3. Basket depth (Warenkorbtiefe) - items per order
        items_per_order = full_df.groupby(['user_id', 'order_number']).size()
        analysis['max_basket_depth'] = items_per_order.max()
        analysis['min_basket_depth'] = items_per_order.min()
        analysis['avg_basket_depth'] = round(items_per_order.mean(), 2)
        
        # 4. Product variety (Artikelvielfalt)
        unique_products = full_df['product_id'].nunique()
        analysis['max_products'] = unique_products
        
        # 5. Temporal depth (Zeitliche Tiefe) - unique time periods
        # For this, we'll use the number of unique order_numbers as a proxy for time periods
        unique_orders = full_df['order_number'].nunique()
        analysis['max_temporal_periods'] = unique_orders
        
        # Additional useful stats
        analysis['total_transactions'] = len(full_df)
        analysis['total_orders'] = full_df.groupby(['user_id', 'order_number']).ngroups
        
        return analysis
    
    def display_analysis(self, dataset_name: str, analysis: Dict[str, Any]):
        """Display dataset analysis in a formatted way."""
        print(f"\n{'='*50}")
        print(f"📈 Dataset Analysis: {dataset_name.upper()}")
        print(f"{'='*50}")
        print(f"🔢 Total customers: {analysis['max_customers']:,}")
        print(f"🛒 Orders per customer: {analysis['min_orders_per_customer']}-{analysis['max_orders_per_customer']} (avg: {analysis['avg_orders_per_customer']})")
        print(f"📦 Basket depth: {analysis['min_basket_depth']}-{analysis['max_basket_depth']} items (avg: {analysis['avg_basket_depth']})")
        print(f"🏷️  Product variety: {analysis['max_products']:,} unique products")
        print(f"⏰ Temporal periods: {analysis['max_temporal_periods']:,} unique time periods")
        print(f"📊 Total transactions: {analysis['total_transactions']:,}")
        print(f"🛍️  Total orders: {analysis['total_orders']:,}")
    
    def get_user_restrictions(self, dataset_name: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Prompt user for restriction values."""
        print(f"\n{'='*60}")
        print(f"🎯 Configure Data Limitations for {dataset_name.upper()}")
        print(f"{'='*60}")
        print("Based on your thesis data limitations, please specify how much data to keep:")
        print("(Enter values between the minimum and maximum available)")
        
        restrictions = {}
        
        # 1. Customer count limitation
        print(f"\n1️⃣  CUSTOMER COUNT LIMITATION (Kundenanzahl)")
        print(f"   Available: {analysis['max_customers']:,} customers")
        while True:
            try:
                max_customers = int(input(f"   How many customers to keep? (1-{analysis['max_customers']}): "))
                if 1 <= max_customers <= analysis['max_customers']:
                    restrictions['max_customers'] = max_customers
                    break
                else:
                    print(f"   ❌ Please enter a number between 1 and {analysis['max_customers']}")
            except ValueError:
                print("   ❌ Please enter a valid number")
        
        # 2. Shopping frequency limitation  
        print(f"\n2️⃣  SHOPPING FREQUENCY LIMITATION (Einkaufsfrequenz)")
        print(f"   Available: {analysis['min_orders_per_customer']}-{analysis['max_orders_per_customer']} orders per customer")
        while True:
            try:
                min_orders = int(input(f"   Minimum orders per customer to keep? ({analysis['min_orders_per_customer']}-{analysis['max_orders_per_customer']}): "))
                if analysis['min_orders_per_customer'] <= min_orders <= analysis['max_orders_per_customer']:
                    restrictions['min_orders_per_customer'] = min_orders
                    break
                else:
                    print(f"   ❌ Please enter a number between {analysis['min_orders_per_customer']} and {analysis['max_orders_per_customer']}")
            except ValueError:
                print("   ❌ Please enter a valid number")
        
        # 3. Basket depth limitation
        print(f"\n3️⃣  BASKET DEPTH LIMITATION (Warenkorbtiefe)")
        print(f"   Available: {analysis['min_basket_depth']}-{analysis['max_basket_depth']} items per basket")
        while True:
            try:
                min_basket_items = int(input(f"   Minimum items per basket to keep? ({analysis['min_basket_depth']}-{analysis['max_basket_depth']}): "))
                if analysis['min_basket_depth'] <= min_basket_items <= analysis['max_basket_depth']:
                    restrictions['min_basket_items'] = min_basket_items
                    break
                else:
                    print(f"   ❌ Please enter a number between {analysis['min_basket_depth']} and {analysis['max_basket_depth']}")
            except ValueError:
                print("   ❌ Please enter a valid number")
        
        # 4. Product variety limitation
        print(f"\n4️⃣  PRODUCT VARIETY LIMITATION (Artikelvielfalt)")
        print(f"   Available: {analysis['max_products']:,} unique products")
        while True:
            try:
                max_products = int(input(f"   How many products to keep? (1-{analysis['max_products']}): "))
                if 1 <= max_products <= analysis['max_products']:
                    restrictions['max_products'] = max_products
                    break
                else:
                    print(f"   ❌ Please enter a number between 1 and {analysis['max_products']}")
            except ValueError:
                print("   ❌ Please enter a valid number")
        
        # 5. Temporal depth limitation
        print(f"\n5️⃣  TEMPORAL DEPTH LIMITATION (Zeitliche Tiefe)")
        print(f"   Available: {analysis['max_temporal_periods']:,} time periods")
        while True:
            try:
                max_periods = int(input(f"   How many time periods to keep? (1-{analysis['max_temporal_periods']}): "))
                if 1 <= max_periods <= analysis['max_temporal_periods']:
                    restrictions['max_temporal_periods'] = max_periods
                    break
                else:
                    print(f"   ❌ Please enter a number between 1 and {analysis['max_temporal_periods']}")
            except ValueError:
                print("   ❌ Please enter a valid number")
        
        return restrictions
    
    def save_config(self, dataset_name: str, analysis: Dict[str, Any], restrictions: Dict[str, Any]):
        """Save configuration to JSON file."""
        config = {
            "dataset": dataset_name,
            "timestamp": datetime.now().isoformat(),
            "original_stats": analysis,
            "restrictions": restrictions,
            "limitation_types": {
                "1": "Kundenanzahl (Customer Count)",
                "2": "Einkaufsfrequenz (Shopping Frequency)", 
                "3": "Warenkorbtiefe (Basket Depth)",
                "4": "Artikelvielfalt (Product Variety)",
                "5": "Zeitliche Tiefe (Temporal Depth)"
            },
            "description": "NBR data limitations configuration for Next Basket Prediction thesis"
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
        config_file = os.path.join(self.output_dir, f"{dataset_name}_restrictions_config.json")
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Configuration saved to: {config_file}")
        
        # Also save a summary
        self.print_config_summary(config)
    
    def print_config_summary(self, config: Dict[str, Any]):
        """Print a summary of the configuration."""
        print(f"\n{'='*60}")
        print(f"📋 RESTRICTION SUMMARY for {config['dataset'].upper()}")
        print(f"{'='*60}")
        
        restrictions = config['restrictions']
        original = config['original_stats']
        
        print(f"🔢 Customers: {restrictions['max_customers']:,} / {original['max_customers']:,} ({100*restrictions['max_customers']/original['max_customers']:.1f}%)")
        print(f"🛒 Min orders per customer: {restrictions['min_orders_per_customer']} (filtering out customers with fewer orders)")
        print(f"📦 Min basket size: {restrictions['min_basket_items']} items (filtering out smaller baskets)")
        print(f"🏷️  Products: {restrictions['max_products']:,} / {original['max_products']:,} ({100*restrictions['max_products']/original['max_products']:.1f}%)")
        print(f"⏰ Time periods: {restrictions['max_temporal_periods']:,} / {original['max_temporal_periods']:,} ({100*restrictions['max_temporal_periods']/original['max_temporal_periods']:.1f}%)")
        
    def run_interactive(self):
        """Run the interactive CLI."""
        print("🎯 NBR Restrictor - Next Basket Prediction Data Limitation Tool")
        print("="*65)
        print("This tool helps you apply data limitations to NBP datasets based on")
        print("the limitation types identified in your thesis research.")
        
        # Show available datasets
        available_datasets = []
        for dataset in self.datasets:
            history_file = os.path.join(self.input_dir, f"{dataset}_history.csv")
            if os.path.exists(history_file):
                available_datasets.append(dataset)
        
        if not available_datasets:
            print(f"❌ No datasets found in {self.input_dir}/")
            print("Expected files: *_history.csv")
            return
        
        print(f"\n📁 Available datasets: {', '.join(available_datasets)}")
        
        # Select dataset
        while True:
            dataset_name = input(f"\nSelect dataset ({'/'.join(available_datasets)}): ").lower().strip()
            if dataset_name in available_datasets:
                break
            print(f"❌ Invalid dataset. Choose from: {', '.join(available_datasets)}")
        
        try:
            # Analyze dataset
            analysis = self.analyze_dataset(dataset_name)
            self.display_analysis(dataset_name, analysis)
            
            # Get user restrictions
            restrictions = self.get_user_restrictions(dataset_name, analysis)
            
            # Save configuration
            self.save_config(dataset_name, analysis, restrictions)
            
            print(f"\n🎉 Success! Configuration ready for preprocessing.")
            print(f"You can now run the preprocessing pipeline using the generated config.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="NBR Restrictor - Apply data limitations to Next Basket Prediction datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nbr_restrictor.py                    # Run interactive mode
  python nbr_restrictor.py --input data/      # Specify input directory
  python nbr_restrictor.py --help             # Show this help

Data Limitation Types (from thesis):
  1. Kundenanzahl (Customer Count) - Limited number of customers
  2. Einkaufsfrequenz (Shopping Frequency) - Low repeat purchases per customer  
  3. Warenkorbtiefe (Basket Depth) - Few items per basket
  4. Artikelvielfalt (Product Variety) - Limited product assortment
  5. Zeitliche Tiefe (Temporal Depth) - Short observation periods
        """
    )
    
    parser.add_argument(
        "--input", 
        default="input",
        help="Input directory containing dataset CSV files (default: input/)"
    )
    
    parser.add_argument(
        "--output", 
        default="output",
        help="Output directory for configuration files (default: output/)"
    )
    
    args = parser.parse_args()
    
    restrictor = NBRRestrictor(args.input, args.output)
    restrictor.run_interactive()


if __name__ == "__main__":
    main()