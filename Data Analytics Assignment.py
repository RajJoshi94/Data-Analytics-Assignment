#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


get_ipython().system('pip install openpyxl')


# In[3]:


pip show openpyxl


# In[4]:


import openpyxl


# In[5]:


#loading the file
df = pd.read_excel(r'C:\Users\raj94\Downloads\DataAnalystInternAssignment.xlsx', engine='openpyxl')


# In[6]:


#loading all the sheets
user_details = pd.read_excel(r'C:\Users\raj94\Downloads\DataAnalystInternAssignment.xlsx', sheet_name="UserDetails.csv")
cooking_sessions = pd.read_excel(r'C:\Users\raj94\Downloads\DataAnalystInternAssignment.xlsx',sheet_name="CookingSessions.csv")
order_details = pd.read_excel(r'C:\Users\raj94\Downloads\DataAnalystInternAssignment.xlsx', sheet_name="OrderDetails.csv")


# In[7]:


#checking for missing values
print(user_details.isnull().sum())
print(cooking_sessions.isnull().sum())
print(order_details.isnull().sum())


# In[8]:


#fill missing values with the mode
order_details['Rating']= order_details['Rating'].fillna(4)
print(order_details.head())


# In[9]:


#check for duplicates in user_details
user_details = user_details.drop_duplicates()
print(user_details)


# In[10]:


#check for duplicates in Cooking_sessions
cooking_sessions = cooking_sessions.drop_duplicates()
print(cooking_sessions)


# In[11]:


#check for duplicates in order_details
order_details = order_details.drop_duplicates()
print(order_details)


# In[12]:


#Merge OrderDetails and CookingSessions
merged_data = order_details.merge(cooking_sessions, on="Session ID", how="left", suffixes=('_order', '_session'))
print(merged_data)


# In[13]:


# Merge the merged_data with UserDetails on 'User ID'
final_merged_data = merged_data.merge(user_details, left_on='User ID_order', right_on='User ID', how='left')


# In[14]:


# Check the final merged data columns
print("Final Merged Data Columns:", final_merged_data.columns.tolist())


# In[17]:


final_merged_data.head() 


# In[15]:


# Check data types and null values
final_merged_data.info()


# In[16]:


# Get summary statistics for numerical columns
final_merged_data.describe() 


# In[18]:


#Filter completed orders
completed_orders = order_details[order_details['Order Status'] == 'Completed']


# In[19]:


#Group by Dish Name and count orders
popular_dishes = completed_orders['Dish Name'].value_counts().reset_index()
popular_dishes.columns = ['Dish Name', 'Order Count']


# In[20]:


#Display popular dishes
print(popular_dishes.head())


# In[21]:


#Plot the popular dishes
top_5_dishes = popular_dishes.head()

plt.figure(figsize=(10, 6))
plt.bar(top_5_dishes['Dish Name'], top_5_dishes['Order Count'], color='coral', alpha=0.8)
plt.title('Top Popular Dishes (Completed Orders)')
plt.xlabel('Dish Name')
plt.ylabel('Order Count')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# In[22]:


# Group by Meal Type to calculate total orders
meal_type_popularity = final_merged_data.groupby('Meal Type_order')['Order ID'].count().reset_index()
meal_type_popularity.rename(columns={'Order ID': 'Total Orders'}, inplace=True)


# In[23]:


# Visualize popularity
plt.figure(figsize=(8, 6))
plt.bar(meal_type_popularity['Meal Type_order'], meal_type_popularity['Total Orders'], color='skyblue', alpha=0.8)
plt.title('Meal Type Popularity in Orders')
plt.xlabel('Meal Type')
plt.ylabel('Total Orders')
plt.grid(axis='y')
plt.show()


# In[24]:


# Group by Location and Favorite Meal
location_meal_distribution = user_details.groupby(['Location', 'Favorite Meal']).size().reset_index(name='Count')


# In[25]:


# Visualize top locations
top_locations = location_meal_distribution.groupby('Location')['Count'].sum().nlargest(5).index
filtered_data = location_meal_distribution[location_meal_distribution['Location'].isin(top_locations)]
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_data, x='Location', y='Count', hue='Favorite Meal')
plt.title('Favorite Meal Distribution by Location')
plt.xlabel('Location')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()


# In[26]:


# Calculate the distribution of Time of Day in OrderDetails
Time_of_Day_distribution = completed_orders['Time of Day'].value_counts().reset_index()
Time_of_Day_distribution.columns = ['Time of Day', 'Count']
print(Time_of_Day_distribution)


# In[27]:


# Pie chart for Time of Day distribution
plt.figure(figsize=(8, 8))
plt.pie(Time_of_Day_distribution['Count'], labels=Time_of_Day_distribution['Time of Day'], autopct='%1.1f%%', colors=['gold', 'lightblue', 'pink'], startangle=90)
plt.title('Time of Day distribution in Orders')
plt.show()


# In[28]:


# Check the highest and lowest age in the UserDetails sheet
max_age = user_details['Age'].max()
min_age = user_details['Age'].min()

print(f"Highest Age: {max_age}")
print(f"Lowest Age: {min_age}")


# In[29]:


# Add Age Group column
def categorize_age(age):
    if age <= 29:
        return '25-29'
    elif age <= 34:
        return '30-34'
    elif age <= 39:
        return '35-39'
    else:
        return '40-42'
user_details['Age Group'] = user_details['Age'].apply(categorize_age)


# In[30]:


# Merge user details with order details
merged_orders = order_details.merge(user_details, on='User ID', how='left')


# In[31]:


# Group by Age Group and calculate metrics
orders_by_age = merged_orders.groupby('Age Group').agg(
    Total_Orders=('Order ID', 'count'),
    Total_Amount=('Amount (USD)', 'sum'),
    Avg_Rating=('Rating', 'mean')
).reset_index()

print(orders_by_age)


# In[32]:


# Bar chart for total orders by age group
plt.figure(figsize=(8, 6))
plt.bar(orders_by_age['Age Group'], orders_by_age['Total_Orders'], color='teal', alpha=0.8)
plt.title('Orders by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Total Orders')
plt.grid(axis='y')
plt.show()


# In[33]:


# Calculate total, completed, and canceled orders per user
order_summary = order_details.groupby('User ID').agg(
    Total_Orders=('Order ID', 'count'),
    Completed_Orders=('Order Status', lambda x: (x == 'Completed').sum()),
    Canceled_Orders=('Order Status', lambda x: (x == 'Canceled').sum())
).reset_index()


# In[34]:


# Add cancellation ratio
order_summary['Cancellation_Ratio'] = order_summary['Canceled_Orders'] / order_summary['Total_Orders']


# In[35]:


# Display users with high cancellation ratios
print(order_summary.sort_values('Cancellation_Ratio', ascending=False))


# In[36]:


# Merge order summary with user details
user_behavior = order_summary.merge(user_details, on='User ID', how='left')


# In[37]:


# Filter users with high cancellation ratios (e.g., greater than 50%)
high_cancellation_users = user_behavior[user_behavior['Cancellation_Ratio'] > 0.5]

print(high_cancellation_users)


# In[38]:


# Bar chart for cancellation ratio per user
plt.figure(figsize=(8, 6))
plt.bar(user_behavior['User ID'], user_behavior['Cancellation_Ratio'], color='orange', alpha=0.8)
plt.title('Cancellation Ratio by User')
plt.xlabel('User ID')
plt.ylabel('Cancellation Ratio')
plt.grid(axis='y')
plt.xticks(rotation=45)
plt.show()


# In[40]:


# Merge completed orders with user details
completed_user_data = completed_orders.merge(user_details, on='User ID', how='left')

# Group by age and count the number of completed orders
age_distribution = completed_user_data.groupby('Age').size().reset_index(name='Completed Orders')

# Display results
print(age_distribution)


# In[41]:


# Bar chart for age distribution
plt.figure(figsize=(8, 6))
sns.barplot(x='Age', y='Completed Orders', data=age_distribution, palette='viridis')
plt.title('Completed Orders by Age')
plt.xlabel('Age')
plt.ylabel('Number of Completed Orders')
plt.show()


# In[42]:


# Group by Location
orders_by_location = merged_orders.groupby('Location').agg(
    Total_Orders=('Order ID', 'count'),
    Avg_Order_Amount=('Amount (USD)', 'mean')
).reset_index()

print(orders_by_location)


# In[43]:


# Bar chart for total orders by location group
plt.figure(figsize=(8, 6))
plt.bar(orders_by_location['Location'], orders_by_location['Total_Orders'], color='teal', alpha=0.8)
plt.title('Orders by Location')
plt.xlabel('Location')
plt.ylabel('Total Orders')
plt.grid(axis='y')
plt.show()


# In[45]:


# Group by location and count the number of completed orders
location_distribution = completed_user_data.groupby('Location').size().reset_index(name='Completed Orders')

# Display results
print(location_distribution)


# In[46]:


plt.figure(figsize=(8, 6))
sns.barplot(x='Location', y='Completed Orders', data=location_distribution, palette='magma')
plt.title('Completed Orders by Location')
plt.xlabel('Location')
plt.ylabel('Number of Completed Orders')
plt.xticks(rotation=45)
plt.show()


# In[ ]:




