from flask import Flask, request, jsonify, render_template
from gtts import gTTS
from playsound import playsound
import os
import webbrowser
import speech_recognition as sr

app = Flask(__name__)

commands_list = [
    "Open YouTube",
    "Play [video name] on YouTube",
    "Take a screenshot",
    "Add a task",
    "List tasks",
    "Hello",
    "Exit"
]

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return "I could not understand your command."
    except sr.RequestError:
        return "Failed to reach the speech recognition service."

@app.route('/')
def home():
    greeting_text = "Hello! How can I help you? Here are some commands you can give me."
    respond(greeting_text)
    return render_template('index.html', commands=commands_list)

def respond(response_text):
    print(f"Responding with: {response_text}")  # Debugging line
    tts = gTTS(text=response_text, lang='en')
    audio_file = "response.mp3"
    tts.save(audio_file)

    try:
        playsound(audio_file)  # Play the audio file
        print("Audio played successfully.")  # Debugging line
    except Exception as e:
        print(f"Error playing audio: {e}")
    
    os.remove(audio_file)  # Cleanup after playing

@app.route('/start_listening', methods=['POST'])
def start_listening():
    command = listen_for_command()
    
    print(f"Received command: {command}")  # Debugging line

    if not command:
        response_text = "No command received."
        respond(response_text)
        return jsonify({'response': response_text})

    # Command processing logic
    if "play" in command:
        video_name = command.replace("play", "").strip()
        if video_name:
            search_url = f"https://www.youtube.com/results?search_query={video_name.replace(' ', '+')}"
            response_text = f"Searching for {video_name} on YouTube."
            respond(response_text)
            webbrowser.open(search_url)
        else:
            response_text = "Please specify a video to play."
            respond(response_text)
    elif "open youtube" in command:
        response_text = "Opening YouTube now."
        respond(response_text)
        webbrowser.open("https://www.youtube.com")
    elif "hello" in command:
        response_text = "Hello! How can I assist you?"
        respond(response_text)
    elif "exit" in command:
        response_text = "Goodbye!"
        respond(response_text)
    else:
        response_text = "I didn't understand that."
        respond(response_text)

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
