Purpose of the script: validate raw data and produce a cleaned data csv file only if validation rules pass.

Input: raw data is located in data/raw folder; the dataset has one row per transaction and follows the expected column schema defined in the script.

Output: cleaned csv file ready for further analysis; the newly created file is saved at data/cleaned folder;
the final cleaned table structure matches the original input schema; the file is overwritten with each successful run. If any validation fails, the script exits with an error and the output csv file is not created.

Pre-requisites: Python environment with pandas and numpy installed.

Allowed value lists (Product Name, Category, Location, Platform) are defined in the script as constants. The expected table schema and required columns are defined in the script as constants.

Steps:
1. open the raw data file
2. validate table structure against the expected schema
3. convert data type in Date column from object to datetime, validate success of conversion
4. validate data types in all columns after Date column conversion 
5. validate Product Name column by checking that all values are in the allowed Product Name list
6. validate Category column by checking that all values are in the allowed Category list
7. validate Sold Units column by checking that values are integers and not negative
8. validate Units Returned column by checking that values are integers and not negative, and validating that Units Returned do not exceed Units Sold
9. validate Price column by checking that values are positive
10. validate Discount column by checking that values are between 0 and 1
11. validate Revenue column by creating three temporary columns for three possible revenue calculation formulas
12. compare respective values in each of the three new columns with the original Revenue column
13. create three temporary columns with True / False validation results for revenue consistency
14. validate that for each row at least one Revenue formula matches the original Revenue value within a small tolerance; if not, exit with an error
15. validate Location column by checking that all values are in the allowed Location list
16. validate Platform column by checking that all values are in the allowed Platform list
17. drop all temporary columns created for revenue calculation and validation
18. validate missing values by checking that required columns (as defined in the script schema) have no missing values
19. create csv file with cleaned data