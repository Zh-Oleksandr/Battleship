import random

BoardLength = 10
BoardWidth = 10
directions = ["Up", "Down", "Left", "Right"]

shipscantouch = False


class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.columns = []
        self.rows = []


class Ai:
    def __init__(self, name, gridpos):
        self.gridpos = gridpos
        self.name = name
        self.shipsunk = ""
        self.sunk = False
        self.hit = False
        self.horizontal = False
        self.vertical = False
        self.yloc = 0
        self.xloc = 0

        self.Carrier = Ship("Carrier", 5)
        self.Battleship = Ship("Battleship", 4)
        self.Destroyer = Ship("Destroyer", 3)
        self.Submarine = Ship("Submarine", 3)
        self.Boat = Ship("Boat", 2)

        self.Board = [[0] * BoardWidth for _ in range(BoardLength)]

        self.Placement = [[0] * BoardWidth for _ in range(BoardLength)]

        self.Columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        self.ships = [self.Carrier, self.Battleship, self.Destroyer, self.Submarine, self.Boat]

        self.shipsalive = [self.Carrier, self.Battleship, self.Destroyer, self.Submarine, self.Boat]

    def place_ship(self, ship):
        # Finding a random point and direction to place the ship on
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        direction = random.choice(directions)
        # Checking if it will fit with the point and direction giveb
        for i in range(0, ship.length):
            pos = True
            if direction == "Up":
                if y - ship.length + 1 >= 0:
                    if (self.Placement[y - i][x] == -2) or (self.Placement[y - i][x] == -1):
                        pos = False
                        break
                else:
                    pos = False
                    break

            elif direction == "Down":
                if y + ship.length <= BoardLength:
                    if self.Placement[y + i][x] == -2 or self.Placement[y + i][x] == -1:
                        pos = False
                        break
                else:
                    pos = False
                    break


            elif direction == "Left":
                if x - ship.length + 1 >= 0:
                    if self.Placement[y][x - i] == -2 or self.Placement[y][x - i] == -1:
                        pos = False
                        break
                else:
                    pos = False
                    break

            elif direction == "Right":
                if x + ship.length <= BoardWidth:
                    if self.Placement[y][x + i] == -2 or self.Placement[y][x + i] == -1:
                        pos = False
                        break
                else:
                    pos = False
                    break

        if pos:
            # Placing the ships and setting the remaining edges to non placement
            for i in range(0, ship.length):
                if direction == "Up":
                    self.Placement[y - i][x] = -2
                    ship.columns.append(x + 1)
                    ship.rows.append(self.Columns[y - i])
                if direction == "Down":
                    self.Placement[y + i][x] = -2
                    ship.columns.append(x + 1)
                    ship.rows.append(self.Columns[y + i])
                if direction == "Left":
                    self.Placement[y][x - i] = -2
                    ship.columns.append(x - i + 1)
                    ship.rows.append(self.Columns[y])
                if direction == "Right":
                    self.Placement[y][x + i] = -2
                    ship.columns.append(x + i + 1)
                    ship.rows.append(self.Columns[y])
            # setting the edges to not palcement
            if not shipscantouch:
                for y in range(BoardLength):
                    for x in range(BoardWidth):
                        if self.Placement[y][x] == -2:
                            if x + 1 != BoardWidth:
                                if self.Placement[y][x + 1] != -2:
                                    self.Placement[y][x + 1] = -1
                            if x - 1 != -1:
                                if self.Placement[y][x - 1] != -2:
                                    self.Placement[y][x - 1] = -1
                            if y + 1 != BoardWidth:
                                if self.Placement[y + 1][x] != -2:
                                    self.Placement[y + 1][x] = -1
                            if y - 1 != BoardWidth:
                                if self.Placement[y - 1][x] != -2:
                                    self.Placement[y - 1][x] = -1

        else:
            # if the ship don't fit with the directions, do it all again
            self.place_ship(ship)

    def spotcheck(self, ship):
        for y in range(BoardLength):
            for x in range(BoardWidth):
                # Check for X
                for i in range(ship.length):
                    fits = True
                    if x + i >= BoardWidth:
                        fits = False
                        break
                    elif (self.Board[y][x + i] == -1 or self.Board[y][x + i] == -2):
                        fits = False
                        break

                if fits:
                    for spotx in range(ship.length):
                        self.Board[y][x + spotx] += 1
                    # Check for Y
                for i in range(ship.length):
                    fits = True
                    if y + i >= BoardLength:
                        fits = False
                        break
                    elif (self.Board[y + i][x] == -1 or self.Board[y + i][x] == -2):
                        fits = False
                        break

                if fits:
                    for spoty in range(ship.length):
                        self.Board[y + spoty][x] += 1

    def spotship(self, ship, locy, locx, horizontal, vertical):
        # Check for X
        if not vertical:
            for x in range(locx - ship.length + 1, locx + 1):
                fits = True
                if (x < 0):
                    fits = False
                    continue
                elif (x + ship.length > 10):
                    fits = False
                    break
                else:
                    for i in range(ship.length):
                        if x + i >= BoardWidth:
                            fits = False
                            break
                        elif (self.Board[locy][x + i] == -1):
                            fits = False
                            break

                    if fits:
                        for spotx in range(ship.length):
                            if self.Board[locy][x + spotx] != -2:
                                self.Board[locy][x + spotx] += 1
        # Check for Y
        if not horizontal:
            for y in range(locy - ship.length + 1, locy + 1):
                fits = True
                if (y < 0):
                    fits = False
                    continue
                elif (y + ship.length > 10):
                    fits = False
                    break
                else:
                    for i in range(ship.length):
                        if y + i >= BoardLength:
                            fits = False
                            break
                        elif (self.Board[y + i][locx] == -1):
                            fits = False
                            break

                    if fits:
                        for spoty in range(ship.length):
                            if self.Board[y + spoty][locx] != -2:
                                self.Board[y + spoty][locx] += 1

    def fire_prob(self, ai, notdraw):
        firex = 20
        firey = 20
        value = 0
        # Finding the most probable point
        if self.hit:
            for y in range(BoardLength):
                for x in range(BoardWidth):
                    if self.Board[y][x] > value:
                        if (y - 1 != -1):
                            if (self.Board[y - 1][x] == -2):
                                value = self.Board[y][x]
                                firex = x
                                firey = y
                        if (y + 1 != BoardLength):
                            if (self.Board[y + 1][x] == -2):
                                value = self.Board[y][x]
                                firex = x
                                firey = y
                        if (x + 1 != BoardWidth):
                            if (self.Board[y][x + 1] == -2):
                                value = self.Board[y][x]
                                firex = x
                                firey = y
                        if (x - 1 != -1):
                            if (self.Board[y][x - 1] == -2):
                                value = self.Board[y][x]
                                firex = x
                                firey = y
        else:
            for y in range(BoardLength):
                for x in range(BoardWidth):
                    if self.Board[y][x] > value:
                        value = self.Board[y][x]
                        firex = x
                        firey = y

        if notdraw:
            shoton = self.Columns[firey] + str(firex + 1)

            hit = ai.player_fire(shoton)
            # self.print_board()
            # If hit or miss
            if hit:
                self.Board[firey][firex] = -2
            else:
                self.Board[firey][firex] = -1
            return hit, firey, firex
        else:
            return firey, firex

    def player_fire(self, shoton):
        hit = False
        row = "".join(c for c in shoton if c.isalpha())
        column = int("".join(c for c in shoton if c.isdecimal()))
        for ship in self.shipsalive:
            for i in range(len(ship.rows)):
                if ship.columns[i] == column and ship.rows[i] == row:
                    hit = True
                    ship.rows.remove(row)
                    ship.columns.remove(column)
                    self.Placement[self.Columns.index(row)][column - 1] = -3
                    break
        if hit:
            return True
        else:
            return False

    def print_board(self):
        print("")
        print(self.name)
        print("")
        for y in range(BoardLength):
            print(self.Board[y])

    def print_placement(self):
        print("")
        print(self.name)
        print("")
        for y in range(BoardLength):
            print(self.Placement[y])

    def clear_board(self):
        for y in range(BoardLength):
            for x in range(BoardWidth):
                if self.Board[y][x] != -1 and self.Board[y][x] != -2:
                    self.Board[y][x] = 0

    def place_ships(self):
        for ship in self.shipsalive:
            self.place_ship(ship)

    def game_over(self):
        for ship in self.shipsalive:
            if len(ship.rows) == 0:
                self.shipsalive.remove(ship)
        if len(self.shipsalive) == 0:
            return True
        return False

    def take_turn(self, ai):
        self.clear_board()
        if self.hit:
            for ship in self.ships:
                self.spotship(ship, self.yloc, self.xloc, self.horizontal, self.vertical)
            hittest, firey, firex = self.fire_prob(ai, True)
            if hittest:
                prevy = self.yloc
                prevx = self.xloc
                self.yloc = firey
                self.xloc = firex
                if not shipscantouch:
                    if self.xloc == prevx and (self.yloc == prevy + 1 or self.yloc == prevy - 1):
                        self.vertical = True
                    elif prevy == self.yloc and (self.xloc == prevx + 1 or self.xloc == prevx - 1):
                        self.horizontal = True
                for ship in ai.shipsalive:
                    if len(ship.rows) == 0:
                        self.shipsunk = ship.name
                        self.sunk = True
                if self.sunk:
                    self.hit = False
                    self.vertical = False
                    self.horizontal = False
                    if not shipscantouch:
                        for y in range(BoardLength):
                            for x in range(BoardWidth):
                                if self.Board[y][x] == -2:
                                    if x + 1 != BoardWidth:
                                        if self.Board[y][x + 1] != -2:
                                            self.Board[y][x + 1] = -1
                                    if x - 1 != -1:
                                        if self.Board[y][x - 1] != -2:
                                            self.Board[y][x - 1] = -1
                                    if y + 1 != BoardWidth:
                                        if self.Board[y + 1][x] != -2:
                                            self.Board[y + 1][x] = -1
                                    if y - 1 != -1:
                                        if self.Board[y - 1][x] != -2:
                                            self.Board[y - 1][x] = -1
                for ship in self.ships:
                    if ship.name == self.shipsunk:
                        self.ships.remove(ship)
                self.sunk = False
        else:
            for ship in self.ships:
                self.spotcheck(ship)
            self.hit, self.yloc, self.xloc = self.fire_prob(ai, True)
            if self.hit:
                for ship in ai.shipsalive:
                    if len(ship.rows) == 0:
                        self.shipsunk = ship.name
                        self.sunk = True
                if self.sunk:
                    self.hit = False
                    self.vertical = False
                    self.horizontal = False
                    for y in range(BoardLength):
                        for x in range(BoardWidth):
                            if self.Board[y][x] == -2:
                                if x + 1 != BoardWidth:
                                    if self.Board[y][x + 1] != -2:
                                        self.Board[y][x + 1] = -1
                                if x - 1 != -1:
                                    if self.Board[y][x - 1] != -2:
                                        self.Board[y][x - 1] = -1
                                if y + 1 != BoardWidth:
                                    if self.Board[y + 1][x] != -2:
                                        self.Board[y + 1][x] = -1
                                if y - 1 != -1:
                                    if self.Board[y - 1][x] != -2:
                                        self.Board[y - 1][x] = -1
                for ship in self.ships:
                    if ship.name == self.shipsunk:
                        self.ships.remove(ship)
                self.sunk = False
