import sys, numpy

winLength = 5
whites = []
blacks = []
white = 'O'
black = 'X'

def setColors(board, positions, color, minX, minY):
    for position in positions:
        board[(len(board) - 1) -
                (position[1] - minY)][position[0] - minX] = color

def first(x):
    return x[0]

def last(x):
    return x[-1]

# Draws the board.
def print_board():
    allStones = blacks + whites
    if allStones:
        minX = min(map(first, allStones))
        minY = min(map(last, allStones))
        maxX = max(map(first, allStones))
        maxY = max(map(last, allStones))
        board = numpy.full((maxY -
                minY + 1, maxX -
                minX + 1), " ", dtype=str)
        setColors(board, whites, white, minX, minY)
        setColors(board, blacks, black, minX, minY)
        i=maxY
        sys.stdout.write("\n")
        for row in board:
            sys.stdout.write(str(i))
            for space in row:
                sys.stdout.write("\t" + space)
            i-= 1
            sys.stdout.write("\n")
        for j in range(minX, maxX + 1):
            sys.stdout.write("\t" + str(j))
        print("\n")

# Takes a stone position, a list of other stones (assumed to be of the
# same color), and an offset direction, and finds the index where
# the stones stop being there.
def outer((moveX, moveY), stones, (directionX, directionY)):
    if (moveX, moveY) in stones:
        return outer((moveX + directionX, moveY + directionY),
                stones, (directionX, directionY))
    if directionX:
        return moveX
    return moveY

# Four directions that stones can move in.  The oposites of these four
# are determined and taken into account when finding row lengths.
directions = ((0,1),(1,0),(1,1),(-1,1))

# After playing in move (x,y), does color win?  Recursively looks down
# a row of the player's colored stones in two directions to determine whether
# the difference between them is greater than or equal to five.
def winner(move, stones):
    for (directionX, directionY) in directions:
        if (outer(move, stones, (directionX, directionY)) - outer(move, stones,
                (-directionX, -directionY)) - 1 >= winLength):
            return True
    return False

def turn(color, playerStones):
    print_board()
    while True:
        choice = raw_input(color + " > ")
        try:
            x, y = choice.split()
            move = (int(x), int(y))
        except ValueError:
            print "give x y to play"
            continue
        # the block following comment checks whether the move overlaps a
        # previous move
        if move in blacks + whites:
            print "position not empty, try again"
            continue
        playerStones.append(move)
        if winner(move, playerStones):
            print_board()
            raise Exception(color + " wins")
        # no need to check if the board is full, because the board
        # essentially CAN'T be filled
        break
        
def game():
    while True:
        turn(black, blacks)
        turn(white, whites)
game()
