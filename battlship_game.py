import random
import time
import pygame
import battleship_ai

random.seed(0)

Screen_Width = 1200
Screen_Height = 1200

wait = False

screen = pygame.display.set_mode((Screen_Width, Screen_Height))
screen.fill((50, 50, 80))

griddist = Screen_Width / (3 * battleship_ai.BoardLength)

ai1 = battleship_ai.Ai("ai1", griddist)
ai2 = battleship_ai.Ai("ai2", Screen_Width - ((battleship_ai.BoardWidth) * 1.25 * griddist))
player1 = battleship_ai.Player("player1", griddist)
player2 = battleship_ai.Player("player2", Screen_Width - (battleship_ai.BoardWidth * griddist))

battleship_ai.BoardWidth = 10
battleship_ai.BoardLength = 10

pvp = False
pva = True
ava = False

pygame.init()


def Draw_grid_player(player):
    block_size = Screen_Width / (3 * battleship_ai.BoardLength)  # Set the size of the grid block
    for x in range(0, battleship_ai.BoardWidth):
        for y in range(0, battleship_ai.BoardLength):
            rect = pygame.Rect(player.gridpos + (1.25 * block_size) * x,
                               y * (block_size + 10) + block_size, block_size,
                               block_size)
            if player.Board[y][x] == -2:
                pygame.draw.rect(screen, (100, 0, 0), rect)
            elif player.Board[y][x] == -1:
                pygame.draw.rect(screen, (0, 0, 0), rect)
            else:
                pygame.draw.rect(screen, (0, 0, 150), rect)
    pygame.display.update()


def Draw_placement_player(player):
    block_size = Screen_Width / (2 * battleship_ai.BoardLength) - 20  # Set the size of the grid block
    for x in range(0, battleship_ai.BoardWidth):
        for y in range(0, battleship_ai.BoardLength):
            rect = pygame.Rect(player.gridpos + (block_size + 10) * x,
                               y * (block_size + 10) + 650, block_size,
                               block_size)
            if player.Placement[y][x] == -2:
                pygame.draw.rect(screen, (0, 0, 200), rect)
            elif player.Placement[y][x] == -3:
                pygame.draw.rect(screen, (200, 0, 0), rect)
            else:
                pygame.draw.rect(screen, (80, 80, 120), rect)
    pygame.display.update()


def Draw_initial_Grid_ai(ai):
    for ship in ai.ships:
        ai.spotcheck(ship)
    value = 0
    block_size = Screen_Width / (2 * battleship_ai.BoardLength) - 20  # Set the size of the grid block
    for x in range(0, battleship_ai.BoardWidth):
        for y in range(0, battleship_ai.BoardLength):
            rect = pygame.Rect(ai.gridpos + (block_size + 10) * x,
                               y * (block_size + 10) + block_size, block_size,
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


def Wait(x):
    if wait:
        time.sleep(x)


def draw_board_ai(ai, prespot):
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


def draw_placement_ai(ai, notinitial):
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
    if ava:
        ai1.place_ships()
        ai2.place_ships()
        draw_placement_ai(ai1, False)
        Draw_initial_Grid_ai(ai1)
        draw_placement_ai(ai2, False)
        Draw_initial_Grid_ai(ai2)
    elif pva:
        for ship in player1.shipsalive:
            player1.place_ship(ship)
            Draw_placement_player(player1)
        Draw_placement_player(player1)
        Draw_grid_player(player1)
        ai2.place_ships()
        draw_placement_ai(ai2, False)
        Draw_initial_Grid_ai(ai2)
    else:
        for ship in player1.shipsalive:
            player1.place_ship(ship)
            Draw_placement_player(player1)
        Draw_grid_player(player1)
        for ship in player2.shipsalive:
            player2.place_ship(ship)
            Draw_placement_player(player2)
        Draw_grid_player(player2)
    pygame.display.update()
    i = 0
    Wait(1)
    while not end_display:
        if not game_over:
            i += 1
            if ava:
                draw_board_ai(ai1, True)
                Wait(1)
                ai1.take_turn(ai2)
                draw_board_ai(ai1, False)
                draw_placement_ai(ai2, True)
                if ai2.game_over():
                    print("ai1 won")
                    game_over = True
                Wait(1)
                if not game_over:
                    draw_board_ai(ai2, True)
                    Wait(1)
                    ai2.take_turn(ai1)
                    draw_board_ai(ai2, False)
                    draw_placement_ai(ai1, True)
                    if ai1.game_over():
                        print("ai2 won")
                        game_over = True
                    Wait(1)

                else:
                    draw_placement_ai(ai1, True)
                    draw_board_ai(ai1, False)
                    draw_placement_ai(ai2, True)
                    draw_board_ai(ai2, False)
            elif pva:
                Draw_grid_player(player1)
                player1.take_turn(ai2)
                Draw_grid_player(player1)
                draw_placement_ai(ai2, True)
                if ai2.game_over():
                    print("player1 won")
                    game_over = True
                Wait(1)
                if not game_over:
                    draw_board_ai(ai2, True)
                    Wait(1)
                    ai2.take_turn(player1)
                    draw_board_ai(ai2, False)
                    draw_placement_ai(player1, True)
                    if player1.game_over():
                        print("ai2 won")
                        game_over = True
                    Wait(1)

                else:
                    Draw_grid_player(player1)
                    Draw_placement_player(player1)
                    draw_placement_ai(ai2, True)
                    draw_board_ai(ai2, False)
            else:
                Draw_grid_player(player1)
                player1.take_turn(player2)
                Draw_grid_player(player1)
                Draw_placement_player(player2)
                if player2.game_over():
                    print("player1 won")
                    game_over = True
                if not game_over:
                    Draw_grid_player(player2)
                    player2.take_turn(player1)
                    Draw_grid_player(player2)
                    Draw_placement_player(player1)
                    if player1.game_over():
                        print("player2 won")
                        game_over = True
                else:
                    Draw_grid_player(player1)
                    Draw_placement_player(player1)
                    Draw_grid_player(player2)
                    Draw_placement_player(player2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_display = True

    print(f"i = {i}")


runai()
