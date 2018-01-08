#!/usr/bin/env python

from datetime import datetime
import speech_recognition as sr
import sys
import os, platform
import socket
import psutil
import requests


weather_key = "88eb55351af5beaf25d3a4f9ca84207a"

def Sphinx(r):
    # recognize speech using Sphinx
    try:
        result = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + result)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return result

# recognize speech using Google Speech Recognition
def Google_speech(r):
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + result)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return result



def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def parse(cmd):
    cmd = cmd.lower()

    #1. system date
    if cmd.find("date") != -1:
        os.system("date")

    #2. system battery
    if cmd.find("battery") != -1:
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = str(battery.percent)
        if plugged==False: plugged="Not Plugged In"
        else: plugged="Plugged In"
        print("Battery at " + percent+'% and '+plugged)

    #3. system internet
    if cmd.find("check") != -1 and cmd.find("internet") != -1:
        if is_connected():
            print "Connected to the internet"
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            print "Local ip: " + s.getsockname()[0]
            print "Global ip: " + os.system("curl https://api.ipify.org?format=txt")
            os.system("say Connected to the internet.")
        else:
            print "Not connected"
            os.system("say Not conncted to the internet.")

    #4. internet google image multiple
    if cmd.find("image") != -1 and cmd.find("internet") != -1:
        result = raw_input("what would you like to see? ")
        result = result.lower().replace(" ", "")
        url = "open 'http://www.google.com/search?tbm=isch&q=" + result + "'"
        print url
        os.system(url)

    #5. internet facebook
    if cmd.find("facebook") != -1:
        os.system("open http://www.facebook.com")
    
    #6. internet exchange multiple
    if cmd.find("exchange") != -1:
        print "Suggested currencies: EUR, RON, USD, GBP"
        base = raw_input("select base ")
        symbol = raw_input("select target")

        r = requests.get('https://api.fixer.io/latest?base=' + base.upper() + '&symbols=' + symbol.upper())
        print r.text

    #7. internet youtube
    if cmd.find("youtube") != -1:
        print "What would you like to query"
        os.system("say What would you like to query")
        result = raw_input()
        result = result.replace(" ", "")
        print "Searching " + result
        url = "open 'http://www.youtube.com/results?search_query='" + result
        os.system(url)

    #8. internet weather multiple
    if cmd.find("weather") != -1:
        print "London, Bucharest, Paris etc.\nChoose city"
        os.system("say Choose city")
        result = raw_input()
        result = result.replace(" ", "+")
        weather_url = "http://api.openweathermap.org/data/2.5/weather?q=" + result
        weather_url = weather_url + "&APPID=" + weather_key

        r = requests.get(weather_url)
        print r.text

    #9. app music (iTunes.app)
    if cmd.find("music") != -1:
        result = raw_input("Choose song ")
        os.system("open " + result)

    #10. app image (Preview.app)
    if cmd.find("image") != -1 and cmd.find("internet") == -1:
        result = raw_input("Choose img ")
        os.system("open " + result)
    #11. app mail (Mail.app)
    if cmd.find("mail") != -1:
        os.system("open /Applications/Mail.app")

    #12. app video (QuickTime Player)
    if cmd.find("video") != -1:
        result = raw_input("Choose video: ")
        os.system("open " + result)

    #13. app Steam
    if cmd.find("games") != -1:
        os.system("open /Applications/Steam.app")

    #14. system uptime
    if cmd.find("uptime") != -1:
        os.system("uptime")

    #15. app Calculator
    if cmd.find("calculator") != -1:
        os.system("open /Applications/Calculator.app")


    if cmd.find("exit") != -1 or cmd.find("quit") != -1:
        sys.exit()

if __name__ == "__main__":

    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug = True

    
    day = 1
    if datetime.now().hour < 18 and datetime.now().hour > 12:
        day = 2
    else: day = 3

    if day == 1:
        print "Good morning!"
        os.system("say Good morning!")
    elif day == 2:
        print "Good afternoon!"
        os.system("say Good afternoon!")
    elif day == 3:
        print "Good evening!"
        os.system("say Good evening!")
        

    while 1:
        # obtain audio from the microphone

        r = sr.Recognizer()
        result = ""
        if not debug:
            with sr.Microphone() as source:
                print "What would you like to do?"
                os.system("say What would you like to do?")       
                audio = r.listen(source)

            response = int(raw_input("1 for Google\n2 for crappy(Sphinx)\n3 to exit program\n4 for text input\n"))
            
            if response == 1:
                result = Google_speech(r)
            elif response == 2:
                result = Sphinx(r)
            elif response == 3:
                sys.exit()
            elif response == 4:
                result = raw_input()
            else:
                print "Invalid response"

        else:
            result = raw_input("Enter command: ")


        

        parse(result)

        print "\n#######\n"
