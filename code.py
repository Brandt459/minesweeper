from turtle import onclick
import pygame
import sys
import pygame_widgets
from game import Game
from widgets.dropdown import DropdownClass
from widgets.reset_button import resetButton

from requests import head

width = 1200
height = 900
size = width, height

pygame.init()

screen = pygame.display.set_mode(size=size)

headSurface = pygame.Surface((1200, 100))
headSurface.fill((0, 255, 0))

boardSurface = pygame.Surface((1200, 800))
boardSurface.fill((255, 0, 0))

flag = pygame.image.load('images/flag.png').convert()
mine = pygame.image.load('images/mine.png').convert()

game = Game(0)

DropdownClass(headSurface, screen, game)
resetButton(headSurface, game)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3) and not game.gameover:
            pos = pygame.mouse.get_pos()
            for xindex, i in enumerate(range(10, game.columns * 30 + 10, 30)):
                for yindex, j in enumerate(range(10, game.rows * 30 + 10, 30)):
                    if pygame.Rect((i, j), (25, 25)).collidepoint((pos[0], pos[1] - 100)):
                        if event.button == 1:
                            if not game.board[xindex][yindex][3]:
                                game.board[xindex][yindex][3] = True
                                if game.board[xindex][yindex][2] == 0:
                                    game.findVoidBorder(xindex, yindex)
                                elif game.board[xindex][yindex][2] == -1:
                                    game.gameover = True
                            else:
                                game.chord(xindex, yindex)
                        elif event.button == 3:
                            if not game.board[xindex][yindex][3]:
                                if game.board[xindex][yindex][4]:
                                    game.flags -= 1
                                else:
                                    game.flags += 1
                                game.board[xindex][yindex][4] = not game.board[xindex][yindex][4]

        elif event.type == pygame.QUIT:
            sys.exit()

    for xindex, i in enumerate(range(10, game.columns * 30 + 10, 30)):
        for yindex, j in enumerate(range(10, game.rows * 30 + 10, 30)):
            squareSurface = pygame.Surface((25, 25))
            squareSurface.fill((255, 255, 255))
            if game.board[yindex][xindex][3]:
                font = pygame.font.SysFont(None, 25)
                num = game.board[yindex][xindex][2]
                color = (0, 0, 0)
                if num == 1:
                    color = (0, 0, 255)
                elif num == 2:
                    color = (0, 255, 0)
                elif num == 3:
                    color = (255, 0, 0)
                text = font.render(str(num), True, color)
                text_rect = text.get_rect(center=(12, 12))
                if num == 0:
                    pygame.draw.rect(squareSurface, (220, 220, 220), pygame.Rect((0, 0), (25, 25)), 1)
                    squareSurface.fill((220, 220, 220))
                elif num == -1:
                    squareSurface.blit(pygame.transform.scale(mine, (25, 25)), ((0, 0), (25, 25)))
                else:
                    pygame.draw.rect(text, (220, 220, 220), pygame.Rect((0, 0), (25, 25)), 1)
                    squareSurface.fill((220, 220, 220))
                    squareSurface.blit(text, text_rect)

            if game.board[yindex][xindex][4]:
                squareSurface.blit(pygame.transform.scale(flag, (25, 25)), ((0, 0), (25, 25)))

            boardSurface.blit(squareSurface, (j, i))

    if game.gameover:
        font = pygame.font.SysFont(None, 48)
        text = font.render('Gameover', True, (255, 255, 255))
        text_rect = text.get_rect(center=(600, 500))
        pygame.draw.rect(text, (255, 255, 255), pygame.Rect(0, 0, 100, 100), 1)
        boardSurface.blit(text, text_rect)
    else:
        blankSurface = pygame.Surface((200, 100))
        blankSurface.fill((255, 0, 0))
        boardSurface.blit(blankSurface, (500, 450))

    blankSurface = pygame.Surface((200, 100))
    blankSurface.fill((0, 255, 0))
    headSurface.blit(blankSurface, (200, 0))
    font = pygame.font.SysFont(None, 48)
    text = font.render(str(game.flags), True, (255, 255, 255))
    text_rect = text.get_rect(center=(250, 50))
    pygame.draw.rect(text, (0, 255, 0), pygame.Rect(0, 0, 100, 100), 1)
    headSurface.blit(text, text_rect)

    font = pygame.font.SysFont(None, 48)
    text2 = font.render(str(game.mines - game.flags), True, (255, 255, 255))
    text_rect2 = text.get_rect(center=(350, 50))
    pygame.draw.rect(text2, (0, 255, 0), pygame.Rect(0, 0, 100, 100), 1)
    headSurface.blit(text2, text_rect2)

    screen.blit(headSurface, (0, 0))
    screen.blit(boardSurface, (0, 100))
    pygame_widgets.update(events)
    pygame.display.flip()
