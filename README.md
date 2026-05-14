This repo contains raw and cleaned up dataset. File exploration and cleaning were performed with Python.

The raw dataset Supplements weekly sales from Kaggle 
https://www.kaggle.com/datasets/zahidmughal2343/supplement-sales-data .

## Workflow:
Extracting raw CSV data
Cleaning and transforming data with Pandas:
- Converted the Date column to datetime format
- Validated the date range
- Checked Product Name, Category, Location, and Platform for spelling issues, extra spaces, and inconsistent values
- Inspected Units Sold, Units Returned, Price, Revenue, and Discount for missing, zero, negative, minimum, and maximum values
- Validated the Revenue formula by comparing three possible calculations
- Removed temporary validation columns after confirming the formula

Revenue validation:

Three possible formulas were tested:
1. Units Sold × Price
2. Units Sold × Price × (1 - Discount)
3. Units Sold × Price × Discount

The validation showed that the original Revenue column was calculated as:

Revenue = Units Sold × Price

The cleaned data is stored as csv file in data/cleaned folder. 

##Reproduction preparation:
- prerequisites: Python version 3.9+, pandas, numpy
- raw csv file is stored at data/raw
- ipynb file is stored at notebooks folder
- the cleaned csv file is at data/cleaned

##Execution orrder:
1. Open 1_data_cleaning.ipynb and run it top to bottom
2. As a result of the run a new csv file will be produced. This is the file with the cleaned data. The successful run will prove that the validation passed. 

##Tools used:
- Python
- Pandas
- Jupyter Notebook
- VS Code

Current status:

This project currently includes data exploration, validation, and cleaning.

##Planned improvements:
- Refactor notebook logic into a Python script
- Add automated validation checks
- Load cleaned data into a SQL database
- Add SQL queries for sales and return analysis
- Prepare the project for a cloud-based data pipeline
