import pygame
import random

# setup main game components
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# fonts
font = pygame.font.Font('./LycheeSoda.ttf', 30)
font2 = pygame.font.Font('./LycheeSoda.ttf', 64)

# load sound effects
scored_sound_effect = pygame.mixer.music.load('./scored.ogg')

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
left_score = 0
right_score = 0


# bounce ball if it hits the ceiling
def get_ceiling_ball_collisions(ballsp: float):
    if ball_rect.y + 3 >= 720:
        ballsp *= -1
    elif ball_rect.y - 3 <= 0: 
        ballsp *= -1
    return ballsp

ball_collided = False

scored_text = font2.render(f"", True, color='white',bgcolor= 'black')
draw_timestamp = 0

def draw_scored(isRightPaddle: bool):
    global scored_text
    
    if isRightPaddle:
        scored_text = font2.render(f"RIGHT SCORED!", True, color='white',bgcolor= 'black')
    else:
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
        pygame.mixer.music.play()
        draw_scored(False)
        left_score += 1
        if not ball_collided:
            ball_collided = True
    elif ball_rect.x - 3 <= 0:
        ball_rect.x = 1280 /2
        ball_rect.y = 720/2
        right_score += 1
        draw_scored(True)
        pygame.mixer.music.play()
        if not ball_collided: 
            ball_collided = True

def check_ball_collisions(surf):

    global Y_BALL_SPEED
    global X_BALL_SPEED

    if ball_rect.y >= surf.y and ball_rect.y <= surf.y + surf.height:
        if ball_rect.x + BALL_WIDTH_N_HEIGHT >= surf.x:
            X_BALL_SPEED *= -1
            reduction_factor = (surf.height / 2) / MAX_BALL_VELOCITY
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
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    pygame.draw.rect(screen, 'white', (490, 220, 300, 300), 5)

    draw_over_scored()
    get_x_collisions()

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

    pygame.display.flip()

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
    
    
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()