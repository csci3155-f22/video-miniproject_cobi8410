# Principles and Practice in Programming Languages
# Mini-Project: Fall 2022

See [instructions.md](instructions.md) for submission instructions.

YO. This is Colby and this is my mini project for PPL. I created a little game about being a bee, fighitng bears, and gathering honey.

Download/Play Instructions:
To play, clone repo and run barryBee.exe. The exe was created with Pyinstaller and should work on computers without Python installed. Note: I haven't tested this on mac, feel free to give it a shot. Alternatively, if you have Python 3.10+ and PyGame installed (I have version 2.1.2) you could try to run the source code by opening a terminal, changing directory to the cloned repo, and runing 'python main.py'. Main, as one might expect, is the main driver file that runs everything. Alternatively alternatively, there is a playable web build on my itchio page (at bottom of readme). The web build was created using Pygbag which does some kind of wizardy behind the scenes to make Python and Pygame (as well as the base Python modules) playable on browser. The only small caveat is that performance takes a pretty large hit. The game is definitely worse playing at 1/5 the framerate but its still playable which is cool.

Lore:
It is the last day before the big hibernation. This means that all the forest's bears have gathered to fight for the right to hibernate with the most precious treasure on Earth... honey. You are a bee, and your goal is to win the honey (your honey) and bring it back the hive. 

Gameplay:
As the bee you have two main modes, grounded and flying. While on the ground you walk back and forth, bouncing off of walls and turning pollen into honey using your PolliNator. If you press space while grounded, you will turn direction. If you hold space while grounded, you will take of using the jetpack functionality of your PolliNator, becoming airborn. While flying, you can hold space to spend honey and accelerate updward. If you double tap space with at least one honey left, you will shoot all of your honey straight up in the air to cancel your horizontal momentum and launch yourself quickly to the ground. If you hit the ground while airborn, you become grounded again. 

Your goal is to use your ground and air movement to dodge incoming attacks from your bear opponent. Before every attack, the bear will do a short 'anticipation' movement to give you time to dodge. Bee's communicate through bodily movement and dance, maybe you can read your opponent's 'anticipation' dances... After a certain amount of time (marked by the bee at the top of the screen's progress across the grass), you will wear the bear out, causing it to become vulnerable. When the bear is vulnerable, a part (or parts) of its body will change to a pink color when it is in a state (or states). To defeat the bear, you must fly up to the body part and tap space while touching it. This will give the bear a good sting, incapacitating it and leaving you the victor. BE CAREFUL, just as one good still will incapacitate the bear, one good bear attack will incapacitate you. Be ready to move!

Menus:
To navigate menus, tap space to select the option you would like. Hold space to continue/use selected option. I.e. hold space to go past title menu.

This is very much a beta version of the game. Boss fight system is mostly there (needs particles and polish) but I definitely want to add more bosses and a sense of progression. 

- YouTube: https://youtu.be/TODO.
- Script: script.pdf
- Recording: recording.mp4
- Slides slides.pdf

https://birdboys.itch.io #MY ITCHIO PAGE
https://birdboys.itch.io/barry-bee #BARRY BEE HIDDEN PAGE: PASSWORD = barrybee