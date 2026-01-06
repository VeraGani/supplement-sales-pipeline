This repo contains raw and cleaned up dataset. File exploration and cleaning were performed with Python.

The raw dataset Supplements weekly sales from Kaggle 
https://www.kaggle.com/datasets/zahidmughal2343/supplement-sales-data .

Workflow:
- Extracting raw CSV data
- Cleaning and transformiung data with Pandas: 
a) validated the date range
b) checked columns Product Name, Category for inconsistency, similar names, spelling errors
c) inspected columns Units Sols, Units Returned, Price, and Discount to find out min, max values, and negative and zero 
d) created 3 new columns with the Revenue values calculated with three different formulas. The newly columns were created to compare to the values in the original Revenue column to find out what formula was used to calculate the original Revenue. First column: Units Sold x Price; second column: Units Sold x Price x (1-Discount); third column: Units Sold x Price x Discount. For programmatic validation of the results of the comparison 3 new columns were created: Comparison_1, Comparison_2, Comparison_3. As a result, formula #1 (Units Sold x Price) was used in calculation of the original Revenue. Later all the columns used for formula validation are dropped.
e) columns Location & Platform were inspected. In each column there are 3 unique values (USA, Canada, UK, and iHerb, Amazon, Walmart respectively). The distribution is logical and even. There are no misspeling, trailings, excessive spaces in the strings. 

The cleaned data is stored as csv file in data/cleaned folder. 

Reproduction preparation:
- prerequisites: Python version 3.9+, pandas, numpy
- raw csv file is stored at data/raw
- ipynb file is stored at notebooks folder
- the cleaned csv file is at data/cleaned

Execution orrder:
1. Open -1_data_cleaning.ipynb and run it top to bottom
2. As a result of the run a new csv file will be produced. This is the file with the cleaned data. The successful run will prove that the validation passed. 

Tools used:
- Python
- Pandas
- Jupyter Notebook
- VS Code
