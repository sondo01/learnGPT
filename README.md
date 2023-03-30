# learnGPT
A small python script using chatGPT3.5 and Whisper API as a digital tutor.
Whisper API allows voice communcation instead of boring typing into chatGPT.
YOU NEED YOUR OWN API KEY to run this script.
The answer (from chatGPT) is also converted to voice via ttysx3 module.
The preset system prompt (line 123) instructs chatGPT to be a teacher. You can edit it as you want.

I tested this script on MacBook Pro M1, Debian GNU/Linux 11  and hope it work on other platform

Use with you own risk!

1. Dependency:
On MacOS, an extra package "portaudio" is needed. one need to install it via brew from termial:
- Install brew:
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
NOTE: Follow the instruction at the end of the above step to add brew into the exec path
- Install portaudio
$ brew install portaudio

2. Setup:
- After clonning  or downloading the files, go to the learGPT folder and run:
$ pip install -r requirements.txt
- Edit learnGPT.py file with any text editor you like and add your own OpenAI API key at line 13
- If you want to use and have access to chatGPT4, you can change the the model version at line 108.

3. Run:
$ python learnGPT.py

Note1: Please read and listen carefully the instruction at the beginning.
Note2: There are 2 hot keys: 
- "s": to skip a long answer
- "p": to pause before recording the next conversation.

Enjoy and Remember: Use with your own risk. I am not responsible for any consequences or damages that may result from using this project or its dependencies.
