def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total_revenue = 0.0
    
    for transaction in transactions:
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        
        # Calculate revenue for this transaction
        revenue = quantity * unit_price
        total_revenue += revenue
    
    return total_revenue


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    
    Returns: tuple (date, revenue, transaction_count)
    Expected Output Format: ('2024-12-15', 185000.0, 12)
    """
    date_stats = {}
    
    # Aggregate revenue and transaction count by date
    for transaction in transactions:
        date = transaction.get('Date', '').strip()
        
        # Skip transactions with empty date
        if not date:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        # Initialize date if not exists
        if date not in date_stats:
            date_stats[date] = {
                'total_revenue': 0.0,
                'transaction_count': 0
            }
        
        # Update date statistics
        date_stats[date]['total_revenue'] += revenue
        date_stats[date]['transaction_count'] += 1
    
    # Find the date with highest revenue
    if not date_stats:
        return (None, 0.0, 0)
    
    peak_date = max(
        date_stats.items(),
        key=lambda x: x[1]['total_revenue']
    )
    
    date, stats = peak_date
    return (date, stats['total_revenue'], stats['transaction_count'])


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    
    Returns: dictionary sorted by date
    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }
    
    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """
    date_stats = {}
    
    # Group by date and calculate metrics
    for transaction in transactions:
        date = transaction.get('Date', '').strip()
        
        # Skip transactions with empty date
        if not date:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        customer_id = transaction.get('CustomerID', '').strip()
        
        # Initialize date if not exists
        if date not in date_stats:
            date_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }
        
        # Update date statistics
        date_stats[date]['revenue'] += revenue
        date_stats[date]['transaction_count'] += 1
        
        # Add customer to unique customers set if customer_id exists
        if customer_id:
            date_stats[date]['unique_customers'].add(customer_id)
    
    # Convert sets to counts and prepare final dictionary
    result = {}
    for date in sorted(date_stats.keys()):  # Sort chronologically
        stats = date_stats[date]
        result[date] = {
            'revenue': stats['revenue'],
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['unique_customers'])
        }
    
    return result


def region_wise_sales_analysis(transactions):
    """
    Analyzes sales data by region
    
    Args:
        transactions (list): List of transaction dictionaries
    
    Returns: dict with region-wise statistics
    Expected Output Format:
    {
        'North': {'total_revenue': 150000.50, 'transaction_count': 25},
        'South': {'total_revenue': 120000.30, 'transaction_count': 20},
        'East': {'total_revenue': 100000.20, 'transaction_count': 18},
        'West': {'total_revenue': 90000.10, 'transaction_count': 15}
    }
    """
    region_stats = {}
    
    for transaction in transactions:
        region = transaction.get('Region', '').strip()
        
        # Skip transactions with empty region
        if not region:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        # Initialize region if not exists
        if region not in region_stats:
            region_stats[region] = {
                'total_revenue': 0.0,
                'transaction_count': 0
            }
        
        # Update region statistics
        region_stats[region]['total_revenue'] += revenue
        region_stats[region]['transaction_count'] += 1
    
    return region_stats


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    
    Returns: dictionary with region statistics
    Expected Output Format:
    {
        'North': {'total_sales': 450000.0, 'transaction_count': 15, 'percentage': 29.13},
        'South': {'total_sales': 380000.0, 'transaction_count': 12, 'percentage': 24.60},
        ...
    }
    
    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    region_stats = {}
    total_all_sales = 0.0
    
    # First pass: Calculate total sales per region and overall total
    for transaction in transactions:
        region = transaction.get('Region', '').strip()
        
        # Skip transactions with empty region
        if not region:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        sales = quantity * unit_price
        
        # Initialize region if not exists
        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }
        
        # Update region statistics
        region_stats[region]['total_sales'] += sales
        region_stats[region]['transaction_count'] += 1
        total_all_sales += sales
    
    # Second pass: Calculate percentage for each region
    for region in region_stats:
        if total_all_sales > 0:
            percentage = (region_stats[region]['total_sales'] / total_all_sales) * 100
            region_stats[region]['percentage'] = round(percentage, 2)
        else:
            region_stats[region]['percentage'] = 0.0
    
    # Sort by total_sales in descending order
    sorted_region_stats = dict(
        sorted(
            region_stats.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )
    
    return sorted_region_stats


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    
    Args:
        transactions (list): List of transaction dictionaries
        n (int): Number of top products to return (default: 5)
    
    Returns: list of tuples
    Expected Output Format:
    [('Laptop', 45, 2250000.0), ('Mouse', 38, 19000.0), ...]
    Format: (ProductName, TotalQuantity, TotalRevenue)
    
    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    product_stats = {}
    
    # Aggregate by ProductName
    for transaction in transactions:
        product_name = transaction.get('ProductName', '').strip()
        
        # Skip transactions with empty product name
        if not product_name:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        # Initialize product if not exists
        if product_name not in product_stats:
            product_stats[product_name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }
        
        # Update product statistics
        product_stats[product_name]['total_quantity'] += quantity
        product_stats[product_name]['total_revenue'] += revenue
    
    # Convert to list of tuples and sort by TotalQuantity descending
    product_list = [
        (product_name, stats['total_quantity'], stats['total_revenue'])
        for product_name, stats in product_stats.items()
    ]
    
    # Sort by TotalQuantity (index 1) in descending order
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    # Return top n products
    return product_list[:n]


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    
    Args:
        transactions (list): List of transaction dictionaries
        threshold (int): Maximum total quantity threshold (default: 10)
    
    Returns: list of tuples
    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]
    
    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """
    product_stats = {}
    
    # Aggregate by ProductName
    for transaction in transactions:
        product_name = transaction.get('ProductName', '').strip()
        
        # Skip transactions with empty product name
        if not product_name:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        # Initialize product if not exists
        if product_name not in product_stats:
            product_stats[product_name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }
        
        # Update product statistics
        product_stats[product_name]['total_quantity'] += quantity
        product_stats[product_name]['total_revenue'] += revenue
    
    # Filter products with total quantity < threshold
    low_performing = [
        (product_name, stats['total_quantity'], stats['total_revenue'])
        for product_name, stats in product_stats.items()
        if stats['total_quantity'] < threshold
    ]
    
    # Sort by TotalQuantity (index 1) in ascending order
    low_performing.sort(key=lambda x: x[1])
    
    return low_performing


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    
    Args:
        transactions (list): List of transaction dictionaries
    
    Returns: dictionary with customer statistics
    Expected Output Format:
    {
        'C001': {
            'total_spent': 150000.0,
            'transaction_count': 5,
            'avg_transaction_value': 30000.0
        },
        'C002': {
            'total_spent': 120000.0,
            'transaction_count': 3,
            'avg_transaction_value': 40000.0
        },
        ...
    }
    
    Requirements:
    - Aggregate by CustomerID
    - Calculate total amount spent per customer
    - Count transactions per customer
    - Calculate average transaction value
    """
    customer_stats = {}
    
    for transaction in transactions:
        customer_id = transaction.get('CustomerID', '').strip()
        
        # Skip transactions with empty customer ID
        if not customer_id:
            continue
        
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        transaction_value = quantity * unit_price
        
        # Initialize customer if not exists
        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                'total_spent': 0.0,
                'transaction_count': 0
            }
        
        # Update customer statistics
        customer_stats[customer_id]['total_spent'] += transaction_value
        customer_stats[customer_id]['transaction_count'] += 1
    
    # Calculate average transaction value for each customer
    for customer_id in customer_stats:
        transaction_count = customer_stats[customer_id]['transaction_count']
        if transaction_count > 0:
            avg_value = customer_stats[customer_id]['total_spent'] / transaction_count
            customer_stats[customer_id]['avg_transaction_value'] = round(avg_value, 2)
        else:
            customer_stats[customer_id]['avg_transaction_value'] = 0.0
    
    return customer_stats


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report

    Report Must Include (in this order):

    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed

    2. OVERALL SUMMARY
       - Total Revenue (formatted with commas)
       - Total Transactions
       - Average Order Value
       - Date Range of data

    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total Sales Amount
         * Percentage of Total
         * Transaction Count
       - Sorted by sales amount descending

    4. TOP 5 PRODUCTS
       - Table with columns: Rank, Product Name, Quantity Sold, Revenue

    5. TOP 5 CUSTOMERS
       - Table with columns: Rank, Customer ID, Total Spent, Order Count

    6. DAILY SALES TREND
       - Table showing: Date, Revenue, Transactions, Unique Customers

    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region

    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched

    Expected Output Format (sample):
    ============================================
           SALES ANALYTICS REPORT
         Generated: 2024-12-18 14:30:22
         Records Processed: 95
    ============================================

    OVERALL SUMMARY
    --------------------------------------------
    Total Revenue:        ₹15,45,000.00
    Total Transactions:   95
    Average Order Value:  ₹16,263.16
    Date Range:           2024-12-01 to 2024-12-31

    REGION-WISE PERFORMANCE
    --------------------------------------------
    Region    Sales         % of Total  Transactions
    North     ₹4,50,000     29.13%      25
    South     ₹3,80,000     24.60%      22
    ...
    
    """
    import os
    from datetime import datetime
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # Get current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Calculate overall summary
    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0.0
    
    # Get date range
    dates = [t.get('Date', '') for t in transactions if t.get('Date')]
    min_date = min(dates) if dates else 'N/A'
    max_date = max(dates) if dates else 'N/A'
    
    # Get region-wise performance
    region_stats = region_wise_sales(transactions)
    
    # Get top 5 products
    top_products = top_selling_products(transactions, n=5)
    
    # Get top 5 customers
    customer_stats = customer_analysis(transactions)
    top_customers = sorted(
        [(cid, stats['total_spent'], stats['transaction_count']) 
         for cid, stats in customer_stats.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    # Get daily sales trend
    daily_trend = daily_sales_trend(transactions)
    
    # Get peak sales day
    peak_day = find_peak_sales_day(transactions)
    
    # Get low performing products
    low_products = low_performing_products(transactions, threshold=10)
    
    # Calculate average transaction value per region
    region_avg_value = {}
    for region, stats in region_stats.items():
        if stats['transaction_count'] > 0:
            region_avg_value[region] = stats['total_sales'] / stats['transaction_count']
        else:
            region_avg_value[region] = 0.0
    
    # API Enrichment Summary
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match', False))
    total_enriched = len(enriched_transactions)
    success_rate = (enriched_count / total_enriched * 100) if total_enriched > 0 else 0.0
    unenriched_products = [
        t.get('ProductName', 'Unknown') 
        for t in enriched_transactions 
        if not t.get('API_Match', False)
    ]
    unique_unenriched = sorted(set(unenriched_products))
    
    # Format currency with Indian numbering
    def format_currency(amount):
        return f"₹{amount:,.2f}".replace(',', ',')
    
    # Start building report
    report_lines = []
    
    # 1. HEADER
    report_lines.append("=" * 50)
    report_lines.append(" " * 15 + "SALES ANALYTICS REPORT")
    report_lines.append(" " * 10 + f"Generated: {current_datetime}")
    report_lines.append(" " * 10 + f"Records Processed: {total_transactions}")
    report_lines.append("=" * 50)
    report_lines.append("")
    
    # 2. OVERALL SUMMARY
    report_lines.append("OVERALL SUMMARY")
    report_lines.append("-" * 50)
    report_lines.append(f"Total Revenue:        {format_currency(total_revenue)}")
    report_lines.append(f"Total Transactions:   {total_transactions}")
    report_lines.append(f"Average Order Value:  {format_currency(avg_order_value)}")
    report_lines.append(f"Date Range:           {min_date} to {max_date}")
    report_lines.append("")
    
    # 3. REGION-WISE PERFORMANCE
    report_lines.append("REGION-WISE PERFORMANCE")
    report_lines.append("-" * 50)
    report_lines.append(f"{'Region':<12} {'Sales':<15} {'% of Total':<12} {'Transactions':<12}")
    report_lines.append("-" * 50)
    for region, stats in region_stats.items():
        sales_str = format_currency(stats['total_sales'])
        percentage = stats.get('percentage', 0.0)
        trans_count = stats['transaction_count']
        report_lines.append(f"{region:<12} {sales_str:<15} {percentage:>6.2f}%      {trans_count:<12}")
    report_lines.append("")
    
    # 4. TOP 5 PRODUCTS
    report_lines.append("TOP 5 PRODUCTS")
    report_lines.append("-" * 50)
    report_lines.append(f"{'Rank':<6} {'Product Name':<25} {'Quantity Sold':<15} {'Revenue':<15}")
    report_lines.append("-" * 50)
    for rank, (product_name, quantity, revenue) in enumerate(top_products, 1):
        product_name_short = product_name[:24] if len(product_name) > 24 else product_name
        report_lines.append(f"{rank:<6} {product_name_short:<25} {quantity:<15} {format_currency(revenue)}")
    report_lines.append("")
    
    # 5. TOP 5 CUSTOMERS
    report_lines.append("TOP 5 CUSTOMERS")
    report_lines.append("-" * 50)
    report_lines.append(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<15} {'Order Count':<12}")
    report_lines.append("-" * 50)
    for rank, (customer_id, total_spent, order_count) in enumerate(top_customers, 1):
        report_lines.append(f"{rank:<6} {customer_id:<15} {format_currency(total_spent)} {order_count:<12}")
    report_lines.append("")
    
    # 6. DAILY SALES TREND
    report_lines.append("DAILY SALES TREND")
    report_lines.append("-" * 50)
    report_lines.append(f"{'Date':<12} {'Revenue':<15} {'Transactions':<12} {'Unique Customers':<15}")
    report_lines.append("-" * 50)
    for date, stats in list(daily_trend.items())[:10]:  # Show first 10 days
        report_lines.append(
            f"{date:<12} {format_currency(stats['revenue']):<15} "
            f"{stats['transaction_count']:<12} {stats['unique_customers']:<15}"
        )
    if len(daily_trend) > 10:
        report_lines.append(f"... and {len(daily_trend) - 10} more days")
    report_lines.append("")
    
    # 7. PRODUCT PERFORMANCE ANALYSIS
    report_lines.append("PRODUCT PERFORMANCE ANALYSIS")
    report_lines.append("-" * 50)
    if peak_day[0]:
        report_lines.append(f"Best Selling Day:     {peak_day[0]}")
        report_lines.append(f"  Revenue:            {format_currency(peak_day[1])}")
        report_lines.append(f"  Transactions:       {peak_day[2]}")
    else:
        report_lines.append("Best Selling Day:     N/A")
    report_lines.append("")
    
    if low_products:
        report_lines.append("Low Performing Products (Quantity < 10):")
        report_lines.append(f"{'Product Name':<25} {'Quantity':<12} {'Revenue':<15}")
        report_lines.append("-" * 50)
        for product_name, quantity, revenue in low_products[:10]:  # Show top 10
            product_name_short = product_name[:24] if len(product_name) > 24 else product_name
            report_lines.append(f"{product_name_short:<25} {quantity:<12} {format_currency(revenue)}")
        if len(low_products) > 10:
            report_lines.append(f"... and {len(low_products) - 10} more products")
    else:
        report_lines.append("Low Performing Products: None")
    report_lines.append("")
    
    report_lines.append("Average Transaction Value per Region:")
    report_lines.append(f"{'Region':<12} {'Avg Transaction Value':<20}")
    report_lines.append("-" * 50)
    for region, avg_value in sorted(region_avg_value.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"{region:<12} {format_currency(avg_value)}")
    report_lines.append("")
    
    # 8. API ENRICHMENT SUMMARY
    report_lines.append("API ENRICHMENT SUMMARY")
    report_lines.append("-" * 50)
    report_lines.append(f"Total Products Processed:  {total_enriched}")
    report_lines.append(f"Successfully Enriched:     {enriched_count}")
    report_lines.append(f"Success Rate:              {success_rate:.2f}%")
    report_lines.append("")
    
    if unique_unenriched:
        report_lines.append(f"Products That Couldn't Be Enriched ({len(unique_unenriched)} unique):")
        for product in unique_unenriched[:20]:  # Show first 20
            report_lines.append(f"  - {product}")
        if len(unique_unenriched) > 20:
            report_lines.append(f"  ... and {len(unique_unenriched) - 20} more products")
    else:
        report_lines.append("All products successfully enriched!")
    report_lines.append("")
    
    # Write report to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    return report_lines