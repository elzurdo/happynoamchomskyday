# [Happy Noam Chomsky Day!](https://www.youtube.com/watch?v=dXE6ZafkRMI)
Create and personalise a Google Calendar

![Alt text](./png/hncd_mrfantastic.png?raw=true "Title")


Save birthdays of known (Wikipedia worthy) people as events in your Google Calendar. 

It as easy as:

```
from happynoamchomskyday import chomsky
credentials = chomsky.get_credentials()
l_names = [("Christopher", "Nolan"), ("Noam", "Chomsky"), ("Alexander", "Hamilton"), ("Michael", "Jordan")]
cal, cal_id = chomsky.names2calendar(credentials, l_names, cal_name='favs_birthdays')
```

We will make this more flexible in the future. (E.g, pushing your own dictionary of events and pulling from Google Sheets) 


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
```
from happynoamchomskyday import chomsky  
chomsky.set_credentials()
```
(Best to do in python kernal, as I find that within Jupyter notebook the path is incorrect)

This will:  
1. Prompt the standard Google authorization  
2. Set your credential file `~./credentials/chomsky.json`   
    

# Usage
Once the Setup is set, just load:  
```
from happynoamchomskyday import chomsky
```
Get your creds:  
```
credentials = chomsky.get_credentials()
```
Create a list of Wikipedia worthy paper (we obtain birthdates from Wikipedia, at the moment)  
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
Where `cal` is a Google Calendar object and `cal_id` is its Id.
