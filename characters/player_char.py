import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from projectiles.projectiles import Projectile
import assets
import random

# Centralized consumable data
CONSUMABLE_DATA = {
    "shield_pack": {
        "image": "assets/objects/Item_Shield3.png",
        "width": 35,
        "height": 35
    },
    "repair_kit": {
        "image": "assets/objects/Item_repair_kit2.png",
        "width": 35,
        "height": 35
    },
    "auto_turret": {
        "image": "assets/objects/weapon_auto_turret.png",
        "width": 37,
        "height": 37
    },
    "rocket_launcher": {
        "image": "assets/objects/weapon_rocket_launcher2.png",
        "width": 38,
        "height": 38
    },
    "super_weapon":{
        "image": "assets/objects/weapon_super_weapon.png",
        "width": 38,
        "height": 38
    }
}

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
        self.shot_cooldown = 200  # in milliseconds
        self.last_enemy_collision = 0
        self.got_hit = False
        self.shield = 0
        # weapon
        self.player_weapon = 0 # For use with save system, modify to your needs
        # self.player_model = 0 # For use with save system, modify to your needs
        # weapon list
        #self.weapon_list=[("auto_turrent",10, 200, (0,255,0)), 
        #                   ("rocket_launcher", 25, 500, (255, 0, 0))]
        self.current_weapon = 0
        # self.last_shot_time = 0

        # SUPER WEAPON
        self.is_using_sw = False
        self.sw_start_time = 0
        self.sw_durration = 2000
        self.sw_cooldown = 5000
        self.last_sw_time = 0

    # Weapon system
    def swap_weapon(self):
        self.current_weapon = 1

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
                    "speed": 12,
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
                },
                "rocket_launcher":{
                    "speed": 5,
                    "color":(255,0,0),
                    "size": (5, 20),
                    "sound": "assets/sound_efx/rocket_launcher2.mp3",
                    "cooldown": 500
                },
                "super_weapon":{
                    "speed": 1,
                    "color":(255,0,0),
                    "size": (10, 20),
                    "sound": "assets/sound_efx/super_weapon.mp3",
                    "cooldown": 500
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
                self.shield = min(100, self.shield + 100)
                shield_audio = pygame.mixer.Sound("assets/sound_efx/shield_pick_up.mp3")
                shield_audio.play()
                shield_audio.set_volume(0.13)
            else:
                print("Shields are at full capacity!")
        elif consumable in CONSUMABLE_DATA:
            self.player_weapon = consumable
            print(f"Picked up {consumable}!")

class Consumable(pygame.sprite.Sprite):
    def __init__(self, x, y, consumable_type):
        super().__init__()
        self.consumable_type = consumable_type

        if consumable_type in CONSUMABLE_DATA:
            data = CONSUMABLE_DATA[consumable_type]
            self.image = pygame.image.load(data["image"]).convert_alpha()
            self.image = pygame.transform.scale(self.image, (data["width"], data["height"]))
        else:
            raise ValueError(f"Unknown consumable type: {consumable_type}")

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def spawn_consumable(consumables_group, screen_width, screen_height):
    consumable_type = random.choice(list(CONSUMABLE_DATA.keys()))
    x = random.randint(0, screen_width - 35)
    y = random.randint(0, screen_height - 35)
    consumable = Consumable(x, y, consumable_type)
    consumables_group.add(consumable)
     
    
