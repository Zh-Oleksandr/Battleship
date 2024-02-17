import random
import time
import pygame
import battleship_ai

Screen_Width = 1200
Screen_Height = 1200

wait = False

screen = pygame.display.set_mode((Screen_Width, Screen_Height))
screen.fill((50, 50, 80))

ai1 = battleship_ai.Ai("ai1", 30)
ai2 = battleship_ai.Ai("ai2", 670)

battleship_ai.BoardWidth = 10
battleship_ai.BoardLength = 10

pygame.init()


def Draw_initial_Grid(ai):
    for ship in ai.ships:
        ai.spotcheck(ship)
    value = 0
    block_size = Screen_Width / (2 * battleship_ai.BoardLength) - 20  # Set the size of the grid block
    for x in range(0, battleship_ai.BoardWidth):
        for y in range(0, battleship_ai.BoardLength):
            rect = pygame.Rect(ai.gridpos + (block_size + 10) * x, y * (block_size + 10) + block_size, block_size,
                               block_size)
            if ai.Board[y][x] > value:
                value = ai.Board[y][x]
            if ai.Board[y][x] == -1 or ai.Board[y][x] == 0:
                pygame.draw.rect(screen, (0, 0, 0), rect)
            elif ai.Board[y][x] == -2:
                pygame.draw.rect(screen, (0, 100, 0), rect)
            else:
                pygame.draw.rect(screen, (255 * ai.Board[y][x] / (value), 0, 0), rect)


def Wait(x):
    if wait:
        time.sleep(x)


def draw_board(ai, prespot):
    yloc = 20
    xloc = 20
    if prespot:
        ai.clear_board()
        if ai.hit:
            for ship in ai.ships:
                ai.spotship(ship, ai.yloc, ai.xloc, ai.horizontal, ai.vertical)
        else:
            for ship in ai.ships:
                ai.spotcheck(ship)
        if ai.name == "ai1":
            yloc, xloc = ai.fire_prob(ai2, False)
        elif ai.name == "ai2":
            yloc, xloc = ai.fire_prob(ai1, False)
    value = 0
    block_size = Screen_Width / (2 * battleship_ai.BoardLength) - 20  # Set the size of the grid block
    for x in range(0, battleship_ai.BoardWidth):
        for y in range(0, battleship_ai.BoardLength):
            rect = pygame.Rect(ai.gridpos + (block_size + 10) * x, y * (block_size + 10) + block_size, block_size,
                               block_size)
            if ai.Board[y][x] > value:
                value = ai.Board[y][x]
            if ai.Board[y][x] == -1 or ai.Board[y][x] == 0:
                pygame.draw.rect(screen, (0, 0, 0), rect)
            elif ai.Board[y][x] == -2:
                pygame.draw.rect(screen, (0, 100, 0), rect)
            else:
                pygame.draw.rect(screen, (255 * ai.Board[y][x] / (value), 0, 0), rect)
    pygame.display.update()
    if prespot:
        Wait(1)
        for x in range(0, battleship_ai.BoardWidth):
            for y in range(0, battleship_ai.BoardLength):
                if y == yloc and x == xloc:
                    rect = pygame.Rect(ai.gridpos + (block_size + 10) * x, y * (block_size + 10) + block_size,
                                       block_size,
                                       block_size)
                    pygame.draw.rect(screen, (255, 0, 255), rect)
        pygame.display.update()


def draw_placement(ai, notinitial):
    block_size = Screen_Width / (2 * battleship_ai.BoardLength) - 20  # Set the size of the grid block
    for x in range(0, battleship_ai.BoardWidth):
        for y in range(0, battleship_ai.BoardLength):
            rect = pygame.Rect(ai.gridpos + (block_size + 10) * x, y * (block_size + 10) + 650, block_size,
                               block_size)
            if ai.Placement[y][x] == -2:
                pygame.draw.rect(screen, (0, 0, 200), rect)
            elif ai.Placement[y][x] == -3:
                pygame.draw.rect(screen, (200, 0, 0), rect)
            else:
                pygame.draw.rect(screen, (80, 80, 120), rect)
    if notinitial:
        pygame.display.update()


def runai():
    game_over = False
    end_display = False

    ai1.place_ships()
    ai2.place_ships()
    draw_placement(ai1, False)
    Draw_initial_Grid(ai1)
    draw_placement(ai2, False)
    Draw_initial_Grid(ai2)
    pygame.display.update()
    i = 0
    Wait(1)
    while not end_display:
        if not game_over:
            i += 1
            draw_board(ai1, True)
            Wait(1)
            ai1.take_turn(ai2)
            draw_board(ai1, False)
            draw_placement(ai2, True)
            if ai2.game_over():
                print("ai1 won")
                game_over = True
            Wait(1)
            if not game_over:
                draw_board(ai2, True)
                Wait(1)
                ai2.take_turn(ai1)
                draw_board(ai2, False)
                draw_placement(ai1, True)
                if ai1.game_over():
                    print("ai2 won")
                    game_over = True
                Wait(1)

        else:
            draw_placement(ai1, True)
            draw_board(ai1, False)
            draw_placement(ai2, True)
            draw_board(ai2, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_display = True

    print(f"i = {i}")


runai()
