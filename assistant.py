import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
text_to_speech = pyttsx3.init()

# Set the female voice
voices = text_to_speech.getProperty('voices')
text_to_speech.setProperty('voice', voices[1].id)  # Index 1 typically corresponds to a female voice

def speak(text):
    text_to_speech.say(text)
    text_to_speech.runAndWait()

def listen_wake_word():
    while True:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)

            try:
                wake_word = recognizer.recognize_google(audio, language="en-US")
                print(f"Wake Word: {wake_word}")
                if "hey siri" in wake_word.lower():
                    speak("Hello! How can I help you today?")
                    return
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-US")
            print(f"User: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def get_date():
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    speak(f"The current date is {current_date}.")

def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {current_time}.")

def set_reminder():
    speak("Sure, when would you like me to remind you?")
    reminder_time = listen()

    try:
        reminder_time = datetime.datetime.strptime(reminder_time, "%H:%M")
        current_time = datetime.datetime.now().time()

        if reminder_time < current_time:
            speak("Sorry, I can't set reminders for the past.")
        else:
            delta_time = datetime.datetime.combine(datetime.date.today(), reminder_time) - datetime.datetime.combine(datetime.date.today(), current_time)
            seconds = delta_time.total_seconds()
            speak(f"I will remind you in {int(seconds // 60)} minutes.")
    except ValueError:
        speak("Sorry, I couldn't understand the time format.")

def create_todo():
    speak("What task would you like to add to your to-do list?")
    task = listen()

    if task:
        with open("todo.txt", "a") as todo_file:
            todo_file.write(f"- {task}\n")
        speak(f"Task '{task}' added to your to-do list.")

def search_web():
    speak("What would you like to search the web for?")
    query = listen()

    if query:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Here are the search results for {query}.")

def main():
    listen_wake_word()
    
    while True:
        command = listen()

        if "date" in command:
            get_date()
        elif "time" in command:
            get_time()
        elif "set reminder" in command:
            set_reminder()
        elif "list" in command:
            create_todo()
        elif "search web" in command:
            search_web()
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")

if __name__ == "__main__":
    main()