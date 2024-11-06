## Untitled bullethell game
<img src="/images/project_icon.jpeg" alt="Project Icon" width="100" />


## Team Edosians
> Oscar Morones, Riley Quiroz, Joseph Sheraden-Urrutia, Emilio Aldaco
## Description
> We are creating a bullethell-style game using Python and Pygame. The game will feature fast-paced, challenging gameplay where the player must dodge a constant barrage of enemy bullets while aiming to defeat enemies and complete levels.
> The game is designed for gamers who enjoy high-intensity, skill-based gameplay. Our target audience includes fans of the bullethell genre and players who are looking for a challenging and immersive experience.
> We are developing this game to provide an exciting and engaging gaming experience that tests players' reflexes and strategic thinking. We hope to create a game that challenges the player while offering a sense of achievement as they progress through increasingly difficult levels.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Project Status](#project-status)
<!-- * [License](#license) -->


## Technologies Used
- [Jira](https://www.atlassian.com/software/jira): For project management and tracking tasks.
- [Bitbucket](https://bitbucket.org/): For version control and managing the project repository.
- [Pygame](https://www.pygame.org/): A Python library for creating video games, used for handling graphics, input, and game mechanics.
- [Python](https://www.python.org/): The programming language we are using to develop the game.

## Features
These features are in progress

Save System

    Feature Name: Save System
    Description: Allows players to save their progress during gameplay and load it later.
    Who uses it: Players who wish to save and resume their game.
    User Story: "As a player, I want to be able to save my progress so that I can continue where I left off."

Load Game Functionality

    Feature Name: Load Game Functionality
    Description: Enables players to load previously saved game states.
    Who uses it: Players who have saved their game and want to resume.
    User Story: "As a player, I want to load my saved progress to continue the game from where I stopped."

UI for Save/Load System

    Feature Name: Save/Load System UI
    Description: A graphical interface that allows players to interact with the save and load system.
    Who uses it: Players who need a visual interface to save/load their game.
    User Story: "As a player, I want an intuitive UI to save and load my game progress easily."

In-Game Timer

    Feature Name: In-Game Timer
    Description: Tracks the amount of time the player has spent in the game, and can be paused/resumed.
    Who uses it: Players tracking their session times.
    User Story: "As a player, I want a timer so I can track how long I’ve been playing."

Pause and Resume Timer

    Feature Name: Pause/Resume Timer
    Description: Allows players to pause the in-game timer and resume it.
    Who uses it: Players who wish to take breaks without losing track of their playtime.
    User Story: "As a player, I want to pause the in-game timer when I pause the game, so the tracking remains accurate."

Score Counter System

    Feature Name: Score Counter System
    Description: Tracks and displays the player’s score in real-time.
    Who uses it: Players looking to track their performance throughout the game.
    User Story: "As a player, I want to see my score increase in real-time as I play."

Performance History Screen

    Feature Name: Performance History Screen
    Description: Displays the player's past game performance, including previous scores and times.
    Who uses it: Players who want to review their progress and performance history.
    User Story: "As a player, I want to view my performance history to compare my progress over time."

Unit Testing for Save/Load System

    Feature Name: Unit Testing for Save/Load System
    Description: Unit tests to ensure that the save/load system functions correctly.
    Who uses it: Developers who need to validate the save/load functionality.
    User Story: "As a developer, I want automated tests to verify that the save/load system works as expected."

Unit Testing for Timer Functionality

    Feature Name: Unit Testing for Timer
    Description: Unit tests to verify the functionality of the in-game timer.
    Who uses it: Developers ensuring the timer's accuracy.
    User Story: "As a developer, I want to ensure the timer works properly through automated tests."

Unit Testing and Bug Fixes for Score Counter

    Feature Name: Unit Testing and Bug Fixes for Score Counter
    Description: Tests and fixes related to the score counter to ensure real-time updates work correctly.
    Who uses it: Developers ensuring the scoring system works as intended.
    User Story: "As a developer, I want to ensure the score counter works correctly and updates in real-time."


## Project Status
Project is: IN PROGRESS 




<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->

# Sprint 2

## Contributions

Oscar: Created high-level game states that detect if the player has won or lost the game depending on different parameters (player health and score). Also added reset game logic to reset game and re-initialize logic.

* SCRUM-61 Design Win/Lose Conditions System
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-61
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-61-design-win-lose-conditions-systems

* SCRUM-62 Implement Basic Win Condition Logic
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-62
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-62-implement-basic-win-condition-logic

* SCRUM-64 Display Win/Lose Screen Prompts
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-64
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-64-display-win-lose-screen-prompts

* SCRUM-71 Test Win/Lose Conditions & Bug fixes
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-71
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/SCRUM-71-test-win-lose-conditions-bug-fi

* SCRUM-63 Implement Basic Lose Condition Logic
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-63
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-63-implement-basic-lose-condition-
 
Riley: Created two types of enemies and a spawning/deletion system

* SCRUM-72 Create enemy class
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-72
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-72-create-enemy-class

* SCRUM-73 Create enemy type A
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-73
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-73-create-enemy-type-a

* SCRUM-74 Implement enemy spawn functionality
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-74
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-74-implement-enemy-spawn-functiona

* SCRUM-76 Implement enemy despawn functionality
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-76
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-76-implement-enemy-despawn-functio

* SCRUM-85 Fix Enemy Despawning
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-85
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-85-fix-enemy-despawning

* SCRUM-75 Enemy/Player interactions
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-75
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-75-enemy-player-interactions

* SCRUM-77 Create enemy type B
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-77
 - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FSCRUM-77-create-enemy-type-b


Emilio: Created the player pawn containing the ability to move and shoot. Implimented a health mechanic 
        to the player allowing it to be damaged and die upon hit a threshold. Also work on the Collision
        handling allowing object to hit the player and projectiles to damage the player. Animated background 
        was also implimented this sprint.
        
* **SCRUM-66 Implement Basic Player Pawn and Movement**  
  - Jira: [https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-66](https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-66)  
  - BitBucket: [https://bitbucket.org/cs3398-edosians-f24/edosians_/pull-requests/26/commits](https://bitbucket.org/cs3398-edosians-f24/edosians_/pull-requests/26/commits)

* **SCRUM-67 Add Shooting Mechanism**  
  - Jira: [https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-67](https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-67)  
  - BitBucket: [https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/32/commits](https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/32/commits)

* **SCRUM-68 Set Movement Boundaries**  
  - Jira: [https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-68](https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-68)  
  - BitBucket: [https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/36/commits](https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/36/commits)

* **SCRUM-69 Adjust Movement Speed and health bar + player fixes**  
  - Jira: [https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-69](https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-69)  
  - BitBucket: [https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/42/commits](https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/42/commits)

* **SCRUM-70 Collision Detection and Optimization/Testing**  
  - Jira: [https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-70](https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-70)  
  - BitBucket: [https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/38/commits](https://bitbucket.org/%7B0fa85d64-5596-4404-975e-240762e14465%7D/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/pull-requests/38/commits)

* **SCRUM-86 add background to game**  
  - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-86?atlOrigin=eyJpIjoiNmFiMTJmZjdiMGYyNGE4YmJlM2E5NTRiNTYwNjhmYjgiLCJwIjoiaiJ9
  - BitBucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/pull-requests/43/commits



Joseph: Designed and implemented the in-game obstacles that impede the player in various ways. Each obstacle type expands upon a base Obstacle class and even one another in a few cases.

* SCRUM-78 Design and implement basic obstacle class
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-78
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-78-design-and-implement-basic-obstacle-class

* SCRUM-79 Implement obstacles that deal damage to the player
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-79
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-79-implement-obstacles-that-deal-damage-to-the-player
 
* SCRUM-80 Implement obstacles that impede movement
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-80
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-80-implement-obstacles-that-impede-movement

* SCRUM-81 Implement destructible obstacles
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-81
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-81-implement-destructible-obstacles

* SCRUM-82 Implement "friendly" obstacles
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-82
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-82-implement-friendly-obstacles

* SCRUM-83 Design unique visuals for each obstacle type
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-83
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-83-design-unique-visuals-for-each-obstacle-type

* SCRUM-84 Implement obstacle movement
 - Jira: https://cs3398-edosians-fall24.atlassian.net/browse/SCRUM-84
 - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/SCRUM-84-implement-obstacle-movement

## Burnup Report

 ![image](/images/sprint2_burnup.png)

## Next steps:

Oscar: Next, I plan to work on more tasks that improve game flow and the structure of the game. I can look towards creating more game states beyond the current high-level ones. I also want to see and test if my current work that was done in Sprint 2 is completely bug-free and finished. It seemed mostly finished and fixed, but I plan to confirm more in detail. Lastly, I think I would like to plan out future design decisions so we know as a team, going forward, what we are aiming to accomplish and how our tasks should reflect that.

Riley:

- Creating a boss enemy and updating save/load system to work with current variables.

Emilio: For sprint 3 I plan to impliment consumable items for the player like health packs and sheilds. I would also like to have the player able to pick up various weapons
        Another thing I would like to work on is finding assets to replace the current use of shapes.

Joseph: In our next sprint, I will work on our game's state machine and the various game states that it will use. This will allow for greater efficiency and will help to improve the readability of our codebase.





# Sprint 1 

## Contributions 

Riley: Created a save system for the game capable of saving and loading the time and score 

* CP-24-design-the-save-system
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-24 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/CP-24-design-the-save-system
 
* feature/CP-31-implement-save-game-mechanism
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-31 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/feature/CP-31-implement-save-game-mechanism 

* feature/CP-32-implement-load-game-functionality
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-32  
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/feature/CP-32-implement-load-game-functionality  

* feature/CP-33-design-ui-for-save-load-system
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-33  
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/feature/CP-33-design-ui-for-save-load-system  

* feature/CP-35-unit-testing-the-save-load-system
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-35  
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/feature/CP-35-unit-testing-the-save-load-system  

* feature/CP-59-integrate-save-load-with-game-loop
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-59  
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/feature/CP-59-integrate-save-load-with-game-loop  

 

Emilio: Created the main menu feature navigation to each sub menu (start game, records, settings) and the ability to quit the game on selecting “QUIT”. Each option has a “on hover” effect along with sound efx.  

* CP-19 Design the layout and visual style of the main menu
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-19?atlOrigin=eyJpIjoiNDBiNzlkZGQ4YjhiNDA4ZTlmYjQ3YWJiNWFkOWFjYjUiLCJwIjoiaiJ9 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FCP-19-task-1-design-the-layout-and-visua 

* CP-20 Implement Main menu navigation
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-20?atlOrigin=eyJpIjoiNmE2YjM0MDg1YjM1NDRlZTkwYjYzMDI4ZGQyYTg4YzEiLCJwIjoiaiJ9 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/commits/branch/feature%2FCP-20-task-2-implement-main-menu-navigat 

* CP-21 Implement start game, settings and exit functionality
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-21?atlOrigin=eyJpIjoiNTA2MTA5NGViY2ZjNGI4N2EyZDg4OWQ5YjRlNzM5MDgiLCJwIjoiaiJ9 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/branch/feature/CP-21-task-3-implement-start-game-settin 

* CP-22 Unit testing for menu navigation and selection
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-22?atlOrigin=eyJpIjoiYjc1ODllMTAwZjgyNGQyOTg5NzMyNDE1ODgzZjg0OTEiLCJwIjoiaiJ9 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/branch/feature/CP-22-task-4-unit-testing-for-menu-navig 

 

Joseph: Worked on the in-game timer and the leaderboard for storing fastest finishing times among all players. 

* CP-40 Implement Basic In-Game Timer
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-40 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/CP-40-implement-basic-in-game-timer 

* CP-41 Store and Retrieve Game Times
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-41 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/CP-41-store-and-retrieve-game-times 

* CP-42 Create a Performance History Screen
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-42 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/CP-42-create-a-performance-history-screen 

* CP-43 Pause and Resume Timer
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-43 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/CP-43-pause-and-resume-timer 

* CP-44 Write Unit Tests for Timer Functionality
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-44 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/%7B8f57bb94-4a5c-4e61-84ee-0f7ddb6c2c7a%7D/branch/CP-44-write-unit-tests-for-timer-functionality 

 

Oscar: Created a scoring and score display system. Score can increase, decrease, gain combo and is displayed and updated in real time. 

* CP-45 Task 1: Design the Score Counter System
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-45 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/src/ea9053e5c3ca14494978e6e9e1f47fee068c6f9a/?at=feature%2FCP-45-design-the-score-counter-system 

* CP-46 Task 2: Implement Score Calculation Logic
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-46 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/src/f92dbd68686dd13166e05d0211f134344b72653a/?at=feature%2FCP-46-task-2-implement-score-calculation 

* CP-48 Task 3: Display the Score on Screen
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-48 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/src/7c4dc3272653d9d821344cce29d2f867b99a2ca4/?at=feature%2FCP-48-task-3-display-the-score-on-screen 

* CP-49 Task 4: Update the Score in real-time
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-49 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/src/15d773a226c95606f5aa9e6a157b49c6bd43a350/?at=feature%2FCP-49-task-4-update-the-score-in-real-ti 

* CP-50 Task 5: Unit Testing and Bug Fixes
  - Jira: https://cs3398-edosians-f24.atlassian.net/browse/CP-50 
  - Bitbucket: https://bitbucket.org/cs3398-edosians-f24/edosians_/src/fb3fa64bcb57817c32f8bcf1b33a83b5d857bb07/?at=feature%2FCP-50-task-5-unit-testing-and-bug-fixes 

 
## Burnup Report

![image](/images/sprint-1-burnup-report.png)

## Next Steps 

Riley: 

- Implementing basic enemies (1 to 2 types) to gameplay as well as modify save system to take new variables as needed and only save at end of a level once that is finished. 

Emilio: 

- Work on basic game loop implementing basic features using place holder object to simulate the game. Squares shooting circles that move around. 

Joseph: 

- Work on a state machine that separates each game mode into its own logical component for purposes of program efficiency and code readability. 

Oscar: 

- Work on game loop and hopefully be able to properly integrate scoring system with new features that will be added next sprint. 
