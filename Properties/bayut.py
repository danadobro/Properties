#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:55:12 2024

@author: danadobrosavljevic
"""

import json
import pandas as pd


json_file = open('property_transaction_data.json')
data = json.load(json_file)


#storing json data in a data frame
transaction_data = pd.DataFrame(data)

transaction_data.describe()


#delete the entries that are purchased land and aren't properties
transaction_data = transaction_data[transaction_data['area_size'] != '-']


#Reset index after filtering
transaction_data = transaction_data.reset_index(drop=True)


#remove all the office and commercial properties 

transaction_data = transaction_data[transaction_data['beds'] != '-']
#Reset index after filtering
transaction_data = transaction_data.reset_index(drop=True)


# Count the unique values for 'beds' to see what properties sold the most
bed_counts = transaction_data['beds'].value_counts()




#add a price per square foot column to help comare prices in different areas

#check if price and area are numeric so we can perform division
is_price_numeric = pd.api.types.is_numeric_dtype(transaction_data['price'])
is_area_numeric = pd.api.types.is_numeric_dtype(transaction_data['area_size'])



#remove the commas from the price and area values to be able to covert to numeric values

transaction_data['price'] = transaction_data['price'].str.replace(',', '')
transaction_data['area_size'] = transaction_data['area_size'].str.replace(',', '')


transaction_data['price'] = pd.to_numeric(transaction_data['price'], errors='coerce')
transaction_data['area_size'] = pd.to_numeric(transaction_data['area_size'], errors='coerce')


transaction_data['price_per_sqft'] = transaction_data['price'] / transaction_data['area_size']





#changing the date from string to datetime format
transaction_data['date'] = pd.to_datetime(transaction_data['date'], format='%d %b\n%Y', errors='coerce')



#deleting rows from December 2023

transaction_data = transaction_data[~((transaction_data['date'].dt.year == 2023) & (transaction_data['date'].dt.month == 12))]

#display only date not time
transaction_data['date'] = transaction_data['date'].dt.date






#dividing location into multiple columns for location name and location area

# Split the 'location' column by newline character
split_location = transaction_data['location'].str.split('\n', expand=True)

transaction_data['property'] = split_location[0]
transaction_data['location_area'] = split_location[1]








transaction_data.to_csv('bayut_transaction_data_cleaned.csv', index= True)





