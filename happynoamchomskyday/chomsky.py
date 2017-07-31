import requests
import httplib2
from apiclient import discovery

SCOPES = ['https://www.googleapis.com/auth/calendar']

path = '/Users/ekazin/Personal/projects/happynoamchomskyday/happynoamchomskyday/aux/'
CLIENT_SECRET_FILE = '{}client_secret_chomsky.json'.format(path)
APPLICATION_NAME = 'Noam Chomsky day'

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def set_credentials():
	try:
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	except ImportError:
		flags = None

	return get_credentials(flags=flags)	

def get_credentials(flags=None):
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	#credential_path = os.path.join(credential_dir, 'sheets2calendar.json')

	credential_path = os.path.join(credential_dir, 'chomsky.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		print CLIENT_SECRET_FILE
		print SCOPES
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

class Calendar():

	def __init__(self, credentials):
		http = credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=http)

	def print_cal_list(self):
		page_token = None
		while True:
			calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
			for calendar_list_entry in calendar_list['items']:
				print '\t', calendar_list_entry['summary'], calendar_list_entry['id']
				print 'tz\t', calendar_list_entry['timeZone']
				print '-' * 20
			page_token = calendar_list.get('nextPageToken')
	
			if not page_token:
			  break 

	def create_cal(self, summary=None, timeZone_ = 'Europe/London'):
		if not summary:
			raise ValueError('Must enter `summary` as str of Calendar name')
		calendar = {
			'summary': summary,
			'timeZone': timeZone_
		}

		created_calendar = self.service.calendars().insert(body=calendar).execute()
		return created_calendar['id']

	def delete_cal(self, cal_id):
		# Deleting a secondary calendar
		self.service.calendars().delete(calendarId=cal_id).execute()

	def _event(self, summary=None, description=None, dateStart=None, dateEnd=None, freq=None, interval=None):
		if not dateStart:
			raise Exception("dateStart required to be of format 'YYYY-MM-DD'")
		 
		EVENT = {'summary': summary, 'description': description}
		EVENT['start'] = {'date': dateStart}
		if not dateEnd:
			dateEnd = dateStart
		EVENT['end'] = {'date': dateEnd}
		
		if freq:
			recurrence = "RRULE:FREQ={}".format(freq) #"RRULE:FREQ={};INTERVAL={}".format(freq, interval)
			if interval:
				recurrence += ";INTERVAL={}".format(interval)
			EVENT['recurrence'] = [recurrence]  #['RRULE:FREQ={};INTERVAL={}'.format(freq, interval)]
		
		return EVENT

	def add_event(self, cal_id, notify=True, *args, **kwargs):
		EVENT = self._event(*args, **kwargs)
		
		e = self.service.events().insert(calendarId=cal_id, sendNotifications=notify, body=EVENT).execute()

		return e

	def add_events(self, cal_id, events, notify=True, verbose=True):
		for event in events:
			self.add_event(cal_id, notify=notify, **event)

			if verbose:
				print "Added {}".format(event['summary'])




def name2wikiurl(first, last):
	# must be first name, last name
	# does not deal with one named people like:
	# stage names: https://en.wikipedia.org/wiki/Madonna_(entertainer)
	f = str.title(first)
	l = str.title(last)
	
	url = 'https://en.wikipedia.org/w/index.php?action=raw&title={}_{}'.format(f, l)
	
	return url

def wiki_parse_bdate(str_, verbose=False):
	if not 'birth_date' in str_:
		return None
	
	# pinpointing the birthdate part
	str_ = str_[:5000].split('birth_date')[1].split('}}')[0]
	
	# 'YYYY-MM-DD'
	zero_element = str_.split('|')[1]
	
	# the response might have the 'df=yes' or 'mf=yes' before or after the birth date
	# see differences between:
	# before: requests.get('https://en.wikipedia.org/w/index.php?action=raw&title=Albert_Einstein')
	# after: r = requests.get('https://en.wikipedia.org/w/index.php?action=raw&title=Michael_Jordan')
	
	# For people who lived in the time of usage of the Julian calendar Wikipedia corrects for the Gragorian
	# For example: https://en.wikipedia.org/w/index.php?action=raw&title=Isaac_Newton
	if 'New Style' in zero_element:
		str_ = str_.split('New Style')[1]
		zero_element = str_
			
	if 'yes' in zero_element:
		idxs = [2, 3, 4]
	else:
		idxs = [1, 2, 3]
	
	str_ = str_.split('{{')[1]
	l_split = str_.split('|')
	l_ = [l_split[idx] for idx in idxs]
	
	if verbose:
		print l_
	# verifying month and day have two digets
	l_[1] = "{:02.0f}".format(int(l_[1]))
	l_[2] = "{:02.0f}".format(int(l_[2]))
	
	# might have to verify year has four ...
	#TBD
	
	str_bday = "-".join(l_)
	
	return str_bday
		
def name2wikibdate(first, last, verbose=False):
	url = name2wikiurl(first, last)
	if verbose:
		print url
	r = requests.get(url)
	return wiki_parse_bdate(r.content, verbose=verbose)


def names2calendar(credentials, names, cal_name=None, cal_id=None, 
	interval=5, freq='YEARLY', summary = "Happy %s %s Day!", verbose=False):

	cal = Calendar(credentials)
	if not cal_id:
		# need to check if calendar exists ....
		if not cal_name:
			raise ValueError("Since `cal_id` is not given `cal_name` needs to be set")
		if verbose:
			print "Creating {} calendar".format(cal_name)
		
		cal_id = cal.create_cal(summary=cal_name)

	# Pulling birth days from Wikipedia
	l_events = []
	for name in names:
		bday = name2wikibdate(name[0], name[1])
		summary_temp = summary%(name[0], name[1])

		# creating an event
		event = {'summary': summary_temp, 'dateStart': bday, 'freq':freq, 'interval':interval}
		l_events.append(event)

	# Adding all events to calendar
	cal.add_events(cal_id, l_events)

	return cal, cal_id

