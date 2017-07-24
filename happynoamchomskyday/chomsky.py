import requests
import httplib2
from apiclient import discovery

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
