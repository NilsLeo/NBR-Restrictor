# NBR Restrictor - Dataset User Sampling Tool

A command-line tool for filtering and sampling next-basket recommendation datasets.

## Usage

```bash
python cli.py <history_file> <future_file> [options]
```

### Arguments
- `history_file`: Path to history dataset CSV
- `future_file`: Path to future dataset CSV

### Options
- `--user-col`: User column name (default: `user_id`)
- `--basket-col`: Basket/order column name (default: `order_number`)
- `--product-col`: Product column name (default: `product_id`)

## Features

1. **Sample random users** - Randomly select N users and keep all their data
2. **Filter by basket count per user** - Keep users with min-max baskets
3. **Filter by items per basket** - Keep baskets with min-max items
4. **Show dataset statistics** - View current dataset stats
5. **Save and exit** - Split and save as history/future CSVs

## Data Structure

Expected CSV format:
```csv
user_id,order_number,product_id
1,1,101
1,1,102
1,2,103
```

- Each row represents one item purchase
- `order_number` is per-user (resets for each user)
- Multiple items in same basket share the same `user_id` and `order_number`

## Output

When saving, data is automatically split:
- **History CSV**: All baskets except the most recent per user
- **Future CSV**: Only the most recent basket per user

Files are saved as `{dataset_name}_history.csv` and `{dataset_name}_future.csv` in the `output/` directory.