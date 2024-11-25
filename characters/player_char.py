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
        
        # Initialize weapon to default
        self.player_weapon = "default"  # Ensure the player starts with the default weapon
        self.current_weapon = 0

        # SUPER WEAPON
        self.is_using_sw = False
        self.sw_start_time = 0
        self.sw_durration = 2000
        self.sw_cooldown = 5000
        self.last_sw_time = 0
        self.is_charging = False
        self.charge_start_time = 0
        self.charge_duration = 2000  # 2 seconds to charge (adjust as needed)
        self.laser_charge_sound = pygame.mixer.Sound("assets/sound_efx/charge_up_shot.mp3")
        self.laser_charge_sound.set_volume(0.3)
        self.laser_beam_sound = pygame.mixer.Sound("assets/sound_efx/beam_firing_loop.mp3")
        self.laser_beam_sound.set_volume(0.3)
        self.beam_audio_playing = False  # Ensure this attribute is initialized





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

        if self.player_weapon == "super_weapon" and not stopped:
            if keys[pygame.K_SPACE]:  # Start or maintain the beam
                if not self.is_using_sw and not self.is_charging and current_time - self.last_sw_time > self.sw_cooldown:
                    # Begin charging
                    self.is_charging = True
                    self.charge_start_time = current_time
                    self.laser_charge_sound.play()  # Play the charging sound
                    print("[DEBUG] Laser charging...")

                if self.is_charging:
                    # Check if charging is complete
                    if current_time - self.charge_start_time >= self.charge_duration:
                        self.is_charging = False
                        self.is_using_sw = True  # Activate the beam
                        self.sw_start_time = current_time
                        self.laser_charge_sound.stop()
                        self.is_charging = False  # Stop charging sound
                        print("[DEBUG] Laser beam firing!")

                if self.is_using_sw:
                    # Play the beam firing sound
                    if not hasattr(self, "beam_audio_playing") or not self.beam_audio_playing:
                        print("[DEBUG] Starting beam firing sound")
                        self.laser_beam_sound.play(-1)  # Play in a loop
                        self.beam_audio_playing = True

                    # Draw the beam
                    self.draw_beam(screen=None)  # Replace `None` with the actual screen object if needed

            else:  # Space bar released
                if self.is_using_sw or self.is_charging:
                    self.is_using_sw = False
                    self.is_charging = False
                    self.laser_charge_sound.stop()  # Stop charging sound
                    if hasattr(self, "beam_audio_playing") and self.beam_audio_playing:
                        print("[DEBUG] Stopping beam firing sound")
                        self.laser_beam_sound.stop()  # Stop beam sound
                        self.beam_audio_playing = False
                    print("[DEBUG] Laser beam deactivated.")


        # Logic for other weapons
        if self.player_weapon in ["auto_turret", "rocket_launcher", "default"]:
            weapon_info = {
                "auto_turret": {
                    "speed": 12,
                    "color": (0, 255, 255),
                    "size": (5, 15),
                    "damage": 1,
                    "sound": "assets/sound_efx/shoot_default.mp3",
                    "cooldown": 100  # Faster cooldown for machine gun effect
                },
                "default": {
                    "speed": 10,
                    "color": (255, 0, 0),
                    "size": (5, 10),
                    "damage": 1,
                    "sound": "assets/sound_efx/shoot_default.mp3",
                    "cooldown": 250  # Standard cooldown for single shots
                },
                "rocket_launcher": {
                    "speed": 5,
                    "color": (255, 0, 0),
                    "size": (5, 20),
                    "damage": 5,
                    "sound": "assets/sound_efx/rocket_launcher2.mp3",
                    "cooldown": 500
                }
            }

            detail = weapon_info[self.player_weapon]

            # Check cooldown for firing
            if current_time - self.last_shot_time > detail["cooldown"]:
                # Create projectile with weapon-specific properties
                bullet = Projectile(
                    self.x + self.width // 2,
                    self.y,
                    speed=detail["speed"],
                    color=detail["color"],
                    size=detail["size"],
                    damage=detail["damage"]
                )
                self.projectiles_group.add(bullet)
                self.last_shot_time = current_time

                # Play the weapon-specific sound
                shoot_audio = pygame.mixer.Sound(detail["sound"])
                shoot_audio.set_volume(0.2)
                shoot_audio.play()



    def draw(self, screen, curr_time):
        # Determine color based on health
        color = (255, 255, 0) if self.health < 50 else (0, 255, 0)
        if self.is_alive:
            self.draw_beam(screen)
        if(self.got_hit):
            color = (255,255,255)
        pygame.draw.rect(screen, color, self.rect)
        # Draw health bar
        self.draw_health_bar(screen)
        self.draw_shield_bar(screen)

    def draw_beam(self, screen):
        if self.is_using_sw and self.player_weapon == "super_weapon":
            beam_color = (128, 0, 128) #beam color
            beam_width = 10
            beam_start = (self.x + self.width // 2, self.y)  # Start at the player's current position
            beam_length = 300  # Set the desired beam length
            beam_end_y = max(0, self.y - beam_length)  # Ensure it doesn't go above the screen
            beam_end = (self.x + self.width // 2, beam_end_y)  # End point is shorter by beam_length

            if screen:  # Ensure the screen is valid
                pygame.draw.line(
                    screen, beam_color,
                    beam_start,
                    beam_end,
                    beam_width
                )
            print("[DEBUG] Drawing beam.")





    def deactivate_super_weapon(self):
        self.is_using_sw = False
        if hasattr(self, "beam_coords"):
            del self.beam_coords



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
        if consumable == "super_weapon":
            self.player_weapon = "super_weapon"
            self.is_using_sw = False  # Ensure the super weapon is not firing initially
            self.is_charging = False  # Reset charging state
            super_weapon_pickup_audio = pygame.mixer.Sound("assets/sound_efx/sw_pickup_audio.mp3")
            super_weapon_pickup_audio.play()
            print("SUPER WEAPON PICKED UP")
        elif consumable == "repair_kit":
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
            weapon_pick_up_audio = pygame.mixer.Sound("assets/sound_efx/weapon_pickup_sound.mp3")
            weapon_pick_up_audio.play()

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
     
    
