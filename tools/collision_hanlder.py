import pygame

def check_projectile_enemy_collisions(projectiles, enemies, damage=1):
    collisions = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    for hit_projectile, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.decrease_health(damage=damage)  # Apply specified damage
            print(f"Projectile hit enemy at {enemy.rect.topleft}, damage: {damage}")

def check_player_projectile_collisions(player, enemy_projectiles, damage=10):
    """
    Check if the player collides with any enemy projectiles.
    Decreases player health upon collision and removes the projectile.
    """
    collided_projectiles = pygame.sprite.spritecollide(player, enemy_projectiles, True)
    for projectile in collided_projectiles:
        player.take_dmg(damage)  # Adjust to match the method in CharacterPawn
        print(f"Player hit by projectile at {projectile.rect.topleft}, damage: {damage}")

def check_player_object_collisions(player, objects):
    collided_objects = pygame.sprite.spritecollide(player, objects, False)
    for obj in collided_objects:
        handle_player_object_collision(player, obj)

def handle_player_object_collision(player, obj):
    print(f"Player collided with object at {obj.rect.x}, {obj.rect.y}")

def check_player_enemy_physical_collision(player, enemy):
    if player.is_alive and player.rect.colliderect(enemy.rect):
        player.take_dmg(10)
        if not player.is_alive:
            print("Player defeated!")