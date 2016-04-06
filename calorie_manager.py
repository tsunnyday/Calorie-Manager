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



def add_new_food_eaten_entry_to_db(date, time_eaten, food_name, amount, unit, calories, fat, carbs, protein):
	c = conn.cursor()
	
	c.execute("INSERT INTO Food_Eaten VALUES(?,?,?,?,?,?,?,?,?)", (date, time_eaten, food_name, amount, unit, calories, fat, carbs, protein))
	conn.commit()
	
def add_new_saved_food_entry_to_db(food_name, base_amount, unit, base_calories, base_fat, base_carbs, base_protein):
	c = conn.cursor()
	
	c.execute("INSERT INTO Food_Items VALUES(?,?,?,?,?,?,?)", (food_name, base_amount, unit, base_calories, base_fat, base_carbs, base_protein))
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
		
	if check_if_food_and_unit_in_db(food_name, unit):
		print "There is an entry for this food and unit in the database already."
		row = get_food_and_unit_in_db(food_name, unit)
		r_name = row['name']
		r_amount = row['base_amount']
		r_unit = row['base_amount_unit']
		r_calories = row['calories']
		r_fat = row['fat']
		r_carbs = row['carbs']
		r_protein = row['protein']
		print "\nName:{}\nAmount:{}\nUnit:{}\nCalories:{}\nFat:{}\nCarbs:{}\nProtein:{}\n".format(r_name, str(r_amount), r_unit, str(r_calories), str(r_fat), str(r_carbs), str(r_protein))
		if get_confirm_from_user("Would you like to use this entry? "):
			calories = (amount * row['calories']) / row['base_amount']
			protein = (amount * row['protein']) / row['base_amount']
			carbs = (amount * row['carbs']) / row['base_amount']
			fat = (amount * row['fat']) / row['base_amount']
			
			
		else:
			calories = get_float_from_user("Calories: ")
			protein = get_float_from_user("Protein: ")
			carbs = get_float_from_user("Carbs: ")
			fat = get_float_from_user("Fat: ")
	
			
		
	else:
		calories = get_float_from_user("Calories: ")
		protein = get_float_from_user("Protein: ")
		carbs = get_float_from_user("Carbs: ")
		fat = get_float_from_user("Fat: ")
	
	
	print "\n\n\nDate:{} \nTime:{} \nFoodName:{} \nAmount:{} Unit:{} \nCalories:{} \nFat:{} \nCarbs:{} \nProtein:{}".format(date, time_eaten, food_name, str(amount), unit, str(calories), str(fat), str(carbs), str(protein))
	if get_confirm_from_user("Is this okay?"):
		
		add_new_food_eaten_entry_to_db(date, time_eaten, food_name, amount, unit, calories, fat, carbs, protein)
		print "Saved to database Food_Eaten"
		
		if check_if_food_and_unit_in_db(food_name, unit):
			print "Food and unit already saved"
		else:
		
			if(get_confirm_from_user("Would you like to add this food to the database, to be referenced later? ")):
				print "Saving '{}' in unit '{}' to foods database".format(food_name, str(unit))
				base_amount = get_float_from_user("What amount would you like to set as the default? ")
				base_calories = round((calories * base_amount) / amount)
				base_protein = round_to_nearest_half((protein * base_amount) / amount)
				base_carbs = round_to_nearest_half((carbs * base_amount) / amount)
				base_fat = round_to_nearest_half((fat * base_amount) / amount)
				print "\n\n\nFoodName:{} \nBaseAmount:{} BaseUnit:{} \nBaseCalories:{} \nBaseFat:{} \nBaseCarbs:{} \nBaseProtein:{}".format(food_name, str(base_amount), unit, str(base_calories), str(base_fat), str(base_carbs), str(base_protein))
				if(get_confirm_from_user("Is this okay?")):
					add_new_saved_food_entry_to_db(food_name, base_amount, unit, base_calories, base_fat, base_carbs, base_protein)
					print "Saved to database Food_Items"
					return
				else:
					print "Scrapping this entry"
					return
			
		
	
	else:
		print "Scrapping this entry"
	return

def check_if_food_and_unit_in_db(food_name, unit):
	c = conn.cursor()
	c.execute('SELECT * FROM Food_Items WHERE name=(?) AND base_amount_unit=(?)', (food_name, unit))
	rows = c.fetchall()
	if rows:
		return True
	else:
		return False
		
def get_food_and_unit_in_db(food_name, unit):
	c = conn.cursor()
	c.execute('SELECT * FROM Food_Items WHERE name=(?) AND base_amount_unit=(?)', (food_name, unit))
	rows = c.fetchall()
	if len(rows) > 1:
		print "More than one entry of same name and unit. Just showing one for now."
	return rows[0]

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
			
def get_confirm_from_user(message):
	confirm = ""
	while confirm != "y" and confirm != "n":
		confirm = raw_input(message + " (y/n): ")
		if confirm != "y" and confirm != "n":
			print "Use y or n"
	if confirm == "y":
		return True
	else:
		return False
			
def get_time_eaten_from_user():
	time_eaten = raw_input("Please enter a time:")
	if(time_eaten == "m1"):
		time_eaten = MEAL_1_TIME
	elif(time_eaten == "m2"):
		time_eaten = MEAL_2_TIME
	elif(time_eaten == "m3"):
		time_eaten = MEAL_3_TIME
	return time_eaten
	
def round_to_nearest_half(float_in):
	return round(float_in / .5) * .5
	
	
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
