import speech_recognition as sr
import yaml
import sys
import socket
import datetime
import webbrowser
import os
from gtts import gTTS

yaml_data = []

def say(param):
    tts = gTTS(text=param, lang='en')
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")

def show_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('IP address is ' + str(s.getsockname()[0]))
    s.close()


def show_time():
    print('Today is ' + str(datetime.datetime.now()))


def show_city_time(r):
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=None)
            try:
                city = r.recognize_google(audio).lower()
                break
            except sr.UnknownValueError:
                print("Your assistent could not understand audio, please say again!")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognision " + e)


def check_network_connection():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        say('This computer is connect to internet')
        print('This computer is connect to internet')
    except urllib.request.URLError as err:
        say('You don\'t have internet connection')
        print('You don\'t have internet connection')


def search_on_google(list_to_search):
    string = '\n'.join(map(str, list_to_search))
    webbrowser.open("http://google.com/?#q=" + str(string))


def execute(input, r):
    if input == yaml_data['STOP']:
        sys.exit(0)
    if input == yaml_data['IP']:
        show_ip()
        return
    if input == yaml_data['TIME']['default']:
        show_time()
        return
    if input == yaml_data['TIME']['city']:
        show_city_time(r)
        return
    if input == yaml_data['NETWORK']:
        check_network_connection()
        return
    if input.split()[0] == yaml_data['SEARCH']:
        lst = input.split()[1:]
        search_on_google(lst)
        return

def main():
    global yaml_data
    with open('constants.yaml') as f:
        yaml_data = yaml.load(f)

    r = sr.Recognizer()
    r.pause_threshold = 0.6  # seconds of non-speaking audio before a phrase is considered complete
    r.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    r.non_speaking_duration = 0.4  # seconds of non-speaking audio to keep on both sides of the recording
    r.energy_threshold = 110000
    r.dynamic_energy_adjustment_damping = 0.15
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=None)
            try:
                input_speech = r.recognize_google(audio).lower()
                print('Your assistent think you said ' + input_speech)
                execute(input_speech, r)
            except sr.UnknownValueError:
                print("Your assistent could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognision " + str(e))


if __name__ == "__main__":
    main()
