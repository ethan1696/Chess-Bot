import requests
import json
import select

# bot API token
BOT_API_TOKEN = "lip_Y1QXe5YG2bmbnjThxrvv"
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
    """
    letter_map = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e', 5 : 'f', 6 : 'g', 7 : 'h'}

    return letter_map[coord1[0]] + str(coord1[1]) + letter_map[coord2[0]] + str(coord2[1])

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
                        accept_challenge(challenge_id)
                        response.close()
                        break
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

        while True:
            ready = None
            # Wait for the response to be ready for reading
            if not response.raw.closed:
                ready = select.select([response.raw], [], [], None)
            else:
                print("Game Over.")
                break


            if ready[0]:
                # Read the available data from the response
                line = response.raw.readline()
                print("IN GAME -- ", line)
                if line.strip():
                    event = json.loads(line)
                    move = ""
                    if event['moves'] != "":
                        move = (event['moves'].split())[-1]
                    print("MOVE -- ", move)
                    is_my_turn = not is_my_turn
                    # play_move(challenge_id, "g8h6")
                    
            else:
                # The response has no data available, so wait for more events
                pass

while(True):
    main()