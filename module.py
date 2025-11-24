import pygame as pg
import config
import random

class Game():
    '''
    Manages the main game loop, events, and rendering for the car game.
    '''
    def __init__(self):
        '''
        Initializes game window, state variables, sprites, text, and plays intro music.
        '''
        self.screen = pg.display.set_mode(config.screen_size)
        pg.display.set_caption('Car Game')
        self.clock = pg.time.Clock()
        self.is_driving = False
        self.running = True
        self.score = 0
        self.counter = 0
        self.dy = config.start_speed
        self.player_speed = config.player_speed
        self.init_sprites()
        self.init_text()
        pg.mixer.Channel(2).play(pg.mixer.Sound('assets/intro.mp3'))

    def init_text(self):
        '''
        Creates Text objects for menu, score, and about screen messages.
        '''
        self.start_text = Text('Start Game', 35, (config.screen_size[0]/2, config.screen_size[1]*(3/7)))
        self.exit_text = Text('Exit Game', 35, (config.screen_size[0]/2, config.screen_size[1]*(4/7)))
        self.score_text_small = Text(f'Score: {self.score:.0f}', 15, (20, 20), False)
        self.score_text_big = Text(f'Score: {self.score:.0f}', 35, (config.screen_size[0]/2, config.screen_size[1]*(1/7)))
        self.about_text = Text('About', 25, (config.screen_size[0]/2, config.screen_size[1]*(6/7)))
        self.back_text = Text('Go Back', 25, (config.screen_size[0]/2, config.screen_size[1]*(6/7)))

        self.line1_text = Text('Welcome to the game!', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)))
        self.line2_text = Text('Use ← and → arrow keys', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*2))
        self.line3_text = Text('to steer your car.', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*3))
        self.line4_text = Text('Collect hourglasses', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*4))
        self.line5_text = Text('to slow down.', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*5))
        self.line6_text = Text('Collect energy boxes', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*6))
        self.line7_text = Text('to steer faster.', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*7))
        self.line8_text = Text('Press ESC at any time', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*8))
        self.line9_text = Text('to quit.', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*9))
        self.line10_text = Text('Good luck!', 17, (config.screen_size[0]/2, config.screen_size[1]*(2/7)+self.line1_text.textrect.h*2*11))

    def init_sprites(self):
        '''
        Initializes road, player, cars, and effect sprites.
        '''
        road = Road('assets/road.png')
        self.road_sprite = pg.sprite.GroupSingle(road)

        player = Player('assets/player.png')
        self.player_sprite = pg.sprite.GroupSingle(player)

        car1 = Car('assets/car1.png', -200)
        car2 = Car('assets/car2.png', -800)
        car3 = Car('assets/car3.png', -1400)
        car4 = Car('assets/car4.png', -2000)
        self.car_sprites = pg.sprite.Group(car1, car2, car3, car4)
        
        self.hourglass = Effect('assets/hourglass.png', -4000)
        self.hourglass_sprite = pg.sprite.GroupSingle(self.hourglass)
        self.energy = Effect('assets/energy.png', -1000)
        self.energy_sprite = pg.sprite.GroupSingle(self.energy)

    def run(self):
        '''
        Main loop that handles menu navigation and starts gameplay or about screen.
        '''
        while self.running:
            choice = self.menu()

            if choice == 'about':
                self.about()

            if choice == 'drive':
                self.drive()

    def menu(self):
        '''
        Displays menu, handles input, and returns next action ('drive', 'about', or 'exit').
        '''
        while self.running and not self.is_driving:
            self.clock.tick(120)

            mouse_pos = (0, 0)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    self.running = False
                    return 'exit'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        return 'exit'
        
            self.screen.fill(config.green)
            self.road_sprite.draw(self.screen)

            if self.score > 0:
                self.score_text_big.update_rect(f'Score: {self.score:.0f}')
                self.score_text_big.textrect.center = (config.screen_size[0]/2, config.screen_size[1]*(1/7))  
                self.score_text_big.render(self.screen, config.yellow)

            self.start_text.render(self.screen, config.white) 
            self.exit_text.render(self.screen, config.white) 
            self.about_text.render(self.screen, config.white) 

            if self.start_text.textrect.collidepoint(mouse_pos):
                pg.mixer.Channel(1).play(pg.mixer.Sound('assets/effect.ogg'))
                pg.time.wait(600)
                self.is_driving = True
                self.init_sprites()
                return 'drive'

            if self.exit_text.textrect.collidepoint(mouse_pos):
                self.running = False
                return 'exit'

            if self.about_text.textrect.collidepoint(mouse_pos):
                pg.mixer.Channel(1).play(pg.mixer.Sound('assets/effect.ogg'))
                return 'about'

            pg.display.update()

    def about(self):
        '''
        Displays about screen with instructions and handles exit back to menu.
        '''
        is_about = True
        while self.running and is_about:
            self.clock.tick(120)

            mouse_pos = (0, 0)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            self.screen.fill(config.green)
            self.road_sprite.draw(self.screen)

            self.line1_text.render(self.screen, config.white) 
            self.line2_text.render(self.screen, config.white) 
            self.line3_text.render(self.screen, config.white) 
            self.line4_text.render(self.screen, config.white) 
            self.line5_text.render(self.screen, config.white) 
            self.line6_text.render(self.screen, config.white) 
            self.line7_text.render(self.screen, config.white) 
            self.line8_text.render(self.screen, config.white) 
            self.line9_text.render(self.screen, config.white) 
            self.line10_text.render(self.screen, config.white) 

            self.back_text.render(self.screen, config.white) 

            if self.back_text.textrect.collidepoint(mouse_pos):
                pg.mixer.Channel(1).play(pg.mixer.Sound('assets/effect.ogg'))
                is_about = False

            pg.display.update()
        
    def drive(self):
        '''
        Starts gameplay loop: resets variables, plays music, and updates game state until collision.
        '''
        self.score = 0
        self.dy = config.start_speed
        self.player_speed = config.player_speed
        self.clock.tick()
        self.start_music()
        while self.running and self.is_driving:
            dt = self.clock.tick(120)
            self.dy += dt/1500
            self.update_score_text()
            self.reset_player_speed(dt)
            self.handle_exit()
            self.check_collisions()
            self.update_positions()
            self.draw_run()
            self.score += dt/100

    def handle_exit(self):
        '''
        Handles quitting the game when ESC or window close event occurs.
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def reset_player_speed(self, dt):
        '''
        Resets or maintains player speed after a speed boost duration based on elapsed time.
        '''
        if self.player_speed != config.player_speed and self.counter > config.player_speed_boost_duration/self.dy:
            self.player_speed = config.player_speed
            self.counter = 0
        elif self.player_speed != config.player_speed and self.counter < config.player_speed_boost_duration/self.dy:
            self.counter += dt
            
    
    def update_positions(self):
        '''
        Updates positions of player, cars, road, and effects based on speed and input.
        '''
        keys = pg.key.get_pressed()
        direction = 0
        if keys[pg.K_LEFT]:
            direction = -1
        if keys[pg.K_RIGHT]:
            direction = 1

        self.player_sprite.update(direction, self.player_speed)
        self.car_sprites.update(self.dy*0.5)
        self.road_sprite.update(self.dy) 
        self.hourglass_sprite.update(self.dy*0.3)
        self.energy_sprite.update(self.dy*0.3)

    def draw_run(self):
        '''
        Renders game elements and updates display during gameplay.
        '''
        self.screen.fill(config.green)
        self.road_sprite.draw(self.screen)
        self.hourglass_sprite.draw(self.screen)
        self.energy_sprite.draw(self.screen)
        self.car_sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.score_text_small.render(self.screen, config.white)
        pg.display.update()

    def update_score_text(self):
        '''
        Updates the score displayed.
        '''
        self.score_text_small.text = f'Score: {self.score:.0f}' 
        self.score_text_big.text = f'Score: {self.score:.0f}' 

    def check_collisions(self):
        '''
        Checks collisions: ends game on car hit, applies effects for hourglass and energy collisions.
        '''
        if pg.sprite.groupcollide(self.player_sprite, self.car_sprites, False, False) != {}:
            self.pause_music()
            pg.mixer.Channel(0).play(pg.mixer.Sound('assets/crash.ogg'))
            pg.time.wait(600)
            self.is_driving = False

        if pg.sprite.groupcollide(self.player_sprite, self.hourglass_sprite, False, False) != {}:
            pg.mixer.Channel(1).play(pg.mixer.Sound('assets/effect.ogg'))
            self.hourglass.rect.y = 1500
            self.dy = self.dy*0.7

        if pg.sprite.groupcollide(self.player_sprite, self.energy_sprite, False, False) != {}:
            pg.mixer.Channel(1).play(pg.mixer.Sound('assets/effect.ogg'))
            self.energy.rect.y = 1500
            self.player_speed = self.player_speed*2

    def start_music(self):
        '''
        Initializes audio mixer and starts looping background music.
        '''
        pg.mixer.init()
        pg.mixer.music.load('assets/music.wav')
        pg.mixer.music.play(-1)

    def pause_music(self, unpause=False):
        '''
        Pauses/unpauses background music
        '''
        if unpause:
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()
        
class Car(pg.sprite.Sprite):
    '''
    Represents a car obstacle that moves down the screen.
    '''
    def __init__(self, filename, y):
        '''
        Loads car image, sets initial position in a random lane.
        '''
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(config.lanes)
        self.rect.y = y

    def update(self, dy):
        '''
        Moves car down by dy or reset to top if it moves off-screen.
        '''
        if self.rect.y < 1000:
            self.rect.y += dy
        else:
            self.rect.y = -1400
            self.rect.centerx = random.choice(config.lanes)

class Player(pg.sprite.Sprite):
    '''
    Represents the player-controlled car that moves left or right.
    '''
    def __init__(self, filename):
        '''
        Loads player image and sets initial position in a random lane.
        '''
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(config.lanes)
        self.rect.y = config.player_y

    def update(self, dir, speed):
        '''
        Moves player left or right within road boundaries based on input direction and speed.
        '''
        if dir == 1 and self.rect.right < config.roadside[1]:
            self.rect.x += speed 
        if dir == -1 and self.rect.left > config.roadside[0]:
            self.rect.x -= speed
           
class Road(pg.sprite.Sprite):
    '''
    Represent the scrolling road background.
    '''
    def __init__(self, filename):
        '''
        Loads road image and sets initial vertical position.
        '''
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = -1296
        self.rect.centerx = 408

    def update(self, dy):
        '''
        Scrolls road image down by dy or loops when past a threshold.
        '''
        if self.rect.y <= -324:
            self.rect.y += dy
        else:
            self.rect.y = -1296
            self.rect.y += dy

class Text():
    '''
    Utility class for rendering text to the screen.
    '''
    def __init__(self, text, font_size, position, center=True):
        '''
        Initializes font, text content, and position for rendering.
        '''
        self.font = pg.freetype.Font('assets/font.ttf', font_size)
        self.text = text 
        self.textrect = self.font.get_rect(text)
        if center:
            self.textrect.center = position
        else:
            self.textrect = position

    def render(self, screen, color):
        '''
        Draws text onto given screen surface in specified color.
        '''
        self.font.render_to(screen, self.textrect, self.text, color)

    def update_rect(self, text):
        '''
        Updates text rectangle based on new text content.
        '''
        self.textrect = self.font.get_rect(text)

class Effect(pg.sprite.Sprite):
    '''
    Represents collectible effects (hourglass or energy) that move down the screen.
    '''
    def __init__(self, filename, y):
        '''
        Loads effect image, sets initial position in a random lane.
        '''
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(config.lanes)
        self.rect.y = y

    def update(self, dy):
        '''
        Moves effect down by dy or resets to top when off-screen.
        '''
        if self.rect.y < 3000:
            self.rect.y += dy
        else:
            self.rect.y = -5000
            self.rect.centerx = random.choice(config.lanes)
