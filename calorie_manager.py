# This is intended to be a simple console program to make it easy for me to log the food I consume, along
# with its calorie and macro breakdown. In the future, I would like to possibly move it to a web app, as well
# as implementing a sync function with offline support. This is the first time I've ever used a database before.
#

import sqlite3 
import time
import re

MEAL_1_TIME = "9:00"
MEAL_2_TIME = "14:30"
MEAL_3_TIME = "16:00"



def add_new_food_entry_to_db(date, time_eaten, food_name, amount, unit, calories, fat, carbs, protein):
	c = conn.cursor()
	
	c.execute("INSERT INTO Food_Eaten VALUES(?,?,?,?,?,?,?,?,?)", (date, time_eaten, food_name, amount, unit, calories, fat, carbs, protein))
	conn.commit()


def get_new_food_entry_from_user():
	print "Add New Entry\n------------------------------------------------"
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
	time_eaten = get_time_eaten_from_user()
	
	food_name = raw_input("Food Name: ")
	amount = get_float_from_user("Amount: ")
	unit = raw_input("In units: ")
	if(unit == "-"):
		unit = food_name
	calories = get_float_from_user("Calories: ")
	protein = get_float_from_user("Protein: ")
	carbs = get_float_from_user("Carbs: ")
	fat = get_float_from_user("Fat: ")
	
	
	print "\n\n\nDate:{} \nTime:{} \nFoodName:{} \nAmount:{} Unit:{} \nCalories:{} \nFat:{} \nCarbs:{} \nProtein:{}".format(date, time_eaten, food_name, str(amount), unit, str(calories), str(fat), str(carbs), str(protein))
	confirm = ""
	while confirm != "y" and confirm != "n":
		confirm = raw_input("Is this okay? (y/n): ")
		if confirm != "y" and confirm != "n":
			print "Use y or n"
	if confirm == "y":
		add_new_food_entry_to_db(date, time_eaten, food_name, amount, unit, calories, fat, carbs, protein)
	
	else:
		print "Scrapping this entry"
	return

def show_user_day_total():
	date = ""
	while not re.match("^[01]\d/[0-3]\d/20\d\d$", date) and date != "today":
		date = raw_input("Please enter a date, of the form MM/DD/YYYY (or enter 'today' for ({}): ".format(time.strftime("%m/%d/%Y")))
	if(date == "today"):
		date = time.strftime("%m/%d/%Y")
	c = conn.cursor()
	c.execute('SELECT * FROM Food_Eaten WHERE date=(?)', (date,))
	rows = c.fetchall()
	if not rows:
		print "No entries for that date." 
		return
	else:
		t_cals, t_protein, t_carbs, t_fat = get_total_macros(rows)
		print "Date: {}".format(date)
		print "Total Calories: {}".format(str(t_cals))
		print "Total Protein: {}".format(str(t_protein))
		print "Total Carbs: {}".format(str(t_carbs))
		print "Total Fat: {}".format(str(t_fat))
		print "\n\n"
		return
		
def show_user_day_and_time_total():
	date = ""
	while not re.match("^[01]\d/[0-3]\d/20\d\d$", date) and date != "today":
		date = raw_input("Please enter a date, of the form MM/DD/YYYY (or enter 'today' for ({}): ".format(time.strftime("%m/%d/%Y")))
	if(date == "today"):
		date = time.strftime("%m/%d/%Y")
	time_eaten = get_time_eaten_from_user()
	c = conn.cursor()
	c.execute('SELECT * FROM Food_Eaten WHERE date=(?) AND time=(?)', (date,time_eaten))
	rows = c.fetchall()
	if not rows:
		print "No entries for that date and time." 
		return
	else:
		t_cals, t_protein, t_carbs, t_fat = get_total_macros(rows)
		print "Date: {} Time: {}".format(date, time_eaten)
		print "Total Calories: {}".format(str(t_cals))
		print "Total Protein: {}".format(str(t_protein))
		print "Total Carbs: {}".format(str(t_carbs))
		print "Total Fat: {}".format(str(t_fat))
		print "\n\n"
		return

def get_total_macros(rows):		
	total_calories = 0.0
	total_protein = 0.0
	total_carbs = 0.0
	total_fat = 0.0
	for row in rows:
		total_calories += row["calories"]
		total_protein += row["protein"]
		total_carbs += row["carbs"]
		total_fat += row["fat"]
	return (total_calories, total_protein, total_carbs, total_fat) 
		
		
def display_help():
	print "a: Add an entry"
	print "td: Display totals for a specific date"
	print "tdt: Display totals for a specific date and time"
	print "h: Display help"
	print "q: Quit"

	
def get_float_from_user(message):
	while 1:
		try:
			f = float(raw_input(message))
			return f
		except ValueError:
			print "Please enter a number"
			
def get_time_eaten_from_user():
	time_eaten = raw_input("Please enter a time:")
	if(time_eaten == "m1"):
		time_eaten = MEAL_1_TIME
	elif(time_eaten == "m2"):
		time_eaten = MEAL_2_TIME
	elif(time_eaten == "m3"):
		time_eaten = MEAL_3_TIME
	return time_eaten
	
if __name__ == "__main__":
	conn = sqlite3.connect("calories.db")
	conn.row_factory = sqlite3.Row
	cmd = ""
	while 1:
		cmd = raw_input("What would you like to do (h for help): ")
		if cmd == "q":
			print "Quitting."
			break
		elif cmd == "h":
			display_help()
		elif cmd == "a":
			get_new_food_entry_from_user()
		elif cmd == "td":
			show_user_day_total()
		elif cmd == "tdt":
			show_user_day_and_time_total()
		else:
			print "Unrecognized command (h for help)"

	conn.close()
