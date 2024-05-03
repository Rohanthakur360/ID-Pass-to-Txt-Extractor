import os

api_id = 3748059
api_hash = os.environ.get("API_HASH", "f8c9df448f3ba20a900bc2ffc8dae9d5")
bot_token = os.environ.get("BOT_TOKEN")
auth_users = os.environ.get("AUTH_USERS", "5591734243,1369808729")
sudo_users = [int(num) for num in auth_users.split(",")]
osowner_users = os.environ.get("OWNER_USERS", "5591734243,1369808729")
owner_users = [int(num) for num in osowner_users.split(",")]
