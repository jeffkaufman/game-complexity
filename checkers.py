board = [' w w w w',
         'w w w w ',
         ' w w w w',
         '. . . . ',
         ' . . . .',
         'b b b b ',
         ' b b b b',
         'b b b b ']
board = [list(row) for row in board]

def valid(x, y):
  return x >= 0 and x < 8 and y >= 0 and y < 8

def print_board():
  for row in board:
    print row

def color_at(x, y):
  return board[x][y].lower()

def empty(x, y):
  return board[x][y] == "."

def king(x, y):
  return board[x][y] in ['W', 'B']

def direction(color):
  return 1 if color == 'w' else -1

def adjacent(x, y, distance):
  dn = direction(color_at(x, y))
  assert distance in [1, 2]
  def h(forwards):
    assert forwards in [-1, 1]
    return [(xv,yv) for (xv,yv) in [(x + (dn * forwards * distance), y+distance),
                                    (x + (dn * forwards * distance), y-distance)]
            if valid(xv,yv)]
  return h(1) + (h(-1) if king(x,y) else [])

def apply_move(color, x_start, y_start, x_end, y_end, x_jumped_to, y_jumped_to):
  def actually_apply_move():
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
  if x_jumped_to != None:
    if x_start != x_jumped_to or y_start != y_jumped_to:
      return "continuing after a jump with the wrong token"
  if (x_end, y_end) in adjacent(x_start, y_start, 1):
    if x_jumped_to != None:
      return "continuing after a jump without another jump"
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

def turn(color):
  jumped_to = None, None
  while True:
    print_board()
    choice = raw_input(color + " > ")
    if jumped_to[0] != None and choice == "pass":
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

def game():
  while True:
    turn("b")
    turn("w")
game()
