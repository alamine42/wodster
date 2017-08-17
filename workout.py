from __future__ import print_function
import datetime
import requests
import sqlite3

WORKOUTS_FILE = 'invictus_db'
WORKOUTS_TABLE = 'invictus_workouts'
LEVELS = ['fitness', 'performance']

class WOD:

	base_url = 'http://www.crossfitinvictus.com/wod/'

	def __init__(self, wod_date, wod_day, level):
		self.wod_date = wod_date
		self.wod_day = wod_day
		self.wod_level = level
		self.wod_url = self.base_url + self.wod_date + '-' + self.wod_level
		self.wod_alt_url = self.base_url + self.wod_date + '-performance-fitness'
		self.wod_retrieved = False
		self.wod_desc = None

	def __repr__(self):
		return self.wod_desc

	def save(self):
		conn = sqlite3.connect(WORKOUTS_FILE)
		c = conn.cursor()


def get_workout(wod_url, alt_wod_url):

	workout_found = False
	response = requests.get(wod_url)
	if response.status_code == 200:
		workout_found = True
	else:
		response = requests.get(alt_wod_url)
		if response.status_code == 200:
			workout_found = True
	
	if workout_found:
		soup = BeautifulSoup(response.text, 'html.parser')
		wod_desc = soup.find("meta",  property="og:description")
		return wod_desc['content']
	else:
		return 'Workout does not exist at URL: %s' % wod_url

def main():
	today = datetime.date.today()

	# MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
	idx = (today.weekday() + 1) % 7 

	last_week_wod_dict = {}

	for i in range(1, 8):
		wod_date = today - datetime.timedelta(7+idx-i)
		wod_day = wod_date.strftime('%A')
		wod_date_str = '{:%B-%d-%Y}'.format(wod_date).replace('-0', '-').lower()

		last_week_wod_dict[i] = []

		for level in levels:
			wod = WOD(wod_date_str, wod_day, level)
			last_week_wod_dict[i].append(wod)

	for key in sorted(last_week_wod_dict.iterkeys()):
		wod_instance = last_week_wod_dict[key][0]
		print('%s - %s ' % (wod_instance.wod_level, wod_instance.wod_date))
		if key != 7:
			print(get_workout(wod_instance.wod_url, wod_instance.alt_wod_url))
		else:
			print('No workout on Sunday')
		print('-------------------\n')

def print_dict(my_dict):
	for key in sorted(my_dict.iterkeys()):
		print('Key: %s' % (key))
		print('Value: %s' % (my_dict[key]))
		print('----------------------')

if __name__ == '__main__':
	main()