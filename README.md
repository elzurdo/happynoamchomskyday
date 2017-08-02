# [Happy Noam Chomsky Day!](https://www.youtube.com/watch?v=dXE6ZafkRMI)
Create and personalise a Google Calendar

![Alt text](./png/hncd_mrfantastic.png?raw=true "Title")


Save birthdays of known (Wikipedia worthy) people as events in your Google Calendar. 

It's as easy as:

```
from happynoamchomskyday import chomsky  

credentials = chomsky.get_credentials()  

l_names = [("Christopher", "Nolan"), ("Noam", "Chomsky"), ("Alexander", "Hamilton"), ("Michael", "Jordan")]  

cal, cal_id = chomsky.names2calendar(credentials, l_names, cal_name='favs_birthdays')
```

We will make this more flexible in the future. (E.g, pushing your own dictionary of events and pulling from Google Sheets) 

# Support 
python 2.7    
We will update to python 3 in the near future. 

# Setup
The usual:
```
python setup.py install 
```
or 
```
python setup.py develop
```

## Setup credentials  
The Google Calendars requires authentication. 
In a python kernal do:  
```
from happynoamchomskyday import chomsky  
chomsky.set_credentials()
```
(Best to run this in the kernel, as Jupyter notebook currently refers to the wrong path)

This will:  
1. Prompt the standard Google authorization  
2. Create the necessary credential file `~./credentials/chomsky.json`   
    

# Usage
Once the Setup is set, just load:  
```
from happynoamchomskyday import chomsky
```
Get your creds:  
```
credentials = chomsky.get_credentials()
```
Create a list of Wikipedia worthy people (we obtain birthdates from Wikipedia, at the moment)  
```
l_names = [("Christopher", "Nolan"), ("Noam", "Chomsky"), ("Alexander", "Hamilton"), ("Michael", "Jordan")]
```
(the format must be a list of tuples of `(firstNAme, lastName)` as appears on their Wiki page.  
E.g, entries like: https://en.wikipedia.org/wiki/Albert_Einstein    
are fine but others like: https://en.wikipedia.org/wiki/Madonna_(entertainer)  
are not set up for yet.  

```
cal, cal_id = chomsky.names2calendar(credentials, l_names, cal_name='favs_birthdays')
```
, where `cal` is an object and `cal_id` is the ID of the created Calendar (in this case of 'favs_birthdays').

To verify creation of the calendar, just check your [Google Calendar](www.calendar.google.com) or run this script:
```
cal.print_cal_list()
```



If you would like to delete the newly created calendar just do:  
```
cal.delete_cal(cal_id)
```
and verify that it is delete with 
```
cal.print_cal_list()
```
again.  
