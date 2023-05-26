import pygame , os
from abc import ABC , abstractmethod
#class untuk hero yang akan dimainkan 
class Karakter(ABC):
    def __init__ (self ,   health, damage, gambar, posisi_x, posisi_y):
        pygame.init()
        self.health = health 
        self.health_def = health/2
        self.current_health = 200
        self.damage = damage
        self.width_P , self.height_P = 100 ,140
        self.basic_image = gambar
        self.image = pygame.transform.scale( self.basic_image , (self.width_P , self.height_P))
        self.rect = pygame.Rect(posisi_x, posisi_y ,self.width_P , self.height_P)
        self.health_bar_length = 300
        self.health_ratio = self.health / self.health_bar_length
        self.health_change_speed = 10
        self.basic_att = []
        self.v_jump = 20
        self.jmp = True
        

    @abstractmethod
    def dead (self):
        pass

    @abstractmethod
    def maju (self):
        pass
    
    @abstractmethod
    def mundur (self):
        pass
    
    @abstractmethod
    def jump (self):
        pass
    
    @abstractmethod
    def peluru(self):
        pass


    def basic_action (self):
        self.image = pygame.transform.scale( self.basic_image , (self.width_P , self.height_P))
        return self.image

    def jumping (self):
        gravitasi = 1
        self.rect.y -= self.v_jump
        self.v_jump -= gravitasi

        if self.v_jump < -20:
            self.v_jump = 20
            self.jmp = False    
    
    def display(self, screen, check, nama):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.health:
            self.current_health += self.health_change_speed
            transition_width = int((self.health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)

        if self.current_health > self.health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        if check:
            health_bar_width = int(self.current_health / self.health_ratio)
            health_bar = pygame.Rect(10, 10, health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.right, 10, transition_width, 25)

            pygame.draw.rect(screen, (255, 0, 0), health_bar)
            pygame.draw.rect(screen, transition_color, transition_bar)
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 25), 4)

            font = pygame.font.Font(os.path.join('Assets/Font/Another America.ttf'), 30)
            nama_text = font.render(nama, True, (255, 255, 255))
            nama_rect = nama_text.get_rect()
            nama_rect.midtop = (260, health_bar.bottom + 2)
            screen.blit(nama_text, nama_rect)

        if not check:
            health_bar_width = int(self.current_health / self.health_ratio)
            health_bar = pygame.Rect(800 - health_bar_width, 10, health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.left, 10, transition_width, 25)

            pygame.draw.rect(screen, (255, 0, 0), health_bar)
            pygame.draw.rect(screen, transition_color, transition_bar)
            pygame.draw.rect(screen, (255, 255, 255), (800 - self.health_bar_length, 10, self.health_bar_length, 25), 4)

            font = pygame.font.Font(os.path.join('Assets/Font/Another America.ttf'), 30)
            nama_text = font.render(nama, True, (255, 255, 255))
            nama_rect = nama_text.get_rect()
            nama_rect.midtop = (530, health_bar.bottom + 2)
            screen.blit(nama_text, nama_rect)

    def defend(self, enemy_damage):
        if self.health > 0 :
            if self.health < self.health_def :
                self.health -= enemy_damage         
            else :
                self.health -= enemy_damage
            
        else :
            self.health = 0


class Hero_1(Karakter):
    def __init__ (self, react_x, react_y):
        self.Hero_G = pygame.image.load(os.path.join('Assets/Karakter/MasDor/karakter_diam.png'))
        Karakter.__init__(self,  1500,  50, self.Hero_G, react_x, react_y + 30)

    def dead(self):
        self.dead_image = pygame.image.load(os.path.join('Assets/Karakter/MasDor/karakter_mati.png'))
        self.image  = pygame.transform.scale(self.dead_image , (120 , 80))
        self.rect.y = 350
        
    def maju(self):
        maju_image = pygame.image.load(os.path.join('Assets/Karakter/MasDor/karakter_gerak.png'))
        self.image = pygame.transform.scale(maju_image, (self.width_P , self.height_P))

    def mundur (self):
        mundur_image = pygame.image.load(os.path.join('Assets/Karakter/MasDor/karakter_gerak.png'))
        self.image = pygame.transform.scale(mundur_image, (self.width_P , self.height_P))
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        jump_image = pygame.image.load(os.path.join('Assets/Karakter/MasDor/karakter_jump.png'))
        self.image = pygame.transform.scale(jump_image, (self.width_P , self.height_P))
        
    def peluru(self):
        bulet_image = pygame.image.load(os.path.join('Assets/Karakter/MasDor/shot.png'))
        bulet_image = pygame.transform.scale(bulet_image, (15, 10))
        return bulet_image




class Hero_2(Karakter):
    def __init__ (self, react_x, react_y):
        self.Hero_G = pygame.image.load(os.path.join('Assets/Karakter/MasEker/karakter_diam.png'))
        Karakter.__init__(self,  1500,  50, self.Hero_G, react_x, react_y + 30)
        

    def dead(self ):
        self.dead_image = pygame.image.load(os.path.join('Assets/Karakter/MasEker/karakter_mati.png'))
        self.image  = pygame.transform.scale(self.dead_image , (120,80))
        self.rect.y = 350
        
    def maju(self):
        maju_image = pygame.image.load(os.path.join('Assets/Karakter/MasEker/karakter_gerak.png'))
        self.image = pygame.transform.scale(maju_image, (self.width_P , self.height_P))
        
    def mundur (self):
        mundur_image = pygame.image.load(os.path.join('Assets/Karakter/MasEker/karakter_gerak.png'))
        self.image = pygame.transform.scale(mundur_image, (self.width_P , self.height_P))
        self.image = pygame.transform.flip(self.image, True, False)
        
    def jump(self):
        jump_image = pygame.image.load(os.path.join('Assets/Karakter/MasEker/karakter_jump.png'))
        self.image = pygame.transform.scale(jump_image, (self.width_P , self.height_P))
        
    def peluru(self):
        bulet_image = pygame.image.load(os.path.join('Assets/Karakter/MasEker/shot.png'))
        bulet_image = pygame.transform.scale(bulet_image, (25,10))
        return bulet_image

        
class Hero_3(Karakter):
    def __init__ (self, react_x, react_y):
        self.Hero_G = pygame.image.load(os.path.join('Assets/Karakter/PakPol/karakter_diam.png'))
        Karakter.__init__(self, 1500, 50, self.Hero_G, react_x, react_y + 30)

    def dead(self ):
        self.dead_image = pygame.image.load(os.path.join('Assets/Karakter/PakPol/karakter_mati.png'))
        self.image  = pygame.transform.scale(self.dead_image , (120 , 80))
        self.rect.y = 350
        
    def maju(self):
        maju_image = pygame.image.load(os.path.join('Assets/Karakter/PakPol/karakter_gerak.png'))
        self.image = pygame.transform.scale(maju_image, (self.width_P , self.height_P))

    def mundur (self):
        mundur_image = pygame.image.load(os.path.join('Assets/Karakter/PakPol/karakter_gerak.png'))
        self.image = pygame.transform.scale(mundur_image, (self.width_P , self.height_P))
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        jump_image = pygame.image.load(os.path.join('Assets/Karakter/PakPol/karakter_jump.png'))
        self.image = pygame.transform.scale(jump_image, (self.width_P , self.height_P))

    def peluru(self):
        bulet_image = pygame.image.load(os.path.join('Assets/Karakter/PakPol/shot.png'))
        bulet_image = pygame.transform.scale(bulet_image, (20, 10))
        return bulet_image


class Hero_4(Karakter):
    def __init__ (self, react_x, react_y):
        self.Hero_G = pygame.image.load(os.path.join('Assets/Karakter/PakMob/karakter_diam.png'))
        Karakter.__init__(self, 1500, 50, self.Hero_G, react_x, react_y  + 30)
        
    def dead(self):
        self.dead_image = pygame.image.load(os.path.join('Assets/Karakter/PakMob/karakter_mati.png'))
        self.image  = pygame.transform.scale(self.dead_image , (120 , 80))
        self.rect.y = 350
        
    def maju(self):
        maju_image = pygame.image.load(os.path.join('Assets/Karakter/PakMob/karakter_gerak.png'))
        self.image = pygame.transform.scale(maju_image, (self.width_P , self.height_P))

    def mundur (self):
        mundur_image = pygame.image.load(os.path.join('Assets/Karakter/PakMob/karakter_gerak.png'))
        self.image = pygame.transform.scale(mundur_image, (self.width_P , self.height_P))
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        jump_image = pygame.image.load(os.path.join('Assets/Karakter/PakMob/karakter_jump.png'))
        self.image = pygame.transform.scale(jump_image, (self.width_P , self.height_P))
    
    def peluru(self):
        bulet_image = pygame.image.load(os.path.join('Assets/Karakter/PakMob/shot.png'))
        bulet_image = pygame.transform.scale(bulet_image, (20, 14))
        return bulet_image

