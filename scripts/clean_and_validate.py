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

# Validate that each value in each column belong to the list of allowed values. If not, raise an error.
def validate_allowed_values(
        df: pd.DataFrame,
        column: str,
        allowed_values: set,
        *,
        allow_null: bool = False,
        normalize: bool = True
) -> None:
    if column not in df.columns:
        raise ValueError(f"Allowed values validation failed: column '{column}' not found.")
    
    series = df[column]

    #Normalize strings, trim whitespace
    if normalize and od.api.types.is_object_dtype(series):
        series = series.astype("string").str.strip()

    # Treat empty strings as missing
    empty_as_na = series.isna()
    if pd.api.types.is_string_dtype(series):
        empty_as_na = empty_as_na | (series == "")

    if not allow_null:
        if empty_as_na.amy():
            bad_rows = df.loc[empty_as_na, [column]].head(10)
            raise ValueError(
                f"Allowed values validation failed for '{column}':" 
                f"missing/blank values found. Examples: \n{bad_rows.to_string(index = True)}"
            ) 
        
    # Validate only non-missing values
    to_check = series[~empty_as_na] if allow_null else series

    invalid_mask = ~to_check.isin(allowed_values)
    if invalid_mask.any():
        invalid_values = sorted(set(to_check[invalid_mask].astype(str).unique()))
        examples = df.loc[to_check.index[invalid_mask], [colum]].head(10)

        raise ValueError(
            f"Allowed values validation failed for '{column}'."
            f"Invalid values: {invalid_values}."
            f"Example rows:\n{examples.to_string(index=True)}"
        )

# Validating Units Sold column, checking missing values, all values are integers and non-negative
def validate_sold_units(df: pd.DataFrame) -> None:

    coumn = "Units Sold"

    if column not in df.columns:
        raise ValueError(f"Units Sold validation failed: column'{column}' is missing")
    
    if df[column].isna().any():
        raise ValueError("Units Sold validation failed: missing value found")
    
    if not (df[column] % 1 == 0).all():
        raise ValueError("Units Sold validation failed: non-integer values found.")
    
    if (df[column] < 0).any():
        raise ValueError("Units Sold validation failed: negative values found.")
    
# Validating Units Returned column, the column must exist, the values non-negative integers, and do not surpass Units Sold
def validate_units_returned(df: pd.DataFrame) -> None:

    column = "Units Returned"
    sold_column = "Units Sold"

    if column not in df.columns:
        raise ValueError(f"Units Returned validation failed: column '{column}' is missing.")
    
    if sold_column not in df.columns:
        raise ValueError(f"Units Returned validation failed: required column '{sold_column}' is missing.")
    
    if df[column].isna().any():
        raise ValueError("Units Returned validation failed: missing values found.")
    
    if not (df[column] % 1 == 0).all():
        raise ValueError("Units Returned validation failed: non-integer values found.")
    
    if (df[column] < 0).any():
        raise ValueError("Units Returned validation failed: negative values found.")
    
    if (df[column] > df[sold_column]).any():
        raise ValueError("Units Returned validation failed: returned units exceed sold units.")

# Validating Price column, column must exist, no missing values, values numeric and positive
def validate_price(df: pd.DataFrame) -> None:

    column = "Price"

    if column not in df.columns:
        raise ValueError(f"Price validation failed: column '{column}' is missing.")
    
    if df[column].isna().any():
        raise ValueError("Price validation failed: missing values found.")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError("Price validation failed: non-numeric values found.")
    
    if (df[column] <= 0).any():
        raise ValueError("Price validation failed: zero or negative values found.")
    
# Validating Discount column, column must exist, values numeric, non-negative, and between 0 and 1 inclusive
def validate_discount(df: pd.DataFrame) -> None:

    column = "Discount"

    if column not in df.columns:
        raise ValueError(f"Discount column validation failed: column '{column}' is missing.")
    
    if df[column].isna().any():
        raise ValueError("Discount column validation failed: missing values found.")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError("Discount validation failed: non-numeric values found.")
    
    if ((df[column] < 0) | (df[column] > 1)).any():
        raise ValueError("Discount column validation failed: values outside range 0... 1 found.")

# Validating Reveinue column by checlking that each row match at least one of 3 possible formulas for calculating revenue within the given tolerance.
def validate_revenue(df: pd.DataFrame, tolerance: float) -> None:
    required_columns = {"Revenue", "Units Sold", "Price", "Discount"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Revenue validation failed: missing required columns {missing}")
    
    revenue_f1 = df["Units Sold"] * df["price"]
    revenue_f2 = df["Units Sold"] * df["Price"] * (1 - df["Discount"])
    revenue_f3 = df["Units Sold"] * df["Price"] * df["Discount"]

    match_f1 = np.isclose(df["Revenue"], revenue_f1, atol=tolerance)
    match_f2 = np.isclose(df["Revenue"], revenue_f2, atol=tolerance)
    match_f3 = np.isclose(df["Revenue"], revenue_f3, atol=tolerance)

    valid_rows = match_f1 | match_f2 | match_f3

    if not valid_rows.all():
        failed_count = (~valid_rows).sum()
        raise ValueError(f"Revenue validation failed: {failed_count} rows do not match any valid formula")
    

drop_temporary_columns(df)
validate_missing_required(df, required_columns)
write_clean_csv(df, out_path)

main()

if _name_ == "_main_": main()