import os
from pyrogram import Client, filters
from pymongo import MongoClient

# Retrieve configuration from environment variables
API_ID = int(os.environ.get("API_ID", 0))  # Ensure to set a valid API_ID in your environment
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
MONGO_URI = os.environ.get("MONGO_URI", "")

# MongoDB setup
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["UserbotDB"]
collection = db["SavedMessages"]

# Initialize Pyrogram Client (Userbot) in memory
app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, in_memory=True)

# Save command handler (only owner or userbot can use)
@app.on_message(filters.command("save") & filters.reply & (filters.me | filters.chat(OWNER_ID)))
async def save_message(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: Reply to a message with `/save <text>`")
        return

    save_text = message.text.split(maxsplit=1)[1].lower()
    replied_message = message.reply_to_message

    # Copy the replied message to the channel
    copied_msg = await replied_message.copy(CHANNEL_ID)

    # Store in MongoDB
    collection.insert_one({
        "key": save_text,
        "message_id": copied_msg.id
    })

    await message.reply(f"Message saved with key: `{save_text}`")

# Message handler to retrieve saved messages (only userbot can send)
@app.on_message(filters.private & filters.text)
async def retrieve_message(client, message):

    query = message.text.lower()
    saved_data = collection.find_one({"key": query})

    if saved_data:
        msg_id = saved_data["message_id"]

        # Directly copy message from channel to user
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=msg_id
        )

# Run the userbot
app.run()
