from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
import sys

web_address = "https://merseyrail.org/"

#Email address and password for gmail SMTP server.
server_adr = ''
server_pwd = ''

#Returns a HTTPResponse object
web_request = urlopen(web_address)

#Parses HTTPResponse to HTML
page_parsed = BeautifulSoup(web_request, 'html.parser')

#Locates Kirkby train tags and isolates it with relevant tags.
#Can use one parent and next_sibling when looking at service status.
service = page_parsed.find('div', attrs={'class' : 'line northern'}).find(text='Southport').parent.parent

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

#Open email tempate and converts to list  
open_file = open('email_template.txt', 'r')
email_txt = open_file.read().split('\n')

#Locates services that have a disruption using popup that explains reason.
disruption = service.parent.find('div', attrs={'class' : 'status-pop'})

#Constructs email body
if disruption == None :
    email_txt[-1] = 'There appears to be no disruptions to your service today.'
else :
    #Explanation given my Merseyrail for disruptions
    email_txt[-1] = disruption.text.replace('  ', ' ').replace('Impace:', ' ')

#Convert back to string to send email.    
email_txt = ''.join(str(e + '\n') for e in email_txt)

try :
    #Sends email using first arguement.
    server.sendmail('', '', email_txt)
    
except Exception as e :
    print("Connection failed!")
    print(e)
    
    #Exits application
    sys.exit(0)

print("Email Sent!")