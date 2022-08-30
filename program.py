# Author: Daniel E. Rodriguez Olivera
# Date: April 22, 2022

#Importing the imports necesary for the project
import sys
import csv
import math
import mmh3

#####INPUT######
openbloom = open(sys.argv[1], 'r') # The variable openbloom opens the input file we will use to create the bloom by using the sys import
openinput = open(sys.argv[2], 'r') # The variable openinput opens the input file we will use against the bloom filter by using the sys import

bloomreader = csv.reader(openbloom) #The variable bloomreader stores what was read of the bloom input file by using the import csv
inputreader = csv.reader(openinput) #The variable inputreader stores what was read of the input file by using the import csv

#Variables
bloomemailslist = [] #The variable bloomemailslist will hold all the emails from our bloom input file
inputemailslist = [] #The variable inputemailslist will hold all the emails from our input file
numberofemails = 0 #The variable numberofemails will hold the number of emails in the bloom file
lengthofinput = 0 #The variable lengthofinput will hold the length of the input file

#This for loop iterates through our bloom input file and adds all our bloom emails to a list 
# while counting the number of emails
for row in bloomreader:
    if row[0] == 'Email':
        continue
    else:
        numberofemails += 1
        bloomemailslist.append(row)


#This for loop iterates through our input file and adds all our emails to a list 
# while counting the length of the file
for emails in inputreader:
    if emails[0] == 'Email':
        continue
    else:
        lengthofinput += 1
        inputemailslist.append(emails)
#####INPUT######

#Variables
falsepositives = 0.0000001 #The variable falsepositives holds the probability we want of false positives
numberofbits = math.ceil((numberofemails * math.log(falsepositives))/ math.log(1 / math.pow(2, math.log(2)))) #The variable numberofbits holds the number of bits our filter will have
numberofhash = round((numberofbits / numberofemails) * math.log(2)) #The variable numberofhash holds the number of hash functions we will need
bitlist = [0] * numberofbits #The variable bitlist holds a list of our bits

bloomresult = []  #The variable bloomresult will hold a list of wether or not an email possibly is or not in the database


#####FUNCTIONS######
#This function will create the bloom filter using the list of emails we get 
# from the first input file (openbloom/bloomreader/bloomemailslist)
def bloom(emails):

    #This for loop will iterate through the emails
    for email in emails:
        counter = 0  #The variable counter will count until we complete the number of hashes required

        #This while loop is used to change the values in the bitlist according to the hash we get while incrementing 
        # counter so we don't have an infinite loop
        while counter <= numberofhash:
            number = mmh3.hash(str(email), counter) % numberofbits
            bitlist[number] = 1
            counter += 1


#The function results will hash the emails from the inputemailslist and see if they are or are not in the bitlist 
# if they are the string "Probably in the DB" will be added to bloomresult 
# if they are not the string "Not in the DB" will be added to bloomresult
def results(emails):

    #This for loop will iterate through the emails
    for email in emails:
        counter = 0
        falsecounter = 0 #The variable falsecounter will hold the value of how many times a bitlist search is 0

        #This while loop is used to check if the values bitlist holds where the email is hashed too
        #are 0 or 1, if they are 0 then the falsecounter increments
        while counter <= numberofhash:
            number = mmh3.hash(str(email), counter) % numberofbits
            counter += 1
            if bitlist[number] == 0:
                falsecounter += 1

        #These statements check if the falsecounter is more than zero, which means if at least one position 
        # is 0 then its not in the database but if not then it probably is in the database
        if(falsecounter > 0):
            bloomresult.append("Not in the DB")
        else:
            bloomresult.append("Probably in the DB")

#####FUNCTIONS######


#Calling functions so they do their jobs
bloom(bloomemailslist)
results(inputemailslist)


#######OUTPUT#########
result = open('Results.csv', 'a', newline="") #Creation of Results.csv file that will have the results as specified by the professor
header = ['Email,Result'] #The variable header stores the column title as specified by the professor

#We use our import csv to start writing to our result file
writer = csv.writer(result)
writer.writerow(header)

counting = 0 #The variable counting will help us iterate through the lists

#This while loop iterates through the values of inputemailslist
# while also putting the string in the format specified by the professor
# and adding that line to our output file
while lengthofinput > counting:
    resultslist = []
    email = str(inputemailslist[counting])
    email = email[2:-2]
    resultslist.append(email + ',' + bloomresult[counting])
    writer.writerow(resultslist)
    counting += 1


#Finally we close all the opened files
openbloom.close()
openinput.close()
result.close()

#######OUTPUT#########