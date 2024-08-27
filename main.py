import pygame
import random

# setup main game components
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# fonts
font = pygame.font.Font('./LycheeSoda.ttf', 30)
start_button_font = pygame.font.Font('./LycheeSoda.ttf', 40)
font2 = pygame.font.Font('./LycheeSoda.ttf', 64)
Title = pygame.font.Font('./LycheeSoda.ttf', 80)
# load sound effects
scored_sound_effect = pygame.mixer.Sound('./newscored.mp3')
start_btn_sound = pygame.mixer.Sound('./hit.ogg')
hit_sound = pygame.mixer.Sound('./energy.mp3')
enterance_sound = pygame.mixer.Sound('./enterance_sound.mp3')
puase_soundtrack = pygame.mixer.Sound('pausesoundtrack.mp3')
boundary_touch_soundeffect = pygame.mixer.Sound('./boundary_touch.mp3')
boundary_touch_soundeffect_2 = pygame.mixer.Sound('./boundary_touch_2.mp3')

# 'paddle' variables
PONG_RECT_WIDTH = 10
PONG_RECT_HEIGHT = 200
PONG_MOVE_SPEED = 7

white_surf = pygame.Surface((PONG_RECT_WIDTH,PONG_RECT_HEIGHT))
white_surf.fill("white")
white_rect_1 = white_surf.get_frect(center = (5, 720/2))
white_rect_2 = white_surf.get_frect(center = (1275, 720/2))

# ping pong ball variables
BALL_WIDTH_N_HEIGHT = 25
MAX_BALL_VELOCITY = 10
Y_BALL_SPEED = 6
X_BALL_SPEED = 6

ball_surf = pygame.Surface((BALL_WIDTH_N_HEIGHT, BALL_WIDTH_N_HEIGHT))
ball_surf.fill('white')
ball_rect = ball_surf.get_frect(center = (1280/2, 720/2))
animation_ball_rect = ball_surf.get_frect(center= (640, 500))
left_score = 0
right_score = 0

# chose random sound

sound_effect_list = ['1', '2']

def chooseRandomBoundarySound(sound: list):
    choosedSound = random.choice(sound)
    if choosedSound == '1':
        boundary_touch_soundeffect.play().set_volume(0.5)
    elif choosedSound == '2':
        boundary_touch_soundeffect_2.play()




# bounce ball if it hits the ceiling
def get_ceiling_ball_collisions(ballsp: float):
    if ball_rect.y + 3 >= 720:
        ballsp *= -1
        chooseRandomBoundarySound(sound_effect_list)
    elif ball_rect.y - 3 <= 0: 
        ballsp *= -1
        chooseRandomBoundarySound(sound_effect_list)
    return ballsp

ball_collided = False

scored_text = font2.render(f"", True, color='white',bgcolor= 'black')
draw_timestamp = 0

def draw_scored(isRightPaddle: bool):
    global scored_text
    
    if isRightPaddle:
        scored_text = font2.render(f"RIGHT SCORED!", True, color='white',bgcolor= 'black')
    elif not isRightPaddle:
        scored_text = font2.render(f"LEFT SCORED!", True, color='white',bgcolor= 'black')

def draw_over_scored():
    global scored_text
    global draw_timestamp

    current_time = pygame.time.get_ticks()
    difference_in_time = current_time - draw_timestamp 
    if draw_timestamp == 0:
        return None
    if difference_in_time >= 1500:
       scored_text = font2.render(f"", True, color='white',bgcolor= 'black')



# check if ball goes outside of the playing box then increment score
def get_x_collisions():
    global left_score
    global right_score
    global ball_collided
    if ball_rect.x + 3 >= 1280:
        ball_rect.x = 1280 / 2
        ball_rect.y = 720 / 2
        scored_sound_effect.play()
        draw_scored(False)
        left_score += 1
        if not ball_collided:
            ball_collided = True
    elif ball_rect.x - 3 <= 0:
        ball_rect.x = 1280 /2
        ball_rect.y = 720/2
        right_score += 1
        draw_scored(True)
        scored_sound_effect.play()
        if not ball_collided: 
            ball_collided = True

def check_ball_collisions(surf):

    global Y_BALL_SPEED
    global X_BALL_SPEED

    if ball_rect.y >= surf.y and ball_rect.y <= surf.y + surf.height:
        if ball_rect.x + BALL_WIDTH_N_HEIGHT >= surf.x:
            X_BALL_SPEED *= -1
            reduction_factor = (surf.height / 2) / MAX_BALL_VELOCITY
            hit_sound.play()
            difference_in_y = surf.centery - ball_rect.y
            if difference_in_y < 0:
                difference_in_y *= -1
                y_vel =  difference_in_y / reduction_factor
                if y_vel > 6:
                    y_vel = 6
                    Y_BALL_SPEED = (y_vel * -1)
            else:
                y_vel =  difference_in_y / reduction_factor
                if y_vel > 6:
                    y_vel = 6
                    Y_BALL_SPEED = (y_vel * -1) 
    else: 
        print("uhhh sussy")

completedDownRun = False

def animatePaddles(rect: pygame.Rect):
    global completedDownRun
    if rect.y >= 10 and completedDownRun:
        rect.y -= 5
        if rect.top <= 10:
            completedDownRun = False
            rect.y += 5
    elif rect.y <= 720 and not completedDownRun:
        rect.y += 5
        if rect.bottom >= 710:
            completedDownRun = True 
            rect.y -= 5

def ball_animation_physics(rect):

    global X_BALL_SPEED
    global Y_BALL_SPEED

    rect.x += X_BALL_SPEED
    rect.y += Y_BALL_SPEED
    
    if rect.y + 3 >= 720:
        Y_BALL_SPEED *= -1
    elif rect.y - 3 <= 0: 
        Y_BALL_SPEED *= -1
    if rect.x <= 20:
        X_BALL_SPEED *= -1
    if rect.x >= 1260:
        X_BALL_SPEED *= -1

def what_direction():
        rand_choice_list = ["-", "+"]
        if random.choice(rand_choice_list) == "-":
            return True
        elif random.choice(rand_choice_list) == "+":
            return False
        else:
            return False



pygame.display.set_caption("Ping Pong")

# I do this here as it should run once and then the value should stay the same
starting_y_direction = what_direction()
starting_x_direction = what_direction()


is_game_paused = True
IS_MOUSE_BUTTON_PRESSED= False

start_button_surf = pygame.surface.Surface((200, 50))
start_button_surf.fill('lightgreen')  
start_button_rect = start_button_surf.get_frect(center=(640, 400))
start_btn_font_surf = start_button_font.render('START', True, 'black')

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            IS_MOUSE_BUTTON_PRESSED = True
        elif event.type == pygame.MOUSEBUTTONUP:
            IS_MOUSE_BUTTON_PRESSED = False
    screen.fill("black")
    pygame.draw.rect(screen, 'white', (490, 220, 300, 300), 5)

    get_x_collisions()
    # apparently I broke this idk why 
    draw_over_scored()

    pygame.draw.line(screen, color='white', start_pos=((1280/2), 0), end_pos=((1280/2), 720), width=8)

    screen.blit(white_surf, white_rect_1)
    screen.blit(white_surf, white_rect_2)
    screen.blit(scored_text, scored_text.get_rect(center= (640, 320)))
    screen.blit(ball_surf, ball_rect)



    left_score_text = font.render(f"Left Score: {left_score}", True, color='white',bgcolor= 'black')
    left_score_rect = left_score_text.get_rect(center= (320, 30))
    right_score_text = font.render(f"Right Score: {right_score}", True, color='white',bgcolor= 'black')
    right_score_rect = right_score_text.get_rect(center= (860, 30))

    screen.blit(left_score_text, left_score_rect)
    screen.blit(right_score_text, right_score_rect)


   
   
    if not is_game_paused:
        enterance_sound.stop()
        Y_BALL_SPEED = get_ceiling_ball_collisions(Y_BALL_SPEED)
        


        if ball_rect.colliderect(white_rect_1):
            check_ball_collisions(white_rect_1)
        elif ball_rect.colliderect(white_rect_2):
            check_ball_collisions(white_rect_2)

            
        if starting_y_direction:
            ball_rect.y += Y_BALL_SPEED
        else:
            ball_rect.y -= Y_BALL_SPEED
        if starting_x_direction:
            ball_rect.x += X_BALL_SPEED
        else: 
            ball_rect.x -= X_BALL_SPEED


        keys = pygame.key.get_pressed()
        if not  white_rect_1.y <= 7.5:
            if keys[pygame.K_w]:
                white_rect_1.y -= PONG_MOVE_SPEED
        if not white_rect_1.y >= 515:
            if keys[pygame.K_s]:
                white_rect_1.y += PONG_MOVE_SPEED
        if not white_rect_2.y >= 515:
            if keys[pygame.K_DOWN]:
                white_rect_2.y += PONG_MOVE_SPEED
        if not white_rect_2.y <= 7.5:
            if keys[pygame.K_UP]:
                white_rect_2.y -= PONG_MOVE_SPEED
        if keys[pygame.K_p]:
            is_game_paused = True
    else:
        # bro just load a button png 
        screen.fill("black")  
        mouse_pos = pygame.mouse.get_pos()    
        screen.blit(ball_surf, animation_ball_rect)
        screen.blit(start_button_surf, start_button_rect)
        screen.blit(start_btn_font_surf, (590, 380))
        pygame.draw.rect(screen, 'white', (540, 376, 200, 50), 4, 3)
        pygame.draw.rect(screen, 'white', (545, 371, 190, 59), 4, 3)
        screen.blit(white_surf, white_rect_1)
        screen.blit(white_surf, white_rect_2)
        screen.blit(font.render("© Made by Mushtaq", True, 'white'), (540, 660))
        puase_soundtrack.play()

        if IS_MOUSE_BUTTON_PRESSED:
            if start_button_rect.collidepoint(mouse_pos):
                start_btn_sound.play()
                is_game_paused = False
        elif start_button_rect.collidepoint(mouse_pos):
               start_button_surf.set_alpha(230)
               puase_soundtrack.stop()
               screen.blit(font2.render('LETS PLAY! :)', True, 'LIGHT GREEN'), (510, 200))
               enterance_sound.play(1)
               animatePaddles(white_rect_1)
               animatePaddles(white_rect_2)
               ball_animation_physics(animation_ball_rect)
        else: 
            enterance_sound.stop()
            screen.blit(font2.render('NO PLAY NO SLAY! :(', True, 'RED'), (410, 200))    
            start_button_surf.set_alpha(255)

        screen.blit(font2.render('THE PING PONG GAME', True, 'white'), (390, 50))

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()