# will be used to spawn in enemies
import pygame
import random
from characters.enemies.enemy_type_a import EnemyTypeA
from characters.enemies.enemy_type_b import EnemyTypeB
from characters.enemies.enemy_type_c import EnemyTypeC

# spawns an enemy out of sight
def spawnEnemy(enemy_list, current_time, enemy_type = 0):
    # Spawn in correct type of enemy
    if (enemy_type == 0):
        # Enemy type A
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
        # Enemy type B
        new_ship_x = 400
        new_ship_y = 50   
        ship_path_distance = 200
        right_bound = new_ship_x + ship_path_distance
        left_bound = new_ship_x - ship_path_distance
        enemy_list.add(EnemyTypeB(new_ship_x, new_ship_y, left_bound, right_bound, current_time))
    elif (enemy_type == 2):
        # Enemy type C
        new_ship_x = random.randint(100, 700)
        new_ship_y = random.randint(50, 150)
        ship_path_distance = random.randint(100, 200)
        right_bound = new_ship_x + ship_path_distance
        left_bound = new_ship_x - ship_path_distance
        if(left_bound  < 30):
            left_bound = 30
        if(right_bound > 770):
            right_bound = 770
        enemy_list.add(EnemyTypeC(new_ship_x, new_ship_y, left_bound, right_bound, current_time))

def startRetreat(enemy, list_of_retreating):
    if enemy.heading_home == True and enemy not in list_of_retreating:
        list_of_retreating.add(enemy)

def despawnEnemy(retreating):
    for enemy in retreating:
        if(enemy.pos_y <= -30):
            enemy.kill()

# destroys an enemy            
def destroyEnemy(destEnemies, enemy, destroySound):
    destEnemies.append((enemy.rect.center, pygame.time.get_ticks(), enemy.size))
    enemy.kill()
    destroySound.play()

# Spawn logic for levels    
def levelSpawner(currTime, isStopped, enemy_group, max_enemies, lastSpawn, lastWave, currLevel):
    # In progress
    if(currLevel == 0): # Level 1
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4:
            spawnEnemy(enemy_group, currTime, 0)
            lastSpawn = currTime
    if(currLevel == 1): # Level 2
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4:
            spawnEnemy(enemy_group, currTime, 1)
            lastSpawn = currTime
    if(currLevel == 2): # Level 3
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4:
            spawnEnemy(enemy_group, currTime, 2)
            lastSpawn = currTime
    return lastSpawn

# Spawner from sprint 2, kept for version parity     
def oldSpawner(currTime, isStopped, enemy_group, max_enemies, lastSpawn, lastWave):
    if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4:
        spawnEnemy(enemy_group, currTime, 0)
        lastSpawn = currTime
    if not isStopped and currTime - lastWave >= 30: #Spawn wave is not blocked by max enemies, set to 30s for demoing(ideally would be longer)
        spawnEnemy(enemy_group, currTime, 1)
        spawnEnemy(enemy_group, currTime, 0)
        spawnEnemy(enemy_group, currTime, 0)
        lastWave = currTime
    return lastSpawn, lastWave