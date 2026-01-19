def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Args:
        filename (str): Path to the sales data file

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
            
            # Skip header row (first line) and remove empty lines
            data_lines = []
            for line in lines[1:]:  # Skip first line (header)
                stripped_line = line.strip()
                if stripped_line:  # Only add non-empty lines
                    data_lines.append(stripped_line)
            
            return data_lines
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found.")
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except Exception as e:
            # If it's not a UnicodeDecodeError, re-raise it
            raise
    
    # If all encodings failed, raise an error
    raise ValueError(
        f"Unable to decode file '{filename}' with any of the attempted encodings: {', '.join(encodings_to_try)}"
    )


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Args:
        raw_lines (list): List of raw transaction lines (strings)

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]

    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    transactions = []
    expected_fields = 8  # TransactionID, Date, ProductID, ProductName, Quantity, UnitPrice, CustomerID, Region
    
    for line in raw_lines:
        if not line or not line.strip():
            continue
        
        # Split by pipe delimiter
        fields = line.split('|')
        
        # Skip rows with incorrect number of fields
        if len(fields) != expected_fields:
            continue
        
        # Extract and clean fields
        transaction_id = fields[0].strip()
        date = fields[1].strip()
        product_id = fields[2].strip()
        product_name = fields[3].strip()
        quantity_str = fields[4].strip()
        unit_price_str = fields[5].strip()
        customer_id = fields[6].strip()
        region = fields[7].strip()
        
        # Handle commas in ProductName (remove commas)
        product_name = product_name.replace(',', '')
        
        # Remove commas from numeric fields and convert to proper types
        # Convert Quantity to int
        try:
            quantity_cleaned = quantity_str.replace(',', '').strip()
            quantity = int(quantity_cleaned)
        except (ValueError, AttributeError):
            # Skip if conversion fails
            continue
        
        # Convert UnitPrice to float
        try:
            unit_price_cleaned = unit_price_str.replace(',', '').strip()
            unit_price = float(unit_price_cleaned)
        except (ValueError, AttributeError):
            # Skip if conversion fails
            continue
        
        # Create transaction dictionary
        transaction = {
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        }
        
        transactions.append(transaction)
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0
    
    # Required fields
    required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                       'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    # Validate transactions
    for transaction in transactions:
        is_valid = True
        
        # Check all required fields are present
        for field in required_fields:
            if field not in transaction or not transaction[field]:
                is_valid = False
                break
        
        if not is_valid:
            invalid_count += 1
            continue
        
        # Check TransactionID starts with 'T'
        transaction_id = str(transaction.get('TransactionID', '')).strip()
        if not transaction_id.startswith('T'):
            is_valid = False
        
        # Check ProductID starts with 'P'
        product_id = str(transaction.get('ProductID', '')).strip()
        if not product_id.startswith('P'):
            is_valid = False
        
        # Check CustomerID starts with 'C'
        customer_id = str(transaction.get('CustomerID', '')).strip()
        if not customer_id.startswith('C'):
            is_valid = False
        
        # Check Quantity > 0
        quantity = transaction.get('Quantity')
        if not isinstance(quantity, (int, float)) or quantity <= 0:
            is_valid = False
        
        # Check UnitPrice > 0
        unit_price = transaction.get('UnitPrice')
        if not isinstance(unit_price, (int, float)) or unit_price <= 0:
            is_valid = False
        
        if is_valid:
            valid_transactions.append(transaction)
        else:
            invalid_count += 1
    
    # Display available regions
    if valid_transactions:
        regions = sorted(set(t.get('Region', '') for t in valid_transactions if t.get('Region')))
        print(f"\nAvailable regions: {', '.join(regions)}")
        
        # Calculate and display transaction amount range
        amounts = [t.get('Quantity', 0) * t.get('UnitPrice', 0) for t in valid_transactions]
        if amounts:
            min_transaction_amount = min(amounts)
            max_transaction_amount = max(amounts)
            print(f"Transaction amount range: ${min_transaction_amount:,.2f} - ${max_transaction_amount:,.2f}")
    
    print(f"\nTotal input transactions: {total_input}")
    print(f"Valid transactions after validation: {len(valid_transactions)}")
    print(f"Invalid transactions: {invalid_count}")
    
    # Apply region filter
    filtered_by_region = 0
    if region is not None:
        before_region_filter = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if t.get('Region', '').strip() == region.strip()]
        filtered_by_region = before_region_filter - len(valid_transactions)
        print(f"After region filter ('{region}'): {len(valid_transactions)} transactions")
    
    # Apply amount filters
    filtered_by_amount = 0
    if min_amount is not None or max_amount is not None:
        before_amount_filter = len(valid_transactions)
        filtered_transactions = []
        for t in valid_transactions:
            transaction_amount = t.get('Quantity', 0) * t.get('UnitPrice', 0)
            if min_amount is not None and transaction_amount < min_amount:
                continue
            if max_amount is not None and transaction_amount > max_amount:
                continue
            filtered_transactions.append(t)
        
        filtered_by_amount = before_amount_filter - len(filtered_transactions)
        valid_transactions = filtered_transactions
        print(f"After amount filter (min: {min_amount}, max: {max_amount}): {len(valid_transactions)} transactions")
    
    final_count = len(valid_transactions)
    
    # Create filter summary
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': final_count
    }
    
    return valid_transactions, invalid_count, filter_summary

