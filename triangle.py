import geoip2.database #Library for working with MMDB files
import sys
import os.path

def findTarget(ip):
    if not os.path.exists("db.mmdb"): #Check if database file exists
        print ("[ERROR] Database could not be found")
        sys.exit() #Fail if database doesn't exist
    else:
        reader = geoip2.database.Reader('db.mmdb') #Create reader object containing database
        response = reader.city(ip) #Get location data from DB (stored in reader object) and store into variable
        print ("LOCATION DATA PULLED FOR " + ip)
        print ("COUNTRY: " + response.country.name)
        print ("STATE: " + response.subdivisions.most_specific.name)
        print ("CITY: " + response.city.name)
        print ("ZIP: " + response.postal.code)
        print ("COORDINATES: " + str(response.location.latitude) + "," + str(response.location.longitude))
        reader.close()
        return

def main(argv):
    usage = "USAGE: triangle.py [FLAGS] <input>\n-ip [IP_TO_LOCATE] Locate IP Address\n"

    if not argv: #Display usage if arguments are undefined
        print (usage)
        sys.exit()
    if argv[0] == "-ip":
        findTarget(argv[1]) #Launch primary function for analyzing location data
    
    sys.exit()

main(sys.argv[1:]) #Read arguments