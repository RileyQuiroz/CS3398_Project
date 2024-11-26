from menu.main_menu import main_menu
from gamestates.Game import Game

def run_game():
    game = Game()

    game.states[game.current_state].enter(game)

    while True:
        game.update()
        game.draw()

# Call the main menu function
if __name__ == "__main__":
    main_menu()
    #run_game()

##comments,