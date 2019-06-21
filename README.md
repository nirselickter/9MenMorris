# 9MenMorris
Implement 9 Men Morris to play by two players

Preface
-------------------
This is pilot code for a test between high school in Israel and high school in Germany.
This is part of system engineering department.The final target of the project is make two robots plays together from bothe side of the internet.

The code work quite OK but i did not finished it.
i build some infrastructure for my students and hope that they will continue to develop this game or other
game (e.g checkers ) for the project.

There is WORD file that i document all the developed process.
In the word Example2 means V0.1 ,
example 18 means v0.17


How to use the code
---------------------------
The code was developed in windows with python 3.7

If you download v0.26, you can play with over tcp socket in the same LAN
If you download v0.28, you can play with over MQTT over the internet

to run the server you should write in CMD

"python 9memmorris.py server white"

and to run the client, you should write in CMD

"python 9memmorris.py client black"


what else can be do for this project
------------------------------------
*add security to the communication
*when one side can take coin from other side , he first need to take from non mill position and if there is no such free coin, take it from mill
*there is no check if other side can't move his coins
*maybe more rules of the game not implment
* add some session ID for each two computers that play over the internet. now only two computer can work
* the whole area of mqtt shall be improved








