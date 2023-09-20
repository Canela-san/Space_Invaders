import os
# Game config
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
FPS = 60
level = 0
lives = 5
font_type = "comicsans"
font_size = 40
font_type_big = "comicsans"
font_size_big = 60
player_vel = 5
player_lazer_vel = -2
wave_length = 0
wave_increase = 5
enemy_vel = 1
enemy_lazer_vel = 1.5
enemy_lazer_frequence = 2
shoot_cooldown = 30
damage = 10
title = 'Space Invaders'

# IMAGES
RED_SPACE_SHIP = os.path.join("Images", "pixel_ship_red_small.png")
BLUE_SPACE_SHIP = os.path.join("Images", "pixel_ship_blue_small.png")
GREEN_SPACE_SHIP = os.path.join("Images", "pixel_ship_green_small.png")

# player ship
YELLOW_SPACE_SHIP = os.path.join("Images", "pixel_ship_yellow.png")

# Lazers
RED_LAZER = os.path.join("Images", "pixel_laser_red.png")
GREEN_LAZER = os.path.join("Images", "pixel_laser_green.png")
BLUE_LAZER = os.path.join("Images", "pixel_laser_blue.png")
YELLOW_LAZER = os.path.join("Images", "pixel_laser_yellow.png")

# Background
BG = os.path.join("Images", "background-black.png")