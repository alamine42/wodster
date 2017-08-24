from __future__ import print_function

from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, session, flash, redirect, url_for
from utils import exec_sql
from workout import WOD, WORKOUTS_TABLE, LEVELS
from invictus import update_wods

# Create application object
app = Flask(__name__)

def format_query(starting_date, ending_date, level='fitness'):
	return 'SELECT * FROM {tbl} ' \
		'WHERE workout_date >= \"{start_date}\" ' \
		'AND workout_date < \"{end_date}\" ' \
		'AND workout_level = \"{wod_level}\";'.\
		format(tbl=WORKOUTS_TABLE, 
			start_date=str(starting_date),
			end_date=str(ending_date), 
			wod_level=level)

def get_workouts(starting_date, ending_date, level='fitness'):
	query = format_query(starting_date, ending_date, level)
	wods = exec_sql(query)
	return wods

@app.route("/")
def view_all():
	update_wods()

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_till_end_of_week = 7 - today.weekday()

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	next_monday_date = today + timedelta(days=days_till_end_of_week)

	this_week_fitness_wods = get_workouts(last_monday_date, next_monday_date, 'fitness')
	this_week_performance_wods = get_workouts(last_monday_date, next_monday_date, 'performance')

	this_week_wods = {
		'fitness': this_week_fitness_wods, 
		'performance': this_week_performance_wods
		}

	return render_template('index.html', weekly_wods=this_week_wods)

@app.route("/fitness")
def view_fitness():
	update_wods()

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_till_end_of_week = 7 - today.weekday()

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	next_monday_date = today + timedelta(days=days_till_end_of_week)

	this_week_fitness_wods = get_workouts(last_monday_date, next_monday_date, 'fitness')

	this_week_wods = {
		'fitness': this_week_fitness_wods
		}

	return render_template('fitness.html', weekly_wods=this_week_wods)

@app.route("/performance")
def view_performance():
	update_wods()

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_till_end_of_week = 7 - today.weekday()

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	next_monday_date = today + timedelta(days=days_till_end_of_week)

	this_week_fitness_wods = get_workouts(last_monday_date, next_monday_date, 'performance')

	this_week_wods = {
		'performance': this_week_fitness_wods
		}

	return render_template('performance.html', weekly_wods=this_week_wods)

@app.route("/lastweek")
def view_last_week():
	update_wods()

	today = date.today()
	days_since_start_of_week = today.weekday()
	days_since_start_of_last_week = days_since_start_of_week + 7

	last_monday_date = today - timedelta(days=days_since_start_of_week)
	monday_before_last = today - timedelta(days=days_since_start_of_last_week)

	last_week_fitness_wods = get_workouts(monday_before_last, last_monday_date, 'fitness')
	last_week_performance_wods = get_workouts(monday_before_last, last_monday_date, 'performance')

	last_week_wods = {
		'fitness': last_week_fitness_wods, 
		'performance': last_week_performance_wods
		}

	return render_template('index.html', weekly_wods=last_week_wods)

if __name__ == '__main__':
	app.run(debug=True)


