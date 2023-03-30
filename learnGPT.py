import openai
import json
import datetime
import pyaudio
import wave
import numpy as np
import pyttsx3
from langdetect import detect
from pynput import keyboard
import threading
import time

# Replace with your OpenAI API key
openai.api_key = ""
langs_detect = {"en": "english", "vi": "vietnamese", "de": "german", "fr": "french", "it": "italian", "ja": "japanese"}
interrupt_speech = False
pause_event = threading.Event()
# Initialize the speaker engine
speaker = pyttsx3.init()
# Set the rate and volume
speaker.setProperty('rate', 180)
speaker.setProperty('volume', 0.7)

file_path = "in.wav"

def record_audio():
    CHUNK = 4096  # increase buffer size
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050  # reduce sample rate
    THRESHOLD = 0.01
    SILENCE_LIMIT = 2
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    print("Recording...")

    # Wait for the audio to be loud enough to start recording
    while True:
        data = stream.read(CHUNK)
        if np.max(np.frombuffer(data, dtype=np.int16)) >= THRESHOLD * 32767:
            break
    # Start recording
    frames = []
    silence_count = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if np.max(np.frombuffer(data, dtype=np.int16)) < THRESHOLD * 32767:
            silence_count += 1
            if silence_count > SILENCE_LIMIT * (RATE / CHUNK):
                break
        else:
            silence_count = 0

    print("Finished recording")

    # Stop the stream and close the PyAudio object
    stream.stop_stream()
    stream.close()
    p.terminate()
    # Convert the list of frames into a single byte string
    audio_data = b"".join(frames)
    # Write the audio data to a WAV file
    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(p.get_sample_size(FORMAT))
        wav_file.setframerate(RATE)
        wav_file.writeframes(audio_data)

    # send audio file to whisper to convert to text
    audio_file= open("in.wav", "rb")
    if base_lang == "":
        Whisper_prompt = f"Use English languages"
    else:
        Whisper_prompt = f"Use either {to_learn} or {base_lang} languages"

    whisper_parms = {
        "file": audio_file,
        "model": "whisper-1",
        "prompt": Whisper_prompt
    }
    wprompt = openai.Audio.transcribe("whisper-1", audio_file, whisper_parms).text
    return wprompt
def on_press(key):
    global interrupt_speech, pause_event
    try:
        if key.char == 's':  # Replace 's' with desired key
            speaker.stop()
        if key.char == 'p':  # Use space to pause/resume
            if pause_event.is_set():
                pause_event.clear()
            else:
                pause_event.set()

    except AttributeError:
        pass
def speak(t):
    # Start speech
    speaker.say(t)
    speaker.runAndWait()
def chatGPT_query(prompt):
    model_engine = "gpt-3.5-turbo" # Replace with your preferred GPT-3 model
    completions = openai.ChatCompletion.create(
        model=model_engine,
        messages= prompt,
        # max_tokens=2048,
        temperature=0.4,
    )
    response = completions['choices'][0]['message']['content']
    return response

def main():
    global pause_event
    voices_learn = {
    "vietnamese": "com.apple.voice.compact.vi-VN.Linh",
    "english": "com.apple.speech.synthesis.voice.samantha",
    "japanese": "com.apple.speech.synthesis.voice.kyoko.premium",
    "french": "com.apple.speech.synthesis.voice.thomas",
    "german": "com.apple.speech.synthesis.voice.anna",
    "italian": "com.apple.speech.synthesis.voice.alice"
    }
    base_lang = ""
    to_learn = ""
    is_foreign = ""
    speaker.setProperty('voice', voices_learn['english'])
    system_prompt = "Hello, I'm Alice, your teacher for today. I can assist you in learning foreign languages (such as English, Vietnamese, Japanese, French, German, Italian) as well as math, science, humanity, and social science. Here are two important instructions for our conversation: First, to ensure smooth communication, we will take turns speaking. When you see 'Recording...', it's your turn to talk. If you pause for more than 2 seconds, it will be my turn to speak, and you will see 'Finished recording.' Secondly, if you would like to change the topic of the conversation, please say 'Please start a new conversation.'"
    print(system_prompt)
    speak(system_prompt)


    while base_lang == "" or base_lang not in voices_learn:
        if base_lang == "":
            st1 = "What is your native language? "
        else:
            st1 = f"I don't know {base_lang}. Could you please tell me again your native language? "
        print(st1)
        speak(st1)

        base_lang = record_audio()
        base_lang = base_lang.lower()
        if base_lang.endswith(".") or base_lang.endswith("?") or base_lang.endswith("!"):
            base_lang = base_lang[:-1]
        print(base_lang)
    while is_foreign == "" or ("yes" not in is_foreign and "no" not in is_foreign) :
        if is_foreign == "":
            st1 = "Do you want to learn a foreign language today? Please choose Yes or No"
        else:
            st1 = f"Could you please answer Yes or No?"
        print(st1)
        speak(st1)

        is_foreign = record_audio()
        is_foreign = is_foreign.lower()

        print(is_foreign)
    if "yes" in is_foreign:
        while to_learn == "" or to_learn not in voices_learn:
            if to_learn == "":
                st1 = "Which language do you want to practice? "
            else:
                st1 = f"I don't know {to_learn}. Could you please tell me again what language you want to practice? "
            print(st1)
            speak(st1)

            to_learn = record_audio()
            to_learn = to_learn.lower()
            if to_learn.endswith(".") or to_learn.endswith("?") or to_learn.endswith("!"):
                to_learn = to_learn[:-1]
            print(to_learn)
            start_str = f"Great, you are {base_lang} native speaker and you want to learn {to_learn}. Let's start!"
    else :
        start_str = f"Great, Let's start!"
        to_learn = base_lang



    print(start_str)
    speak(start_str)
    initdata = ""
    instruction = f"You are Alice, a teacher who teach {to_learn} language as well as social science, humanities, mathematic and science. You are a Socratic teacher and also humorous, nice and kind. At the beginning of the conversation, you will give a greating to your student and ask their name, their year level to adapt your teaching curriculum. You will answer to maintain the conversations with users in {to_learn}. You will use {base_lang} to comment  and correct users' input, including grammar and structure. Your response will have 2 parts separated by ||. The first part is your conversation in {to_learn} language. the second part is your comment in {base_lang}. You don't answer questions those are not related to the learning topics. You should encourage students to engage into the conversation if they are shy or keeping silent by asking questions about culture or history that relevant to their age or year level."
    messages=[
        {"role": "system", "content":instruction},
        {"role": "assistant", "content": 'initdata: ' + initdata}
    ]

    prompt = "Hello"
    while True:
        for i in range(10):
            print(prompt)
            if prompt:
                if  "start a new conversation" in prompt.lower() :
                    messages=[
                        {"role": "system", "content":instruction},
                        {"role": "assistant", "content": 'initdata: ' + initdata}
                    ]
                    messages.append({"role": "user", "content": "Let's start a new conversation"})
                    res = chatGPT_query(messages)
                else:
                    messages.append({"role": "user", "content": prompt})
                    res = chatGPT_query(messages)
                    print("==========")
                    print(f"RES: {res}")
                    ress = res.split("||")
                    speaker.setProperty('voice', voices_learn[to_learn])
                    speak(ress[0])

                    if len(ress) > 1:
                        speaker.setProperty('voice', voices_learn[base_lang])
                        speak(ress[1])

                    messages.append({"role": "assistant", "content": res})
                prompt = ""
            pause_event.wait()
            prompt = record_audio()
            if prompt:
                lang = detect(prompt)
                if lang not in langs_detect or (to_learn != langs_detect[lang] and base_lang != langs_detect[lang]):
                    prompt = ""
            time.sleep(1)

if __name__ == "__main__":
    pause_event.set()

    # Start a thread to listen for key press
    key_listener = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start())
    key_listener.start()
    main()

    speaker.startLoop(False)
    while speaker.isBusy():
        if interrupt_speech:
            speaker.stop()
            break
        time.sleep(0.1)
    engine.endLoop()
    key_listener.join()
