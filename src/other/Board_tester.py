from Board import Board

my_board = Board()
my_board.print_board()
my_board.make_move([1, 4], [3, 4])
my_board.print_board()
my_board.make_move([7, 6], [5, 5])
my_board.print_board()
my_board.make_move([1, 3], [3, 3])
my_board.print_board()
my_board.make_move([5, 5], [3, 4])
my_board.print_board()
my_board.make_move([3, 3], [4, 3])
my_board.print_board()
my_board.make_move([6, 4], [4, 4])
my_board.print_board()
my_board.make_move([4, 3], [5, 4])
my_board.print_board()
my_board.make_move([7, 3], [3, 7])
my_board.print_board()
my_board.make_move([5, 4], [6, 5])
my_board.print_board()


possible_moves = my_board.get_all_moves(my_board.BLACK)

print(possible_moves)

for move in possible_moves:
    move[1].print_board()