"""
Main entry point for the Sales Analytics System.
"""

import os
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    find_peak_sales_day,
    daily_sales_trend,
    region_wise_sales,
    top_selling_products,
    low_performing_products,
    customer_analysis,
    generate_sales_report
)
from utils.api_handler import (
    get_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():
    """
    Main execution function

    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations

    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors

    Expected Console Output:
    ========================================
    SALES ANALYTICS SYSTEM
    ========================================

    [1/10] Reading sales data...
    ✓ Successfully read 95 transactions

    [2/10] Parsing and cleaning data...
    ✓ Parsed 95 records

    [3/10] Filter Options Available:
    Regions: North, South, East, West
    Amount Range: ₹500 - ₹90,000

    Do you want to filter data? (y/n): n

    [4/10] Validating transactions...
    ✓ Valid: 92 | Invalid: 3

    [5/10] Analyzing sales data...
    ✓ Analysis complete

    [6/10] Fetching product data from API...
    ✓ Fetched 30 products

    [7/10] Enriching sales data...
    ✓ Enriched 85/92 transactions (92.4%)

    [8/10] Saving enriched data...
    ✓ Saved to: data/enriched_sales_data.txt

    [9/10] Generating report...
    ✓ Report saved to: output/sales_report.txt

    [10/10] Process Complete!
    ========================================
    """
    try:
        # Welcome message
        print("=" * 50)
        print(" " * 15 + "SALES ANALYTICS SYSTEM")
        print("=" * 50)
        print()

        # Step 1: Read sales data
        print("[1/10] Reading sales data...")
        try:
            input_file = 'data/sales_data.txt'
            raw_lines = read_sales_data(input_file)
            print(f"✓ Successfully read {len(raw_lines)} transactions")
        except Exception as e:
            print(f"✗ Error reading sales data: {str(e)}")
            return
        print()

        # Step 2: Parse and clean transactions
        print("[2/10] Parsing and cleaning data...")
        try:
            transactions = parse_transactions(raw_lines)
            print(f"✓ Parsed {len(transactions)} records")
        except Exception as e:
            print(f"✗ Error parsing transactions: {str(e)}")
            return
        print()

        # Step 3: Display filter options
        print("[3/10] Filter Options Available:")
        try:
            # Get available regions and amount range from transactions
            regions = sorted(set(t.get('Region', '') for t in transactions if t.get('Region')))
            amounts = [t.get('Quantity', 0) * t.get('UnitPrice', 0.0) for t in transactions]
            min_amount = min(amounts) if amounts else 0
            max_amount = max(amounts) if amounts else 0
            
            print(f"Regions: {', '.join(regions)}")
            print(f"Amount Range: ₹{min_amount:,.2f} - ₹{max_amount:,.2f}")
            print()
            
            # Ask user if they want to filter
            filter_choice = input("Do you want to filter data? (y/n): ").strip().lower()
            
            region_filter = None
            min_amount_filter = None
            max_amount_filter = None
            
            if filter_choice == 'y':
                # Ask for region filter
                region_input = input(f"Enter region to filter (or press Enter to skip): ").strip()
                if region_input and region_input in regions:
                    region_filter = region_input
                
                # Ask for amount filters
                min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
                if min_input:
                    try:
                        min_amount_filter = float(min_input)
                    except ValueError:
                        print("Invalid minimum amount, skipping...")
                
                max_input = input("Enter maximum amount (or press Enter to skip): ").strip()
                if max_input:
                    try:
                        max_amount_filter = float(max_input)
                    except ValueError:
                        print("Invalid maximum amount, skipping...")
        except Exception as e:
            print(f"✗ Error in filter options: {str(e)}")
            region_filter = None
            min_amount_filter = None
            max_amount_filter = None
        print()

        # Step 4: Validate transactions
        print("[4/10] Validating transactions...")
        try:
            valid_transactions, invalid_count, filter_summary = validate_and_filter(
                transactions,
                region=region_filter,
                min_amount=min_amount_filter,
                max_amount=max_amount_filter
            )
            print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        except Exception as e:
            print(f"✗ Error validating transactions: {str(e)}")
            valid_transactions = transactions
        print()

        # Step 5: Perform data analyses
        print("[5/10] Analyzing sales data...")
        try:
            # Call all analysis functions (they're called internally by generate_sales_report)
            # But we can call them here to ensure they work
            total_revenue = calculate_total_revenue(valid_transactions)
            peak_day = find_peak_sales_day(valid_transactions)
            daily_trend = daily_sales_trend(valid_transactions)
            region_stats = region_wise_sales(valid_transactions)
            top_products = top_selling_products(valid_transactions, n=5)
            low_products = low_performing_products(valid_transactions, threshold=10)
            customer_stats = customer_analysis(valid_transactions)
            print("✓ Analysis complete")
        except Exception as e:
            print(f"✗ Error in analysis: {str(e)}")
        print()

        # Step 6: Fetch products from API
        print("[6/10] Fetching product data from API...")
        try:
            api_response = get_all_products()
            products_list = api_response.get('products', [])
            print(f"✓ Fetched {len(products_list)} products")
        except Exception as e:
            print(f"✗ Error fetching products from API: {str(e)}")
            print("  Continuing without API enrichment...")
            products_list = []
        print()

        # Step 7: Enrich sales data
        print("[7/10] Enriching sales data...")
        enriched_transactions = valid_transactions.copy()
        try:
            if products_list:
                product_mapping = create_product_mapping(api_response)
                enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
                enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match', False))
                success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
                print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")
            else:
                print("⚠ Skipped (no API data available)")
        except Exception as e:
            print(f"✗ Error enriching data: {str(e)}")
            print("  Using original transactions...")
        print()

        # Step 8: Save enriched data
        print("[8/10] Saving enriched data...")
        try:
            save_enriched_data(enriched_transactions, 'data/enriched_sales_data.txt')
            print("✓ Saved to: data/enriched_sales_data.txt")
        except Exception as e:
            print(f"✗ Error saving enriched data: {str(e)}")
        print()

        # Step 9: Generate report
        print("[9/10] Generating report...")
        try:
            generate_sales_report(valid_transactions, enriched_transactions, 'output/sales_report.txt')
            print("✓ Report saved to: output/sales_report.txt")
        except Exception as e:
            print(f"✗ Error generating report: {str(e)}")
        print()

        # Step 10: Success message
        print("[10/10] Process Complete!")
        print("=" * 50)
        print()
        print("Generated Files:")
        print("  - data/enriched_sales_data.txt")
        print("  - output/sales_report.txt")
        print()
        print("Thank you for using Sales Analytics System!")

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()