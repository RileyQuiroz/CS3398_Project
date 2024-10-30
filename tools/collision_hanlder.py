import pygame

def check_projectile_enemy_collisions(projectiles, enemies):
    """
    Check for collisions between projectiles and enemies using Pygame's built-in sprite collision.
    Removes the projectile upon collision and decreases enemy health.
    """
    # Use groupcollide to detect collisions between projectiles and enemies
    collisions = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    
    for hit_projectile, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.decrease_health(damage=1)

def check_player_object_collisions(player, objects):
    """
    Check for collisions between the player and objects using Pygame's built-in sprite collision.
    Handles the response to the collision in a separate function.
    """
    # Use spritecollide to check if the player collides with any object
    collided_objects = pygame.sprite.spritecollide(player, objects, False)
    
    for obj in collided_objects:
        handle_player_object_collision(player, obj)

def handle_player_object_collision(player, obj):
    """
    Handle what happens when the player collides with an object.
    You can customize this to stop movement, trigger events, etc.
    """
    print(f"Player collided with object at {obj.rect.x}, {obj.rect.y}")
    # Example: Stop player movement or trigger an event
    # player.stop_movement() or any other logic you want
    
def check_projectile_player_collisions(projectile, player):
    '''
    Check for collisions between enemy projectiles and the player using Pygame's built-in sprite collision.
    Removes the projectile upon collision and decreases enemy health.
    '''
    print("imagine getting hit")
    collisions = pygame.sprite.groupcollide(projectile, player, True, False)
    
    for hit_projectile, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.decrease_health(damage=1)
