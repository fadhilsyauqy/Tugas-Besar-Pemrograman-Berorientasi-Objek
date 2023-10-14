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


        img_start = pygame.image.load(os.path.join('Assets/Background/Start.png'))
        img_quit = pygame.image.load(os.path.join('Assets/Background/Quit.png'))

        playagain = Menu(img_start, self.width/4, 250, 150, 150)
        Exit = Menu(img_quit, self.width*(2/4) + 50, 250, 150, 150)

        if playagain.display_Menu(self.window):
            self.loop()
            
        if Exit.display_Menu(self.window):
            self.run = False

        pygame.display.update() 
        
     #logic peluru
    def attck_handle(self): 
        for bulet in self.Player_1.basic_att:
            bulet.x += self.b_vel
            if self.Player_2.rect.colliderect(bulet):
                pygame.event.post(pygame.event.Event(self.player2_hit))
                self.Player_1.basic_att.remove(bulet)
            elif bulet.x > self.width :
                self.Player_1.basic_att.remove(bulet)

        for bulet in self.Player_2.basic_att:
            bulet.x -= self.b_vel
            if self.Player_1.rect.colliderect(bulet):
                pygame.event.post(pygame.event.Event(self.player1_hit))
                self.Player_2.basic_att.remove(bulet)
            elif bulet.x < 0 :
                self.Player_2.basic_att.remove(bulet)


                    
    #fungsi ini agar player dapat berjalan 
    def movement_handle (self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.Player_1.rect.x - self.vel > 0 :  # LEFT
            self.Player_1.rect.x -= self.vel
            self.Player_1.mundur()
        if keys_pressed[pygame.K_d] and self.Player_1.rect.x + self.Player_1.width_P  + self.vel < self.width:  # RIGHT
            self.Player_1.rect.x += self.vel
            self.Player_1.maju()
        if keys_pressed[pygame.K_w] and self.Player_1.rect.y - self.vel > 0: # UP
            self.jump_1 = True  
            self.Player_1.jump()     

        if keys_pressed[pygame.K_LEFT] and self.Player_2.rect.x - self.vel :  # LEFT
            self.Player_2.rect.x -= self.vel
            self.Player_2.maju()
        if keys_pressed[pygame.K_RIGHT] and self.Player_2.rect.x + self.vel < self.width  - 100:  # RIGHT
            self.Player_2.rect.x += self.vel
            self.Player_2.mundur()
        if keys_pressed[pygame.K_UP] and self.Player_2.rect.y - self.vel > 0:  # UP
            self.jump_2 = True
            self.Player_2.jump()    

        if self.jump_1 :
            self.Player_1.jumping()

            if self.Player_1.jmp == False:
                self.jump_1 = False
                self.Player_1.jmp = True
        else :
            pass

        if self.jump_2 :
            self.Player_2.jumping()

            if self.Player_2.jmp == False:
                self.jump_2 = False
                self.Player_2.jmp = True
        else :
            pass
    
    
    #fungsi untuk mendapatkan event terhadap kejadian pada game. Mis QUIT, PLAY, START, dll
    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(self.Player_1.basic_att) < self.peluru :
                    bullet = pygame.Rect(self.Player_1.rect.x + self.Player_1.width_P, self.Player_1.rect.y + self.Player_1.height_P//2 -2 , 10, 5)
                    self.Player_1.basic_att.append(bullet)
    
                if event.key == pygame.K_RCTRL and len(self.Player_2.basic_att) < self.peluru :
                    bullet = pygame.Rect(self.Player_2.rect.x, self.Player_2.rect.y + self.Player_2.height_P//2 -2, 10, 5)
                    self.Player_2.basic_att.append(bullet)

            if event.type == self.player1_hit:
                self.Player_1.defend(self.Player_2.damage)

            if event.type == self.player2_hit:
                self.Player_2.defend(self.Player_1.damage)

    #fungsi ini untuk menampilkan tampilan game
    def draw_window(self):
        self.window.blit(self.bg, (0, 0))

        self.Player_1.display(self.window, True, self.Player1_nama)
        self.Player_2.display(self.window, False, self.Player2_nama)


        self.window.blit(self.Player_1.image, (self.Player_1.rect.x , self.Player_1.rect.y))
        self.window.blit(pygame.transform.flip(self.Player_2.image, True, False), (self.Player_2.rect.x , self.Player_2.rect.y))

        
        for bulet in self.Player_1.basic_att:
            bulet_image = self.Player_1.peluru()
            self.window.blit(bulet_image, (bulet.x, bulet.y - 25))
            
        for bulet in self.Player_2.basic_att:
            bulet_image = self.Player_2.peluru()
            bulet_image = pygame.transform.flip(bulet_image, True, False)
            self.window.blit(bulet_image, (bulet.x + 15 , bulet.y  - 25))


        pygame.display.update()

        self.Player_1.basic_action()
        self.Player_2.basic_action()
        
     # Fungsi menu hero atau fungsi untuk memilih hero untuk player 1 dan player 2
    def load_hero(self, A, B, C, D):
        i = 1
        pygame.time.delay(200)
        while i < 3:
            self.get_event()
            
            # Untuk player 1 dapat memilih hero terlebih dahulu
            if i == 1:
                self.window.blit(self.bg_menu1, (0,0))
                player1_image = pygame.image.load(os.path.join('Assets/Background/player1.png'))
                self.window.blit(player1_image, (self.width/2 - player1_image.get_width() /2, 40))
                
                if A.display_Menu(self.window):
                    self.Player_1 = Hero_1(50, 250)
                    self.Player1_nama = "Mas Dor"
                    i= 2
                    A.selected = True
                elif B.display_Menu(self.window):
                    self.Player_1 = Hero_2(50, 250)
                    self.Player1_nama = "Mas Eker"
                    i= 2
                elif C.display_Menu(self.window):
                    self.Player_1 = Hero_3(50, 250)
                    self.Player1_nama = "Pak Pol"
                    i= 2
                elif D.display_Menu(self.window):
                    self.Player_1 = Hero_4(50, 250)
                    self.Player1_nama = "Pak Mob"
                    i= 2
                
            # Untuk player 2 dapat memilih hero setelah player 1 selesai memilih hero
            elif i == 2:
                self.window.blit(self.bg_menu2, (0,0))
                player2_image = pygame.image.load(os.path.join('Assets/Background/player2.png'))
                self.window.blit(player2_image, (self.width/2 - player2_image.get_width() /2, 40))
                
                if A.display_Menu(self.window):
                    self.Player_2 = Hero_1(650, 250)
                    self.Player2_nama= "Mas Dor"
                    i= 3
                elif B.display_Menu(self.window):
                    self.Player_2 = Hero_2(650, 250)
                    self.Player2_nama= "Mas Eker"
                    i= 3
                elif C.display_Menu(self.window):
                    self.Player_2 = Hero_3(650, 250)
                    self.Player2_nama= "Pak Pol"
                    i= 3
                elif D.display_Menu(self.window):
                    self.Player_2 = Hero_4(650, 250)
                    self.Player2_nama= "Pak Mob"
                    i= 3
                    

            pygame.display.update()

    #fungsi ini untuk membuat objek menu
    def login_game(self):
        img_start = pygame.image.load(os.path.join('Assets/Background/start.png'))
        img_quit = pygame.image.load(os.path.join('Assets/Background/quit.png'))
        Hero_1_image_menu = pygame.image.load(os.path.join('Assets/Karakter/MasDor/MasDor.png'))
        Hero_2_image_menu = pygame.image.load(os.path.join('Assets/Karakter/MasEker/MasEker.png'))
        Hero_3_image_menu = pygame.image.load(os.path.join('Assets/Karakter/PakPol/PakPol.png'))
        Hero_4_image_menu = pygame.image.load(os.path.join('Assets/Karakter/PakMob/PakMob.png'))

        self.Start = Menu(img_start, self.width/2 - 80, 295, 150, 50)
        self.Quit = Menu(img_quit, self.width/2 - 80,  375, 150, 50)
        MasDor = Menu(Hero_1_image_menu, 25, self.height /2 - 50,150, 220)
        MasDor.selected = False
        MasEker = Menu(Hero_2_image_menu,225, self.height/2 - 50, 150, 220 )
        MasEker.selected = False
        PakPol = Menu(Hero_3_image_menu,425, self.height/2 - 50, 150, 220)
        PakPol.selected = False
        PakMod = Menu(Hero_4_image_menu,625, self.height/2 - 50, 150, 220)
        PakMod.selected = False

        mixer.music.load('Assets/Musik/menu_sound.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        while self.run == True:
            
            self.window.blit(self.menuhome, (0,0))

            self.get_event()
            if self.Start.display_Menu(self.window):
                self.load_hero(MasDor, MasEker, PakPol, PakMod)
                self.loop()
            
            if self.Quit.display_Menu(self.window):
                self.run = False

            pygame.display.update() 

if __name__ == "__main__":
    Mbaktembak = Game()

    Mbaktembak.login_game()


