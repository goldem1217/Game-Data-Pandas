#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

herodata = "herodata.csv"

#read file as dataframe
hero_data_df = pd.read_csv(herodata)

hero_data_df.head()


# In[ ]:


#PLAYER COUNT

hero_data_df.dropna()
players = hero_data_df["SN"].unique()
player_count = len(players)
player_count


# In[ ]:


#PURCHASE ANALYSIS (ALL)

#find number of unique items
item_list = hero_data_df["Item ID"].unique()
unique_items = len(item_list)

#find average item price
average_price = hero_data_df["Price"].mean()

#find number of purchases
purchase_number = len(hero_data_df)

#find total revenue
total_revenue = hero_data_df["Price"].sum()

#create and format summary dataframe #1
purchasing_analysis = [{"Number of Unique Items":unique_items,
                          "Average Item Price":average_price,
                          "Number of Purchases":purchase_number,
                          "Total Revenue":total_revenue}]

purchasing_analysis = pd.DataFrame(purchasing_analysis).style.format({"Average Item Price":"${:.2f}",
                                                                      "Total Revenue": "${:.2f}"})

purchasing_analysis


# In[ ]:


#GENDER DEMOGRAPHICS

#drop duplicate usernames to get accurate counts
unduplicated = hero_data_df.drop_duplicates(["SN"])

#find total counts and percentages
gender_counts = unduplicated.groupby(["Gender"]).count()
gender_counts = gender_counts["SN"]

gender_percents = (gender_counts/player_count)*100

#put them together
gender_demographics = {"Total Count":gender_counts,
                       "Percentage of Players":gender_percents}

gender_demographics = pd.DataFrame(gender_demographics).style.format({"Percentage of Players":"{:.2f}%"})

gender_demographics


# In[ ]:


#PURCHASE ANALYSIS (GENDER)

gp_counts = hero_data_df.groupby(["Gender"]).count()
gp_sums = hero_data_df.groupby(["Gender"]).sum()

#Purchase counts (pc) by gender
g_pc = gp_counts["SN"]

#Total purchases (tp) by gender
g_tp = gp_sums["Price"]

#Average purchase price (avg) by gender
g_avg = g_tp/g_pc

#Average purchase total (apt) by player and gender
g_apt = g_tp/gender_counts

#Create and format dataframe
gender_analysis = {"Number of Purchases":g_pc,
                  "Total Expenditure":g_tp,
                  "Avg. Purchase Amount":g_avg,
                  "Avg. Expenditure Per Player":g_apt}

gender_analysis = pd.DataFrame(gender_analysis).style.format({"Total Expenditure":"${:.2f}",
                                                             "Avg. Purchase Amount":"${:.2f}",
                                                             "Avg. Expenditure Per Player":"${:.2f}"})

gender_analysis


# In[ ]:


#AGE DEMOGRAPHICS

#find max age to create a flexible range & create a bin range
#if changing bin intervals, need to change bin labels
max_age = hero_data_df['Age'].max()
bins = np.arange(0,max_age+10,10)

#make labels for the bins after checking how many bins are in the bin range
labels = ["<10","11-20","21-30","31-40",">40"]

#put the data into the bins
age_bins = pd.cut(hero_data_df['Age'], bins, labels=labels)

#make a new column for the dataframe
hero_data_df["Age Group"] = age_bins

#total counts for each age group
#percentage of players for each age group
unique_ages = hero_data_df.drop_duplicates(["SN"])

age_counts = unique_ages.groupby(["Age Group"]).count()
age_percents = (age_counts["Price"]/player_count)*100

age_demographics = {"Total Count":age_counts["Price"],
                    "Percentage of Players":age_percents}

age_demographics = pd.DataFrame(age_demographics).style.format({"Percentage of Players": "{:.2f}%"})
age_demographics


# In[ ]:


#PURCHASE ANALYSIS (AGE)

#use full df with age group column
ap_counts = hero_data_df.groupby(["Age Group"]).count()
ap_sums = hero_data_df.groupby(["Age Group"]).sum()

#purchase count (pc)
a_pc = ap_counts["SN"]

#total purchase value (tpv)
a_tpv = ap_sums["Price"]

#average purchase price (avg)
a_avg = a_tpv/a_pc

#average purchase total per person (apt)
a_apt = a_tpv/age_counts["Price"]


#create and format dataframe
age_analysis = {"Number of Purchases":a_pc,
                "Total Expenditure":a_tpv,
                "Avg. Purchase Price":a_avg,
                "Avg. Expenditure Per Player":a_apt}

age_analysis = pd.DataFrame(age_analysis).style.format({"Avg. Purchase Price": "${:.2f}", 
                                                              "Total Expenditure": "${:.2f}",
                                                              "Avg. Expenditure Per Player": "${:.2f}"})
age_analysis


# In[ ]:


#BIG SPENDERS

#Isolate the top spenders
total_spent = hero_data_df.groupby(["SN"]).sum()

#to get a bigger list or to see the whole list, adjust the number in .head or remove altogether
big_spenders = total_spent["Price"].sort_values(ascending=False).head(10)

player_names = big_spenders.index

top_spenders = hero_data_df.loc[hero_data_df["SN"].isin(player_names)]

#Get the Purchase Count, Average Purchase Price, and Total Purchase Value for each
bs_counts = top_spenders.groupby(["SN"]).count()
bs_sums = top_spenders.groupby(["SN"]).sum()

#purchase count (pc)
s_pc = bs_counts["Age"]

#Total Purchase Value (tpv)
s_tpv = bs_sums["Price"]

#Average purchase price (avg)
s_avg = s_tpv/s_pc

#Create, sort, and format dataframe
top_analysis = {"Number of Purchases":s_pc,
                "Avg. Purchase Price":s_avg,
                "Total Expenditure":s_tpv}


top_analysis = pd.DataFrame(top_analysis).sort_values(by=["Total Expenditure"],ascending=False)

top_analysis = top_analysis.style.format({"Avg. Purchase Price": "${:.2f}", 
                                          "Total Expenditure": "${:.2f}"})

top_analysis 


# In[ ]:


#POPULAR ITEMS

#Drop unneeded columns
most_popular = hero_data_df.drop(columns=["Purchase ID","Age","Gender","Age Group","SN"])

#get the item counts, item total revenue, and item prices
mp_counts = most_popular.groupby(["Item ID","Item Name"]).count()
mp_sums = most_popular.groupby(["Item ID", "Item Name"]).sum()
mp_price = mp_sums/mp_counts

#add prices and total revenue to the item count dataframe, rename the item count column
mp_counts["Item Price"] = mp_price["Price"]
mp_counts["Total Purchase Value"] = mp_sums["Price"]
mp_counts = mp_counts.rename(columns={"Price":"Purchase Count"})

#sort by ascending popularity, get the top 10, and format. For different length lists, adjust .head
top_items = mp_counts.sort_values(by=["Purchase Count"],ascending=False).head(10)

top_items = top_items.style.format({"Item Price": "${:.2f}",
                                    "Total Purchase Value": "${:.2f}"})
top_items


# In[ ]:


#MOST PROFITABLE

#grab the un-sorted dataframe from above
#sort by ascending profitability, get the top 10, and format. For different length lists, adjust .head
most_profitable = mp_counts.sort_values(by=["Total Purchase Value"],ascending=False).head(10)

most_profitable = most_profitable.style.format({"Item Price": "${:.2f}",
                                                "Total Purchase Value": "${:.2f}"})

most_profitable

