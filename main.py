from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
import sys
import datetime

web_address = "https://merseyrail.org/"

#Email address and password for gmail SMTP server.
server_adr = ''
server_pwd = ''

#Returns a HTTPResponse object
web_request = urlopen(web_address)

#Parses HTTPResponse to HTML
page_parsed = BeautifulSoup(web_request, 'html.parser')

#Determine what the service the the user would like to check and what line it is on.
users_service = input("What service would you like to check for disruptions?").lower().title()

if users_service in ['Southport', 'Hunts Cross', 'Kirkby', 'Ormskirk'] :
    #Services are on the Northern line
    service_line = 'northern'
elif users_service in ['Ellesmere Port', 'Chester', 'West Kirby', 'New Brighton'] :
    #Services are on the Wirral line
    service_line = 'wirral'
else :
    print('Service not available on the Merseyrail network.')
    sys.exit(0)
    
#Determines the time the user would likme to check for disruptions.    
time_check = input('What time would you like to check for disruptions? Note: Must be written in hh:mm format')

if len(time_check) != 5 :
    #Incorrect time format.
    print('Please use appropriate format. HH:MM')
    sys.exit(0)
else :
    #Converts hours and minutes to a measurable format.
    hour = int(time_check[:2])
    mins = int(time_check[3:])

#Calculates how long to pause for before continuing/sending email
time_stamp1 = datetime.datetime.now()
time_stamp2 = time_stamp1.replace(hour=hour, minute=mins)
delta = time_stamp2 - time_stamp

#Pauses application for seconds calculated above
pause.seconds(delta.total_seconds())

#Locates service train tags and isolates it with relevant tags.
#Can use one parent and next_sibling when looking at service status.
service = page_parsed.find('div', attrs={'class' : 'line ' + service_line}).find(text=users_service).parent.parent

#Locates service status of isolated service.
service_status = service.find('span', attrs={'class' : 'service'}).text

try :
    #Creates a secure connection to SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()

    #Logs in to senders email address.
    server.login(server_adr, server_pwd)
    
except Exception as e :
    print("Connection failed!")
    print(e)
    
    #Exits application
    sys.exit(0)

#Open email template and converts to list  
open_file = open('email_template.txt', 'r')
email_txt = open_file.read().split('\n')

#Locates services that have a disruption using popup that explains reason.
disruption = service.parent.find('div', attrs={'class' : 'status-pop'})

#Constructs email body
if disruption == None :
    
    if service_status == 'Good Service' :
        #Service is good, no disruptions.
        email_txt[-1] = 'There appears to be no disruptions to your service at this time.'
    else :
        #Disrupted service with no explanation given on Merseyrail website.
        email_txt[-1] = 'There are currently disruptions to your service at the time. Please check the Merseyrail Twitter for more information.'
else :
    #Explanation given my Merseyrail for disruptions
    email_txt[-1] = disruption.text.replace('  ', ' ').replace('Impact:', ' ')

#Convert back to string to send email.    
email_txt = ''.join(str(e + '\n') for e in email_txt) + '\nRegards,\nTrain Updates'

try :
    #Sends email using first arguement.
    server.sendmail('', '', email_txt)
    
except Exception as e :
    print("Connection failed!")
    print(e)
    
    #Exits application
    sys.exit(0)