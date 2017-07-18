import geoip2.database #Library for working with MMDB files
import sys
import os
import urllib.request #Library used for downloading database if it doesn't exist
import tarfile #Library to extract tarballs 
import shutil
import glob
import hashlib

def installDatabase():
    extracted = tarfile.open('archive.tar.gz',"r:gz") #Extract database file
    extracted.extractall()
    extracted.close()
    current = os.getcwd() #Store working directory
    db_file = glob.glob(r'*/*.mmdb') #Get database filename and location
    shutil.copy(db_file[0], current) #Copy database to working directory
    del_dir,del_file = db_file[0].split("\\") #Get temporary directory for removal
    os.rename(del_file, "db.mmdb") #Rename and install database
    print ("Cleaning up...")
    shutil.rmtree(del_dir) #Clean up temporary files
    os.remove("archive.tar.gz")
    return

def checkDatabase():
    if not os.path.exists("db.mmdb"): #Check if database file exists
        if os.path.exists("archive.tar.gz"):
            checksum = hashlib.md5(open("archive.tar.gz", 'rb').read()).hexdigest()
            if checksum == "b0d93822d6937bcbaa549e1ab90b235a":
                print ("Partially installed database found...finishing setup...")
                installDatabase()
                return
            else:
                print ("Corrupted database found...re-installing")
        print ("Running setup scripts...")
        print ("Downloading database...")
        urllib.request.urlretrieve('http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz','archive.tar.gz')
        print ("Installing database...")
        installDatabase()
    return

def findTarget(ip):
    checkDatabase()
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