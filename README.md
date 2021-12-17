# FruitNinja
Fruit Ninja is a classic and famous screen-touch game which caught people's love over several years. 
Inspired by this fascinating game, we want to develop a motion controlled fruit ninja game.
Players can hold a "sword" in their hands and use it to "cut" the fruits in front of camera to get scores.

The project consists of two main components: the Fruit Ninja game and the motion detection system.
The game is developed in pygame. Similar with Fruit Ninja, players need to cut fruits to get scores and avoid bomb to survive. In addition, players can choose either easy mode or hard mode to play.
Player can choose to play the game on the piTFT touch-screen or use motion control.
The motion detection system is based on OpenCV. With pictures captured by Picamera, the motion detection algorithm will find the contour of red object in a frame, calculate the area of red object, find the biggest red object, and calcuate the center. 
Player use a red "sword" and the algorithm continuously tracks the center of red "sword" to track the motion of players.

For more details and information, please see my respository named "FruitNinjaWeb", which is a web using HTML5/CSS to introduce this project.
