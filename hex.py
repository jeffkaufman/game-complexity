# The board is a list of lists with:
#
#  abc
#  def
#  ghi
#
# representing:
#   _   _   _
#  /a\_/b\_/c\_
#  \_/d\_/e\_/f\_
#    \_/g\_/h\_/i\
#      \_/ \_/ \_/
#
# Adjacencies are up, down, up-right, and down-left.
import sys
SIZE = 2
board = []
moves = [0]
for x in range(SIZE):
  board.append([])
  for y in range(SIZE):
    board[-1].append(' ')

# Is this point on the board?
def valid(x, y):
  return 0 <= x < SIZE and 0 <= y < SIZE

def adjacent(x, y):
  return [(x, y)
          for (x, y) in [(x+1, y), (x-1, y), (x-1, y+1), (x+1, y-1)]
          if valid(x,y)]

# Draws the board.  I'm lazy and didn't want to take the time to make it accurate so 
def print_board():
  for x, row in enumerate(board):
    for i in range(x):
      sys.stdout.write("  ")
    for y in range(SIZE):
      sys.stdout.write("/" + board[x][y] + "\_")
    sys.stdout.write("\n")

# After playing in x,y, does color win?  Consider recursive paths
# through that color out of this point and count a winner if they
# connect along the x axis (b) or y axis (w)
def winner(x, y, color):
  reached = [False, False] # max, min
  visited = set()
  def helper(xs, ys):
    if board[xs][ys] != color:
      return
    if (xs, ys) in visited:
      return
    visited.add((xs, ys))
    consider = xs if color == 'b' else ys
    if consider == SIZE-1:
      reached[0] = True
    if consider == 0:
      reached[1] = True
    for (xc, yc) in adjacent(xs, ys):
      helper(xc, yc)
  helper(x, y)
  return reached[0] and reached[1]

def turn(color):
  print_board()
  while True:
    choice = raw_input(color + " > ")
    try:
      x, y = choice.split()
      x, y = int(x), int(y)
    except ValueError:
      print "give x y to play"
      continue
    if not valid(x, y):
      print "position not on board, try again"
      continue
    if board[x][y] != ' ':
      print "position not empty, try again"
      continue
    board[x][y] = color
    moves[0] += 1
    if winner(x, y, color):
      print_board()
      raise Exception(color + " wins")
    if moves[0] == SIZE*SIZE:
      raise Exception("board filled: draw")
    break
    
def game():
  while True:
    turn('b')
    turn('w')
game()
