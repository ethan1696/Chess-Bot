import sys
sys.path.append("../board_simulator")
sys.path.append("../engines")

from Board import Board

def move2string(coord1, coord2):
    """
    Converts from coordinate moves into a string that gets sent to the API

    Args:
        coord1 (list): coordinate of source
        coord2 (list): coordinate of destination

    Returns:
        move string that gets sent to the API
    """
    letter_map = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e', 5 : 'f', 6 : 'g', 7 : 'h'}

    return letter_map[coord1[1]] + str(coord1[0] + 1) + letter_map[coord2[1]] + str(coord2[0] + 1)

def string2move(string):
    """
    Converts from string from the API to a coordinate move

    Args:
        string (str): string of move from the API
    
    Returns:
        coord1 (list): coordinate of source
        coord2 (list): coordinate of destination
    """
    promotion = None
    char_map = {'a': 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}

    coord1 = [int(string[1]) - 1, char_map[string[0]]]
    coord2 = [int(string[3]) - 1, char_map[string[2]]]

    if len(string) == 5:
        prom_map = {'n' : 'KN', 'b' : 'BI', 'r' : 'RO', 'q' : 'QU'}
        promotion = prom_map[string[4]]

    return [coord1, coord2], promotion

my_board = Board()
moves = "e2e4 a7a5 f1b5 b7b6 b5d7 e8d7 g1f3 f7f6 f3h4 d7e8 h4f5 h7h5 d1h5 h8h5 g2g4 h5h2 e1g1 g7g5 g1h2 d8d6 h2h1".split()

for move in moves:
    rl_move, promotion = string2move(move)

    my_board.make_move(rl_move[0], rl_move[1], promotion)

    my_board.print_board()

my_board.print_board()
print("====================================")


possible_moves = my_board.get_all_moves(my_board.BLACK)

print(possible_moves)

for move in possible_moves:
    move[1].print_board()
    print("-------")

import sys



# Open the .zst file in binary mode
with open('../../datasets/lichess_db.zst', 'rb') as file:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(file) as reader:
        # Iterate over the lines in the file
        chunk = "temp"
        num_bytes_read = 0
        num_open, num_start, num_mid, num_end = 0, 0, 0, 0
        while(chunk != b''):
            chunk_size = 30000 
            chunk = reader.read(chunk_size)
            lines = chunk.splitlines()


            game_str = ""

            for line in lines:
                dline = line.decode('utf-8')
                if len(dline) > 6 and dline[:6] == '[Event':
                    num_open, num_start, num_mid, num_end = process_game(game_str, num_open, num_start, num_mid, num_end)
                    game_str = dline + '\n'
                else:
                    game_str += dline + '\n'
            num_bytes_read += chunk_size
            print(adj_l(str(num_bytes_read / 1073741824), 5), " | ", adj_l(str(num_open), 15), " | ", adj_l(str(num_start), 15), " | ", adj_l(str(num_mid), 15), " | ", adj_l(str(num_end), 15), " | ", adj_l(str(len(df)), 15))



            
        