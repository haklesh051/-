import os
from pyrogram import Client, filters
from pyrogram.types import InputMediaVideo

# === CONFIG ===
API_ID = int(os.environ.get("API_ID", 123456))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

CHAT_ID = int(os.environ.get("CHAT_ID", -1001234567890))  # Group ka ID
TOPIC_ID = int(os.environ.get("TOPIC_ID", 456))  # Topic ka message_thread_id
VIDEO_FOLDER = "videos"  # Local folder jisme videos rakhe hain

# === BOT INIT ===
app = Client("video_sender_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to send all videos in topic
@app.on_message(filters.command("sendvideos") & filters.user([123456789]))  # Apna Telegram user ID daalo
def send_videos(_, message):
    if not os.path.exists(VIDEO_FOLDER):
        message.reply("❌ Video folder nahi mila!")
        return

    video_files = [
        os.path.join(VIDEO_FOLDER, f) for f in os.listdir(VIDEO_FOLDER)
        if f.lower().endswith((".mp4", ".mkv", ".mov", ".avi"))
    ]

    if not video_files:
        message.reply("❌ Folder me koi video nahi mila!")
        return

    message.reply(f"📤 {len(video_files)} videos bhejne suru kar raha hu topic me...")

    # Send videos in batches of 10
    for i in range(0, len(video_files), 10):
        batch = video_files[i:i+10]
        media_group = [InputMediaVideo(video, caption=os.path.basename(video)) for video in batch]

        app.send_media_group(
            chat_id=CHAT_ID,
            media=media_group,
            message_thread_id=TOPIC_ID
        )
    message.reply("✅ Sare videos topic me bhej diye gaye!")

print("🚀 Bot started...")
app.run()
