# This is intended to be a simple console program to make it easy for me to log the food I consume, along
# with its calorie and macro breakdown. In the future, I would like to possibly move it to a web app, as well
# as implementing a sync function with offline support. This is the first time I've ever used a database before.
#

import sqlite3 
import time
import re

conn = sqlite3.connect("calories.db")


def add_food_entry:
	c = conn.cursor()
	confirm = ""
	while confirm not in "yn":
		confirm = raw_input("Did you eat this food today ({})? (y/n): ".format(time.strftime("%d/%m/%Y")))
		if confirm not in "yn":
			print "Use y or n"
	if confirm == "y":
		date = time.strftime("%d/%m/%Y")
	else:
		date = ""
		while not re.match("^[01]\d/[0-3]\d/20\d\d$", date):
			date = raw_input("Please enter a date, of the form MM/DD/YYYY: ")
		
			
		
		
	food_name = raw_input("Food Name":)
	



