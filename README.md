This repo contains raw and cleaned up dataset, all done with Python.

The raw dataset Supplements weekly sales from Kaggle 
https://www.kaggle.com/datasets/zahidmughal2343/supplement-sales-data .

Workflow:
- Extracting raw CSV data
- Cleaning and transformiung data with Pandas: 
a) validated the date range
b) checked columns Product Name, Category for inconsistency, similar names, spelling errors
c) inspected columns Units Sols, Units Returned, Price, and Discount to find out min, max values, and negative and zero 
d) created 3 new columns with the Revenue values calculated with three different formulas. The newly columns were created to compare to the values in the original Revenue column to find out what formula was used to calculate the original Revenue. First column: Units Sold x Price; second column: Units Sold x Price x (1-Discount); third column: Units Sold x Price x Discount. For visual observation of the results of the comparuison 3 new columns were created: Comparison_1, Comparison_2, Comparison_3. As a result, formula #1 (Units Sold x Price) was used in calculation of the original Revenue. Two other columns (Comparison_2, Comparison_3) are kept for now for demonstration perposes only.
e) columns Location & Platform were inspected. In each column there are 3 unique values (USA, Canada, UK, and iHerb, Amazon, Walmart respectively). The distribution is logical and even. There are misspeling, trailings, excessive spaces in the strings. 

Tools used:
- Python
- Pandas
- Jupyter Notebook
- VS Code
