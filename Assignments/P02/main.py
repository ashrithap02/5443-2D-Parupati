import pygame
import math

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

ARCHERY_HIT_SOUND = pygame.mixer.Sound('Archery_hit.mp3')
ARCHERY_FIRE_SOUND = pygame.mixer.Sound('Archery_fire.mp3')

POINTS_FONT = pygame.font.SysFont('comicsans', 26)
WINNER_FONT = pygame.font.SysFont('Shrikhand', 85)
global time
VEL = 5
MAX_ARROWS = 3
ARCHER_WIDTH, ARCHER_HEIGHT = 55, 50

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BLUE_ARCHER_IMAGE = pygame.image.load('blue_archery.png')
BLUE_ARCHER = pygame.transform.rotate(pygame.transform.scale(
    BLUE_ARCHER_IMAGE, (ARCHER_WIDTH, ARCHER_HEIGHT)), 0)

RED_ARCHER_IMAGE = pygame.image.load('red_archery.png')
RED_ARCHER = pygame.transform.rotate(pygame.transform.scale(
    RED_ARCHER_IMAGE, (ARCHER_WIDTH, ARCHER_HEIGHT)), 0)

SPACE = pygame.transform.scale(pygame.image.load('battleground.png'), (WIDTH, HEIGHT))


def draw_window(red, blue, red_arrows, blue_arrows, red_points, blue_points):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_points_text = POINTS_FONT.render("POINTS: " + str(red_points), True, BLACK)
    blue_points_text = POINTS_FONT.render("POINTS: " + str(blue_points), True, BLACK)
    WIN.blit(red_points_text, (WIDTH - red_points_text.get_width() - 10, 10))
    WIN.blit(blue_points_text, (10, 10))

    WIN.blit(BLUE_ARCHER, (blue.x, blue.y))
    WIN.blit(RED_ARCHER, (red.x, red.y))

    for arrow in red_arrows:
        pygame.draw.rect(WIN, RED, arrow)

    for arrow in blue_arrows:
        pygame.draw.rect(WIN, BLUE, arrow)


def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # RIGHT
        blue.x += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL


def handle_arrows(blue_arrows, red_arrows, blue, red, dt, shoot):
    for arrow in blue_arrows:
        x_pos, y_pos = update(arrow, dt, shoot)
        arrow.x = x_pos
        arrow.y = y_pos

        if red.colliderect(arrow):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_arrows.remove(arrow)
        elif arrow.x > WIDTH:
            blue_arrows.remove(arrow)
            global t
            t = 0
    for arrow in red_arrows:
        x_pos, y_pos = update(arrow, dt, shoot)
        arrow.x = x_pos
        arrow.y = y_pos
        if blue.colliderect(arrow):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_arrows.remove(arrow)
        elif arrow.x < 0:
            red_arrows.remove(arrow)
            t = 0


def update(arrow, dt, shoot, velocity=15):
    angle = 0
    # Increment time
    if shoot == 1:
        angle = 60
    elif shoot == 2:
        angle = 120
    global t
    t += dt
    gravity = 9.8
    # Calculate the position of the projectile
    pygame.time.delay(10)
    radians = math.radians(angle)
    x_pos = arrow.x + (velocity * math.cos(radians) * t)
    y_pos = arrow.y - (velocity * math.sin(radians) * t) + (0.5 * gravity * t ** 2)
    return x_pos, y_pos


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, BLACK)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, ARCHER_WIDTH, ARCHER_HEIGHT)
    blue = pygame.Rect(100, 300, ARCHER_WIDTH, ARCHER_HEIGHT)

    red_arrows = []
    blue_arrows = []
    red_points = 0
    blue_points = 0
    global t
    t = 0
    dt = 0
    shoot = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT and len(blue_arrows) < MAX_ARROWS:
                        arrow = pygame.Rect(blue.x + blue.width, blue.y + blue.height // 2 - 2, 10, 5)
                        blue_arrows.append(arrow)
                        ARCHERY_FIRE_SOUND.play()
                        shoot = 1

                    if event.key == pygame.K_RSHIFT and len(red_arrows) < MAX_ARROWS:
                        arrow = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                        red_arrows.append(arrow)
                        shoot = 2
                        ARCHERY_FIRE_SOUND.play()

                if event.type == RED_HIT:
                    t = 0
                    blue_points += 1

                    ARCHERY_HIT_SOUND.play()

                if event.type == BLUE_HIT:
                    red_points += 1
                    t = 0
                    ARCHERY_HIT_SOUND.play()

            winner_text = ""
            if red_points >= 10:
                winner_text = "Red Wins!"

            if blue_points >= 10:
                winner_text = "Blue Wins!"

            if winner_text != "":
                draw_winner(winner_text)
                break

            keys_pressed = pygame.key.get_pressed()
            blue_handle_movement(keys_pressed, blue)
            red_handle_movement(keys_pressed, red)

            if shoot == 1 or shoot == 2:
                handle_arrows(blue_arrows, red_arrows, blue, red, dt, shoot)

            draw_window(red, blue, red_arrows, blue_arrows, red_points, blue_points)

            pygame.display.update()
            dt = clock.tick(60) / 100
        except:
            quit()
    main()


if __name__ == "__main__":
    main()