import pygame
import projectiles


def check_beam_enemy_collisions(player, enemies, damage=1):
    current_time = pygame.time.get_ticks()

    # Add a cooldown for beam damage
    if not hasattr(player, "beam_damage_cooldown"):
        player.beam_damage_cooldown = 0  # Initialize cooldown

    if current_time > player.beam_damage_cooldown:
        # Define the shortened beam's collision area
        beam_length = 300  # Set the visual and damage beam length
        beam_rect = pygame.Rect(
            player.x + player.width // 2 - 5,  # Beam's x position (centered on the player)
            player.y - beam_length,           # Start y position of the beam
            10,                               # Beam's width
            beam_length                       # Beam's height
        )

        for enemy in enemies:
            if enemy.rect.colliderect(beam_rect):  # Check collision within the beam's range
                enemy.decrease_health(damage=damage)
                print(f"[DEBUG] Beam hit enemy at {enemy.rect.topleft}, damage: {damage}")

        # Set the cooldown to apply damage every 200ms
        player.beam_damage_cooldown = current_time + 200




def check_projectile_enemy_collisions(projectiles, enemies, damage=1):
    collisions = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    for hit_projectile, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.decrease_health(damage=damage)  # Apply specified damage
            print(f"Projectile hit enemy at {enemy.rect.topleft}, damage: {damage}")
            
def check_projectile_boss_collisions(projectiles, enemies): # For boss only
    for projectile in projectiles:
        for enemy in enemies:
            if enemy.central_rect.colliderect(projectile.rect):
                enemy.decrease_health(damage=projectile.damage)
                projectile.kill()
                print(f"Boss health: {enemy.health}")
            elif enemy.left_wing_rect.colliderect(projectile.rect):
                enemy.decrease_health(damage=projectile.damage)
                projectile.kill()
                print(f"Boss health: {enemy.health}")
            elif enemy.right_wing_rect.colliderect(projectile.rect):
                enemy.decrease_health(damage=projectile.damage)
                projectile.kill()
                print(f"Boss health: {enemy.health}")

def check_player_projectile_collisions(player, enemy_projectiles, damage, curr_time):
    """
    Check if the player collides with any enemy projectiles.
    Decreases player health upon collision and removes the projectile.
    """
    collided_projectiles = pygame.sprite.spritecollide(player, enemy_projectiles, True)
    for projectile in collided_projectiles:
        player.last_enemy_collision = curr_time
        player.got_hit = True
        player.take_dmg(damage)  # Adjust to match the method in CharacterPawn
        print(f"Player hit by projectile at {projectile.rect.topleft}, damage: {damage}")
        if(curr_time - player.last_enemy_collision >= 1):
            player.got_hit = False

def check_player_object_collisions(player, objects):
    collided_objects = pygame.sprite.spritecollide(player, objects, False)
    for obj in collided_objects:
        handle_player_object_collision(player, obj)

def handle_player_object_collision(player, obj):
    print(f"Player collided with object at {obj.rect.x}, {obj.rect.y}")

def check_player_enemy_physical_collision(player, enemy, curr_time):
    if player.is_alive and player.rect.colliderect(enemy.rect) and curr_time - player.last_enemy_collision >= 1:
        player.last_enemy_collision = curr_time
        player.got_hit = True
        player.take_dmg(10)
        if not player.is_alive:
            print("Player defeated!")
    elif(curr_time - player.last_enemy_collision >= 1):
        player.got_hit = False

def check_player_consumable_collisions(player, consumables_group):
    """
    Check if the player collides with any consumables.
    Consumes the item and applies its effect.
    """
    collided_consumables = pygame.sprite.spritecollide(player, consumables_group, True)
    for consumable in collided_consumables:
        player.consume(consumable.consumable_type)
        print(f"Player consumed: {consumable.consumable_type}")



