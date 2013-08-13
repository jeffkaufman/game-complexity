board = []
scores = {'w':0,'b':0}
SIZE=2
for x in range(SIZE*2+2):
  board.append([])
  for y in range(SIZE*2+2):
    board[-1].append(" ")

def print_board():
  for row in board:
    print "".join(row)

def valid(x,y):
  return 0 <= x < SIZE and 0 <= y < SIZE

def apply_move(color, x_start, y_start, x_end, y_end):
  if not valid(x_start, y_start) :
    return "bad start coordinates"
  if not valid(x_end, y_end):
    return "bad end coordinates"
    
  if x_start > x_end:
    x_start, x_end = x_end, x_start
  if y_start > y_end:
    y_start, y_end = y_end, y_start

  if x_start == x_end and y_end == y_start + 1:
    board_x = 2 * x_start
    board_y = 2 * y_start + 1
    ch = '-'
  elif y_start == y_end and x_end == x_start + 1:
    board_x = 2 * x_start + 1
    board_y = 2 * y_start
    ch = '|'
  else:
    return "those points aren't adjacent"

  if board[board_x][board_y] != ' ':
    return "that spot is occupied"

  board[board_x][board_y] = ch

  def check_surrounded(x, y):
    if surrounded(x, y):
      board[x][y] = color # optional
      scores[color] += 1
      return True
    return False

  if ((ch == '-' and (check_surrounded(board_x + 1, board_y) or
                      check_surrounded(board_x - 1, board_y))) or
      (ch == '|' and (check_surrounded(board_x, board_y + 1) or
                      check_surrounded(board_x, board_y - 1)))):
    return "again"
  return "done"

def surrounded(x, y):
  for xs, ys in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
    if xs < 0 or ys < 0 or xs > SIZE*2+2 or ys > SIZE*2+2:
      return False
    if board[xs][ys] == ' ':
      return False
  return True

def turn(color):
  while True:
    print_board()
    if scores['w'] + scores['b'] == (SIZE-1)*(SIZE-1):
      winner = "tie"
      if scores['w'] > scores['b']:
        winner = 'w'
      if scores['b'] > scores['w']:
        winner = 'b'
      raise Exception(winner + " wins")
    choice = raw_input(color + " > ")
    try:
      x_start, y_start, x_end, y_end = [int(val) for val in choice.split()]
    except ValueError:
      print "give x_start, y_start, x_end, y_end"
      continue
    response = apply_move(color, x_start, y_start, x_end, y_end)
    if response == "again":
      continue
    if response == "done":
      break
    print response

def game():
  while True:
    turn("w")
    turn("b")
game()
