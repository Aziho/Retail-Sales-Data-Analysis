
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
"-------------------------Load Data-------------------------------------"
pd.set_option('display.max_columns', None)
path=""
df=pd.read_csv(path+"retail_sales_dirty_project.csv")
"-----------------------Data Inspection---------------------------------"
print(df.head())
print(df.describe())
df.info()
print(df.dtypes)
print(df.shape)
"------------------------------Standardized Region-----------------------"
print(df['Region'].unique())
df['Region']=df['Region'].str.strip()

"-----------------------Customer_ID Cleaning ---------------------------"
print(df[df['Customer_ID'].isna()])
print(df[df['Customer_ID'].notna()])
print(df['Customer_ID'].isna().sum())
df['Customer_ID']=df['Customer_ID'].fillna('unknown')
"-----------------------Salesperson Cleaning ---------------------------"
print(df['Customer_ID'].isna().sum())
print(df[df['Salesperson'].isna()])
print(df[df['Salesperson'].notna()])
df['Salesperson']=df['Salesperson'].fillna('unknown')
print(df['Salesperson'].isna().sum())

"-----------------------UnitPrice Cleaning---------------------------"
print(df[df['Unit_Price'].isnull()])
price_numeric = pd.to_numeric(df['Unit_Price'], errors='coerce')
print(df[price_numeric.isna()][['Product', 'Unit_Price']])
print(df['Unit_Price'].isna().sum())
print(price_numeric.isna().sum())
"****To check the unit price that are not notna in dataframe but they didnt get numeric and are Nan****"
problem_prices = df[df['Unit_Price'].notna() & price_numeric.isna()]

"***values with $ couldnt get numberic. they are replaced with '' and then numeric"
print(problem_prices[['Product', 'Unit_Price']])

# Remove currency symbols and convert prices to numeric
df['Unit_Price']=df['Unit_Price'].str.replace('$','',regex=False)
df['Unit_Price']=pd.to_numeric(df['Unit_Price'], errors='coerce')
print(df['Unit_Price'].isna().sum())
print(df['Unit_Price'].dtypes)
print(df['Product'].unique())
# Fill missing prices with the median price of the corresponding product
product_median = df.groupby('Product')['Unit_Price'].transform('median')
df['Unit_Price']=df['Unit_Price'].fillna(product_median)

"---------------------Standardized Productname---------------------------------"
df['Product'] = df['Product'].str.strip()

"-----------------------PaymentMethod Cleaning ---------------------------"
print(df[df['Payment_Method'].isna()])
print(df['Payment_Method'].unique())
df['Payment_Method']=df['Payment_Method'].str.lower()
print(df['Payment_Method'].unique())
df['Payment_Method']=df['Payment_Method'].fillna('unknown')
print(df.isna().sum())
"-----------------------Category Cleaning ---------------------------"
print(df['Category'].unique())
df['Category'] = df['Category'].str.strip().str.lower()
"-----------------------Order Date Cleaning ---------------------------"
print(df['Order_Date'].dtype)
print(df['Order_Date'].unique())

"Because the date format is different in the rows "
# Convert mixed date formats to datetime
orderdate=pd.to_datetime(df['Order_Date'], format='mixed', errors='coerce')
df['Order_Date']=orderdate
print(df['Order_Date'].isna().sum())
print(df['Order_Date'].dtypes)
"-----------------------Discount cleaning column---------------------------"
# Convert percentage strings such as "20%" to decimal values
print(df['Discount'].dtype)
print(df['Discount'].unique())
has_percent = df['Discount'].str.contains('%')
print(has_percent.sum())
print(df[has_percent])
print(df.loc[has_percent, 'Discount'])
percent_value=df.loc[has_percent, 'Discount'].str.replace('%','',regex=False)
percent_value=pd.to_numeric(percent_value, errors='coerce')
percent_value= percent_value /100
df.loc[has_percent, 'Discount']=percent_value.astype('str')

# Convert the entire Discount column to numeric
df['Discount']=pd.to_numeric(df['Discount'], errors='coerce')
print(df['Discount'].unique())
print(df['Discount'].isna().sum())

"-----------------------Quantity cleaning column---------------------------"
print(df['Quantity'].dtype)
print(df['Quantity'].unique())
print(df[df['Quantity']=='unknown'])
# Convert quantity to numeric; invalid values become NaN
quantitynumeric=pd.to_numeric(df['Quantity'], errors='coerce')
# Fill missing quantities with the median quantity for the corresponding product
quntitymedian=quantitynumeric.groupby(df['Product']).transform('median')
quantitynumeric.fillna(quntitymedian, inplace=True)
df['Quantity']=quantitynumeric
print(df['Quantity'].dtype)

"***be reminded that next line dont change the data type only it will change datatype while printing"
print(df['Quantity'].astype(int))
df['Quantity'] = df['Quantity'].astype(int)
"-------Validation--------"
print(df['Quantity'].dtype)
print(df['Quantity'].unique())
print(df['Quantity'].isna().sum())
"--------------------------------------- Remove Duplicates----------------------------------"
"Which rows are completely same"
print(df[df.duplicated(keep=False)])
print(df.duplicated().sum())
print(df['Order_ID'].duplicated().sum())
print("all duplicate rows:", df.duplicated(keep=False).sum())
print("extra duplicate rows:", df.duplicated().sum())
print("total rows:", len(df))
df=df.drop_duplicates()
print(df.shape)
print(df.duplicated().sum())
print(df['Order_ID'].duplicated().sum())
"-------------Cleaning Validation---------------------------------"
print(df.dtypes)
print("Dataset shape after cleaning:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())
# Validate numeric ranges
print(df[(df['Discount']<0) | (df['Discount'] >1)])
print(df[(df['Quantity']<1)])

"-------------Unit Price negative Validation--------------------------------"
# Assume non-positive prices are data errors rather than refunds
print(df[(df['Unit_Price']<=0)])
print(df[(df['Product']=='Storage Bench')])
unitpricemedian=df.groupby('Product')['Unit_Price'].transform('median')
negativeunipricevalues=df['Unit_Price']<=0
"-----in this case, we assumed d=negative values are errors, not refund"
df.loc[negativeunipricevalues,'Unit_Price']= unitpricemedian
print("\nInvalid unit prices after correction:")
print(df[(df['Unit_Price']<=0)])
"-------------Feature Creation-------------------------------------------------"
# Calculate sales metrics
df['Gross_Sales'] = df['Quantity'] * df['Unit_Price']
df['Discount_Amount'] = df['Gross_Sales'] * df['Discount']
df['Net_amount'] = df['Gross_Sales'] - df['Discount_Amount']

print(df[['Discount', 'Quantity', 'Unit_Price',
    'Gross_Sales', 'Discount_Amount', 'Net_amount']].isna().sum())
print("\nOrders where net amount exceeds gross sales:")
print(df[df['Net_amount'] > df['Gross_Sales']])

"---------------------------Orders in months---------------------------"
"year month is the best way for time-base analysis"
df['Order_Month']=df['Order_Date'].dt.to_period('M')
print(df['Order_Month'])

"***------------------------Data Analysis----------------------------***"
"How much is the total Net Sales?"
Total_Net_Sales=df['Net_amount'].sum()
print("Total Net Sales:", format(Total_Net_Sales, '.2f'))

"How much is each Region's Net Sales?"
print(df.groupby('Region')['Net_amount'].sum())

"Which region generated the highest net sales?"
# Total net sales by region
region_sales=df.groupby('Region')['Net_amount'].sum().sort_values(ascending=False)
print("\nNet Sales by Region:")
print(region_sales.round(2))

"How many orders were placed in each region?"
print(df.groupby('Region')['Order_ID'])
# Business Question:
# Why did North Vancouver generate the highest net sales?
# - Did it have more orders than other regions?
# - Or did it have a similar number of orders but a higher average order value?
# To investigate, we will compare:
# 1. Total number of orders by region
# 2. Average Order Value (AOV) by region
print(df.groupby('Region')['Order_ID'].count().sort_values(ascending=False))
print(df.groupby('Region')['Net_amount'].mean().sort_values(ascending=False))
"""***Insight:
  North Vancouver generated the highest total net sales primarily because,
 it had the highest number of orders (261), not because it had the highest
 average order value.
 Surrey had the highest AOV, but fewer orders than North Vancouver.*** """
# Business Question:
# Which product generated the highest net sales?
# We will compare total net sales across products
# to identify the highest-performing product.
print(df.groupby('Product')['Net_amount'].sum().sort_values(ascending=False).round(2))
# Business Question:
# Why did Sideboard generate the highest net sales?
# - Did it have more orders than other products?
# - Or did it have a similar number of orders but a higher average order value?
# To investigate, we will compare:
# 1. Total number of orders by product
# 2. Average Order Value (AOV) by Product
print(df.groupby('Product')['Order_ID'].count().sort_values(ascending=False))
print(df.groupby('Product')['Net_amount'].mean().sort_values(ascending=False).round(2))
""" Insight:
Sideboard generates the highest Total Net Sale even though it did not have the highest number of orders
It had 128 orders, compared with 139 orders for both cabinets and Storage Bench
It high net sales were driven by the highest average order value at approximately $2.3K
"""# Business Question:
# How did net sales change over time?
# What were the strongest and weakest sales months?
print(df.groupby('Order_Month')['Net_amount'].sum())
Ordermonthsale=df.groupby('Order_Month')['Net_amount'].sum()
print('\n','Highest sale month:',Ordermonthsale.idxmax(), 'Highest Netsale:',Ordermonthsale.max().round(2),'\n')
print('Lowest sale month:',Ordermonthsale.idxmin(),'Lowest Netsale:',Ordermonthsale.min().round(2))

# Business Question:
# How did net sales change from month to month?
'We need to calculate Monthly sale and then see the percentage changes'
print(round(Ordermonthsale.pct_change()*100,2))

# Business Question:
# Which product category generated the highest net sales?
print('$'+df.groupby('Category')['Net_amount'].sum().sort_values(ascending=False).round(2).astype(str))

# Business Question:
# Which salesperson generated the highest net sales?
print(df.groupby('Salesperson')['Net_amount'].sum().sort_values(ascending=False).round(2))

# Was the salesperson's performance driven by a higher number of orders or a higher average order value?
print(df.groupby('Salesperson')['Order_ID'].count().sort_values(ascending=False))
print(df.groupby('Salesperson')['Net_amount'].mean().sort_values(ascending=False).round(2))
"""# Insight:
David generated the highest total net sales ($281,647.07).
However, he did not have the highest number of orders or the highest AOV.
Sara had the most orders, while John had the highest AOV among known salespeople.
David's leading net sales resulted from a combination of relatively high
order volume and relatively high average order value."""

# Business Question:
# Which payment methods were used most frequently by customers?
print(df.groupby('Payment_Method')['Net_amount'].sum().sort_values(ascending=False).round(2))
print(df['Payment_Method'].value_counts())
""" Insight:
 Credit card was the most frequently used payment method with 304 orders,
 closely followed by cash with 301 orders.
 Credit card also generated the highest total net sales at $381,233.42."""

# Business Question:
# How do net sales vary by season?
# Which season generated the highest net sales?
df['Month']=df['Order_Date'].dt.month
print(df['Month'].unique())
def get_season(month):
    if month in (12,1,2):
        return 'Winter'
    elif month in (3,4,5):
        return 'Spring'
    elif month in (6,7,8):
        return 'Summer'
    elif month in (9,10,11):
        return 'Fall'
df['Season']=df['Month'].apply(get_season)
df['Year']=df['Order_Date'].dt.year
print(df.groupby(['Year','Season'])['Net_amount'].sum())
"""Seasonal Insight:
 In 2025, Spring generated the highest net sales, while Summer generated
 the lowest net sales.
 Seasonal comparisons should be interpreted carefully because the dataset
 does not contain complete seasonal data for all years."""

"""-----------------------------------------------------------------------------------------------------
-----------------------------------VISUALIZATION--------------------------------------------------------"""
"How are sale trending?"
X=Ordermonthsale.index.astype(str)
Y=Ordermonthsale.values
plt.figure(figsize=(14,8))
plt.xticks(rotation=60)
plt.title('Sale trending by month')
plt.xlabel('Month')
plt.ylabel('Net Sales $')
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'${x/1000:.0f}K'))
plt.plot(X,Y)
plt.show()
#What drove the sales spike in October 2025?
Monthly_orders=df.groupby('Order_Month')['Order_ID'].nunique().sort_values(ascending=False)
print(df.groupby('Order_Month')['Net_amount'].mean().sort_values(ascending=False))
print('\n Number of orders in October 2025:',Monthly_orders.loc['2025-10'])
""" First :The sales spike in October 2025 was primarily driven by a significantly higher
 AOV rather than a higher number of orders. October had 55 orders, while AOV reached approximately 
 $2,040, substantially higher than in other months."""
#Why was AOV so high in October?
October_2025=df[df['Order_Month']=='2025-10']
print(October_2025.groupby('Product')['Net_amount'].sum().sort_values(ascending=False).round(2))
"""Insight:October 2025 recorded the highest monthly net sales. The increase was not driven by
 unusually high order volume, as the month had only 55 orders. Instead, AOV increased to approximately 
 $2,040. Further analysis showed that Cabinet and Coffee Table sales were major contributors, 
 generating approximately $73K combined."""

#Which regions generate the most net sales?
regionsale=df.groupby('Region')['Net_amount'].sum().sort_values(ascending=False)
print(regionsale)
X=regionsale.index
Y=regionsale.values
plt.figure(figsize=(10, 6),facecolor='yellow')
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'${x/1000:.0f}K'))
plt.title('Net Sale by Region')
plt.xlabel('Region')
plt.ylabel('Net Sales $')
bars=plt.bar(X,Y,color='blue')
lables1=[]
for value in Y:
    lables1.append('$'+str(round(value/1000))+'k')
plt.bar_label(bars,labels=lables1)
plt.show()
"""Insight: North Vancouver generated the highest net sales at approximately $305K.
The result was primarily driven by higher order volume, with North Vancouver recording 261 orders, the highest among all regions.
Surrey had the highest AOV, but its lower order volume resulted in lower total net sales than North Vancouver."""

#which product generate the most net sales?
productnetsale=df.groupby('Product')['Net_amount'].sum().sort_values(ascending=False)
X=productnetsale.index
Y=productnetsale.values
plt.figure(figsize=(14, 9))
plt.title('Net Sales by Product')
plt.ylabel('Product')
plt.xlabel('Net Sales $')
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda Y, pos: f'${Y/1000:.0f}K'))
hbars=plt.barh(X,Y,color='blue')
lables2=[]
for value in Y:
    lables2.append('$'+str(round(value/1000))+'k')
plt.bar_label(hbars,labels=lables2)
plt.show()
"""Insight: Sideboard generated the highest net sales at approximately $295K, followed by Cabinet at approximately $279K.
Sideboard did not have the highest number of orders. Its strong performance was primarily driven by the highest AOV, 
at approximately $2.3K. This indicates that higher-value purchases, rather than higher order volume, were the main driver 
of Sideboard's leading net sales."""
# Salesperson Performance Analysis
# Which salesperson generated the highest net sales?
# Was the performance driven by higher order volume or higher average order value (AOV)?
known_salespeople = df[df['Salesperson'] != 'unknown']
salespersonssale=known_salespeople.groupby('Salesperson')['Net_amount'].sum().sort_values(ascending=False).round(2)
X=salespersonssale.index
Y=salespersonssale.values
plt.figure(figsize=(12, 8))
hbars=plt.barh(X,Y,color='Red')
lables3=[]
for value in Y:
    lables3.append('$'+str(round(value/1000))+'k')
plt.bar_label(hbars,labels=lables3)
plt.title('Net Sales by Salesperson')
plt.xlabel('Net Sales $')
plt.ylabel('Salesperson')
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda Y, pos: f'${Y/1000:.0f}K'))

# Was the salesperson's performance driven by a higher number of orders or a higher average order value?
print(df.groupby('Salesperson')['Order_ID'].count().sort_values(ascending=False))
print(df.groupby('Salesperson')['Net_amount'].mean().sort_values(ascending=False).round(2))

plt.show()

#How does order value distribution vary across regions?
groups = df.groupby('Region')['Net_amount']
box_data=[]
box_region=[]
for region, values in groups:
    box_region.append(region)
    box_data.append(values)
plt.boxplot(box_data, tick_labels=box_region)
plt.show()
#what is the highest sale product for Surrey?
surrey_max = df[df['Region'] == 'Surrey']['Net_amount'].max()
print(df[(df['Region'] == 'Surrey') & (df['Net_amount'] == surrey_max)])
print(df['Quantity'].describe())
print(df[df['Quantity']> 10])
"""Outlier Investigation:
The box plot identified several unusually high order values.
 Further investigation showed that four orders had a quantity of 50, 
 while the typical order quantity was much lower, with a median of 3.
These high-quantity orders contributed to some of the largest outliers, 
including a $33,557 Cabinet order in Surrey and a $17,490.60 Coffee Table order in Vancouver.
Since there was no evidence that these orders were data errors,
 they were kept in the dataset rather than removed."""
"""Insight:Order Value Distribution by Region:
Order values are fairly similar across the different regions. 
The median order value is also similar, although Burnaby has a slightly higher median.
There are some outliers, especially in Surrey. 
After checking these orders, we found that some of the high values came from orders 
with a quantity of 50.
Since there was no evidence that these orders were data errors, we kept them in the 
dataset."""

#How are order values distributed?
plt.figure(figsize=(10, 6))
plt.hist(df['Net_amount'], bins=20)
plt.title('Order Value Distribution')
plt.xlabel('Order Value ($)')
plt.ylabel('Number of Orders')
plt.show()
"""Order Value Distribution:
Most orders have relatively low values,
 while only a small number of orders have very high values. 
This creates a right-skewed distribution.
"""
#Is there a relationship between unit price and order value?
plt.scatter( df['Unit_Price'],df['Net_amount'])
plt.title('Unit Price vs. Order Value')
plt.xlabel('Unit Price ($)')
plt.ylabel('Order Value ($)')
plt.show()

#Do higher discounts lead to higher order values?
discount_aov=df.groupby('Discount')['Net_amount'].mean()
X=discount_aov.index
Y=discount_aov.values
plt.scatter(X,Y)
plt.show()
"""Insight:Discount vs. Average Order Value:
Higher discounts were not associated with higher average order values.
Overall, orders with lower discounts had higher average values in this dataset."""

"-----------------------------------------------------DataFrame to CSV----------------------------------------------"
df.to_csv('cleaned_retail_sale.csv',index=False)
