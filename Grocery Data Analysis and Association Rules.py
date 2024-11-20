# Databricks notebook source
# MAGIC %md
# MAGIC Created By:
# MAGIC
# MAGIC Mukul Aggarwal
# MAGIC
# MAGIC MSD23007

# COMMAND ----------

import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

# COMMAND ----------

import plotly.express as px
import plotly.io as pio

# COMMAND ----------

# Load the table into a DataFrame
df = spark.table("Groceries_Transactions")

# COMMAND ----------

df.show()

# COMMAND ----------

pandas_df = df.toPandas()

# COMMAND ----------

pandas_df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Count of Unique Items

# COMMAND ----------

pandas_df['itemDescription'].unique().size

# COMMAND ----------

# MAGIC %md
# MAGIC #### Items Sold Per Year

# COMMAND ----------

sns.set_style('darkgrid')

# COMMAND ----------

yearly_count = pandas_df['Year'].value_counts().reset_index()
yearly_count.columns = ['Year', 'Count']
yearly_count.sort_values(by='Year', inplace=True)

fig = px.bar(yearly_count, x='Year', y='Count',
             title='Items Sold Per Year',
             labels={'Year': 'Year', 'Count': 'Number of Items Sold'},
             text='Count')

fig.update_traces(textposition='outside')
fig.update_layout(xaxis_title='Year',
                  yaxis_title='Number of Items Sold')

fig.show()

# COMMAND ----------

pio.write_html(fig, file="Plots/Items Sold Per Year.html", auto_open=False)

# COMMAND ----------

plt.figure(figsize=(10,7))
sns.countplot(x=pandas_df['Year'])
plt.title('Items Sold Per Year')
plt.xlabel('Year')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Sales increase in 2015 as compared to 2014

# COMMAND ----------

# MAGIC %md
# MAGIC #### Items Sold Per Month

# COMMAND ----------

plt.figure(figsize=(10,7))
df_monthly = pandas_df.copy()
df_monthly['Date'] = df_monthly['Date'].apply(lambda x: pd.to_datetime(f"{x.year}/{x.month}/{1}"))


df_monthly = df_monthly.groupby('Date').count()['itemDescription'].reset_index()
plt.plot(df_monthly['Date'],df_monthly['itemDescription'], color='darkblue')
plt.xlabel('Date')
plt.ylabel('Number of items bought')
plt.title('Number of items sold (each month)')
plt.show()

# COMMAND ----------

df_monthly = pandas_df.copy()
df_monthly.drop(['Member_number','Date','WeekOfYear'],axis=1,inplace=True)
df_monthly = df_monthly.groupby(['Year','Month']).count().reset_index()
d_2014 = df_monthly[df_monthly['Year'] == 2014]
d_2015 = df_monthly[df_monthly['Year'] == 2015]

plt.figure(figsize=(10,7))
plt.plot(d_2014['Month'],d_2014['itemDescription'],label='2014')
plt.plot(d_2015['Month'],d_2015['itemDescription'],label='2015')
plt.title('Number of items sold (each month)')
plt.xlabel('Month')
plt.ylabel('item count')
plt.legend()
plt.show()

# COMMAND ----------

corr=d_2014.merge(right=d_2015,on='Month')[['itemDescription_x','itemDescription_y']].corr().values[0][1]
print(f'Correlation between Sales in 2014 and 2015: {corr}')

# COMMAND ----------

# MAGIC %md
# MAGIC The correlation value of 0.4654402963659504 between sales in 2014 and 2015 indicates a moderate positive correlation, it suggests that as sales in 2014 increased, sales in 2015 also tended to increase.
# MAGIC
# MAGIC The sales patterns in 2014 and 2015 may be influenced by similar factors, such as market trends, customer preferences, or seasonality. However, other factors also contribute, as the correlation is not very high.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### Items Sold Per Day

# COMMAND ----------

plt.figure(figsize=(10,7))
df_daily = pandas_df.groupby('Date').count()['itemDescription'].reset_index()
plt.plot(df_daily['Date'],df_daily['itemDescription'], color='darkblue')
plt.xlabel('Date')
plt.ylabel('Number of items sold')
plt.title('Number of items sold per day')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Observations:
# MAGIC 1. **Fluctuating Sales**: The number of items sold daily varies significantly, ranging approximately from **20 to 100 items per day**. 
# MAGIC 2. **No Strong Trend**: There doesn't appear to be a clear upward or downward trend in the number of items sold over time. The sales seem to oscillate randomly within the range.
# MAGIC 3. **Seasonality**: There might be some **seasonal patterns**, as occasional spikes can be observed during certain periods (e.g., beginning of 2015). However, the patterns are not immediately obvious from this graph alone.
# MAGIC 4. **Sales Peaks**: There are noticeable spikes where sales exceed **90 items per day**. These may indicate specific events, promotions, or external factors influencing higher sales.
# MAGIC 5. **Steady Base Level**: Despite fluctuations, the daily sales hover mostly between **40 and 70 items per day**, suggesting a relatively stable baseline demand.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Number of times each item has been sold

# COMMAND ----------

df_items = pandas_df.groupby('itemDescription').count().sort_values(by='Member_number',ascending=False).reset_index()
df_items.rename(columns={'itemDescription': 'Item',
                   'Member_number': 'Number of sales'},inplace=True)
df_items.drop(['Date','Year','Month','Day','WeekOfYear'],axis=1,inplace=True)
df_items.head()

# COMMAND ----------

df_items['Number of sales'].describe()

# COMMAND ----------

# Histogram for number of sales of each item
import numpy as np
counts, bins = np.histogram(df_items['Number of sales'], bins=10)

norm = plt.Normalize(counts.min(), counts.max())

plt.figure(figsize=(10, 7))
bars = plt.bar(bins[:-1], counts, width=np.diff(bins), align='edge', color=plt.cm.plasma(norm(counts)))

plt.xlabel('Sales Count')
plt.ylabel('Item Count')
plt.title("Number of Times Each Item Was Sold")
plt.show()


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC There appear to be some outliers in the data. Let's examine these outliers more closely.

# COMMAND ----------

df_new = pandas_df.groupby('itemDescription').count().sort_values(by='Member_number',ascending=False).head(10).reset_index()
df_new.drop(['Date','Year','Month','Day','WeekOfYear'],axis=1,inplace=True)
df_new.rename(columns={'itemDescription': 'Item',
                   'Member_number' : 'Number of sales'},inplace=True)

plt.figure(figsize=(10,7))
sns.barplot(data=df_new, x='Item', y='Number of sales', palette='viridis')

plt.title('Most Purchased Items')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
plt.show()

# COMMAND ----------

df_cust = pandas_df.groupby('Member_number').count().sort_values(by='itemDescription',ascending=False).head(10).reset_index()
df_cust.drop(['Date','Year','Month','Day','WeekOfYear'],axis=1,inplace=True)
df_cust.rename(columns={'itemDescription': 'Item Count',
                   'Member_number' : 'Customer ID'},inplace=True)

df_cust['Customer ID'] = df_cust['Customer ID'].astype(str)
plt.figure(figsize=(10,7))
sns.barplot(data=df_cust, x='Customer ID', y='Item Count', palette='viridis')

plt.title('Top Customers by Number of Items Purchased')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Currently, our data is structured in a way that prevents us from determining how many items (and which specific items) each customer purchased during each visit to the store. For instance, consider the following table

# COMMAND ----------

pandas_df[pandas_df['Member_number'] == 4875].sort_values(by='Date').head()


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC We can see that the customer with ID 4875 purchased 4 items on April 04, 2014. However, the issue is that we don't know how many times this customer visited the store on that day, nor what items they bought during each visit. It’s possible that they visited the store 4 times, purchasing one item each time. Alternatively, they might have visited twice. Or perhaps they visited just once and bought all 4 items together. Without this information, we cannot determine the exact scenario. For meaningful association analysis, though, we need this level of detail. Since the available data does not provide this information, we will make the following assumption:
# MAGIC
# MAGIC **Assumption:** Each customer visited the store **only once per day**."

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating Transactions Document

# COMMAND ----------

pandas_df.head()

# COMMAND ----------

pandas_df.iloc[:,0:3]

# COMMAND ----------

df1 = pandas_df.iloc[:,0:3].copy()

df1['itemDescription'] = df1['itemDescription'].apply(lambda x: [x,]).copy()
df1 = df1.groupby(['Member_number','Date']).agg(sum).reset_index()
df1.rename(columns={'itemDescription': 'Items_Bought'},inplace=True)
df1.head()

# COMMAND ----------

# MAGIC %md
# MAGIC Items_Bought represents the set of all items purchased during a visit by a customer

# COMMAND ----------

df1['Basket size'] = df1['Items_Bought'].apply(lambda x: len(x))

# COMMAND ----------

plt.figure(figsize=(10,7))
df1['Basket size'].hist(alpha=0.6)
plt.xlabel('item count')
plt.ylabel('customer count')
plt.title("Count of Customers vs Items in Basket")
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we will apply Association Rule Learning to explore potential patterns in customers' purchasing behavior. To generate a set of meaningful rules, we will use two popular algorithms: the Apriori algorithm and FP-growth.

# COMMAND ----------

from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.frequent_patterns import association_rules
import mlxtend as ml

# COMMAND ----------

df1 = pandas_df.iloc[:,0:3].copy()
df1['itemDescription'] = df1['itemDescription'].apply(lambda x: [x,]).copy()
df1 = df1.groupby(['Member_number','Date']).agg(sum).reset_index()
df1.rename(columns={'itemDescription': 'Items_Bought'},inplace=True)
df1.head()

# COMMAND ----------

all_items = pandas_df['itemDescription'].unique()
data = []


for transaction in df1['Items_Bought']:
    row = []
    for item in all_items:
        if item in transaction:
            row.append(1)
        else:
            row.append(0)
    data.append(row)

df2 = pd.DataFrame(data,columns=all_items)    
df2 = df2.rename_axis('Transcation ID')

# COMMAND ----------

df2.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Applying Apriori Algorithm

# COMMAND ----------

frequent_itemsets = apriori(df2, min_support=0.001, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", num_itemsets=2)
rules.sort_values('confidence', ascending = False, inplace = True)

# COMMAND ----------

rules = rules[rules['confidence'] > 0.1].copy()
rules.head()

# COMMAND ----------

rows = rules.shape[0]
print(f'Number of rules: {rows}')

# COMMAND ----------

# MAGIC %md
# MAGIC We observe that the support for all the rules in our dataset is quite low, meaning the proportion of transactions that include items from both baskets is minimal. This could pose a challenge, as any results derived from this analysis may not be statistically significant.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Rules with the highest lift

# COMMAND ----------

rules.sort_values(by='lift',ascending=False).head(10).iloc[:,:-2][['antecedents',
                                                                  'consequents',
                                                                   'consequent support',
                                                                  'lift']]

# COMMAND ----------

# MAGIC %md
# MAGIC We observe that the itemsets (yogurt, whole milk) and (sausage) have the highest lift, which means that once a customer buys yogurt and whole milk, it becomes 2.2 times more likely that they will also purchase sausage. However, as we’ve noted, due to the low support, it's difficult to determine whether this is a genuine association or just a random occurrence.
# MAGIC
# MAGIC Similarly, we will examine the rules with the lowest lift, where the items in the antecedent and consequent are less likely to be bought together.

# COMMAND ----------

rules.sort_values(by='lift',ascending=True).head(10).iloc[:,:-2][['antecedents',
                                                                  'consequents',
                                                                   'consequent support',
                                                                  'lift']]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualizing the relation between support, confidence and lift

# COMMAND ----------

sup = rules['support'].values
conf = rules['confidence'].values
lift = rules['lift'].values

plt.figure(figsize=(10,6))
sc = plt.scatter(sup,conf,c=lift)
plt.colorbar(sc,label='Lift')
plt.xlabel('support')
plt.ylabel('confidence')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC We can make the following observations:
# MAGIC
# MAGIC 1. **Low Support with Higher Confidence:** Most of the rules are clustered in the lower-left section of the graph, indicating low support values. However, their confidence tends to be slightly higher, with most values lying between 0.10 and 0.14. This suggests that while the rules are not frequent (low support), when they do occur, they have a reasonable chance of being accurate (moderate confidence).
# MAGIC
# MAGIC 2. **Outliers with High Confidence:** There is one outlier in the top left corner with high confidence (~0.26), which indicates that this rule is highly confident but still has low support. This could point to a potentially interesting association, but its low support makes it less reliable.
# MAGIC
# MAGIC 3. **Lift:** The colors in the graph represent lift, with darker colors corresponding to lower lift values (around 1). Lift values for most of the points are below 1.5, indicating that the associations are not strongly significant. Only a few points have a higher lift (up to 2), meaning that for these specific rules, the items appear more frequently together than would be expected by chance.
# MAGIC
# MAGIC **Conclusion:**
# MAGIC - Most associations identified are weak, with low support and only moderate confidence.
# MAGIC - A few potential strong rules (with higher confidence and lift) stand out, but these need to be treated cautiously due to the low support.
# MAGIC - The overall data suggests that while there might be associations, they are not very robust and may not be statistically significant enough for reliable conclusions.[](url)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Applying FP Growth Algorithm

# COMMAND ----------

frequent_itemsets = fpgrowth(df2, min_support=0.001, use_colnames=True)

# COMMAND ----------

fp_rules = association_rules(frequent_itemsets, num_itemsets=10, metric="confidence", min_threshold=0.1)

# COMMAND ----------

fp_rules.head()

# COMMAND ----------

len(fp_rules)

# COMMAND ----------

# MAGIC %md
# MAGIC Again the support is very low.

# COMMAND ----------

fp_rules.sort_values(by='lift',ascending=False).head(10).iloc[:,:-2][['antecedents',
                                                                  'consequents',
                                                                   'consequent support',
                                                                  'lift']]

# COMMAND ----------

# MAGIC %md
# MAGIC We observed similar results in apriori

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **Conclusion:**
# MAGIC
# MAGIC Both the Apriori and FP-Growth algorithms yield similar results, but the Apriori algorithm generates less association rules compared to FP-Growth. However, the robustness of these rules is limited due to the low support values in the dataset, indicating that the associations identified may not be statistically significant. Consequently, while the algorithms provide insights into potential associations, the results should be interpreted with caution.

# COMMAND ----------

rules.to_csv('Apriori_rules.csv', index=False)

# COMMAND ----------

fp_rules.to_csv('FP_rules.csv', index=False)
