'''
Zachary DeNoto
DSC 540 Midterm

**warning the dataset contains a lot of data, I would recommend installing python-levenshtein**


'''

#imports library to read in csv files and date times
from csv import DictReader
from datetime import datetime
from statistics import mean
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


#opens csv file and saves it as variable called data
data = DictReader(open('AB_NYC_2019.csv', encoding="utf8"))

#saves our data from csv file to variable called data_rows
data_rows = [d for d in data]

#creates variable called test_data to show us a sample of our data for the first 5 rows
test_data = data_rows[:5]

#prints out the data rows created above
print(test_data)

#prints out our headers for the csv file which we want to change
print("\nColumn Headers:")
for x in range(0,1):
    for key, val in test_data[x].items():
        print(key)


#sets two variables for our new data and inner lists for when we change headers
new_data = []
rows =[]

#list for prices needed for finding mean prices
prices = []

#sets condition for variable isempty which finds out if a row has missing data.
#Sets variable missing_data equal to 0 for number of rows with missing data
isempty = False
missing_data = 0

#sets new variable ids to list for holding unique id's for airbnbs to test
#for duplicate records
ids = []

#creates array needed for fuzzy matching
descrips = []
fuzzy_matches = []


#main loop to go through the data, put in new headers,
#changes date formatting, calculates amount of rows
#missing data and data formatting. Appends all the
#new data to a new list
for x in range(0,len(data_rows)):
    isempty = False
    rows = []
    for key, val in data_rows[x].items():
        #changes the header from name to Description
        if key == "name":
            key = "Description"
            descrips.append(val)

        #Changes header of last_reivew to Review Date and changes the date format.
        #Creates new variable called diff for the difference in days from when you run
        #the program since the date in last_review for new column to be added later in the code.

        elif key == "last_review" and val != "":
            key = "Review Date"
            val = datetime.strptime(val, '%Y-%m-%d')
            diff = (datetime.today()-val).days
            val = val.strftime('%b %m %Y')
        elif key == 'price':
            prices.append(float(val))
        elif val == '':
            isempty = True
        elif key == 'id':
            ids.append(val)
        rows.append(tuple((key, val)))
    #adds new column and uses the variable diff from above
    rows.append(tuple(('Days Since Last Review',diff)))
    new_data.append(list(rows))
    #increases count for rows with missing data
    if isempty:
        missing_data +=1

#prints out our new data
print("\n")
print(new_data)

#Prints out number of rows with missing data
print("\nThere are " + str(missing_data) + " rows containing missing data")

#function to find outliers based on a dataset of values
def detect_outliers(dataset):
    outliers = []
    threshold = 3
    mean_1 = np.mean(dataset)
    std_1 = np.std(dataset)

    for y in dataset:
        z_score = (y - mean_1) / std_1
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers

#we run the function to find outliers for prices
list_of_outliers = detect_outliers(prices)

#prints out list of any outliers based on price
print("\nThis is the list of price outliers: ", list_of_outliers)

#creates variable for number of unique ids based on list of ids created above
num_of_uniq_ = np.unique(ids)

#if statement to say how many duplicate records were found or if none were found based on
#the number of unique and total ids
if len(num_of_uniq_) == len(ids):
    print("\nNo Duplicate Records Found!")
else:
    print("There were " + str(len(ids)-len(num_of_uniq_)) + "found")


#list of fuzzy matching words
fuzzy_match_words = ['lux','bdrm','gym', 'apt']

#loops to compare each word in list above to the description for the airbnb by comparing each word
for x in range(0,len(fuzzy_match_words)):
    fuzzy_matches = []

    for y in range(0,len(descrips)):
        split_ent = []
        split_ent = descrips[y].split()
        max_ent = []
        if descrips[y] != "":
            for z in range(len(split_ent)):
                max_ent.append(fuzz.token_sort_ratio(fuzzy_match_words[x],split_ent[z]))
            max_num = max(max_ent)
            if max_num >= 60:
                fuzzy_matches.append(max_num)

    print("\nThere are " + str(len(fuzzy_matches)) + " fuzzywuzzy matches with a match of at least 60% or greater for the phrase " + fuzzy_match_words[x])

