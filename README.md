# **Darkest Castle - Game Design Document**

The repository contains a prototype implementation of a game in Pygame, which was implemented as a final project for the Object Technologies course. 

**Author**: Denys Klinkov

**Chosen theme**: Dark and light

---
## **1. Introduction**
The proposed game serves as a demonstration for the subject Object Technologies, with the aim of creating a functional prototype of the game as a project for the exam. The created game meets the requirements of the assigned topic (Dark and light). The game world is pure darkness with only one source of light which player should save until end of the game, avoiding different obstacles on his way.

### **1.1 Inspiration**
<ins>**Flappy Bird**</ins>

Flappy Bird is a side-scroller where the player controls a bird, attempting to fly between columns of green pipes without hitting them. The game became famous because of it's absurd difficulty. The bird moves persistently to the right and if it collides with anything on the screen, the gameplay will end. This game is endless, but you can try to improve your best result by collecting more points.
<p align="center">
  <img src="https://github.com/DenBlade/DarkestCastle/blob/main/readme_files/flappybird.jpg" alt="Flappy Bird">
  <br>
  <em>Figure 1 Preview of Flappy Bird</em>
</p>

<ins>**Geometry Dash**</ins>

Geometry Dash is a side-scrolling music platforming game. The player is controlled by pressing or holding inputs to navigate through auto-scrolling levels until the end is reached. The level restarts from the beginning if the player collides with an obstacle, such as a spike or wall. It causes serious difficulty, which is why this game so popular.

<p align="center">
  <img src="https://github.com/DenBlade/DarkestCastle/blob/main/readme_files/geometry_dash.png" alt="Geometry Dash">
  <br>
  <em>Figure 2 Preview of Geometry Dash</em>
</p>

### **1.2 Player Experience**
The goal of the game is for the player to reach the end of the level, avoiding all the obstacles in a pure darkness. Key words that describe player experience are `fear` and `unknown`. You will never know if there are obstacles around if don't get to close to them.

### **1.3 Development Software**
- **Pygame-CE**: chosen programming language.
- **PyCharm 2024.1**: chosen IDE.
- **Tiled 1.10.2**: graphical tool for creating levels.
- **Itch.io**: source of graphic assets and sounds for the game.
- **Fresound.org**: source of sounds for the game

---
## **2. Concept**

### **2.1 Gameplay Overview**
The player controls light source with a mouse(drag and drop system) and tries to survive until the end of the level. As soon as game started the camera will start moving to the right, forcing player to go forward(if light source get out of the camera scope, the game will end up). Main difficulty will create walls(will push light source out of screen) and spikes(will kill player immediately).

### **2.2 Theme Interpretation (Dark and light)**
**"Dark and light"** - all level is dark, you cannot see anything, neither background nor walls nor spikes. The only object you will see on screen is a light source which will give you ability to see other objects in a small range around it.

### **2.3 Primary Mechanics**
- **Obstacles**: there are objects on the map that create an active obstacle for the player.
- **Increasing speed**: the speed will increase the farther you go from starting position, making game difficulty increase over time.
- **Player movement**: player moves the light source by dragging it with mouse. Light source have it's own speed and momentum parameters, which will make the game harder.

### **2.4 Class design**
- **Game**: class that will contain the main game logic (start screen, game loop, game ending, ...).
- **Player**: class representing the player, player control, character rendering.
- **Ui**: class created specifically for user interface, contain buttons, progressbar.
---
## **3. Art**

### **3.1 Theme Interpretation (Dark and light)**
Since all the game based on light and darkness, a decision was made to use pygame blend modes. On top of the game surface was placed another filled with black color surface with blend_mult mode. This mode will darken all dark pixels. By creating pixels with different colors we can achieve smooth darkness effect. The light "bulb" was generated similiarlly, by drawing circles with different colors with blend_add mode which will lighten all the light pixels.

### **3.2 Design**
The game map uses assets from itch.io, specifically Generic DUNGEON Pack (https://bakudas.itch.io/generic-dungeon-pack), with some objects serving as active obstacles. The goal was to achieve a feeling of dark scary castle, being in which is not safe.   

<p align="center">
  <img src="https://github.com/DenBlade/DarkestCastle/blob/main/readme_files/level_example.jpg" alt="Level design">
  <br>
  <em>Figure 3 Level design example without darkness effect</em>
</p>

---
---
## **4. Audio**

### **4.1 Music**
The selection of main menu background music was focused on creating feelings of something mysterious and unknow. The music was taken from "Fears(Horror Music)" (https://devtrap.itch.io/fears). The level music aims the same, but also is more upbeat. (https://dos88.itch.io/dos-88-music-library).

### **4.2 Sound Efects**
The sounds make the game much better. Without them game just don't feels right. Game sounds were added for start of level, end of level, defeat and for thunder in main menu. All the sounds for the game were selected from **FreeSound.org** (https://freesound.org/).

---
## **5. Game Experience**

### **5.1 UI**
The user interface will be oriented towards the overall graphic style and the start screen will include the option to watch tutorial, start and exit the game. 

### **5.2 Controls**

<ins>**Mouse**</ins> 
- **Left button(hold)**: move a light source.
