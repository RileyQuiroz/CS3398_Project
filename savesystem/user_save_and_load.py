import pygame
import json
import os


save_state = {
    # Temporary variable names, will change and add more according to other files
    # Saved values will also be changed to reflect in-game values once those parts of code are finished
    # only score and finish time actually change as of now
    "player_health": 3,
    "current_level": 0,
    "current_weapon": 0,
    "ship_color": 0,
    "score": 0,
    "finish_time": 0
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

# Update save_state's total time
def updateTime(currTime):
    save_state["finish_time"] = currTime

# Will call all update functions to update save_state, currently just score and time, returns the message
# to be printed to the screen as well as the begining of its countdown before text disappears
def saveHandling(newScore, newTime):
    updateScore(newScore)
    updateTime(newTime)
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
        return message, start_time, save_state["score"], save_state["finish_time"]
    else:
        message = 'No save data found'
        return message, start_time, currScore, currTime
