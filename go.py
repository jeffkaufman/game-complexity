# The board is a 19x19 list of lists.  Each element can be a character,
# 'b', 'w', or ' ' for "black", "white", and "empty".
board = []
for x in range (19):
  board.append([])
  for y in range(19):
    board[-1].append(' ')
past_boards = []

# Check if a point is on the board.
def valid(x, y):
  return 0 <= x < 19 and 0 <= y < 19

# Return all points on the board adjacent to a given point.
def adjacent(x, y):
  return [(xv, yv)
          for xv, yv in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
          if valid(xv, yv)]

# Add a board to the list of past board we use for checking that we've
# not got stuck in a loop.
def save_board():
  past_boards.append([])
  for row in board:
    past_boards[-1].append(row[:])

def print_board():
  for row in board:
    print "".join(row)

# Tromp: "A point P, not colored C, is said to reach C, if there is a
# path of (vertically or # horizontally) adjacent points of P's color
# from P to a point of color C."
#
# If a piece reaches "empty" then it has a liberty and can stay on the
# board.  If an empty space reaches only pieces of one color, that's
# territory of that color.
#
# Calculated recursively, with visited keeping track of where we've
# been.
def reach(x, y, target):
  color = board[x][y]
  visited = set()
  def helper(xh, yh):
    if (xh, yh) in visited:
      return False
    visited.add((xh, yh))
    if board[xh][yh] == target:
      return True
    if board[xh][yh] == color:
      for xv, yv in adjacent(xh, yh):
        if helper(xv, yv):
          return True
    return False
  return helper(x, y)

# Point x,y scores for black if it only reaches black, white if it only
# reaches white, otherwise neither.  Return ' ', 'b', or 'w' as
# appropriate.
def score_for(x, y):
  if board[x][y] == ' ':
    reaches_b = reach(x, y, 'b')
    reaches_w = reach(x, y, 'w')
    if reaches_b and reaches_w:
      return ' '
    if reaches_b:
      return 'b'
    if reaches_w:
      return 'w'
    return ' '
  return board[x][y]

# Consider every space on the board and determine whether it counts for
# black, white, or neither.  Following Tromp, uses area scoring
# (Chinese).
def score():
  scores = { ' ':0, 'b':0, 'w':0 }
  for x in range(19):
    for y in range(19):
      scores[score_for(x, y)] += 1
  if scores['b'] == scores['w']:
    print "tie"
  elif scores['b'] > scores['w']:
    print "b wins"
  else:
    print "w wins"

# Remove point x,y and the rest of its same-color group.
def clear(x, y):
  color = board[x][y]
  def helper(xh, yh):
    if board[xh][yh] != color:
      return
    board[xh][yh] = ' '
    for xv, yv in adjacent(xh, yh):
      helper(xv, yv)
  helper(x, y)

def opponent(color):
  return 'b' if color == 'w' else 'w'

# Consider every point on the board and if it's the specified color and
# has no liberties, remove the whole group.
def check_clearing(color):
  for x in range(19):
    for y in range(19):
      if board[x][y] == color:
        if not reach(x, y, " "):
          clear(x, y)

# Have we been here before?
def repeat_board():
  return board in past_boards

# Ask the user to choose a place to play, update the board for their
# choice, return True if they passed.
def turn(color):
  print_board()
  x, y = None, None
  while True:
    choice = raw_input(color + " > ")
    if choice == "pass":
      return True
    try:    
      x_s, y_s = choice.strip().split()
      x, y = int(x_s), int(y_s)
    except ValueError:
      print "give x and y coordinates separated by a space: 0 3"
      print "or write pass"
      continue
    if not valid(x, y):
      print "out of bounds"
      continue
    if board[x][y] != ' ':
      print "not empty [%s, %s]=%s" % (x, y, board[x][y])
      continue
    break
  save_board()
  board[x][y] = color
  check_clearing(opponent(color))
  check_clearing(color)
  if repeat_board():
    raise Exception("%s repeated a past board, and loses" % color)
  return False

# Alternate turns until both players pass, then score the game and
# declare a winner.
def game():
  b_passed = False
  w_passed = False
  while not b_passed or not w_passed:
    b_passed = turn('b')
    if not b_passed or not w_passed:
      w_passed = turn('w')
  score()

game()
