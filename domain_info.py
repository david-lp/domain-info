import sys
import requests
import socket
import whois

#requires python-whois lib
#returns http status code, IP address, registered org, and redirect destination of given domains 
#usage "domain_info.py input_file > output_file"
#input file must contain URLs in scheme://netloc format and seperated by line-break

#would like to be able to pass -f for file argument or single domains, ie domain_info.py http://www.abc.com
#would also be nice to just input domains as subdomain.domain.tld. Requests requires scheme, socket and whois do not

#HTTP Status codes 
#2xx Success
#3xx Redirection
#4xx Client Error
#5xx Server Error

file_name = sys.argv[1]
input_file = open(file_name)

print "http_status;domain;ip_addr;org;redirect"

for line in input_file:
    line = line.rstrip()
    domain = line.split("//")[-1].split("/")[0]
    try:
		
        r = requests.head(line)
        
        try:
		    r2 = requests.get(line)
        except requests.exceptions.RequestException as e: # pass at requests exceptions because they are jerks
            pass
			
        ip_addr = socket.gethostbyname(domain)
		
        try:
            org = str(whois.whois(domain).org)
        except whois.parser.PywhoisError as e: # just say you didn't find it, don't cock up the whole program
            org = "no_match"
		
		# fetch final destination, good for collecting redirect, pass on error
        try:
            location = r2.history[0].headers['Location']
        except IndexError:
            location = "empty"
			
        print str(r.status_code) + ";" + domain + ";" + ip_addr + ";" + org + ";" + location
    except requests.ConnectionError:
        print ("failed to connect") + ";" + domain + ";;;"
