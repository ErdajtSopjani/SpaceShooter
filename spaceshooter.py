import pygame
import os
pygame.font.init()
pygame.mixer.init()

#900, 500
#WINDOW VALUES
WIDTH, HEIGHT = 1000 , 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
#OTHER VALUES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BORDER = pygame.Rect(495, 0, 10, HEIGHT)
BORDER_X = 495
FPS = 144

BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join("music.mp3"))
BACKGROUND_MUSIC.set_volume(0.03)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("shoot2.mp3"))
BULLET_HIT_SOUND.set_volume(0.05)

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("shoot1.mp3"))
BULLET_FIRE_SOUND.set_volume(0.05)

HEALTH_FONT = pygame.font.SysFont("arial", 30)
WINNER_FONT = pygame.font.SysFont("impact", 100)

CHAR_WIDTH, CHAR_HEIGHT = 60, 50
VEL = 2

BULLETS_VEL = 3
MAX_BULLETS = 999

CHAR1_HIT = pygame.USEREVENT + 1 
CHAR2_HIT = pygame.USEREVENT + 2



#BACKGROUND
SPACE_BACKGROUND = pygame.image.load(
    os.path.join('bg3.png'))

#KARAKTERI 1
UFO_CHARACTER = pygame.image.load(
    os.path.join('ufo1.png'))
UFO_CHARACTER = pygame.transform.scale(UFO_CHARACTER, (CHAR_WIDTH, CHAR_HEIGHT))

#KARAKTERI 2
UFO_CHARACTER1 = pygame.image.load(
    os.path.join('spaceship.png'))
UFO_CHARACTER1 = pygame.transform.scale(UFO_CHARACTER1, (CHAR_WIDTH, CHAR_HEIGHT))



#LEVIZJA E KARAKTERIT 1
def char2_movement(keys_pressed, char2):
        
        if keys_pressed[pygame.K_a] and char2.x - VEL > 0: #N'T MAJT left
            char2.x -= VEL
        if keys_pressed[pygame.K_d] and char2.x + VEL + char2.width < BORDER_X: #N'T DJATHT right
            char2.x += VEL
        if keys_pressed[pygame.K_w] and char2.y - VEL > 0: #NALT up
            char2.y -= VEL
        if keys_pressed[pygame.K_s] and char2.y +VEL + char2.height < HEIGHT - 5: #POSHT down 
            char2.y += VEL



#LEVIZJA E KARAKTERIT 2
def char1_movement(keys_pressed, char1):
        if keys_pressed[pygame.K_LEFT]  and char1.x - VEL > BORDER_X + BORDER.width:#N'T MAJT left
            char1.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and char1.x + VEL + char1.width < WIDTH:    #N'T DJATHT right
            char1.x += VEL
        if keys_pressed[pygame.K_UP]    and char1.y - VEL > 0:                      #NALT up
            char1.y -= VEL
        if keys_pressed[pygame.K_DOWN]  and char1.y +VEL + char1.height < HEIGHT - 5:   #POSHT down 
            char1.y += VEL
    
#Levizja dhe kontrollimi i plumave
def handle_bullets(char1_bullets, char2_bullets, char1, char2):
    
    for bullet in char1_bullets:
        bullet.x -= BULLETS_VEL
        if char2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(CHAR2_HIT))
            char1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            char1_bullets.remove(bullet)


    for bullet in char2_bullets:
        bullet.x += BULLETS_VEL
        if char1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(CHAR1_HIT))
            char2_bullets.remove(bullet)
        elif bullet.x < 0:
            char2_bullets.remove(bullet)    
   
        

    
#DRAWING FUNCTION
def draw_window(char1, char2, char1_bullets, char2_bullets, char1_health, char2_health):
    
    WIN.blit(SPACE_BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    char1_health_text = HEALTH_FONT.render("Health: " + str(char1_health), 1, WHITE)
    char2_health_text = HEALTH_FONT.render("Health: " + str(char2_health), 1, WHITE)
    WIN.blit(char1_health_text, (855, 5))
    WIN.blit(char2_health_text, (5, 5))
    
    WIN.blit(UFO_CHARACTER, (char1.x, char1.y))
    WIN.blit(UFO_CHARACTER1, (char2.x, char2.y))
    
    
    for bullet in char1_bullets:
        pygame.draw.rect(WIN, GREEN , bullet)
    
    for bullet in char2_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    pygame.display.update()
    
    

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 
                         HEIGHT//2 - draw_text.get_height()//2))   
    pygame.display.update() 
    pygame.time.delay(2000)


    
#MAIN FUNCTION, (MAIN LOOP)
def main():
    char1 = pygame.Rect(730, 300, CHAR_WIDTH, CHAR_HEIGHT)
    char2 = pygame.Rect(100, 300, CHAR_WIDTH, CHAR_HEIGHT)
    
    char1_bullets = []
    char2_bullets = []
     
    char1_health = 10
    char2_health = 10
    
    clock = pygame.time.Clock()
    run = True
    

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            BACKGROUND_MUSIC.play()
        #BULLETS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(char2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        char2.x + char2.width, char2.y + char2.height//2 - 2, 10, 5)
                    char2_bullets.append(bullet)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(BULLET_FIRE_SOUND), maxtime=1000)
                    
                if event.key == pygame.K_RCTRL and len(char1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        char1.x, char1.y + char1.height//2 - 2, 10, 5)
                    char1_bullets.append(bullet)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(BULLET_FIRE_SOUND), maxtime=1000)
            
            
            if event.type == CHAR2_HIT:
                char2_health -= 1
                
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(BULLET_HIT_SOUND), maxtime=1000)
                
            if event.type == CHAR1_HIT:
                char1_health -= 1
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(BULLET_HIT_SOUND), maxtime=1000)
                
        winner_text = ""
        if char1_health <= 0:
            winner_text = "PLAYER2 WINS!"
            
        if char2_health <= 0:
            
            winner_text = "PLAYER1 WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break    
        
        
        keys_pressed = pygame.key.get_pressed()
        char2_movement(keys_pressed, char2)
        char1_movement(keys_pressed, char1)
        
        handle_bullets(char1_bullets, char2_bullets, char1, char2)
        
        draw_window(char1, char2, char1_bullets, char2_bullets, char1_health, char2_health)
        
    main()
    
if __name__ == "__main__":
    main()