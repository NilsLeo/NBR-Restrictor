# NBR Restrictor Use Cases

## Simple Limitations (Single Filter)

### 1. E-commerce Startup - User Sampling
**Industry:** Online Retail  
**Company Size:** Small startup with limited computational resources  
**Original Dataset:** 50,000 customers, 2.3M transactions  
**Limitation Applied:** Sample random users → 2,000 users  

### 2. Grocery Chain - Basket Count Filtering  
**Industry:** Retail Grocery  
**Company Size:** Regional chain (150 stores)  
**Original Dataset:** 800,000 customers with varying shopping frequencies  
**Limitation Applied:** Filter by basket count → 5-25 baskets per user  
**Business Reason:** Focus on regular shoppers who provide stable purchasing patterns, excluding one-time buyers and extreme outliers.

### 3. Fashion Retailer - Items Per Basket
**Industry:** Fashion E-commerce  
**Company Size:** Mid-market online retailer  
**Original Dataset:** 200,000 customers with highly variable cart sizes  
**Limitation Applied:** Filter by items per basket → 3-12 items per basket  
**Business Reason:** Target typical shopping behavior, excluding single-item purchases and bulk orders that don't represent normal browsing patterns.

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

### 5. Subscription Box Service - Active Subscriber Focus
**Industry:** Subscription Commerce  
**Company Size:** Growing subscription service  
**Original Dataset:** 100,000 subscribers with mixed engagement  
**Limitations Applied:**
- Sample random users → 8,000 users
- Filter by basket count → 8-36 baskets per user  
**Business Reason:** Study highly engaged subscribers to optimize retention and cross-selling strategies for monthly box curation.

### 6. B2B Office Supplies - Regular Business Customers
**Industry:** B2B E-commerce  
**Company Size:** Enterprise supplier to SMBs  
**Original Dataset:** 75,000 business customers  
**Limitations Applied:**
- Filter by basket count → 12-48 baskets per user
- Filter by items per basket → 5-25 items per basket  
**Business Reason:** Focus on established business accounts with predictable ordering patterns for automated reorder recommendations.

### 7. Pharmacy Chain - Chronic Care Patients
**Industry:** Healthcare Retail  
**Company Size:** National pharmacy chain  
**Original Dataset:** 2M patients with prescription and OTC purchases  
**Limitations Applied:**
- Sample random users → 25,000 users
- Filter by basket count → 15-60 baskets per user
- Filter by items per basket → 2-8 items per basket  
**Business Reason:** Target patients with chronic conditions for medication adherence and health product recommendations.

### 8. Specialty Coffee Retailer - Loyalty Program Members
**Industry:** Food & Beverage  
**Company Size:** Specialty coffee chain (50 locations)  
**Original Dataset:** 180,000 customers including casual visitors  
**Limitations Applied:**
- Sample random users → 12,000 users
- Filter by basket count → 20-80 baskets per user  
**Business Reason:** Focus on frequent customers for seasonal product recommendations and loyalty program optimization.

### 9. Home Improvement Store - DIY Enthusiasts
**Industry:** Home Improvement Retail  
**Company Size:** Regional home improvement chain  
**Original Dataset:** 400,000 customers with project-based purchases  
**Limitations Applied:**
- Filter by basket count → 6-30 baskets per user
- Filter by items per basket → 8-35 items per basket
- Sample random users → 20,000 users  
**Business Reason:** Target active DIY customers for project-based product bundles and seasonal tool recommendations.

### 10. Pet Supply Chain - Multi-Pet Households
**Industry:** Pet Retail  
**Company Size:** National pet supply retailer  
**Original Dataset:** 600,000 pet owners with varying needs  
**Limitations Applied:**
- Sample random users → 18,000 users
- Filter by basket count → 12-45 baskets per user
- Filter by items per basket → 6-20 items per basket  
**Business Reason:** Focus on dedicated pet owners with multiple or high-maintenance pets for premium product recommendations and subscription services.
