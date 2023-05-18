
# Collects games played yesterday by streamers on chess.com.
#
# The timezone this script uses is UTC.
#
# With the collected data, this script connects to the S3 bucket,
# chess-dot-com-streamer-data, and sends the collected data
# to that bucket.
#
# This script uses an error_logs folder for error handling.
# The .gitignore in the repo containing this script will make
# git ignore this error_logs folder.


from chessdotcom import get_streamers, get_player_game_archives
import requests
from datetime import datetime, timedelta

import boto3
import json
import time
from tqdm import tqdm

import os


# Only get those games played yesterday. Use UTC timezone.

def is_yesterday(game):

    if "pgn" not in game:
        return False

    yesterday = datetime.utcnow() - timedelta(days=1)
    substring = f"{yesterday.year}.{yesterday.month:02d}.{yesterday.day:02d}"

    return substring in game["pgn"]


# Use the chess.com API to get games played by streamers yesterday.

def yesterdays_games(streamers):

    unames = list(map(lambda x: x['username'], streamers))
    yesterdays_games = {}

    for uname in tqdm(unames):

        data = get_player_game_archives(uname).json

        if 'archives' not in data:
            continue

        data = data['archives']

        if len(data) == 0:
            continue

        games = requests.get(data[-1]).json()['games']
        games = list(filter(lambda x: is_yesterday(x), games))

        if len(games) >= 1:
            yesterdays_games[uname] = games

    return yesterdays_games


# Connect to the chess-dot-com-streamer-data S3 bucket and move the collected
# data into that bucket.

def store(folder_name, data):

    s3 = boto3.client('s3')

    json_data = json.dumps(data)
    bucket_name = 'chess-dot-com-streamer-data'

    yesterday = datetime.utcnow() - timedelta(days=1)
    file_name = f"{folder_name}_data_{yesterday.strftime('%Y_%m_%d')}.json"
    object_key = f"{folder_name}/{yesterday.strftime('%Y')}/{yesterday.strftime('%m')}/{file_name}"

    s3.put_object(Body=json_data, Bucket=bucket_name, Key=object_key)


# Error handling.

def record_error(e):

    current_dir = os.path.dirname(__file__)

    yesterday = datetime.utcnow() - timedelta(days=1)
    directory_path = os.path.join(current_dir, "error_logs",\
                                                    yesterday.strftime('%Y'),\
                                                    yesterday.strftime('%m'))
    os.makedirs(directory_path, exist_ok=True)

    file_name = f"error_log_{yesterday.strftime('%Y_%m_%d')}.txt"
    file_path = os.path.join(current_dir, directory_path, file_name)

    with open(file_path, "w") as file:
        file.write("Error: " + repr(e) + "\n")
        file.write("Message: " + repr(e.args[0]) + "\n")
        file.write("Details: " + repr(e.args[1:]) + "\n")



def main():

    try:
        print("getting yesterdays's games ...")
        games = yesterdays_games(streamers)
    except Exception as e:
        record_error(e)
        return

    try:
        print("saving yesterday's games ...")
        store('games', games)
    except Exception as e:
        record_error(e)
        return


if __name__ == "__main__":
    main()

