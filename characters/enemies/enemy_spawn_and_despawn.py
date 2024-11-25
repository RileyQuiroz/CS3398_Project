# will be used to spawn in enemies
import pygame
import random
from characters.enemies.enemy_type_a import EnemyTypeA
from characters.enemies.enemy_type_b import EnemyTypeB
from characters.enemies.enemy_type_c import EnemyTypeC
from characters.enemies.boss_enemy import Boss


def spawnBoss(enemy_list, current_time, difficulty):
    enemy_list.add(Boss(400,80,current_time, difficulty))

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
    isBoss = 0
    if(enemy.size == 100):
        isBoss = 1
    destEnemies.append((enemy.rect.center, pygame.time.get_ticks(), enemy.size, isBoss))
    enemy.kill()
    destroySound.play()

def drawEnemyDestruction(dest_enemies, screen, ship_destroyed_sound, score_system):
    for enemy_center, time_destroyed, size, isBoss in dest_enemies[:]:
        explosion_durration = pygame.time.get_ticks() - time_destroyed
        # Boss destruction sequence
        if isBoss == 1 and explosion_durration <= 3750:
            # Draw destroyed boss
            if explosion_durration <= 3600:
                center_size = 75
                wing_size_x = 75
                wing_size_y = 20
                boss_color = (255, 140, 70)
                square_rect = pygame.Rect(enemy_center[0] - center_size // 2, enemy_center[1] - center_size // 2, center_size, center_size)
                pygame.draw.rect(screen, boss_color, square_rect)
                left_rect = pygame.Rect(enemy_center[0] - center_size // 2 - wing_size_x, enemy_center[1] - wing_size_y // 2, wing_size_x, wing_size_y)
                pygame.draw.rect(screen, boss_color, left_rect)
                right_rect = pygame.Rect(enemy_center[0] + center_size // 2, enemy_center[1] - wing_size_y // 2, wing_size_x, wing_size_y)
                pygame.draw.rect(screen, boss_color, right_rect)
            # Boss explosions
            if explosion_durration <= 1200:
                wing_center = (enemy_center[0] + 75, enemy_center[1])
                pygame.draw.circle(screen, (200, 180, 0), wing_center, size/2)
                if explosion_durration == 0:
                    ship_destroyed_sound.play()
            elif explosion_durration <= 2400:
                wing_center = (enemy_center[0] - 75, enemy_center[1])
                pygame.draw.circle(screen, (200, 180, 0), wing_center, size/2)
                if explosion_durration <= 1216:
                    ship_destroyed_sound.play()
            elif explosion_durration <= 3600:
                pygame.draw.circle(screen, (200, 180, 0), enemy_center, size*1.3)
                if explosion_durration <= 2417:
                    ship_destroyed_sound.play()
        elif isBoss != 1 and explosion_durration <= 250:
            pygame.draw.circle(screen, (200, 180, 0), enemy_center, size)
        else:
            if(isBoss == 1):
                score_system.increase(990) # Get more points for destroying boss
            dest_enemies.remove((enemy_center, time_destroyed, size, isBoss))

# Spawn logic for levels    
def levelSpawner(currTime, isStopped, enemy_group, max_enemies, lastSpawn, lastSpecialSpawn, currLevel, lvlThreeSwitch, difficulty):
    if(currLevel == 0): # Level 1
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4:
            spawnEnemy(enemy_group, currTime, 0)
            lastSpawn = currTime
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpecialSpawn >= 10 and difficulty == 2: # only spawns on hard
            spawnEnemy(enemy_group, currTime, 1)
            lastSpecialSpawn = currTime
    if(currLevel == 1): # Level 2
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4 and lastSpawn <= lastSpecialSpawn:
            spawnEnemy(enemy_group, currTime, 0)
            lastSpawn = currTime
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpecialSpawn >= 7:
            spawnEnemy(enemy_group, currTime, 1)
            lastSpecialSpawn = currTime
        if not isStopped and currTime >= 20 and currTime <=20.01 and difficulty == 2: # only spawns on hard
            spawnEnemy(enemy_group, currTime, 2)
            lastSpecialSpawn = currTime
    if(currLevel == 2): # Level 3
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpawn >= 4 and lastSpawn <= lastSpecialSpawn:
            spawnEnemy(enemy_group, currTime, 0)
            lastSpawn = currTime
        if not isStopped and len(enemy_group) < max_enemies and currTime - lastSpecialSpawn >= 6:
            if (difficulty == 2): # only spawns on hard
                spawnEnemy(enemy_group, currTime, 2)
                lastSpawn = currTime
            if (lvlThreeSwitch == 0):
                spawnEnemy(enemy_group, currTime, 2)
                lvlThreeSwitch = 1
            else:
                spawnEnemy(enemy_group, currTime, 1)
                lvlThreeSwitch = 0
            lastSpecialSpawn = currTime
    return lastSpawn, lastSpecialSpawn, lvlThreeSwitch

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