# NBR Restrictor - Next Basket Prediction Data Limitation Tool

A CLI tool for imposing data limitations on Next Basket Prediction datasets based on the data limitation types identified in thesis research.

## Overview

This tool helps researchers apply systematic data restrictions to NBP datasets to study model performance under various data constraints. It implements the five key data limitation types from Next Basket Prediction research:

1. **Kundenanzahl** (Customer Count) - Limited number of customers
2. **Einkaufsfrequenz** (Shopping Frequency) - Low repeat purchases per customer  
3. **Warenkorbtiefe** (Basket Depth) - Few items per basket
4. **Artikelvielfalt** (Product Variety) - Limited product assortment
5. **Zeitliche Tiefe** (Temporal Depth) - Short observation periods

## Setup

### Prerequisites
- Conda (miniconda or anaconda)
- Python 3.9+

### Environment Setup

1. **Create and activate the conda environment:**
   ```bash
   # Create environment with required packages
   zsh -c "conda create -n nbr-restrictor python=3.9 pandas numpy -y"
   
   # Activate the environment
   conda activate nbr-restrictor
   ```

2. **Verify installation:**
   ```bash
   python nbr_restrictor.py --help
   ```

### Alternative Setup (if conda not available)
```bash
# Using pip with venv
python3 -m venv nbr-restrictor
source nbr-restrictor/bin/activate
pip install -r requirements.txt
```

## Dataset Structure

Place your datasets in the `input/` directory with the following naming convention:
- `{dataset_name}_history.csv` - Historical purchase data
- `{dataset_name}_future.csv` - Future/test purchase data (optional)

Expected CSV format:
```csv
user_id,order_number,product_id
1,1,0
1,1,1
1,2,5
```

Currently supported datasets:
- `dunnhumby` - Dunnhumby dataset
- `instacart` - Instacart dataset  
- `tafeng` - Ta Feng dataset

## Usage

### Interactive Mode (Recommended)
```bash
# Activate environment
conda activate nbr-restrictor

# Run interactive CLI
python nbr_restrictor.py
```

The tool will:
1. 📊 Analyze the selected dataset
2. 📈 Display dataset statistics
3. 🎯 Prompt for restriction values for each limitation type
4. 💾 Generate configuration files

### Command Line Options
```bash
python nbr_restrictor.py --input data/ --output configs/
```

Options:
- `--input DIR` - Input directory containing CSV files (default: `input/`)
- `--output DIR` - Output directory for configuration files (default: `output/`)
- `--help` - Show help message

## Data Limitation Types

### 1. Customer Count (Kundenanzahl)
- **Purpose**: Limit the total number of unique customers
- **Prompt**: "How many customers to keep? (1-{max_available})"
- **Impact**: Reduces dataset size by selecting subset of customers

### 2. Shopping Frequency (Einkaufsfrequenz)
- **Purpose**: Filter customers based on minimum purchase frequency
- **Prompt**: "Minimum orders per customer to keep?"
- **Impact**: Removes customers with too few purchases

### 3. Basket Depth (Warenkorbtiefe)
- **Purpose**: Filter baskets based on minimum item count
- **Prompt**: "Minimum items per basket to keep?"
- **Impact**: Removes small baskets that don't meet threshold

### 4. Product Variety (Artikelvielfalt)
- **Purpose**: Limit the total number of unique products
- **Prompt**: "How many products to keep? (1-{max_available})"
- **Impact**: Reduces product catalog by selecting most frequent items

### 5. Temporal Depth (Zeitliche Tiefe)
- **Purpose**: Limit the number of time periods
- **Prompt**: "How many time periods to keep?"
- **Impact**: Restricts data to specific temporal range

## Output

The tool generates configuration files in JSON format:

```json
{
  "dataset": "dunnhumby",
  "timestamp": "2025-01-27T10:30:00",
  "original_stats": {
    "max_customers": 2500,
    "max_products": 15000,
    "avg_basket_depth": 3.2
  },
  "restrictions": {
    "max_customers": 500,
    "min_orders_per_customer": 3,
    "min_basket_items": 2,
    "max_products": 5000,
    "max_temporal_periods": 100
  },
  "limitation_types": {
    "1": "Kundenanzahl (Customer Count)",
    "2": "Einkaufsfrequenz (Shopping Frequency)",
    "3": "Warenkorbtiefe (Basket Depth)",
    "4": "Artikelvielfalt (Product Variety)",
    "5": "Zeitliche Tiefe (Temporal Depth)"
  },
  "description": "NBR data limitations configuration for Next Basket Prediction thesis"
}
```

## File Structure
```
NBR-Restrictor/
├── nbr_restrictor.py          # Main CLI tool
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── input/                     # Input datasets
│   ├── dunnhumby_history.csv
│   ├── dunnhumby_future.csv
│   ├── instacart_history.csv
│   ├── instacart_future.csv
│   └── tafeng_history.csv
└── output/                    # Generated configurations
    ├── dunnhumby_restrictions_config.json
    ├── instacart_restrictions_config.json
    └── tafeng_restrictions_config.json
```

## Example Session

```bash
$ python nbr_restrictor.py

🎯 NBR Restrictor - Next Basket Prediction Data Limitation Tool
=================================================================
Available datasets: dunnhumby, instacart, tafeng

Select dataset (dunnhumby/instacart/tafeng): dunnhumby

📊 Analyzing dunnhumby dataset...

==================================================
📈 Dataset Analysis: DUNNHUMBY
==================================================
🔢 Total customers: 2,500
🛒 Orders per customer: 1-42 (avg: 14.7)
📦 Basket depth: 1-76 items (avg: 5.1)
🏷️  Product variety: 40,000 unique products
⏰ Temporal periods: 888 unique time periods

============================================================
🎯 Configure Data Limitations for DUNNHUMBY
============================================================

1️⃣  CUSTOMER COUNT LIMITATION
   How many customers to keep? (1-2500): 500

2️⃣  SHOPPING FREQUENCY LIMITATION  
   Minimum orders per customer? (1-42): 5

3️⃣  BASKET DEPTH LIMITATION
   Minimum items per basket? (1-76): 3

4️⃣  PRODUCT VARIETY LIMITATION
   How many products to keep? (1-40000): 10000

5️⃣  TEMPORAL DEPTH LIMITATION
   How many time periods to keep? (1-888): 200

✅ Configuration saved to: output/dunnhumby_restrictions_config.json
```

## Integration with Preprocessing Pipeline

The generated configuration files can be used by preprocessing scripts to apply the specified restrictions to the datasets before model training and evaluation.

## Contributing

This tool is part of a Master's thesis research on Next Basket Prediction under data limitations. For questions or contributions, please refer to the thesis documentation.

## License

Academic research use only.