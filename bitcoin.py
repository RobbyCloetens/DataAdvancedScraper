# Importing the necessary applications for the scraper
# ----------------------------------------------------
# IMPORTS FOR THE ACTUAL SCRAPER
# ------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
import time

# IMPORTS FOR MONGODB
# -------------------
import pymongo as mongo

# IMPORTS FOR REDIS
# -----------------
import redis
import ast

# SCRAPER BLOCKCHAIN
# Start of the actual scraper
# Putting it in a while to make sure that this continues untill the person stops the program.
# -------------------------------------------------------------------------------------------
counter = 0 # Counter to empty redis completely every run
loops = 0 # Loops untill the max loops is reached in this case being 5
while(loops != 5):
    # PREPARING THE DATA TO BE CAPTURED
    # The data we need to start the scraper
    # -------------------------------------
    url = "https://www.blockchain.com/btc/unconfirmed-transactions"
    request = requests.get(url)
    bitcoininfo = BeautifulSoup(request.text, features="html.parser")
    info = bitcoininfo.findAll('div', attrs={"class" : "sc-1g6z4xm-0 hXyplo"})

    # GETTING THE RIGHT DATA
    # Making a list to put in every single transactionline
    # ----------------------------------------------------
    bitcoinlines = []
    # We take all the 50 transactionlines and with regex take out the unnecessary text and replace it with a ; to later use to split 
    #                          the texts so we can take the hash , time , BTC and USD apart
    # -------------------------------------------------------------------------------------------------------------------------------
    for i in range(0,30):
        line = info[i]
        regex1 = re.sub(r"Hash", '', line.text)
        regex2 = re.sub(r"Time", ';', regex1)
        regex3 = re.sub(r"Amount \(BTC\)", ';', regex2)
        bitcoinline = re.sub(r"BTCAmount \(USD\)", ';', regex3)
        bitcoinlines.append(bitcoinline)

    # PREPARING FOR THE DATAFRAME
    # Making a new list that we will use to store all the lists that will be created from splitting up the bitcoin lines
    # As said before we put a ; between every value to know where the next value starts so we know where to split
    # -------------------------------------------------------------------------------------------------------------------
    bitcointijdelijk = []
    for i in range(0, 30):
        bitcoinlinesplit = bitcoinlines[i].split(';')
        bitcointijdelijk.append(bitcoinlinesplit)
    
    # DATAFRAME
    # Here we create the dataframe that will store the different values to be able to take the 5 highest
    # bitcoin lines out of it and change the value of BTC to floats so we can sort them later on
    # --------------------------------------------------------------------------------------------------
    bitcoindata = pd.DataFrame (bitcointijdelijk, columns = ['Hash', 'Time', 'BTC', 'USD'])
    bitcoindata = bitcoindata.astype({'Hash': str, 'Time': str, 'BTC': float, 'USD': str})

    # Here we will sort the dataframe by the BTC values , ignore index is just so we stay with the first line being 0
    # The ascending false is to make sure the biggest value is on top and so on
    # ----------------------------------------------------------------------------------------------------------------
    bitcoindata = bitcoindata.sort_values(by=['BTC'], ascending=False, ignore_index=True)
    # We print 0:5 because we want only the first 5 ( 5 here is not included into this but the 0 is so it prints from 0 to 4)
    # -----------------------------------------------------------------------------------------------------------------------

    # REDIS
    # -----
    # Changing the dataframe to a json file
    # -------------------------------------
    json = bitcoindata[0:5].to_json()
    r = redis.Redis(host='localhost', port=6380) # Connection to redis

    # An if function to reset the redis every time we run the program
    if(counter == 0):
        dataset = r.delete("data") # Empty the redis 
        r.lpush("data", json) # Push the data to the redis
        counter = counter + 1 # Add a count to show we are working with the right data and go into the else
    else:
        r.lpush("data", json) # Push the data to the redis
    
    # We make the program sleep for a minute so he takes the next hashes a minute after the first one he took so there will
    # be a minute difference between the first list and the second list of bitcoinlines
    # ---------------------------------------------------------------------------------------------------------------------
    loops = loops + 1 # Add a loop to run untill the max amount of loops
    if(loops != 5):
        time.sleep(60)


# MORE REDIS
# We put all the data in the variable dataset
# -------------------------------------------
dataset = r.lrange("data", 0,5)
# Here we make a loop so we can change the data into a dictionary and put it back into dataset
# --------------------------------------------------------------------------------------------
for i in range(0,5):
    dictionarybit = dataset[i].decode("UTF-8") # Make the data readable for a dictionary
    mydata = ast.literal_eval(dictionarybit) # Change the data to a dictionary
    dataset[i] = mydata # Put the data back in dataset so we get a list of dictionaries
print(dataset) # Print the dictionaries to see if the program works

# DATABASE
# We make a client where we will connect to the database where we want the data to be saved
# -----------------------------------------------------------------------------------------
client=mongo.MongoClient("mongodb://127.0.0.1:27017")
mydb = client["bitcoindata"]

# Here we make a column called bitcoin that we will put into the database 
col_bitcoin = mydb["Bitcoin"]

# Here we insert the data into the mongodb
insertedcol = col_bitcoin.insert_many(dataset)

# RUN REDIS WITH: redis-server --port 6380