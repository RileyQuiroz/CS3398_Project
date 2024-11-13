import pygame
import json
import os


save_state = {
    # only score and total time actually change as of now
    "player_health": 100,
    "score": 0,
    "weapon_type": 0,
    "current_level": 0,
    "difficulty": 0,
    "shield_active": False,
    "player_model": 0,
}

def save_game(state, filename):
    # Will write all variables in save_state to a json file to be accessed later
    file_path = os.path.join('savesystem/savedata', filename)
    with open(file_path, 'w') as save_file:
        json.dump(state, save_file)
    print("Save success")
    return pygame.time.get_ticks()

def load_game(filename):
    # Attempt to load the desired save file
    file_path = os.path.join('savesystem/savedata', filename)
    if os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as load_file:
            game_state = json.load(load_file)
        print("Load success")
        return game_state, pygame.time.get_ticks()
    print("No savedata")
    return None, pygame.time.get_ticks()

# Update save_state's score
def updateScore(currScore):
    save_state["score"] = currScore
    
def updatePlayer(player):
    save_state["player_health"] = player.health
    save_state["weapon_type"] = 1 # Will be player weapon variable
    save_state["player_model"] = 1 # Will be player weapon variable
    save_state["shield_active"] = 1 # Will be player weapon variable
    
def updateLevel(level):
    save_state["current_level"] = level # Will be variable

def updateDifficulty(currDiff):
    save_state["difficulty"] = currDiff

# Will call all update functions to update save_state, currently just score and time, returns the message
# to be printed to the screen as well as the begining of its countdown before text disappears
# variables that do not exist yet will be default 1 for testing functionality
def saveHandling(newScore, player, currLevel, currDiff):
    updateScore(newScore)
    updateLevel(currLevel)
    updateDifficulty(currDiff)
    updatePlayer(player)
    start_time = save_game(save_state, 'save_data_one.json')
    return 'Game Saved', start_time

# Will load the data from the JSON file and put it in the save_state, then it returns the message
# to be printed to the screen as well as the begining of its countdown before text disappears and 
# the values of save_state, currently just score and time. takes arguments in event of load failure
def loadHandling(currScore, currTime):
    loaded_game, start_time = load_game('save_data_one.json')
    if loaded_game: #only completes the load if it was successful
        save_state = loaded_game
        message = 'Save loaded'
        return message, start_time, save_state["score"], 0 # Load puts you at beginning of last level
    else:
        message = 'No save data found'
        return message, start_time, currScore, currTime
