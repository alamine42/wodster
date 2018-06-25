from __future__ import print_function
import datetime
import requests
import re

from bs4 import BeautifulSoup
from html2text import html2text
from utils import exec_sql

WORKOUTS_FILE = 'invictus.db'
WORKOUTS_TABLE = 'invictus_workouts'
LEVELS = ['fitness', 'performance']
BASE_URL = 'http://www.crossfitinvictus.com/wod/'

html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
}

def html_escape(text):
	"""Produce entities within text."""
	return "".join(html_escape_table.get(c,c) for c in text)

class WOD:

	def __init__(self, wod_date, wod_day, level):
		self.wod_date = wod_date
		self.wod_date_str = '{:%B-%d-%Y}'.format(self.wod_date).replace('-0', '-').lower()
		self.wod_day = wod_day
		self.wod_level = level
		self.wod_url = BASE_URL + self.wod_date_str + '-' + self.wod_level
		self.wod_alt_url = BASE_URL + self.wod_date_str + '-performance-fitness'
		self.wod_retrieved = False
		self.wod_desc = ''
		self.wod_html = ''
		self.wod_final = ''
		self.wod_exists = 0
		self.wod_title = self.wod_level + ' workout for ' + self.wod_day + ' ' + str(self.wod_date)

	def __repr__(self):
		return self.wod_desc

	def is_saved(self):
		select_sql = 'SELECT count(1) FROM {tbl} ' \
			' WHERE workout_url = \"{wod_url}\"'.\
			format(tbl=WORKOUTS_TABLE, wod_url=self.wod_url)
		
		results = exec_sql(select_sql)
		if results[0][0] > 0:
			return True
		else:
			return False

	def save(self):

		if not self.wod_exists:
			print('%s does not exist!' % (self.wod_title))
			return 0
		
		if self.is_saved():
			print('%s already saved!' % self.wod_title)
			return 0

		if len(self.wod_desc) == 0:
			print('%s has no description!' % self.wod_title)
			return 0

		save_sql = 'INSERT INTO {tbl} ' \
			'(workout_date, workout_day, workout_url, workout_alt_url, ' \
			'workout_level, workout_desc, workout_html, workout_final, workout_exists)' \
			' VALUES (\"{wod_dt}\", \"{wod_day}\", \"{wod_url}\", \"{wod_alt_url}\", ' \
			'\"{wod_level}\", \"{wod_desc}\", \"{wod_html}\", \"{wod_final}\", {wod_exists})'.\
			format(tbl=WORKOUTS_TABLE, 
				wod_dt=self.wod_date,
				wod_day=self.wod_day,
				wod_url=self.wod_url,
				wod_alt_url=self.wod_alt_url,
				wod_level=self.wod_level,
				wod_desc=self.wod_desc,
				wod_html=self.wod_html,
				wod_final=self.wod_final,
				wod_exists=self.wod_exists)

		exec_sql(save_sql)
		# print('%s saved!' % self.wod_title)
		return 1		

	def retrieve(self):

		response = requests.get(self.wod_url)
		if response.status_code == 200:
			self.wod_exists = 1
		else:
			response = requests.get(self.wod_alt_url)
			if response.status_code == 200:
				self.wod_exists = 1
		
		if self.wod_exists:
			soup = BeautifulSoup(response.text, 'html.parser')
			wod_text = soup.find("meta",  property="og:description")
			wod_html = soup.find("div", class_="entry-content")
			self.wod_html = str(wod_html).replace("'", "&#39;").replace('"', "&quot;")
			self.wod_desc = str(wod_html).replace("'", "&#39;").replace('"', "&quot;")
			# self.wod_desc = '<p>' + re.sub(r'<.*?>', '', temp) + '</p>'
