# This is intended to be a simple console program to make it easy for me to log the food I consume, along
# with its calorie and macro breakdown. In the future, I would like to possibly move it to a web app, as well
# as implementing a sync function with offline support. This is the first time I've ever used a database before.
#

import sqlite3 
import time
import re




def add_new_food_entry_to_db(date, food_name, amount, unit, calories, fat, carbs, protein):
	c = conn.cursor()
	c.execute("INSERT INTO Food_Eaten VALUES(?,?,?,?,?,?,?,?,?)", (date, "", food_name, amount, unit, calories, fat, carbs, protein))
	conn.commit()


def get_new_food_entry_from_user():
	confirm = ""
	while confirm != "y" and confirm != "n":
		confirm = raw_input("Did you eat this food today ({})? (y/n): ".format(time.strftime("%m/%d/%Y")))
		if confirm != "y" and confirm != "n":
			print "Use y or n"
	if confirm == "y":
		date = time.strftime("%m/%d/%Y")
	else:
		date = ""
		while not re.match("^[01]\d/[0-3]\d/20\d\d$", date):
			date = raw_input("Please enter a date, of the form MM/DD/YYYY: ")
	
	food_name = raw_input("Food Name: ")
	amount = get_float_from_user("Amount: ")
	unit = raw_input("In units: ")
	calories = get_float_from_user("Calories: ")
	fat = get_float_from_user("Fat: ")
	carbs = get_float_from_user("Carbs: ")
	protein = get_float_from_user("Protein: ")
	
	
	print "\n\n\nDate:{} \nFoodName:{} \nAmount:{} Unit:{} \nCalories:{} \nFat:{} \nCarbs:{} \nProtein:{}".format(date, food_name, str(amount), unit, str(calories), str(fat), str(carbs), str(protein))
	confirm = ""
	while confirm != "y" and confirm != "n":
		confirm = raw_input("Is this okay? (y/n): ")
		if confirm != "y" and confirm != "n":
			print "Use y or n"
	if confirm == "y":
		add_new_food_entry_to_db(date, food_name, amount, unit, calories, fat, carbs, protein)
	
	else:
		print "Scrapping this entry"
	return
		
	
def get_float_from_user(message):
	while 1:
		try:
			f = float(raw_input(message))
			return f
		except ValueError:
			print "Please enter a number"
	
if __name__ == "__main__":
	conn = sqlite3.connect("calories.db")
	get_new_food_entry_from_user()

	conn.close()
