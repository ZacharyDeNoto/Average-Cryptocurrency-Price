'''

Zachary DeNoto
DSC 540
Final Project

This final project takes data from the coinlore API
on crypto currencies, changes a few headers, creates a new column
with the average of a few columns, logs errors, as well as texts
a success or failure text message. You will want to change the
phone number in for text to go through.

'''

#import necessary libraries for this project
import requests
import pprint
import pandas as pd
import _json
import logging
from datetime import datetime
from twilio.rest import Client


#this function sets up a logging file
#to monitor scripts. This sets up the filename,
#the level and format of the messages
def start_logger():
    logging.basicConfig(filename='log_report_%s.log'
        %datetime.strftime(datetime.now(), '%m%d%Y_%H%M%S'),
        level=logging.DEBUG,format='%(asctime)s %(message)s',
        datefmt='%m-%d %H:%M:%S')


#starts our logging function created above
#and sets text to tell us we started a script
start_logger()
logging.debug("SCRIPT: Starting")


#sets twilio account information as variables
account_sid = 'ACd7a56b253d7f9e95caa09d0833ff4898'
auth_token = '39e2ec486907f42b797174512cc661f9'
client = Client(account_sid, auth_token)

#url to our API and gets the top 100 crypto
#currentcies, sets as a variable
url = "https://api.coinlore.net/api/tickers"


#uses try/except messages to send a text
#if successful send as success text message,
#if there is an error, will send an unsuccessful
#message as a text
try:
    #grabs the data from the API
    response = requests.request("GET", url)

    #puts the api response into json format
    r = response.json()

    #prints out response to see the data from the API
    print(r)

    #creates an empty list to hold our
    nlst = []

    #loops through each crypto currency entry from the API
    for j, k in r.items():
        if type(k) == list:

            #loops through each row of data
            for i in range(len(r['data'])):

                #creates a dictionary to save our data to
                ndict = {}

                #loops through each header and value for the crypto currencies
                for l, m in k[i].items():

                    #changes the header of nameid to ID Name
                    if l == 'nameid':
                        ndict['ID Name'] = m

                    #changes the header of price_usd to USD Price
                    elif l == 'price_usd':
                        ndict['USD Price'] = m

                    #formats the percentage to add a %
                    elif l == 'percent_change_24h':
                        ndict[l] = '{}%'.format(m)

                    #changes the value to an integer and saves value to use in upcoming variable
                    elif l == 'csupply':
                        ndict[l] = int(float(m))
                        csup = float(m)

                    #saves value to use in upcoming variable and saves value to dictionary
                    elif l == 'tsupply':
                        ndict[l] = m
                        tsup = float(m)

                    #saves value to dictionary and creates a new column with average of c, t, and m supply
                    #if there is no msupply value then it only averages c and t supply, otherwise it averages
                    #all three supplies
                    elif l == 'msupply':
                        ndict[l] = m
                        try:
                            msup = float(m)
                            ndict['Average_supply'] = (csup + tsup + msup) / 3
                        except:
                            ndict['Average_supply'] = (csup + tsup) / 2

                    #saves values to dictionary
                    else:
                        ndict[l] = m

                #appends dictionary to list
                nlst.append(ndict)

    #puts the list of dictionaries to a pandas dataframe
    df = pd.DataFrame(nlst)

    #allows to see all columns and rows
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    #prints the first 10 new rows to see if the changes occured
    print(df[0:10])

    #saves the new data to an Excel spreadsheet
    df.to_excel('DSC540 Final Project.xlsx')

    #sends a success text
    message = client.messages.create(
        to="+15555555555",
        from_="+12563872257",
        body="DSC-540 Final Project Worked!")

except Exception:
    #updates logs if unsuccessful
    logging.exception('SCRIPT: There was a problem!')
    logging.error('SCRIPT: There was an issue with the main() function')

    #sends an unsuccessful text if there was an issue with the code
    message = client.messages.create(
        to="+15856838068",
        from_="+12563872257",
        body="DSC-540 Final Project did not work, try again!")

    #logs that the code is done
    logging.debug('SCRIPT: Finished!')


#prints out the text that was sent if the
#code was successful or not
print("Text message sent: " + message.body)
