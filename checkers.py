# The board is a list of lists, with 'b' for black pieces, 'w' for white
# pieces, '.' for empty spaces, and ' ' for non-spaces.  Capital letters
# are used for kings.
board = [' w w w w',
         'w w w w ',
         ' w w w w',
         '. . . . ',
         ' . . . .',
         'b b b b ',
         ' b b b b',
         'b b b b ']
board = [list(row) for row in board]

# Is the point on the board?
def valid(x, y):
  return x >= 0 and x < 8 and y >= 0 and y < 8

def print_board():
  for row in board:
    print "".join(row)

# Can't just use board[x][y] because of kings.
def color_at(x, y):
  return board[x][y].lower()

def empty(x, y):
  return board[x][y] == "."

def king(x, y):
  return board[x][y] in ['W', 'B']

# White moves towards higher numbered rows, Black towards lower.
def direction(color):
  return 1 if color == 'w' else -1

# Returns a list of all points adjacent to the piece at (x, y), taking
# into account its direction of movement and whether it's a king.  Use
# distance=1 normally, 2 for jumps.
def adjacent(x, y, distance):
  dn = direction(color_at(x, y))
  assert distance in [1, 2]
  def h(forwards):
    assert forwards in [-1, 1]
    return [(xv,yv) for (xv,yv) in [(x + (dn * forwards * distance), y+distance),
                                    (x + (dn * forwards * distance), y-distance)]
            if valid(xv,yv)]
  return h(1) + (h(-1) if king(x,y) else [])

# Is there a jump out there that this player could take?  Needed to
# enforce the rule that you must take jumps.  I chose the simplest
# version of this rule; some rulesets require you to make the set of
# jumps that has the highest value.
def exists_jump(color):
  for xs in range(8):
    for ys in range(8):
      if color_at(xs, ys) == color:
        for xe, ye in adjacent(xs, ys, 2):
          if empty(xe, ye):
            jumped_over_x = (xs+xe)/2
            jumped_over_y = (ys+ye)/2
            if color_at(jumped_over_x, jumped_over_y) not in [color, '.']:
              return True
  return False

# When we know where the person is trying to move, check if that's
# legal, then update the board on the effects of the move.  Returns
# "jump" if the move was good and made a jump, "single" if the move was
# good and normal, and an error string otherwise.
def apply_move(color, x_start, y_start, x_end, y_end, x_jumped_to, y_jumped_to):
  def actually_apply_move():
    # The move is legitamate, and we need to update the board.  Deals
    # with kinging.
    board[x_end][y_end] = board[x_start][y_start]
    board[x_start][y_start] = '.'
    if color == 'w' and x_end == 7:
      board[x_end][y_end] = 'W'
    if color == 'b' and x_end == 0:
      board[x_end][y_end] = 'B'

  if not valid(x_start, y_start) :
    return "bad start coordinates"
  if not valid(x_end, y_end):
    return "bad end coordinates"
  if color_at(x_start, y_start) != color:
    return "no %s piece at (%s, %s), found '%s'" % (
        color, x_start, y_start, board[x_start][y_start])
  if board[x_end][y_end] == ' ':
    return "(%s, %s) not a legal space" % (x_end, y_end)
  if not empty(x_end, y_end):
    return "(%s, %s) not empty; found '%s'" % (
        x_end, y_end, board[x_end][y_end])
  if x_jumped_to != None: # the previous move was a jump
    if x_start != x_jumped_to or y_start != y_jumped_to:
      return "continuing after a jump with the wrong token"
  if (x_end, y_end) in adjacent(x_start, y_start, 1):
    if x_jumped_to != None: # the previous move was a jump
      return "continuing after a jump without another jump"
    if exists_jump(color):
      return "must take jump"
    actually_apply_move()
    return "single"
  if (x_end, y_end) in adjacent(x_start, y_start, 2):
    jumped_over_x = (x_start + x_end)/2
    jumped_over_y = (y_start + y_end)/2
    if color_at(jumped_over_x, jumped_over_y) in [color, '.']:
      return "must jump over opponent to jump"
    board[jumped_over_x][jumped_over_y] = '.'
    actually_apply_move()
    return "jump"
  return "not adjacent"

# Ask the user for a move, make sure its valid, apply the move, repeat
# if they're entitled to go again (continuing a sequence of jumps).
def turn(color):
  jumped_to = None, None
  while True:
    print_board()
    choice = raw_input(color + " > ")
    if jumped_to[0] != None and choice == "pass" and not exists_jump(color):
      break
    if choice == "resign":
      raise Exception(color + " resigned and loses")
    try:
      x_start, y_start, x_end, y_end = [int(val) for val in choice.split()]
    except ValueError:
      print "give x_start, y_start, x_end, y_end"
      print "or write resign"
      print "or write pass after jumping"
      continue
    response = apply_move(color, x_start, y_start, x_end, y_end, *jumped_to)
    if response == "jump":
      jumped_to = x_end, y_end
    elif response == "single":
      break
    else:
      print "not legal:", response

# Alternate turns until someone resigns due to having no legal move
# (including no pieces).
def game():
  while True:
    turn("b")
    turn("w")
game()
