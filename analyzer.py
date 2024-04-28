import csv
import numpy as np
import pandas as pd
from decimal import Decimal

file = open("nba.csv") #opens the nba.csv file
csv_file = csv.reader(file) #reads from the nba csv file

#lists that will contain the data from the nba.csv file.
year = []
first = []
last = []
position = []
team = []
fg = []
ppg = []
rpg = []
apg = []
blocks = []

for row in csv_file: #adds the data from the csv file into each proper list.
    year.append(row[0])
    first.append(row[1])
    last.append(row[2])
    position.append(row[3])
    team.append(row[4])
    fg.append(row[5])
    ppg.append(row[6])
    rpg.append(row[7])
    apg.append(row[8])
    blocks.append(row[9])

def calculator(average): #function that will be used to calculate the average of all the stats.
    counter = 0 #sets value to zero
    for i in average:
        counter = counter + float(i)  #adds all the values from the list
    avg = counter/len(average) #calculates the avg
    avg = round(Decimal(avg),2) #rounds the decimal to tenths
    return(avg) # returns the avg which we can later return

#will be used to compare the stats of the MVP with the top 3 players, and then determine who was robbed.
Average_Ppg = calculator(ppg)
Average_Rpg = calculator(rpg)
Average_Apg = calculator(apg)
Average_Bpg = calculator(blocks)

mvp = open("nba.csv","r") # reads the nba.csv file
mvp1 = csv.reader(mvp)
mvp_s = {} # an empty dictionary to load everything from the nba.csv file, containing the mvp's

for row in mvp1: #will have a key of the player's first and last name and the year they were playing, and the value will be a dictionary with the stats of the player and their position.
    mvp_s[row[0],row[1],row[2]] = {
    "Pos": row[3], "Team": row[4],
    "FG": float(row[5]), "PPG": float(row[6]), "RPG": float(row[7]), "APG": float(row[8]), "BPG": float(row[9])
    }

# Begins working with the top 3 csv file.

top_3 = open("top_3.csv","r") # reads the top_3.csv file
reader = csv.reader(top_3) #reads from the top_3.csv file

top3 = {} # an empty dictionary to load everything from the top_3.csv file, so i can compare the stats of the avg mvp.

for row in reader: #will have a key of the player's first and last name and the year they were playing, and the value will be a dictionary with the stats of the player and their position.
    top3[row[0],row[1],row[2]] = {
    "Pos": row[3], "Team": row[4],
    "FG": float(row[5]), "PPG": float(row[6]), "RPG": float(row[7]), "APG": float(row[8]), "BPG": float(row[9])
}


#edit this function so it takes in a dictionary as a parameter.
def finder(names):
    met = []  # List to store players who met the following conditions:
    for key in names:
        if (names[key]["PPG"] >= Average_Ppg and names[key]["RPG"] >= Average_Rpg) or \
           (names[key]["PPG"] >= Average_Ppg and names[key]["APG"] >= Average_Apg) or \
           (names[key]["PPG"] >= Average_Ppg and names[key]["BPG"] >= Average_Bpg):
            met.append(key)  # Add player to the list
    return met  # Return the list of "robbed" players

# Assuming Average_Ppg, Average_Rpg, Average_Apg, Average_Bpg are defined elsewhere

MVP = finder(mvp_s) # Finds the players who met the following conditions from the nba.csv file.
TOP3 = finder(top3) # Finds the players who met the following conditions from the top_3.csv file.

everyone = MVP + TOP3  # Merges the two lists into one list.

m = sorted(everyone, key=lambda x: x[0])  # Sorts the list by year.

# Finds duplicates
duplicates = set() # Set to store duplicate years.
unique_years = set() # Set to store unique years
for player in m: 
    year = player[0] # Extract year from player tuple.
    if year in unique_years: # If year is already in unique_years, it's a duplicate.
        duplicates.add(year)
    else:
        unique_years.add(year)

# Remove players from duplicate years
filtered_players = [player for player in m if player[0] not in duplicates]

print("The following players have been robbed")
for player in filtered_players:
    print(player)

filename = "robbed.csv"
with open(filename, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Year","First Name", "Last Name"])
    for player in filtered_players:
        writer.writerow(player)
