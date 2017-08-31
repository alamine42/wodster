from __future__ import print_function

from datetime import datetime, date, timedelta

from workout import WOD, WORKOUTS_TABLE, LEVELS
from utils import exec_sql

def get_latest_wod(level):
	latest_wod_sql = 'SELECT MAX(workout_date) FROM {tbl} WHERE workout_level = \"{wod_level}\"'.\
		format(tbl=WORKOUTS_TABLE, wod_level=level)

	results = exec_sql(latest_wod_sql)
	if results[0][0] is not None:
		latest_date_str = results[0][0]
	else:
		latest_date_str = '2016-06-01'
	
	return datetime.strptime(latest_date_str, '%Y-%m-%d').date()

def get_list_dates_to_retrieve(level):

	list_of_dates_to_retrieve = []
	latest_wod_date = get_latest_wod(level)
	today = date.today()
	delta = today - latest_wod_date
	for i in range(1, delta.days + 1):
		list_of_dates_to_retrieve.append(latest_wod_date + timedelta(days=i))		
	return list_of_dates_to_retrieve

def update_wods():
	print('Updating WOD database ...')
	for level in LEVELS:
		list_of_dates = get_list_dates_to_retrieve(level)
		if len(list_of_dates) > 0:
			for wod_date in list_of_dates:
				wod_day = wod_date.strftime('%A')
				wod = WOD(wod_date, wod_day, level)
				wod.retrieve()
				wod.save()
			print('All WODs updated for %s' % level)
		else:
			print('Nothing to update for %s' % level)

def main():
	update_wods()

if __name__ == '__main__':
	main()