# chess-data-pipeline
Data pipeline using AWS EC2 and S3. Collects chess streamer data from chess.com once a day.

A clone of this repo in an EC2 instance is used to collect the streamer data. In addition, pushes to the `chess-data-pipeline` repo on GitHub are automatically pulled to the aforementioned clone due to a webhook attached to this repo and a clone of the `CI-CD-for-chess-data-pipeline` running on the above EC2 instance. The clone of `CI-CD-for-chess-data-pipeline` uses Flask to listen for POST requests from the webhook.

This repo uses `yesterday.py` to do the following:

- Collect yesterday's data, in UTC time, from the chess.com API, on games played by chess.com streamers.

- Connect to an S3 bucket, and move the collected data into that S3 bucket. In order to establish the connection to the S3 bucket, I attached a customized role to the above EC2 instance and used the `boto3` library as specified in `yesterday.py`. The role is detailed in the `role.json` file in this repo.

I set up a cronjob in the EC2 instance to, once a day at 12 AM UTC, run the bash script `yesterday.sh`. The bash script does the following.

- It activates a Python `venv` environment needed for `yesterday.py`. The dependencies needed for this virtual environment are described in `requirements.txt`. In addition, this virtual environment is stored outside of the cloned repo in the EC2 instance.

- It runs `yesterday.py`.

