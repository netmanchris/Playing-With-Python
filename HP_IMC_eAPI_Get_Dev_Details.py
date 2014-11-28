#function to get dev details based on IP address



import sys, subprocess, requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml
from copy import deepcopy

# Set IMC server IP address and credentials
imc_server = '''kontrolissues.thruhere.net:8084'''   #match port number of IMC server default 8080 or 8443
imc_user = '''admin'''
imc_pw = '''#kgf3og#'''

'''
======================================================================================
The following section details global functions and variables that will be used within the
Information Gathering Functions
======================================================================================
'''
#set url global variables
h_url = '''http://'''         #prefix for building URLs use HTTP or HTTPS
url = h_url+imc_server

#auth handler for eAPI calls
auth = requests.auth.HTTPDigestAuth(imc_user,imc_pw)               


#set var to store responses from IMC eAPI server
r = []
funct_array = []
#funct_array = []
#set empty function dictionaries
#GetDevDetDict = ()
#GetIntDetDict = ()
#RealTimeLocDict = ()

#parse XML to create two lists keys and values to create dictionary file 

def parse_r():
    '''  This function will parse Restful API XML content in variable r to create dictionary file funct_dict'''
    global funct_dict, funct_array, keys, values
    keys = []
    values = []
    if r.status_code == 401:
        print (''' Wrong Username or Password''')
    elif r.status_code == 403:
        print ('''Too many attempts. Please try again later''')
    if r.status_code == 200:
      tree = xml.fromstring(r.content)
      for node in tree.iter():
          keys.append(node.tag)
          values.append(node.text)
          funct_dict = dict(zip(keys,values)) #create dictionary file of keys and values
          #funct_dict = dict(zip(keys,values))
          funct_array.append(funct_dict)
          

def list_dict(mydict):
    '''This function will list the all current key/value pairs in a given dictionary file'''
    for key, value in mydict.items():
        print (key,value)

def GetDevDetails(deviceIp):
    '''This function will use the DeviceIp key value from the dictionary file RealTimeLocDict as the input var and
    to perform the Get Device Details API against the HP IMC Server and return the dictionary file GetDevDetDict

    ex. GetDevDetails('10.3.10.5')

    '''
    global r, GetDevDetDict, funct_array
    get_dev_details_url =  ('''/imcrs/plat/res/device?resPrivilegeFilter=false&ip='''+deviceIp+'''&start=0&size=10&orderBy=id&desc=false&total=false''')
    f_url = url + get_dev_details_url
    r = requests.get(f_url, auth=auth)
    parse_r()
    keys = []
    values = []
    GetDevDetDict = deepcopy(funct_array)
    funct_array = []
    
