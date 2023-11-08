import win32com.client
import speech_recognition as sr
import webbrowser
import os
import requests  # Import the requests library for making HTTP requests
import datetime
from config import apikey
import openai
import threading

# Initialize the chatStr variable to store conversation history
chatStr = ""

# Replace with ESP32's IP address
ESP32_IP = "192.168.100.114"


def speak(text):
    print("Jarvis: " + text)  # Print what the AI is saying
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")

    try:
        query = r.recognize_google(audio, language="en-IN")
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        print("Sorry, I'm having trouble processing your request. Please try again later.")
        return ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Jarvis: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0.7,
        max_tokens=150
    )

    speak(response["choices"][0]["message"]["content"])
    chatStr += f"Jarvis: {response['choices'][0]['message']['content']}\n"
    return response["choices"][0]["message"]["content"]


# Function to control relays
def control_relays(relay, action):
    if relay == "1":
        if action == "ON":
            requests.get(f"http://{ESP32_IP}/?Relay1=ON")
            speak("Turning on Relay 1.")
        elif action == "OFF":
            requests.get(f"http://{ESP32_IP}/?Relay1=OFF")
            speak("Turning off Relay 1.")
    elif relay == "2":
        if action == "ON":
            requests.get(f"http://{ESP32_IP}/?Relay2=ON")
            speak("Turning on Relay 2.")
        elif action == "OFF":
            requests.get(f"http://{ESP32_IP}/?Relay2=OFF")
            speak("Turning off Relay 2.")
    else:
        speak("Invalid relay or action.")


if __name__ == "__main__":
    speak("Hello, I am JARVIS, your AI Home assistant. How can I assist you today?")

    # while True:
    #     print("Enter the word you want to say or say 'stop' to exit:")
    #     user_input = input()
    #     if user_input.lower() == "stop":
    #         break

    print("Listening for commands...")
    while True:
        command = takeCommand().lower()
        if "exit" in command:
            speak("Exiting...")
            break
        if "goodbye" in command:
            speak("goodbye sir")
            break
        elif "open" in command:
            if "youtube" in command:
                speak("Opening youtube Sir")
                webbrowser.open("https://www.youtube.com")
            elif "instagram" in command:
                speak("Opening instagram Sir")
                webbrowser.open("https://www.instagram.com")
            elif "google" in command:
                speak("Opening instagram Sir")
                webbrowser.open("https://www.google.com")
            elif " music" in command:
                # Specify the correct path to the music file
                musicPath = r"C:\Users\lenovo\Desktop\music.mp3"
                os.startfile(musicPath)
            elif "word" in command:
                speak("Opening Microsoft Word Sir")
                wordPath = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
                os.startfile(wordPath)
        elif "time" in command:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strfTime}")
        elif "who made you" in command:
            speak("Mr. Sahil made me")
        elif "bulb" in command:
            if "on" in command:
                if "1" in command:
                    speak("Turning On white bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("1", "ON"))
                    relay_thread.start()
                elif "one" in command:
                    speak("Turning On white bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("1", "ON"))
                    relay_thread.start()
                elif "white" in command:
                    speak("Turning On white bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("1", "ON"))
                    relay_thread.start()
                elif "2" in command:
                    speak("Turning On orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "ON"))
                    relay_thread.start()
                elif "two" in command:
                    speak("Turning On orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "ON"))
                    relay_thread.start()
                elif "to" in command:
                    speak("Turning On orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "ON"))
                    relay_thread.start()
                elif "orange" in command:
                    speak("Turning On orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "ON"))
                    relay_thread.start()
                else:
                    speak("Invalid relay or action.")
            elif "off" in command:
                if "1" in command:
                    speak("Turning off white bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("1", "OFF"))
                    relay_thread.start()
                elif "one" in command:
                    speak("Turning Off white bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("1", "OFF"))
                    relay_thread.start()
                elif "white" in command:
                    speak("Turning Off white bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("1", "OFF"))
                    relay_thread.start()
                elif "2" in command:
                    speak("Turning off orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "OFF"))
                    relay_thread.start()
                elif "two" in command:
                    speak("Turning off orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "OFF"))
                    relay_thread.start()
                elif "to" in command:
                    speak("Turning off orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "OFF"))
                    relay_thread.start()
                elif "orange" in command:
                    speak("Turning off orange bulb Sir")
                    relay_thread = threading.Thread(target=control_relays, args=("2", "OFF"))
                    relay_thread.start()
                else:
                    speak("Invalid relay or action.")
        else:
            chat(command)
