# import time
# import requests
# import logging
# import os

# # Set up logging
# logging.basicConfig(filename='status_change.log', level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# # Load bot token from environment variable
# DISCORD_TOKEN = os.getenv('TOKEN')
# if not DISCORD_TOKEN:
#     raise ValueError("DISCORD_TOKEN environment variable not set")

# url = 'https://discord.com/api/v9/users/@me/settings'

# # Load lines from file
# with open("text.txt", "r") as file:
#     lines = file.readlines()

# def ChangeStatus(message):
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }

#     jsondata = {
#         "status": "online",
#         "custom_status": {
#             "text": message
#         }
#     }

#     try:
#         response = requests.patch(url, headers=headers, json=jsondata)
#         response.raise_for_status()
#         logging.info(f"Status changed to: {message}")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Failed to change status: {e}")

# # Main loop
# try:
#     while True:
#         for line in lines:
#             ChangeStatus(line.strip())
#             time.sleep(3)
# except KeyboardInterrupt:
#     logging.info("Script terminated by user")
