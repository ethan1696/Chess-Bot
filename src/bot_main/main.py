import requests
import json
import select
import sys
sys.path.append('.')
from src.board_simulator.Board import Board
import src.engines.engine_v1.engine_v1 as engine

# bot API token
with open('secrets/api_token.txt', 'r') as file:
    BOT_API_TOKEN = file.readline().strip()

BOT_NAME = "carlus_magnusen_9000"

# Define the Lichess API endpoint URLs
base_url = "https://lichess.org"
api_url = f"{base_url}/api"
events_url = f"{api_url}/stream/event"

# Define the headers for the API requests, including the bot API token
headers = {
    "Authorization": f"Bearer {BOT_API_TOKEN}"
}

def accept_challenge(challenge_id):
    """
    This function accepts a challenge

    Args:
        challenge_id (string): ID of the challenge to accept
    """

    accept_url = f"{api_url}/challenge/{challenge_id}/accept"

    data = {
        "seconds": 0 # 0 seconds means unlimited time
    }
    response = requests.post(accept_url, headers=headers, data=data)
    response.raise_for_status()
    
def reject_rematch(challenge_ID):
    """
    This function rejects a rematch request

    Args:
        rematch_ID (string): ID of the rematch to reject
    """

    decline_url = f"{api_url}/challenge/{challenge_ID}/decline"


    response = requests.post(decline_url, headers=headers)
    response.raise_for_status()
    

def play_move(game_id, move):
    """
    This function plays a move

    Args:
        game_id (string): The game that the move would be played on
        move (string): The move to play
    """
    moves_url = f"{api_url}/bot/game/{game_id}/move/{move}"
    data = {
        "ok": True
    }
    response = requests.post(moves_url, headers=headers, data=data)
    response.raise_for_status()

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

def main():
    """
    This function runs one iteration of accepting a challenge and playing the game
    """
    challenge_id = ""
    #Wait for a challenge request
    with requests.get(events_url, headers=headers, stream=True) as response:
        # Use select to wait until the response has data to read
        while True:
            # Wait for the response to be ready for reading
            ready = select.select([response.raw], [], [], None)
            if ready[0]:
                # Read the available data from the response
                line = response.raw.readline()
                print(line.strip())
                if line.strip():
                    event = json.loads(line)
                    # Check if the event is a challenge and accept it if so. Break the loop so other challenges get queued while this game is played
                    if event['type'] == "challenge":
                        challenge_id = event['challenge']['id']

                        if 'rematchOf' not in event['challenge'].keys():
                            accept_challenge(challenge_id)
                            response.close()
                            break
                        else:
                            reject_rematch(challenge_id)
            else:
                # The response has no data available, so wait for more events
                pass
    
    game_state_url = f"{api_url}/bot/game/stream/{challenge_id}"

    with requests.get(game_state_url, headers=headers, stream=True) as response:
        # Read game start information
        ready = select.select([response.raw], [], [], None)

        is_white = False
        is_my_turn = False
        line = response.raw.readline()

        if line.strip():
            event = json.loads(line)
            is_white = event['white']['id'] == BOT_NAME
            is_my_turn = is_white

        board = Board()

        print(f"STARTED GAME \n is_white: {is_white}")

        board.print_board()

        # Play first move if white
        if(is_my_turn):
            bot_move = engine.get_move(board, board.WHITE if is_white else board.BLACK)
            play_move(challenge_id, move2string(bot_move[0], bot_move[1])) 

        print("=========")

        while True:
            ready = None
            # Wait for the response to be ready for reading
            if not response.raw.closed:
                ready = select.select([response.raw], [], [], None)
            else:
                del board
                print("Game Over.")
                break


            if ready[0]:
                # Read the available data from the response
                line = response.raw.readline()
                print("IN GAME -- ", line)
                if line.strip():
                    event = json.loads(line)
                    if event['status'] != "started":
                        del board
                        print(f"Game Over -- {event['status']}")
                        break
                    move_str = ""
                    if event['moves'] != "":
                        move_str = (event['moves'].split())[-1]
                    print(f"MOVE {'BOT   ' if is_my_turn else 'PLAYER'} -- ", move_str)

                    move, promotion = string2move(move_str)

                    board.make_move(move[0], move[1], promotion)

                    board.print_board()

                    print("")

                    is_my_turn = not is_my_turn

                    if(is_my_turn):
                        bot_move = engine.get_move(board, board.WHITE if is_white else board.BLACK)
                        play_move(challenge_id, move2string(bot_move[0], bot_move[1]))                    

                    
                    
            else:
                # The response has no data available, so wait for more events
                pass

while(True):
    main()