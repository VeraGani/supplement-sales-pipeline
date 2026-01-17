# Purpose of the script: validate raw data and produce a cleaned data csv file only if validation rules pass.

# Input: raw data is located in data/raw folder; the dataset has one row per transaction and follows the expected column schema defined in the script.

# Output: cleaned csv file ready for further analysis; the newly created file is saved at data/cleaned folder;
# the final cleaned table structure matches the original input schema; the file is overwritten with each successful run. If any validation fails, the script exits with an error and the output csv file is not created.

# Pre-requisites: Python environment with pandas and numpy installed.

# Allowed value lists (Product Name, Category, Location, Platform) are defined in the script as constants. The expected table schema and required columns are defined in the script as constants.

# Steps:
# 1. open the raw data file
# 2. validate table structure against the expected schema
# 3. convert data type in Date column from object to datetime, validate success of conversion
# 4. validate data types in all columns after Date column conversion 
# 5. validate Product Name column by checking that all values are in the allowed Product Name list
# 6. validate Category column by checking that all values are in the allowed Category list
# 7. validate Sold Units column by checking that values are integers and not negative
# 8. validate Units Returned column by checking that values are integers and not negative, and validating that Units Returned do not exceed Units Sold
# 9. validate Price column by checking that values are positive
# 10. validate Discount column by checking that values are between 0 and 1
# 11. validate Revenue column by creating three temporary columns for three possible revenue calculation formulas
# 12. compare respective values in each of the three new columns with the original Revenue column
# 13. create three temporary columns with True / False validation results for revenue consistency
# 14. validate that for each row at least one Revenue formula matches the original Revenue value within a small tolerance; if not, exit with an error
# 15. validate Location column by checking that all values are in the allowed Location list
# 16. validate Platform column by checking that all values are in the allowed Platform list
# 17. drop all temporary columns created for revenue calculation and validation
# 18. validate missing values by checking that required columns (as defined in the script schema) have no missing values
# 19. create csv file with cleaned data

# Imports
from pathlib import Path
import sys
import pandas as pd
import numpy as np

# Constants
RAW_PATH = Path("data/raw/Supplement_Sales_Weekly_Expanded.csv")

CLEAN_PATH = Path("data/cleaned/supplement_sales_cleaned.csv")

REQUIRED_COLUMNS = {
    "Date", 
    "Product Name", 
    "Category", 
    "Units Sold", 
    "Price", 
    "Revenue", 
    "Discount", 
    "Units Returned", 
    "Location", 
    "Platform"
}

ALLOWED_PRODUCT_NAMES = {
    "Whey Protein", 
    "Vitamin C", 
    "Fish Oil", 
    "Multivitamin", 
    "Pre-Workout", 
    "BCAA", 
    "Creatine", 
    "Zinc", 
    "Collagen Peptides", 
    "Magnesium", 
    "Ashwagandha", 
    "Melatonin", 
    "Biotin", 
    "Green Tea Extract", 
    "Iron Supplement", 
    "Electrolyte Powder"
}

ALLOWED_CATEGORIES = {
    "Vitamin", 
    "Mineral", 
    "Protein", 
    "Performance", 
    "Omega", 
    "Amino Acid", 
    "Herbal", 
    "Sleep Aid", 
    "Fat Burner", 
    "Hydration"
}

ALLOWED_LOCATIONS = {
    "Canada", 
    "UK", 
    "USA"
}

ALLOWED_PLATFORMS = {
    "iHerb", 
    "Amazon", 
    "Walmart"
}

TOLERANCE = 0.01

# Functions

# Validate that the data frame contains all the required columns, raise an error if there are missing columns
def validate_schema(df: pd.DataFrame, required_columns: set) -> None:
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Schema validation failed. Missing required columns: {missing_columns}"
        )

# Convert data type into datetime in Date column. 
# Exit with error if conversion fails.
def convert_date(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerse")
    except Exception as e:
        raise ValueError(f"Date conversion failed with error: {e}")
    
    if df["Date"].isna().any():
        raise ValueError("Data conversion failed: invalid or missing date values found.")
    
    return df

# Validate that all columns have the expected data types after conversion of Date column. 
# Exit with an error if any column has an unexpected data type.

def validate_dtypes(df: pd.DataFrame) -> None:
    expected_dtypes = {
        "Date": "datetime64[ns]", 
        "Product Name": "object", 
        "Category": "object", 
        "Units Sold": "int64", 
        "Price": "float64", 
        "Revenue": "float64", 
        "Discount": "float64", 
        "Units Returned": "int64", 
        "Location": "object", 
        "Platform": "object"
    }

    mismatches = {}

    for col, expected in expected_dtypes.items():
        if col not in df.columns:
            continue

        actual = str(df[col].dtype)
        if actual != expected:
            mismatches[col] = {"expected": expected, "actual": actual}
    
    if mismatches:
        raise ValueError(f"Dtype validation failed: {mismatches}")
    
load_raw_data(path)


validate_dtypes(df)
validate_allowed_values(df, column, allowed_values)
validate_sold_units(df)
validate_units_returned(df)
validate_price(df)
validate_discount(df)
validate_revenue(df, tolerance)
drop_temporary_columns(df)
validate_missing_required(df, required_columns)
write_clean_csv(df, out_path)

main()

if _name_ == "_main_": main()