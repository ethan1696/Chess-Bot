import zstandard as zstd
import chess.pgn
from io import StringIO
import random
import pandas as pd
import sys

data = {'board': [], 'move': []}
df = pd.DataFrame(data)

def flip_move(move_str):
    num1 = 9 - int(move_str[1])
    num2 = 9 - int(move_str[3])

    return move_str[0] + str(num1) + move_str[2] + str(num2)

#Process Game
def process_game(game_str, num_open, num_start, num_mid, num_end):
    global df
    if(game_str == ""):
        return num_open, num_start, num_mid, num_end
    
    #print(game_str)
    try:
        pgn_io = StringIO(game_str)
 
        game = chess.pgn.read_game(pgn_io)
    
        if game == None:
            return num_open, num_start, num_mid, num_end

        board = game.board()
        num_moves = len(list(game.mainline_moves()))
        
    except ValueError as e:
        return num_open, num_start, num_mid, num_end
    
    move_num = 1

    move_dict = {"open" : [], "start" : [], "mid": [], "end" : []}

    try:
        for move in game.mainline_moves():
            board_prev = board.fen().split(" ")[0]
            move_uci = move.uci()
            if move_num % 2 == 0: # Flip if black
                board_prev = board.transform(chess.flip_vertical).fen().split(" ")[0]
                move_uci = flip_move(move_uci)
            board.push(move)
            cur_move = [board_prev, move_uci]
            if move_num <= 8:
                move_dict["open"].append(cur_move)
            else:
                num_pieces = len(board.piece_map())

                #thresholds:
                start_mid = 25
                mid_end = 10

                if num_pieces >= start_mid:
                    move_dict["start"].append(cur_move)
                elif num_pieces >= mid_end:
                    move_dict["mid"].append(cur_move)
                else:
                    move_dict["end"].append(cur_move)
            move_num += 1
            if move_num > num_moves:
                break
    except:
        return num_open, num_start, num_mid, num_end

    random.shuffle(move_dict["open"])
    random.shuffle(move_dict["start"])
    random.shuffle(move_dict["mid"])
    random.shuffle(move_dict["end"])

    while(True):
        min_class = min((num_open * 2, num_start, num_mid, num_end))
        new_data = None
        if min_class == num_open * 2:
            if len(move_dict["open"]) == 0:
                break
            move_elem = move_dict["open"].pop()
            new_data = {'board': [move_elem[0]], 'move': [move_elem[1]]}
            new_df = pd.DataFrame(new_data)
            df = pd.concat([df, new_df], ignore_index=True)
            num_open += 1
        elif min_class == num_start:
            if len(move_dict["start"]) == 0:
                break
            move_elem = move_dict["start"].pop()
            new_data = {'board': [move_elem[0]], 'move': [move_elem[1]]}
            new_df = pd.DataFrame(new_data)
            df = pd.concat([df, new_df], ignore_index=True)
            num_start += 1
        elif min_class == num_mid:
            if len(move_dict["mid"]) == 0:
                break
            move_elem = move_dict["mid"].pop()
            new_data = {'board': [move_elem[0]], 'move': [move_elem[1]]}
            new_df = pd.DataFrame(new_data)
            df = pd.concat([df, new_df], ignore_index=True)
            num_mid += 1
        elif min_class == num_end:
            if len(move_dict["end"]) == 0:
                break
            move_elem = move_dict["end"].pop()
            new_data = {'board': [move_elem[0]], 'move': [move_elem[1]]}
            new_df = pd.DataFrame(new_data)
            df = pd.concat([df, new_df], ignore_index=True)
            num_end += 1
        

    return num_open, num_start, num_mid, num_end

def adj_l(string, n):
    if len(string) < n:
        return string.ljust(n)
    elif len(string) > n:
        return string[:n]
    else:
        return string


class CustomStream:
    def __init__(self, stream):
        self.stream = stream

    def write(self, text):
        # Filter the output based on your conditions
        if "Telemetry" in text:
            self.stream.write(text)

    def flush(self):
        self.stream.flush()

# Create a custom stream object for stdout
custom_stdout = CustomStream(sys.stdout)


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
            print("Telemetry: | ", adj_l(str(num_bytes_read / 1073741824), 5), " | ", adj_l(str(num_open), 15), " | ", adj_l(str(num_start), 15), " | ", adj_l(str(num_mid), 15), " | ", adj_l(str(num_end), 15), " | ", adj_l(str(len(df)), 15))


            
        