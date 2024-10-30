# will be used to spawn in enemies
import pygame
import random
from characters.enemies.enemy_type_a import EnemyTypeA

def spawnEnemy(enemy_list, current_time):
    new_ship_x = random.randint(50, 750)
    new_ship_y = random.randint(30, 200)
    ship_path_distance = random.randint(100, 200)
    left_bound = new_ship_x - ship_path_distance
    right_bound = new_ship_x + ship_path_distance
    # Make sure ship stays within screen borders
    if(left_bound  < 30):
        left_bound = 30
    if(right_bound > 770):
        right_bound = 770
    enemy_list.add(EnemyTypeA(new_ship_x, new_ship_y, left_bound, right_bound, current_time))

def startRetreat(enemy, list_of_retreating):
    enemy.heading_home = True
    list_of_retreating.add(enemy)

# this is meant more for enemy type b, but will use type a for now
def despawnEnemy(retreating):
    for enemy in retreating:
        enemy.heading_home = True
        if(enemy.pos_y <= -30):
            enemy.kill()
