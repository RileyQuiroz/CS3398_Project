import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from projectiles.projectiles import Projectile
import assets
import random

class CharacterPawn:
    def __init__(self, x, y, projectiles_group, screen_width, screen_height, health=100, shield=100):
        # Initialize character position, movement attributes, and screen dimensions
        self.x = x
        self.y = y
        self.speed = 4.5
        self.width = 20
        self.height = 30
        self.projectiles_group = projectiles_group  # Group for handling projectiles
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Player collision rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Stats
        self.health = health
        self.is_alive = True
        # Cooldown to prevent spamming bullets
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_cooldown = 250  # in milliseconds
        self.last_enemy_collision = 0
        self.got_hit = False
        self.shield = 0
        self.player_weapon = 0 # For use with save system, modify to your needs
        self.player_model = 0 # For use with save system, modify to your needs

    def handle_input(self, stopped):
        # Handle basic movement input
        keys = pygame.key.get_pressed()
        if(stopped == False):
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
            if keys[pygame.K_UP]:
                self.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.y += self.speed

        # Boundary conditions
        self.x = max(0, min(self.screen_width - self.width, self.x))
        self.y = max(0, min(self.screen_height - self.height, self.y))

        # Update the rect position
        self.rect.topleft = (self.x, self.y)

    def shoot(self, stopped):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        # Check if space is held down and the game is not stopped
        if keys[pygame.K_SPACE] and not stopped:
            weapon_info = {
                "auto_turret": {
                    "speed": 20,
                    "color": (0, 255, 255),
                    "size": (5, 15),
                    "sound": "assets/sound_efx/shoot_default.mp3",
                    "cooldown": 100  # Faster cooldown for machine gun effect
                },
                "default": {
                    "speed": 10,
                    "color": (255, 0, 0),
                    "size": (5, 10),
                    "sound": "assets/sound_efx/shoot_default.mp3",
                    "cooldown": 250  # Standard cooldown for single shots
                }
            }

            # Determine the weapon type
            weapon = self.player_weapon if self.player_weapon in weapon_info else "default"
            detail = weapon_info[weapon]

            # Check cooldown for firing
            if current_time - self.last_shot_time > detail["cooldown"]:
                # Create projectile with weapon-specific properties
                bullet = Projectile(
                    self.x + self.width // 2,
                    self.y,
                    speed=detail["speed"],
                    color=detail["color"],
                    size=detail["size"]
                )
                self.projectiles_group.add(bullet)
                self.last_shot_time = current_time

                # Play the weapon-specific sound
                shoot_audio = pygame.mixer.Sound(detail["sound"])
                shoot_audio.play()
                shoot_audio.set_volume(0.2)




    def draw(self, screen, curr_time):
        # Determine color based on health
        color = (255, 255, 0) if self.health < 50 else (0, 255, 0)
        if(self.got_hit):
            color = (255,255,255)
        pygame.draw.rect(screen, color, self.rect)
        # Draw health bar
        self.draw_health_bar(screen)
        self.draw_shield_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        fill = (self.health / 100) * bar_width
        health_bar = pygame.Rect(10, self.screen_height - bar_height - 10, bar_width, bar_height)
        health_fill = pygame.Rect(10, self.screen_height - bar_height - 10, fill, bar_height)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)  # Red background for health bar
        pygame.draw.rect(screen, (0, 255, 0), health_fill)  # Green fill for current health

    def draw_shield_bar(self, screen):
        bar_width = 200
        bar_height = 20
        fill = (self.shield / 100) * bar_width
        # Position shield bar just above the health bar
        shield_bar = pygame.Rect(10, self.screen_height - 2 * bar_height - 20, bar_width, bar_height)
        shield_fill = pygame.Rect(10, self.screen_height - 2 * bar_height - 20, fill, bar_height)

        ##this makes the bar transparent unless there is shield active 
        shield_surface = pygame.Surface((shield_bar.width, shield_bar.height), pygame.SRCALPHA)
        shield_surface.fill((255, 0, 0, 128)) 
        pygame.draw.rect(screen, (0, 253, 255), shield_fill)  # Cyan fill for current shield


    def take_dmg(self, amount):
        if self.shield > 0:
            self.shield -= 25
        else:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_alive = False

    def heal(self, amount):
        if self.is_alive:
            self.health = min(100, self.health + amount)
    
    def consume(self, consumable):
        if consumable == "repair_kit":
            if self.health < 100:  # Only consume if health is not full
                self.health = min(100, self.health + 100)
                repair_audio = pygame.mixer.Sound("assets/sound_efx/repair_kit_pick_up.mp3")
                repair_audio2 = pygame.mixer.Sound("assets/sound_efx/repair_kit_pick_up2.mp3")
                repair_audio.play()
                repair_audio2.play()
                repair_audio.set_volume(0.13)
                repair_audio2.set_volume(0.13)
            else:
                print("Health is already full. Cannot consume repair kit.")
                
        elif consumable == "shield_pack":
            if self.shield < 100:
                # Recharge shield to max but respect shield limit
                self.shield = min(100, self.shield + 100)
                # sound efx for shield_pack
                shield_audio = pygame.mixer.Sound("assets/sound_efx/shield_pick_up.mp3")
                shield_audio.play()
                shield_audio.set_volume(0.13)
            else:
                print("Shields are at full capacity!")

        elif consumable == "weapon":
            self.player_weapon = "auto_turret"
            print("picked up auto turret")

            # here i can add the audio for a weapon pickup, just copy code above and change files and var names


class Consumable(pygame.sprite.Sprite):
    def __init__(self, x, y, consumable_type):
        super().__init__()
        self.x = x
        self.y = y
        self.consumable_type = consumable_type  # this can be "repair_kit" or "shield_pack"
        self.image = pygame.Surface((20,20))
        self.image.fill((0, 255, 255) if consumable_type == "shield_pack" else (255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
    
        # logic for the appearance based on the type of consumbale
        if consumable_type == "shield_pack":
            ##self.image.fill((0,244,244)) ## this can be used for testing
            image = pygame.image.load("assets/objects/Item_Shield3.png").convert_alpha()
            # TO RESIZE THE ASSET CHANGE width and height 
            shield_width = 35
            shield_height = 35
            self.image = pygame.transform.scale(image, (shield_width, shield_height))
        elif consumable_type == "repair_kit":
            ##self.image.fill((255, 255, 0))
            image = pygame.image.load("assets/objects/Item_repair_kit2.png").convert_alpha()
            # TO RESIZE THE ASSET
            repair_kit_width = 35
            repair_kit_height = 35
            self.image = pygame.transform.scale(image,(repair_kit_width, repair_kit_height))
        elif consumable_type == "weapon":
            self.weapon_type = "auto_turret"
            # WEAPON ASSET WILL GO HERE
            # weapon_asset = "assets/objects/weapon_auto_turret.png"
            # image = pygame.image.load(weapon_asset).convert_alpha()

            # RESIZE WEAPON ASSET
            weapon_w = 35
            weapon_h = 35
            #self.image = pygame.transform.scale(image, (weapon_w, weapon_h))
        else:
            raise ValueError("whered you find this???")
        self.rect=self.image.get_rect(topleft=(x,y))

    #this draws the consumables on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def spawn_consumable(consumables_group, screen_width, screen_height):
    consumable_type = random.choice(["repair_kit", "shield_pack", "weapon"])
    # random spot on screen (within bounds)
    x = random.randint(0, screen_width -35)
    y = random.randint(0, screen_height -35)
    #create the consumbale and then add it in the group
    consumable = Consumable(x, y, consumable_type)
    consumables_group.add(consumable)
     
    
