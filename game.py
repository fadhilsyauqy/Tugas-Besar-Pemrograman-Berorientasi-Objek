import pygame , os
from karakter import *
from menu import *
from pygame import mixer
import random
pygame.font.init()

#class ini merupakan kelas dari seluruh tampilan dan inisialisasi game
class Game(): 
    def  __init__ (self):
        pygame.mixer.init()
        pygame.init()
        self.width , self.height = 800 , 500 #lebar jendela window
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mbaktembak") #judul window
        self.run = True #varibel untuk mengecek kejadian 
        self.FPS = 60
        self.vel = 5
        self.b_vel = 7
        self.bg = pygame.transform.scale( pygame.image.load(os.path.join('Assets/Background/bg_game.png')) , (self.width , self.height))
        self.bg_menu1 = pygame.transform.scale( pygame.image.load(os.path.join('Assets/Background/bg_menu1.png')) , (self.width , self.height))
        self.bg_menu2 = pygame.transform.scale( pygame.image.load(os.path.join('Assets/Background/bg_menu2.png')) , (self.width , self.height))
        self.menuhome = pygame.transform.scale( pygame.image.load(os.path.join('Assets/Background/bg_awal.png')) , (self.width , self.height))
        
        self.player1_hit = pygame.USEREVENT + 1
        self.player2_hit = pygame.USEREVENT + 2
        self.peluru = random.randint(3, 5)

        
        #variabel instansiasi
        self.Start = None
        self.Quit = None
        self.Player_1 = None
        self.Player_2 = None

        self.jump_1 = False 
        self.jump_2 = False 

    #fungsi ini untuk melakukan perulangan terhadap game
    def loop (self):
        clock =  pygame.time.Clock()
        mixer.music.load('Assets/Musik/war_sound.mp3')
        mixer.music.play(-1)
        while self.run:
            clock.tick(self.FPS)
            
            self.get_event()
            winner_image = None
            if self.Player_1.current_health <= 0:
                    self.Player_1.dead()
                    winner_image = pygame.image.load('Assets/Background/win_p2.png')

            if self.Player_2.current_health <= 0:
                    self.Player_2.dead()
                    winner_image = pygame.image.load('Assets/Background/win_p1.png')


            if winner_image is not None:
                mixer.music.load('Assets/Musik/victory_sound.mp3')
                mixer.music.play(-1)
                self.draw_window()
                scaled_winner_image = pygame.transform.scale(winner_image, (500, 300))
                self.window.blit(scaled_winner_image, (self.width/2 - scaled_winner_image.get_width() / 2, self.height/2 - scaled_winner_image.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(10000)
                
                break
                

            keys_pressed = pygame.key.get_pressed()
            self.movement_handle(keys_pressed)
            self.attck_handle()         
            self.draw_window()
            
        self.login_game()

        
    def endgame(self):
        self.window.blit(self.bg_menu1, (0,0))


        img_start = pygame.image.load(os.path.join('Assets/Background/start.png'))
        img_quit = pygame.image.load(os.path.join('Assets/Background/quit.png'))

        playagain = Menu(img_start, self.width/4, 250, 150, 150)
        Exit = Menu(img_quit, self.width*(2/4) + 50, 250, 150, 150)

        if playagain.display_Menu(self.window):
            self.loop()
            
        if Exit.display_Menu(self.window):
            self.run = False

        pygame.display.update() 
