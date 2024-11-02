# will be used to spawn in enemies
import pygame
import random
from characters.enemies.enemy_type_a import EnemyTypeA
from characters.enemies.enemy_type_b import EnemyTypeB

# spawns an enemy out of sight
def spawnEnemy(enemy_list, current_time, enemy_type = 0):
    # Spawn in correct type of enemy
    if (enemy_type == 0):
        # Enemy moves back and forth and fires one pellet
        new_ship_x = random.randint(50, 750)
        new_ship_y = random.randint(30, 200)
        ship_path_distance = random.randint(100, 200)
        right_bound = new_ship_x + ship_path_distance
        left_bound = new_ship_x - ship_path_distance
        if(left_bound  < 30):
            left_bound = 30
        if(right_bound > 770):
            right_bound = 770
        enemy_list.add(EnemyTypeA(new_ship_x, new_ship_y, left_bound, right_bound, current_time))
    elif (enemy_type == 1):
        # Enemy arcs and fires spread pattern
        new_ship_x = 400
        new_ship_y = 50   
        ship_path_distance = 200
        right_bound = new_ship_x + ship_path_distance
        left_bound = new_ship_x - ship_path_distance
        enemy_list.add(EnemyTypeB(new_ship_x, new_ship_y, left_bound, right_bound, current_time))

# this is meant more for enemy type b, but will use type a for now
def startRetreat(enemy, list_of_retreating):
    enemy.heading_home = True
    list_of_retreating.add(enemy)

# this is meant more for enemy type b, but will use type a for now
def despawnEnemy(retreating):
    for enemy in retreating:
        #enemy.heading_home = True
        if(enemy.pos_y <= -30):
            enemy.kill()

# destroys an enemy            
def destroyEnemy(destEnemies, enemy, destroySound):
    destEnemies.append((enemy.rect.center, pygame.time.get_ticks(), enemy.size))
    enemy.kill()
    destroySound.play()