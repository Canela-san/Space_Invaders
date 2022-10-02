import pygame, random, Bin.config as config

pygame.init()
pygame.font.init()
main_font = pygame.font.SysFont(config.font_type, config.font_size)
big_font = pygame.font.SysFont(config.font_type_big, config.font_size_big)
# Images
RED_SPACE_SHIP = pygame.image.load(config.RED_SPACE_SHIP)
BLUE_SPACE_SHIP = pygame.image.load(config.BLUE_SPACE_SHIP)
GREEN_SPACE_SHIP = pygame.image.load(config.GREEN_SPACE_SHIP)
YELLOW_SPACE_SHIP = pygame.image.load(config.YELLOW_SPACE_SHIP)
RED_LAZER = pygame.image.load(config.RED_LAZER)
GREEN_LAZER = pygame.image.load(config.GREEN_LAZER)
BLUE_LAZER = pygame.image.load(config.BLUE_LAZER)
YELLOW_LAZER = pygame.image.load(config.YELLOW_LAZER)
BG = pygame.transform.scale(pygame.image.load(config.BG), (config.WINDOW_WIDTH,config.WINDOW_HEIGHT))

class Ship:
    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lazer_img = None
        self.lazers = []
        self.cool_down_counter = 0
    
    def cooldown(self):
        if self.cool_down_counter >= config.shoot_cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            lazer = Lazer(self.x,self.y,self.lazer_img)
            self.lazers.append(lazer)
            self.cool_down_counter = 1
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for lazer in self.lazers:
            lazer.draw(window)

    def move_lazers(self, vel, obj):
        self.cooldown()
        for lazer in self.lazers:
            lazer.move(vel)
            if lazer.off_screen(config.WINDOW_HEIGHT):
                self.lazers.remove(lazer)
            elif lazer.collision(obj):
                obj.health -= config.damage
                self.lazers.remove(lazer)


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
    
class Player(Ship):
    def __init__(self, health=100):
        super().__init__(0, 0, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.lazer_img = YELLOW_LAZER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.Reset_Position()

    def move_lazers(self, vel, objs):
        self.cooldown()
        for lazer in self.lazers:
            lazer.move(config.player_lazer_vel)
            if lazer.off_screen(config.WINDOW_HEIGHT):
                self.lazers.remove(lazer)
            else:
                for obj in objs: 
                    if lazer.collision(obj):
                        objs.remove(obj)
                        self.lazers.remove(lazer)

    def Reset_Position(self):
        self.x = config.WINDOW_WIDTH/2 - self.get_width()/2
        self.y = config.WINDOW_HEIGHT - self.get_height() - 35

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LAZER),
                "green": (GREEN_SPACE_SHIP, GREEN_LAZER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LAZER)
                }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y)
        self.ship_img, self.lazer_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def shoot(self):
        if self.cool_down_counter == 0:
            lazer = Lazer(self.x - 15, self.y, self.lazer_img)
            self.lazers.append(lazer)
            self.cool_down_counter = 1
    
    def move(self, vel):
        self.y += vel

class Lazer():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None




def main():
    # WINDOW SETUP
    screen = pygame.display.set_mode((config.WINDOW_WIDTH,config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.title)
    clock = pygame.time.Clock()
    player = Player()
    player.Reset_Position()
    enemies = []
    lost = False
    lost_count = 0
    
    run = True
    def event():
        pass
    def redraw_window():
            screen.blit(BG, (0,0))

            lives_label = main_font.render(f"Lives: {config.lives}", 1, (255,255,255))
            level_label = main_font.render(f"Level: {config.level}", 1, (255,255,255))

            screen.blit(lives_label, (10,10))
            screen.blit(level_label, (config.WINDOW_WIDTH-level_label.get_width()-10,10))

            for enemy in enemies:
                enemy.draw(screen)
            player.draw(screen)

            if lost:
                lost_label = big_font.render("You Lost!!", 1, (255,255,255))
                screen.blit(lost_label,(config.WINDOW_WIDTH/2 - lost_label.get_width()/2,config.WINDOW_HEIGHT/2 - lost_label.get_height()/2))


            pygame.display.update()
    while run:
        clock.tick(config.FPS)
        redraw_window()
        if config.lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            if lost_count > config.FPS * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            config.level += 1
            config.wave_length += config.wave_increase
            for i in range(config.wave_length):
                enemy = Enemy(random.randrange(50, config.WINDOW_WIDTH-100), random.randrange(-1500*config.level/5, -100), random.choice(["red","blue","green"]))
                enemies.append(enemy)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - config.player_vel > 0: #up
            player.y -= config.player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + config.player_vel + player.get_height() < config.WINDOW_HEIGHT: #down
            player.y += config.player_vel
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - config.player_vel > 0: #left
            player.x -= config.player_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + config.player_vel + player.get_width() < config.WINDOW_WIDTH: #right
            player.x += config.player_vel
        if (keys[pygame.K_SPACE]): #right
            player.shoot() 
        
        for enemy in enemies:
            enemy.move(config.enemy_vel)
            enemy.move_lazers(config.enemy_lazer_vel, player)

            if random.randrange(0, config.enemy_lazer_frequence * 60) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > config.WINDOW_HEIGHT:
                config.lives -= 1
                enemies.remove(enemy)
        player.move_lazers(config.player_lazer_vel, enemies)
    
main()
        