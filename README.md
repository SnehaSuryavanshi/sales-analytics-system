# Sales Analytics System

A comprehensive Python-based sales analytics system that processes transaction data, integrates with external APIs, and generates detailed analytical reports.

## Features

- **File Handling & Preprocessing**: Robust file reading with encoding handling, data parsing, and validation
- **Data Processing**: Comprehensive sales analysis including revenue calculations, region-wise performance, and customer insights
- **API Integration**: Fetches product data from DummyJSON API and enriches transaction data
- **Report Generation**: Generates detailed formatted reports with multiple analytical sections
- **Interactive Interface**: User-friendly console interface with filter options

## Prerequisites

- Python 3.7 or higher

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<SnehaSuryavanshi>/sales-analytics-system
cd sales-analytics-system
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is empty or missing, install manually:

```bash
pip install requests
```

## Project Structure

```
sales-analytics-system/
│
├── data/
│   └── sales_data.txt          # Input sales data file
│
├── output/
│   └── sales_report.txt         # Generated report (created after run)
│
├── utils/
│   ├── file_handler.py          # File reading, parsing, validation
│   ├── data_processor.py        # Data analysis functions
│   └── api_handler.py           # API integration functions
│
├── main.py                      # Main execution script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Usage

### Running the Application

1. **Ensure data file exists:**
   - Make sure `data/sales_data.txt` exists with your sales data
   - The file should be pipe-delimited format with header:
     ```
     TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
     ```

2. **Run the main script:**
   ```bash
   python main.py
   ```

### Interactive Workflow

The application will guide you through the following steps:

1. **Reading Sales Data** - Loads and parses the input file
2. **Parsing and Cleaning** - Processes and cleans transaction data
3. **Filter Options** - Shows available regions and amount ranges
   - You can choose to filter by region and/or amount range
   - Enter 'y' to apply filters, 'n' to skip
4. **Validation** - Validates transactions and shows summary
5. **Data Analysis** - Performs comprehensive sales analysis
6. **API Integration** - Fetches product data from DummyJSON API
7. **Data Enrichment** - Enriches transactions with API product information
8. **Saving Enriched Data** - Saves enriched data to file
9. **Report Generation** - Generates comprehensive sales report
10. **Completion** - Shows success message with file locations

### Example Run

```
==================================================
          SALES ANALYTICS SYSTEM
==================================================

[1/10] Reading sales data...
✓ Successfully read 70 transactions

[2/10] Parsing and cleaning data...
✓ Parsed 95 records

[3/10] Filter Options Available:
Regions: East, North, South, West
Amount Range: ₹500.00 - ₹90,000.00

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 92 | Invalid: 3

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
✓ Fetched 30 products

[7/10] Enriching sales data...
✓ Enriched 701/70 transactions (100%)

[8/10] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/10] Generating report...
✓ Report saved to: output/sales_report.txt

[10/10] Process Complete!
==================================================

Generated Files:
  - data/enriched_sales_data.txt
  - output/sales_report.txt

Thank you for using Sales Analytics System!
```

## Output Files

### 1. Enriched Sales Data
**Location:** `data/enriched_sales_data.txt`

Contains original transaction data enriched with API product information:
- Original fields: TransactionID, Date, ProductID, ProductName, Quantity, UnitPrice, CustomerID, Region
- New API fields: API_Category, API_Brand, API_Rating, API_Match

### 2. Sales Report
**Location:** `output/sales_report.txt`

Comprehensive report including:
- Overall Summary (Revenue, Transactions, AOV, Date Range)
- Region-wise Performance
- Top 5 Products
- Top 5 Customers
- Daily Sales Trend
- Product Performance Analysis
- API Enrichment Summary

## Configuration

### Input Data Format

The input file (`data/sales_data.txt`) should follow this format:

```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
T001|2024-12-01|P101|Laptop|2|45000|C001|North
T002|2024-12-01|P102|Mouse|5|500|C002|South
```

### Supported Encodings

The system automatically handles multiple file encodings:
- UTF-8
- Latin-1
- CP1252

## API Integration

The system integrates with [DummyJSON Products API](https://dummyjson.com/products):
- Base URL: `https://dummyjson.com/products`
- Fetches product information to enrich transaction data
- Handles API failures gracefully (continues without enrichment if API is unavailable)

## Error Handling

The application includes comprehensive error handling:
- File not found errors
- Encoding issues
- API connection failures
- Invalid data formats
- User input validation

All errors are displayed with user-friendly messages, and the application continues execution when possible.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'requests'**
   ```bash
   pip install requests
   ```

2. **FileNotFoundError: File 'data/sales_data.txt' not found**
   - Ensure the `data/` directory exists
   - Place your sales data file at `data/sales_data.txt`

3. **API Connection Errors**
   - Check your internet connection
   - The application will continue without API enrichment if the API is unavailable

4. **Encoding Errors**
   - The system tries multiple encodings automatically
   - If issues persist, ensure your file is saved in UTF-8 format

## Development

### Running Tests

To verify the system is working correctly:

```bash
python main.py
```

### Code Structure

- **utils/file_handler.py**: File I/O, parsing, validation
- **utils/data_processor.py**: Data analysis and report generation
- **utils/api_handler.py**: API integration and data enrichment
- **main.py**: Main execution flow and user interaction

## License

This project is part of a learning/assessment exercise.

## Support

For issues or questions, please check:
1. Ensure all dependencies are installed
2. Verify input file format
3. Check error messages for specific issues

---

**Note:** This system requires an active internet connection for API integration. The application will function without API access but will skip the enrichment step.