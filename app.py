import requests
import datetime
import os
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am booji clock Sir. Welcome to the Smart Alarm System!")   

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query    

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Hyderabad&appid=0522c693c9c5862b6297901202ca22e1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = round(data['main']['temp'] - 273.15, 1)
            desc = data['weather'][0]['description']
            return temp, desc
        else:
            print("Failed to retrieve weather data. Please check your internet connection.")
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def set_alarm(time):
    alarm_time = datetime.datetime.strptime(time, "%H:%M")
    while True:
        current_time = datetime.datetime.now()
        if current_time.hour == alarm_time.hour and current_time.minute == alarm_time.minute:
            os.system("start Alarm1.wav")
            return

def main():
    wishMe()
    speak("Please enter your wake up time")


    # Get weather information
    temp, desc = get_weather()
    if temp is not None and desc is not None:
        print(f"City: Hydaerabad, Weather: {desc.capitalize()}, Temperature: {temp}°C")

    # Set wake-up time
    print("\nEnter your wake-up time: ")
    wh = int(input("Hours: "))
    wm = int(input("Minutes: "))
    time = "{:02d}:{:02d}".format(wh, wm)

    # Task input
    n = int(input("\nEnter number of tasks: "))

    tasks_list = []
    tasks_dict = {}
    for i in range(n):
        task = input(f"Enter task {i+1}: ")
        duration_hours = int(input("Enter duration (hours): "))
        duration_minutes = int(input("Enter duration (minutes): "))
        #task_duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)
        task_duration = "{:02d}:{:02d}".format(duration_hours, duration_minutes)
        tasks_list += [task]
        tasks_dict[task] = task_duration

    # Display tasks and their durations
    print("\nYour tasks for the day:")
    for task, duration in tasks_dict.items():
        print(f"- {task}: {duration}")

    print()
    if desc != "raining" or desc != "overcast" or desc != "snowing" or desc != "windy" or desc != "thunder and lightning":
        set_alarm(time)
        print("Alarm ringing at " + time)

    for i in tasks_list:
        a = time.split(":")
        k = tasks_dict[i].split(":")
        h = int(a[0]) + int(k[0])
        m = int(a[1]) + int(k[1])
        time = "{:02d}:{:02d}".format(h, m)
        set_alarm(time)
        print("Alarm ringing at " + time)

if _name__ == "_main_":
    main()