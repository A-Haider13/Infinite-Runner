import pygame
from pygame.locals import *
from BackgroundScreen import Background
from runner import runner
from enemy import Goblin
import sys
import random

pygame.init()

screen_width, screen_height = 1150, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Infinite Runner: Phew Phew")

clock = pygame.time.Clock()

# sprite_sheet_image = pygame.image.load("maincharacter.jpg")
background_image = pygame.image.load("images/background/background.jpg")
background_rect = background_image.get_rect()
background_x = 0

BackGround = Background(background_image, [0, 0])

Runner = runner()  # spawn player
Runner.rect.x = 100  # go to x
Runner.rect.y = 500  # go to y
player_list = pygame.sprite.Group()
player_list.add(Runner)
steps = 7

enemy_list = pygame.sprite.Group()  # Create a group for enemies
goblin = Goblin(screen_width, screen_height)

game_is_running = True

while game_is_running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            game_is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                Runner.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                Runner.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                Runner.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                Runner.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                Runner.control(-steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                Runner.control(0, steps * 2)

    background_x -= 3

    if background_x <= -background_rect.width:
        background_x = 0

    Runner.update()  # update player position
    goblin.update()  # update enemy position
    goblin.animate()  # animate goblin

    if goblin.rect.right < 0:  # Respawn goblin when it goes off the screen
        goblin.rect.left = screen_width
        goblin.rect.y = screen_height - goblin.rect.height

    """
        The code below is to prevent the player from going off the screen
    """
    if Runner.rect.left < 0:
        Runner.rect.left = 0
    if Runner.rect.right > screen_width:
        Runner.rect.right = screen_width
    if Runner.rect.top < 0:
        Runner.rect.top = 0
    if Runner.rect.bottom > screen_height:
        Runner.rect.bottom = screen_height

    screen.blit(background_image, (background_x, 0))  # adds the initial background image
    screen.blit(background_image, (background_x + background_rect.width, 0))  # blit the second image right after the first one making it look like an infinite never ending screen
    player_list.draw(screen)  # Draw the player on the screen
    screen.blit(goblin.image, (goblin.rect.x, goblin.rect.y))
    enemy_list.draw(screen)

    pygame.display.flip()

pygame.quit()
