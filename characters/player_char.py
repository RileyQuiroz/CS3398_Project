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

        ## ADDING WEAPON TIMERS
        self.weapon_timer = 0
        self.weapon_duration= 100
        self.default_weapon = "default"

        #LOAD PLAYER IMAGE
        self.image = pygame.image.load("assets/ships/ship_4.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        
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
        self.laser_charge_sound.set_volume(0.2)
        self.laser_beam_sound = pygame.mixer.Sound("assets/sound_efx/beam_firing_loop.mp3")
        self.laser_beam_sound.set_volume(0.2)
        self.beam_audio_playing = False  # Ensure this attribute is initialized
        # Load the player image
        self.image = pygame.image.load("assets/ships/ship_4.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))  # Adjust size if necessary

        # Update collision rect to align with the image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update_weapon_timer(self):
        if self.player_weapon != self.default_weapon and hasattr(self, "weapon_timer"):
            current_time = pygame.time.get_ticks()
            print(f"[DEBUG] Current time: {current_time}, Weapon timer: {self.weapon_timer}, Duration: {self.weapon_duration}")
            if current_time - self.weapon_timer > self.weapon_duration:
                print("[DEBUG] Weapon timer expired. Reverting to default weapon.")

                # Stop super weapon effects
                if self.player_weapon == "super_weapon":
                    self.deactivate_super_weapon()

                # Revert to default weapon
                self.player_weapon = self.default_weapon
                del self.weapon_timer  # Remove the timer


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
                    self.laser_beam_sound.stop()


        # Logic for other weapons
        if self.player_weapon in ["auto_turret", "rocket_launcher", "default"]:
            weapon_info = {
                "auto_turret": {
                    "speed": 5,
                    "color": (0, 255, 255),
                    "size": (5, 15),
                    "damage": 1,
                    "sound": "assets/sound_efx/auto_turret2.mp3",
                    "cooldown": 200  # Faster cooldown for machine gun effect
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
                bullet_X = self.rect.centerx
                bullet_y = self.rect.top
                bullet = Projectile(
                    # self.x,
                    # self.y,
                    bullet_X,
                    bullet_y,
                    speed=detail["speed"],
                    color=detail["color"],
                    size=detail["size"],
                    damage=detail["damage"]
                )
                self.projectiles_group.add(bullet)
                self.last_shot_time = current_time

                # Play the weapon-specific sound
                shoot_audio = pygame.mixer.Sound(detail["sound"])
                shoot_audio.set_volume(0.1)
                shoot_audio.play()



    def draw(self, screen, curr_time):
        # Determine color based on health
        # color = (255, 255, 0) if self.health < 50 else (0, 255, 0)
        # if self.is_alive:
        #     self.draw_beam(screen)
        # if(self.got_hit):
        #     color = (255,255,255)
        # pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.image, self.rect.topleft)
        self.draw_beam(screen)
        # Draw health bar
        self.draw_health_bar(screen)
        self.draw_shield_bar(screen)

    def draw_beam(self, screen):
        if self.is_using_sw and self.player_weapon == "super_weapon":
            beam_color = (128, 0, 128)  # Purple beam color
            beam_width = 10
            beam_start = (self.rect.centerx, self.rect.top)  # Use the center-top of the player sprite
            beam_length = 300  # Set the desired beam length
            beam_end_y = max(0, self.y - beam_length)  # Ensure it doesn't go above the screen
            beam_end = (self.rect.centerx, beam_end_y)  # Beam's endpoint

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
        self.is_charging = False

        # Stop the sound if it's playing
        if hasattr(self, "beam_audio_playing") and self.beam_audio_playing:
            print("[DEBUG] Stopping super weapon sound.")
            self.laser_beam_sound.stop()
            self.beam_audio_playing = False

        # Stop charging sound if still playing
        self.laser_charge_sound.stop()

        print("[DEBUG] Super weapon deactivated.")




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
        if self.player_weapon == "super_weapon":
            self.is_using_sw = False
            self.is_charging = False
            if self.beam_audio_playing:
                self.laser_beam_sound.stop()
                self.beam_audio_playing = False
            self.laser_charge_sound.stop()

        if consumable == "super_weapon":
            self.player_weapon = "super_weapon"
            self.is_using_sw = False  # Ensure the super weapon is not firing initially
            self.is_charging = False  # Reset charging state
            self.weapon_timer = pygame.time.get_ticks()  # Start the weapon timer
            self.weapon_duration = 10000  # Duration in milliseconds (10 seconds)
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
            self.weapon_timer = pygame.time.get_ticks()  # Start the weapon timer
            self.weapon_duration = 5000  # Duration in milliseconds (10 seconds) ##THIS ONE ACTUALLY WORKS FOR DURRATION
            print(f"Picked up {consumable}!")
            weapon_pick_up_audio = pygame.mixer.Sound("assets/sound_efx/weapon_pickup_sound.mp3")
            weapon_pick_up_audio.play()


import time  # To track time

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
        self.spawn_time = time.time()  # Record the time when the consumable is created

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def has_expired(self, lifespan):
        """Check if the consumable has expired based on its lifespan."""
        return time.time() - self.spawn_time > lifespan

def spawn_consumable(consumables_group, screen_width, screen_height, is_boss_fight=False):
    # Define exclusion zones based on health and shield bar positions
    health_bar_zone = pygame.Rect(10, screen_height - 30, 200, 20)  # Health bar position and size
    shield_bar_zone = pygame.Rect(10, screen_height - 60, 200, 20)  # Shield bar position and size

    # Combine both zones into a single exclusion area
    exclusion_zones = [health_bar_zone, shield_bar_zone]

    # Filter consumables based on whether it's a boss fight
    if is_boss_fight:
        consumable_type = "super_weapon"  # Force spawn the super weapon
    else:
        available_types = [k for k in CONSUMABLE_DATA.keys() if k != "super_weapon"]
        consumable_type = random.choice(available_types)

    # Keep trying until we find a valid spawn location outside the exclusion zones
    while True:
        x = random.randint(0, screen_width - 35)
        y = random.randint(0, screen_height - 35)
        consumable_rect = pygame.Rect(x, y, 35, 35)  # Assume 35x35 is the consumable size

        # Check if the consumable rectangle collides with any exclusion zones
        if not any(zone.colliderect(consumable_rect) for zone in exclusion_zones):
            break  # Valid location found

    # Create and add the consumable
    consumable = Consumable(x, y, consumable_type)
    consumables_group.add(consumable)




