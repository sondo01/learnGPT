A small Python script that uses ChatGPT3.5 and Whisper API as a digital tutor.

You will need your own API key to run this script.

Whisper API enables voice communication instead of boring typing into ChatGPT.  
The answer from ChatGPT is also converted to voice using the ttyx3 module. 
Line 123 contains a preset system prompt that instructs ChatGPT to act as a teacher. You can edit this prompt to customize its behavior.

I tested this script on MacBook Pro M1, Debian GNU/Linux 11, and I hope it works on other platforms. 

Use at your own risk!

1. Dependencies:
On macOS, an extra package, portaudio, is needed. To install it via Terminal:
- Install brew:
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Note: Follow the instructions at the end of the above step to add brew to the exec path.
- Install portaudio:
$ brew install portaudio

2. Setup:
After cloning or downloading the files, go to the learnGPT folder and run:
$ pip install -r requirements.txt
Edit learnGPT.py with any text editor you like and add your own OpenAI API key at line 13.
If you want to use and have access to ChatGPT4, you can change the model version at line 108.

3. Run:
$ python learnGPT.py
That's it.

Note 1: Please read and listen carefully to the instructions at the beginning.

Note 2: There are 2 hot keys:
"s": to skip a long answer
"p": to pause before recording the next conversation.
Enjoy and remember: Use at your own risk. I am not responsible for any consequences or damages that may result from using this project or its dependencies."
