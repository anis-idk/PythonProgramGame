Zombie Shooter Game

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/anis-idk/Zombie-Shooter-Game

## Identification
- **Name: Anis Sahnoune** 
- **P-number: P475508** 
- **Course code: IY499** 

## Declaration of Own Work
I confirm that this assignment is my own work.
Where I have referred to academic sources, I have provided in-text citations and included the sources in the final 
reference list.

## Introduction
This code shows how to use the Pygame package to create a basic zombie shooter game. The soldier in the game has to 
shoot zombies that sporadically pop up from the screen's corners. With the keyboard keys, the player may fire and move 
the soldier. A leaderboard, a login page, and standard gameplay elements like score, sound effects, and health are all 
included in the game.

## Installation
To play the **Zombie Shooter Game**, install the required dependencies and launch the game by following these steps:
- Before running the game make sure you have the following installed :

1) Python : the game is coded in python so please ensure that you have python installed on your computer , you can 
download the latest version of python from : https://www.python.org/downloads/ , you can check if python is installed by 
typing this command in the terminal or command prompt: `python —version`
 
2) Clone The Repository : start by cloning the repository to your local disk using the following command in CMD
`git clone https://github.com/anis-idk/Zombie-Shooter-Game.git`

> [!TIP]
> You can also download the repository as a ZIP file and extract it to a folder of your choice

3) Navigate to the project Directory : `cd Zombie-Shooter-Game`

> [!NOTE]
> Set up a virtual Environment is optional but recommended to use to keep the dependencies isolated

4) Install all the necessary dependencies and libraries by running : `pip install -r requirements.txt`




## How to Play
- Use W, A, S, and D keys to move the soldier.
- Use the mouse or the touchpad to aim .
- Use the spacebar to shoot .
- Navigate through the menu using your mouse to select options.

### Running the Game
Once the installation is done start the game by running : `python PythonProject.py`


### Running Unit Tests

The user experience and game functionality are the primary focus of this project, rather than automated testing.

## Game Elements
- Soldier: The player's character, which can shoot bullets to eliminate zombies.
- Zombies: Enemies that spawn from the edges of the screen and move toward the player.
- Bullets: Weapons to eliminate zombies; their usage is limited by cooldown times.
- Leaderboard: Displays the top scores of players based on their performance. 
- Menu: Displays the main menu with play , leaderboard and quit buttons 
- Game Over screen: Displays the game over screen with the try again button and main menu button
- Login Screen : Displays the login screen which let the user enter its username 

## Libraries Used
The following libraries are used in this project:
- **Pygame**: To handle game rendering, audio, and animations.
- **JSON**: To save and load the leaderboard data.
- **random**: Enables randomness, such as zombie random spawn locations.
- **math**: Offers mathematical operations such as trigonometry and angle computations.
- **os**: controls the file paths for resources, such as pictures and audio.


## Project Structure
- assets : Contains game assets like images and sounds.
- PythonProject.py: The main entry point for the game.
- leaderboard.json: Stores player scores and usernames.
- requirements.txt: A list of Python dependencies.
- README.md: Project documentation, such as installation guidelines and game details.

## Unit Tests (optional)
The project does not include unit tests , This project is more concerned with the user experience and game functioning 
than with automated testing.
