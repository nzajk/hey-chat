import pyttsx3
import openai
import speech_recognition as sr

openai.api_key = 'sk-<your-api-key>'

recognizer = sr.Recognizer()

voice_id = 'com.apple.voice.compact.en-US.Samantha' # change this to your preferred voice
voice_wpm = 180                                     # change this to your preferred words per minute

def response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response.choices[0].message['content'].strip()

def text_to_speech(text):
    engine = pyttsx3.init()

    # adjust the voice and wpm 
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', voice_wpm)

    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            try:
                text = recognizer.recognize_google(audio).lower()
                if text in ['stop', 'stop listening', 'shut up']:
                    break
                if text[0:7] == 'hey gpt':
                    response = response(text[8:])
                    text_to_speech(response)

                # print(text) # for testing purposes

            except sr.UnknownValueError:
                recognizer = sr.Recognizer()
                text_to_speech("Sorry, I didn't catch that. Can you repeat?")

main()
