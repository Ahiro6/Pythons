import pygame
import random
# from playsound import playsound

pygame.init()
gameName = "Snake"

# colors
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.image.load("grass.jpg").convert()

gameWindow.fill(white)
pygame.display.set_caption(gameName)
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)
hightxt = open("highscore.txt", "r+")


def snake(color, size_w, size_h, snk_list):
    for snake_x, snake_y in snk_list:
        pygame.draw.rect(gameWindow, color, [snake_x, snake_y, size_w, size_h])


def food(color, x, y, size_w, size_h):
    pygame.draw.rect(gameWindow, color, ((x, y), (size_w, size_h)))


def line(color, xy1, xy2):
    pygame.draw.line(gameWindow, color, xy1, xy2)


def text(text1, color, x, y):
    screen_text = font.render(text1, True, color)
    gameWindow.blit(screen_text, (x, y))


def img(img1, x, y):
    gameWindow.blit(img1, (x, y))



def game_loop():
    snk_list = []

    score = 0

    x = 0
    y = screen_height/10

    size_w = 50
    size_h = 50

    velocity_x = 0
    velocity_y = 0
    velocity = 4

    food_x = random.randint(5, 750)
    food_y = random.randint(int(screen_height/10), 550)

    snk_length = 1
    fps = 60
    highscore = int(hightxt.readlines()[len(hightxt.readlines()) - 1])
    
    print(str(highscore))

    running = True
    game_over = False

    while running:
        x += velocity_x
        y += velocity_y

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    velocity_x = velocity
                    velocity_y = 0
                elif event.key == pygame.K_LEFT:
                    velocity_x = -velocity
                    velocity_y = 0
                elif event.key == pygame.K_DOWN:
                    velocity_x = 0
                    velocity_y = velocity
                elif event.key == pygame.K_UP:
                    velocity_x = 0
                    velocity_y = -velocity

        if not game_over:

            if x < 0:
                game_over = True
            elif x > screen_width - size_w:
                game_over = True
            elif y < screen_height/10:
                game_over = True
            elif y > screen_height - size_h:
                game_over = True

            if float(food_x + 20) >= x >= float(food_x - 45) and float(food_y + 20) >= y >= float(food_y - 45):
                score += 1
                food_x = random.randint(50, 750)
                food_y = random.randint(int(screen_height/10), 550)
                snk_length += 15
                # playsound('background_music.wav')

        elif game_over:
            x = 0
            y = screen_height/10
            score = 0
            velocity_y = 0
            velocity_x = 0
            game_over = False
            snk_length = 1
            snk_list = []
            food_x = random.randint(50, 750)
            food_y = random.randint(50, 550)

        img(bg, 0, 0)
        # gameWindow.fill(white)

        text("Score: " + str(score) + "   Highscore: " + str(highscore), black, 0, 0)
        line(black, (0, screen_height/10), (screen_width, screen_height/10))

        food(blue, food_x, food_y, 25, 25)

        head = [x, y]

        snk_list.append(head)

        if len(snk_list) > snk_length:
            del snk_list[0]

        if head in snk_list[:-1]:
            game_over = True

        if highscore < score:
            highscore = score
            hightxt.write("\n" + str(highscore))


        snake(red,  size_w, size_h, snk_list)
        pygame.display.update()
        clock.tick(fps)




game_loop()
pygame.quit()
hightxt.close()
