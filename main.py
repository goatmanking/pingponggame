import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(pygame.font.get_default_font(), 32)
font.set_bold(True)

# surface variables
PONG_RECT_WIDTH = 10
PONG_RECT_HEIGHT = 200
PONG_MOVE_SPEED = 7

white_surf = pygame.Surface((PONG_RECT_WIDTH,PONG_RECT_HEIGHT))
white_surf.fill("white")
white_rect_1 = white_surf.get_frect(center = (5, 720/2))
white_rect_2 = white_surf.get_frect(center = (1275, 720/2))
hit_1st_surf = False
hit_2nd_surf = False
# ball surf my nigga
BALL_WIDTH_N_HEIGHT = 25


MAX_BALL_VELOCITY = 10
X_SPEED_NIG = 6
SPED_NIG = 6
Y_BALL_SPEED = SPED_NIG
X_BALL_SPEED = X_SPEED_NIG


ball_surf = pygame.Surface((BALL_WIDTH_N_HEIGHT, BALL_WIDTH_N_HEIGHT))
ball_surf.fill('white')
ball_rect = ball_surf.get_frect(center = (1280/2, 720/2))
score = 0

def get_ceiling_ball_collisions(ballsp: float):
    if ball_rect.y + 3 >= 720:
        ballsp *= -1
    elif ball_rect.y - 3 <= 0: 
        ballsp *= -1
    return ballsp

scoreIncremented = False
ball_collided = False

def get_x_collisions(selp: int):
    global score
    global ball_collided
    if ball_rect.x + 3 >= 1280:
        ball_rect.x = 1280 / 2
        ball_rect.y = 720 / 2
        score += 1
        if not ball_collided:
            ball_collided = True
    elif ball_rect.x - 3 <= 0:
        ball_rect.x = 1280 /2
        ball_rect.y = 720/2
        score += 1
        if not ball_collided: 
            ball_collided = True

def what_direction():
        rand_choice_list = ["-", "+"]
        if random.choice(rand_choice_list) == "-":
            return True
        elif random.choice(rand_choice_list) == "+":
            return False

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



pygame.display.set_caption("Ping Pong")


starting_direction = what_direction()
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    


    screen.fill("black")
    screen.blit(white_surf, white_rect_1)
    screen.blit(white_surf, white_rect_2)
    screen.blit(ball_surf, ball_rect)


    text = font.render(f"Score: {score}", True, color='purple',bgcolor= 'white')
    text_rect = text.get_rect(center= (640, 30))

    screen.blit(text, text_rect)
    pygame.draw.line(screen, color='white', start_pos=((1280/2), 0), end_pos=((1280/2), 720), width=8)
    pygame.display.flip()

    Y_BALL_SPEED = get_ceiling_ball_collisions(Y_BALL_SPEED)
    


    get_x_collisions(X_BALL_SPEED)


    if ball_rect.colliderect(white_rect_1):
        check_ball_collisions(white_rect_1)
    elif ball_rect.colliderect(white_rect_2):
        check_ball_collisions(white_rect_2)

    

    ball_rect.y += Y_BALL_SPEED
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