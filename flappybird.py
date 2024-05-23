import pygame
import neat
import time
import random
import os

WIN_WIDTH = 500
WIN_HEIGHT= 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))]
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))]

class Bird:         
    imgs= BIRD_IMGS             
    max_rotation = 25
    rot_vel = 20
    animation_time = 5

    def __init__(self,x,y):  #location of the birds
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel= 0
        self.height = self.y
        self.img_count= 0       #track which image we are showing for the bird
        self.img = self.imgs[0] #update img of bird

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y 
    
    def move(self): #function called during each frame to actually move bird
        #first calculate the change in height
        self.tick_count +=1
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2    #bird arc implementation (in terms of velocity)
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -=2 
        self.y = self.y + displacement

        #next calculate the tilt/angle of the bird
        if displacement<0 or self.y < self.height+50:       #moving up or 
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:                                               #moving down
            if self.tilt > -90:
                self.tilte -= self.rot_vel

    def draw(self, window):
        self.img_count +=1
        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*4 +1:
            self.img = self.imgs[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img= self.imgs[1]
            self.img_count = self.animation_time*2
        
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft= (self.x, self.y)).center)
        window.blit(rotated_img, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(window, bird):
    window.blit(BG_IMG, (0,0))
    bird.draw(window)
    pygame.display.update()

def main():
    flappybird = Bird(200,200)
    run = True
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False   
        draw_window(window, flappybird)

    pygame.quit()
    quit()

main()