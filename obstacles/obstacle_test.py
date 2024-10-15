from Obstacle import *

def display_position(obst):
    print("Position: ( X:", obst.position[0], "Y:", obst.position[1], ")")

def display_collision_status(obst):
    if obst.is_colliding:
        print("Player is colliding with the obstacle!")
    else:
        print("No collision detected!")

# Initialize the in-game obstacle and player position
test_obstacle = Obstacle(5, (2, 1), (255, 255, 255))
player = Obstacle(7, (2, 2), (200, 200, 255))

# Output the obstacle's current coordinates
display_position(test_obstacle)

# Output the obstacle's current collision status
display_collision_status(test_obstacle)

# Set movement velocity for the obstacle
test_obstacle.velocity = (1, 1)

# Update the obstacle using a dummy value for delta time
test_obstacle.update(player, 0.01)

# Output the obstacle's new coordinates and collision status
display_position(test_obstacle)
display_collision_status(test_obstacle)
