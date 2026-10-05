# Retail-Sales-Data-Analysis

1. Project Overview
2. Dataset
3. Data Cleaning
4. Feature Engineering
5. Business Questions
6. Visualizations
7. Key Insights
8. Tools Used

## Project Overview
In this project, I analyzed data from a furniture retail store using Python. I cleaned and standardized the data and handled missing and unknown values.
The analysis answers different business questions, including sales by region, sales by category, salesperson performance, product performance, and sales trends over time.

To better understand the results, I created different charts and visualizations. These visualizations help stakeholders understand sales performance, trends, and patterns in the data.
## Dataset
The original dataset is a CSV file including 1,218 rows and 11 columns: Order_ID, Order_Date, Customer_ID, Region, Product, Category, Unit_Price, Quantity, Payment_Method, Salesperson, and Discount.
For practicing different data anomalies and data quality issues, I used an AI-generated dataset containing different types of data quality issues that needed to be identified and fixed.
## Data Cleaning
All the data was initially stored as strings. Each column needed to be considered individually based on its data type, null values, mismatched values, standardization, and inconsistencies.
- Order_ID: There were some duplicated records, which were identified and removed using the duplicated() and drop_duplicates() functions.
- Order_Date: There were 6 invalid/missing dates. I left them as null rather than removing the entire rows because the other data in those rows could still be useful for the analysis.
- Customer_ID: Some values were missing and were filled with unknown.
- Region: Region names had inconsistencies that needed to be standardized.
- Product and Category: These string columns also had inconsistent values that needed to be standardized.
- Unit_Price: Some products had missing unit prices, which I filled using the median price for the same product. There were also formatting issues such as $ symbols, which were removed before converting the column to numeric. Some unit prices had negative values. After checking the prices for the same products in other orders, I decided to replace the negative values with the median price for the same product.
- Quantity: A few records contained unknown quantities. I converted the column to numeric and filled these values using the median quantity for the same product.
- Payment_Method: This column had inconsistent text formatting, so I standardized the values and converted them to lowercase. Missing values were grouped as unknown.
- Salesperson: Some salesperson values were missing, so they were filled with unknown.
- Discount: The discount column was initially stored as a string and contained inconsistent formats, including both decimal and percentage values. I standardized these values and converted the column to numeric so the discounts could be calculated correctly.
## Feature Engineering
To analyze the sales trends, Gross_Sales, Discount_Amount, and Net_amount needed to be calculated. I calculated these values and added the three new columns to the dataset.
## Business Questions
This project focuses on answering the following business questions:
1. Which region generates the highest net sales?
2. Which products generate the highest net sales?
3. How do sales change over time?
4. Which salesperson has the strongest sales performance?
5. Which payment methods are used most frequently?
6. How do order values vary across regions?
7. How are order values distributed?
8. Is there a relationship between unit price and order value?
9. Is there a relationship between discount and average order value?
10. Are there any seasonal patterns in sales?
## Visualization
### Monthly Sales Trend
images/Monthly_sales.png

