# INTRO

## Hello everyone welcome to my scraper for the blockchain
## Here i will tell u how i prepared for the scraper and how ive made it
## I will be going over a few steps
## 1 Preparing for the scraper
### Here ill be talking bout what i did before i started coding
## 2 Starting the scraper
### Here ill be talking about how i got the data and what my code does
## 3 The dataframe
### Here ill explain what the dataframe is gonna do in the code

# 1 PREPARING FOR THE SCRAPER
### To prepare for the scraper i had to download and set up a few things
## Virtual machine
### First i set up a ubuntu virtual machine on my computer which is where the scraper has to be made on
## Python & Visual studio code
### Second step is getting Visual studio code and Python 3 downloaded on the virtual machine
### After getting python3 and visual studio code we could almost start programming
## Extensions 
### I had to download some extensions of python3 like python3-bs4 to be able to use Beautifulsoup to scrape the data
### Also had to make sure pandas, regex and time are registered on the ubuntu vm
### Pandas is used to make the dataframe in the end and send the scraped data to this dataframe
### Time will be used for the sleep function that we will use in this code to make sure that the program sleeps a minute and then scrapes again
### Regex will be used to be getting the exact data that we would like for the program to be working with
### i will explain more of those 3 things in 2 starting the scraper

# 2 STARTING THE SCRAPER
## IMPORTS
### First come the imports that we need for the scraper to work as it should
### these imports are: requests, beautifulsoup, time, regex, pandas
### requests will get us the website that we are scraping from
### BeautifulSoup is to make sure we can get the HTML coding of it and so get the text we need
### Time will be used for the sleep function, this function is to make sure that the scraper works every 1 minute ( since our seconds will be on 60 )
### Regex will be used to regex out some of the words that we wont need from the data
### Pandas is here to be making a dataframe in the end but more on that in part 3 The dataframe

## SCRAPING THE DATA OF THE WEB
### As said above we use requests , beautifulsoup to get the url and get the HTML coding of it
### then the variable called "info" shows on what we are scraping of the HTML code
### With this we will get the data that we need for the scraper and that we will be working with

## GETTING THE RIGHT DATA
### In this part the Regex function that we imported will be used
### if we would print of the info from above we would get a line with words that we wont need
### This is why we take the specific texts that we wont need out of it and we replace it with a ";" this will be later be used
### in the end we put this data into a list where we store every transaction line that will later be transformed even more to be used even further

## PREPARING FOR THE DATAFRAME
### Here we will make sure that the data that we have will be ready to be put into a dataframe
### As said before we took all the words that were unnecessary out of the transaction lines and put a ";" in replacement
### That is used here to be splitting each transactionline into the 4 different data values we need being the hash, the time, the btc and the usd
### By splitting this text we make a new list with a length of 4 that we then store inside another list , that list will be used to be put inside the dataframe so we store every list that is made from the transactionlines into that list

# 3 THE DATAFRAME
### now we are gonna start working on the dataframe itself
### In the first line of coding we create the dataframe and put the list with all the other lists with the data stored in inside that dataframe
### We also give the columns a name to know what is actually stored into the dataframe in each column
### After all the data is stored into the dataframe the dataframe is ready to be transformed even further and ready to be worked with to get the data that we really want and need
### We transform the BTC from a string to a float , with this float we can then sort the transactionlines from biggest to smallest by comparing all the BTC values with eachother making a new dataframe with the highest amount of btc on the top and the lowest amount of btc on the bottom
### Then as said before we make a code line where we make sure its sorted by BTC and there we also tell it to go from biggest btc to lowest, the ignore index , is just to make sure that the highest amount of btc becomes line 0 in the dataframe , if we don't put the ignore index we would get the old linenumber of the dataframe it had before the sort
### As last step we need to make sure that we only print the 5 biggest numbers or later on we will be sending those 5 lines to the monodb that will be done later
### After that we put a sleep function so after 60 seconds the whole code returns to the start and will scrape again untill the user stops the program the while that we see all the way in the top is made so that we get inside of an infinite loop which will make it so that the code never stops running unless we stop it ourselves.

# END
### That is how the code works for this scraper and how the preparations before starting the code was done!