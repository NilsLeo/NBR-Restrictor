# NBR Restrictor Use Cases

## Simple Limitations (Single Filter)

### Baseline


```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv original
```

### E-commerce Startup - User Sampling
**Limitation Applied:** Sample random users → 2,000 users  

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv ecommerce --sample-users 2000
```

### Drugstore - Items Per Basket
**Limitation Applied:** Filter by items per basket → 3-12 items per basket  

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv drugstore --min-items 3 --max-items 12
```

### Fashion Store - Basket Count Filtering  
**Limitation Applied:** 3-12 items per basket, Basket count 3-15 baskets per user

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv fashion \
    --min-items 3 --max-items 12 \
    --min-baskets 3 --max-baskets 15
```


## Complex Limitations (Multiple Filters)

### 4. Premium Department Store - High-Value Customer Analysis
**Industry:** Luxury Retail  
**Company Size:** High-end department store chain  
**Original Dataset:** 300,000 customers across all segments  
**Limitations Applied:**
- Sample random users → 15,000 users
- Filter by basket count → 10-40 baskets per user
- Filter by items per basket → 4-15 items per basket  
**Business Reason:** Focus on premium customers with consistent shopping patterns for personalized luxury recommendations.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv premium_customers \
    --sample-users 15000 \
    --min-baskets 10 --max-baskets 40 \
    --min-items 4 --max-items 15 \
    --stats
```

### 5. Subscription Box Service - Active Subscriber Focus
**Industry:** Subscription Commerce  
**Company Size:** Growing subscription service  
**Original Dataset:** 100,000 subscribers with mixed engagement  
**Limitations Applied:**
- Sample random users → 8,000 users
- Filter by basket count → 8-36 baskets per user  
**Business Reason:** Study highly engaged subscribers to optimize retention and cross-selling strategies for monthly box curation.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv active_subscribers \
    --sample-users 8000 \
    --min-baskets 8 --max-baskets 36
```

### 6. B2B Office Supplies - Regular Business Customers
**Industry:** B2B E-commerce  
**Company Size:** Enterprise supplier to SMBs  
**Original Dataset:** 75,000 business customers  
**Limitations Applied:**
- Filter by basket count → 12-48 baskets per user
- Filter by items per basket → 5-25 items per basket  
**Business Reason:** Focus on established business accounts with predictable ordering patterns for automated reorder recommendations.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv regular_businesses \
    --min-baskets 12 --max-baskets 48 \
    --min-items 5 --max-items 25
```

### 7. Pharmacy Chain - Chronic Care Patients
**Industry:** Healthcare Retail  
**Company Size:** National pharmacy chain  
**Original Dataset:** 2M patients with prescription and OTC purchases  
**Limitations Applied:**
- Sample random users → 25,000 users
- Filter by basket count → 15-60 baskets per user
- Filter by items per basket → 2-8 items per basket  
**Business Reason:** Target patients with chronic conditions for medication adherence and health product recommendations.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv chronic_patients \
    --sample-users 25000 \
    --min-baskets 15 --max-baskets 60 \
    --min-items 2 --max-items 8
```

### 8. Specialty Coffee Retailer - Loyalty Program Members
**Industry:** Food & Beverage  
**Company Size:** Specialty coffee chain (50 locations)  
**Original Dataset:** 180,000 customers including casual visitors  
**Limitations Applied:**
- Sample random users → 12,000 users
- Filter by basket count → 20-80 baskets per user  
**Business Reason:** Focus on frequent customers for seasonal product recommendations and loyalty program optimization.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv loyalty_members \
    --sample-users 12000 \
    --min-baskets 20 --max-baskets 80
```

### 9. Home Improvement Store - DIY Enthusiasts
**Industry:** Home Improvement Retail  
**Company Size:** Regional home improvement chain  
**Original Dataset:** 400,000 customers with project-based purchases  
**Limitations Applied:**
- Filter by basket count → 6-30 baskets per user
- Filter by items per basket → 8-35 items per basket
- Sample random users → 20,000 users  
**Business Reason:** Target active DIY customers for project-based product bundles and seasonal tool recommendations.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv diy_enthusiasts \
    --min-baskets 6 --max-baskets 30 \
    --min-items 8 --max-items 35 \
    --sample-users 20000
```

### 10. Pet Supply Chain - Multi-Pet Households
**Industry:** Pet Retail  
**Company Size:** National pet supply retailer  
**Original Dataset:** 600,000 pet owners with varying needs  
**Limitations Applied:**
- Sample random users → 18,000 users
- Filter by basket count → 12-45 baskets per user
- Filter by items per basket → 6-20 items per basket  
**Business Reason:** Focus on dedicated pet owners with multiple or high-maintenance pets for premium product recommendations and subscription services.

```bash
python cli.py input/tafeng_history.csv input/tafeng_future.csv multipet_households \
    --sample-users 18000 \
    --min-baskets 12 --max-baskets 45 \
    --min-items 6 --max-items 20
```
