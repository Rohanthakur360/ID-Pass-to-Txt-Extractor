import asyncio
import json
import logging
import os
import re
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler
from subprocess import getstatusoutput

import requests
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyromod import listen

import online.helpers.vid as helper
from online.Config import *
from online.helpers.button import keyboard
from online.helpers.sudoers import *
from online.helpers.text import *

# ==========Logging==========#
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging = logging.getLogger()

# =========== Client ===========#
bot = Client(
    "bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
)

print(listen.__file__)


# ========== Converter =============#
@bot.on_message(filters.command(["taiyaric"]))
async def gaiyrab(bot: Client, message: Message):
    message.from_user.id if message.from_user is not None else None
    if not one(message.from_user.id):
        return await message.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await message.reply_text(
            "This is help to convert json file to text of taiyari karlo app ",
            disable_web_page_preview=True,
        )
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    to_write = ""
    try:
        with open(x, "r") as file:
            data = json.load(file)
            for entry in data:
                target_change = entry[1][0].get("targetChange")
                if target_change and target_change.get("targetChangeType") == "ADD":
                    continue
                document_change = (
                    entry[1][0]
                    .get("documentChange", {})
                    .get("document", {})
                    .get("fields", {})
                )
                quality = None
                recordings = (
                    document_change.get("recordings", {})
                    .get("arrayValue", {})
                    .get("values", [])
                )
                for recording in recordings:
                    recording_fields = recording.get("mapValue", {}).get("fields", {})
                    quality = recording_fields.get("quality", {}).get("stringValue")
                    if quality == "480p":
                        path = recording_fields.get("path", {}).get("stringValue")
                        title = document_change.get("title", {}).get("stringValue")
                        to_write += f"{title}:{path}\n"
                if document_change.get("type", {}).get("stringValue") == "pdf":
                    title_pdf = document_change.get("title", {}).get("stringValue")
                    ref_pdf = document_change.get("ref", {}).get("stringValue")
                    to_write += f"{title_pdf}:{ref_pdf}\n"
    except Exception as e:
        os.remove(x)
        return await message.reply_text(f"**Error** : {e}")
    with open(f"new.txt", "w", encoding="utf-8") as f:
        f.write(to_write)
        print(1)
    with open(f"new.txt", "rb") as f:
        await asyncio.sleep(5)
        doc = await message.reply_document(document=f, caption="Here is your txt file.")


# =========== Core Commands ======#

shell_usage = f"**USAGE:** Executes terminal commands directly via bot.\n\n<pre>/shell pip install requests</pre>"


@bot.on_message(filters.command(["shell"]))
async def shell(client, message: Message):
    """
    Executes terminal commands via bot.
    """
    if not two(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(shell_usage, quote=True)

    user_input = message.text.split(None, 1)[1].split(" ")

    try:
        shell = subprocess.Popen(
            user_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = shell.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    except Exception as error:
        logging.info(f"{error}")
        return await message.reply_text(f"**Error**:\n\n{error}", quote=True)

    if len(result) > 2000:
        file = BytesIO(result.encode())
        file.name = "output.txt"
        await message.reply_text("Output is too large (Sending it as File)", quote=True)
        await client.send_document(message.chat.id, file, caption=file.name)
    else:
        await message.reply_text(f"**Output:**:\n\n{result}", quote=True)


paid_text = """
» Hello i am online class bot which help you to **Extract** and **Download** video of Physics Wallah / Apni Kaksha / Khan Gs ..... Any Type of Online Class Which You Want.
• **How to Access this bot**

Step 1: Click Below on Developer.
Step 2: Go to Telegram Username
Step 3: Send your Telegram ID From @missrose_bot
"""


# ============== Start Commands ==========#
@bot.on_message(filters.command(["start"]))
async def account_lstarn(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_photo(
            photo="https://telegra.ph/file/e6d2807b0d3074742fe41.jpg",
            caption=paid_text,
            reply_markup=keyboard,
        )
    await m.reply_text(start_text)


# ========== Global Concel Command ============
cancel = False


@bot.on_message(filters.command(["cancel"]))
async def cancel(_, m):
    if not two(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nThis Command is only For Owner",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "Canceling All process Plz wait\n🚦🚦 Last Process Stopped 🚦🚦"
    )
    global cancel
    cancel = False
    await editable.edit("cancelled all")
    return


# ============== Power Commands =================
@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not two(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nYou Don't Have Right To Access This Contact Owner",
        )
    await m.reply_text("➭ 𝗕𝗼𝘁 𝗜𝘀 𝗕𝗲𝗶𝗻𝗴 𝗥𝗲𝘀𝘁𝗮𝗿𝘁𝗶𝗻𝗴. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗞𝗲𝗲𝗽 𝗣𝗮𝘁𝗶𝗲𝗻𝗰𝗲", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


# ============ Download Commands ==============#
@bot.on_message(filters.command(["pyro"]))
async def download_pw(bot: Client, m: Message):
    global cancel
    m.from_user.id if m.from_user is not None else None
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await m.reply_text(pyro_text, disable_web_page_preview=True)
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    links = []
    try:
        with open(x, "r") as f:
            content = f.read()
            new_content = content.split("\n")
            for i in new_content:
                links.append(re.split(":(?=http)", i))
        os.remove(x)
    except Exception as e:
        await m.reply_text(f"**Error** : {e}")
        os.remove(x)
        return
    await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    initial_number = await bot.listen(editable.chat.id)

    try:
        arg = int(initial_number.text)
    except:
        arg = 0

    await m.reply_text(
        f"Total links: **{len(links)}**\n\nSend Me Final Number\n\nBy Default Final is {len(links)}"
    )
    final_number = await bot.listen(editable.chat.id)

    try:
        arg1 = int(final_number.text)
    except:
        arg1 = len(links)
    await m.reply_text("**Enter batch name**")
    input0 = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4 = await m.reply_text(
        "**For Thumb Url**\n\n• Custom url : Use @vtelegraphbot and send me links\n• If Your file Contain Url : `yes`\n• Send no if you don't want : `no`"
    )
    input6 = await bot.listen(editable.chat.id)
    lol_thumb = input6.text

    if arg == "0":
        count = 1
    else:
        count = int(arg)
    cancel = True
    for i in range(arg, arg1):
        try:
            while cancel == False:
                return await m.reply_text("Cancelled Process")
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .strip()
            )
            try:
                if lol_thumb == "yes":
                    old_thumb = links[i][2]
                    getstatusoutput(f"wget '{old_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                elif lol_thumb.startswith("http://") or lol_thumb.startswith(
                    "https://"
                ):
                    old_thumb = lol_thumb
                    getstatusoutput(f"wget '{lol_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                else:
                    thumb = "no"
                    old_thumb = "No Thumbnail"
            except Exception as e:
                return await m.reply_text(e)
            Total_Links = arg1 - int(arg)
            Show_old = f"**Total Links** : {Total_Links}\n\n**Name :-** `{name1}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
            prog_old = await m.reply_text(Show_old)
            if raw_text2 == "144":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "256x144" in out:
                    ytf = f"{out['256x144']}"
                elif "320x180" in out:
                    ytf = out["320x180"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data1 in out:
                        ytf = out[data1]
            elif raw_text2 == "180":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "320x180" in out:
                    ytf = out["320x180"]
                elif "426x240" in out:
                    ytf = out["426x240"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data2 in out:
                        ytf = out[data2]
            elif raw_text2 == "240":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "426x240" in out:
                    ytf = out["426x240"]
                elif "426x234" in out:
                    ytf = out["426x234"]
                elif "480x270" in out:
                    ytf = out["480x270"]
                elif "480x272" in out:
                    ytf = out["480x272"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data3 in out:
                        ytf = out[data3]
            elif raw_text2 == "360":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "640x360" in out:
                    ytf = out["640x360"]
                elif "638x360" in out:
                    ytf = out["638x360"]
                elif "636x360" in out:
                    ytf = out["636x360"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "638x358" in out:
                    ytf = out["638x358"]
                elif "852x316" in out:
                    ytf = out["852x316"]
                elif "850x480" in out:
                    ytf = out["850x480"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["852x470"]
                elif "1280x720" in out:
                    ytf = out["1280x720"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data4 in out:
                        ytf = out[data4]
            elif raw_text2 == "480":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["854x470"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "850x480" in out:
                    ytf = ["850x480"]
                elif "960x540" in out:
                    ytf = out["960x540"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data5 in out:
                        ytf = out[data5]
            elif raw_text2 == "720":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "1280x720" in out:
                    ytf = out["1280x720"]
                elif "1280x704" in out:
                    ytf = out["1280x704"]
                elif "1280x474" in out:
                    ytf = out["1280x474"]
                elif "1920x712" in out:
                    ytf = out["1920x712"]
                elif "1920x1056" in out:
                    ytf = out["1920x1056"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data6 in out:
                        ytf = out[data6]
            elif "player.vimeo" in url:
                if raw_text2 == "144":
                    ytf = "http-240p"
                elif raw_text2 == "240":
                    ytf = "http-240p"
                elif raw_text2 == "360":
                    ytf = "http-360p"
                elif raw_text2 == "480":
                    ytf = "http-540p"
                elif raw_text2 == "720":
                    ytf = "http-720p"
                else:
                    ytf = "http-360p"
            else:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                for dataS in out:
                    ytf = out[dataS]

            try:
                if "unknown" in out:
                    pass
                else:
                    list(out.keys())[list(out.values()).index(ytf)]

                name = f"{name1}"
            except Exception as e:
                return await m.reply(f"Error in ytf : {e}")
            await prog_old.delete(True)
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "youtu" in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<={raw_text2}]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}.%(ext)s"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif url.startswith("https://apni-kaksha.vercel.app"):
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ytf == "0" or "unknown" in out:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ".pdf" or "download" in str(url):
                cmd = "pdf"
            else:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'

            try:
                Show = f"**Downloading:-**\n\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
                prog = await m.reply_text(Show)
                cc = f"**➭ Name » {name1}** \n**➭ Batch » {raw_text0}**"
                cc1 = f"**➭ Name » {name1}** \n**➭ Batch » {raw_text0}**"
                if cmd == "pdf" or ".pdf" in str(url) or ".pdf" in name:
                    print("PDF")
                    try:
                        ka = await helper.aio(url, name)
                        await prog.delete(True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        await m.reply_document(
                            ka,
                            caption=f"{cc1}",
                        )
                        count += 1
                        await reply.delete(True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    filename = await helper.download_video(url, cmd, name)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`"
                )
                continue
        except Exception as e:
            return await m.reply_text(f"Overall Error : {e}")
    await m.reply_text("Done")


@bot.on_message(filters.command(["patna"]))
async def khan_dowbol(bot: Client, m: Message):
    global cancel
    m.from_user.id if m.from_user is not None else None
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await m.reply_text(pyro_text, disable_web_page_preview=True)
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    links = []
    try:
        with open(x, "r") as f:
            content = f.read()
            new_content = content.split("\n")
            for i in new_content:
                links.append(re.split(":(?=http)", i))
        os.remove(x)
    except Exception as e:
        await m.reply_text(f"**Error** : {e}")
        os.remove(x)
        return
    await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    initial_number = await bot.listen(editable.chat.id)

    try:
        arg = int(initial_number.text)
    except:
        arg = 0

    await m.reply_text(
        f"Total links: **{len(links)}**\n\nSend Me Final Number\n\nBy Default Final is {len(links)}"
    )
    final_number = await bot.listen(editable.chat.id)

    try:
        arg1 = int(final_number.text)
    except:
        arg1 = len(links)
    await m.reply_text("**Enter batch name**")
    input0 = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4 = await m.reply_text(
        "**For Thumb Url**\n\n• Custom url : Use @vtelegraphbot and send me links\n• If Your file Contain Url : `yes`\n• Send no if you don't want : `no`"
    )
    input6 = await bot.listen(editable.chat.id)
    lol_thumb = input6.text

    if arg == "0":
        count = 1
    else:
        count = int(arg)
    cancel = True
    for i in range(arg, arg1):
        try:
            while cancel == False:
                return await m.reply_text("Cancelled Process")
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .strip()
            )
            try:
                if lol_thumb == "yes":
                    old_thumb = links[i][2]
                    getstatusoutput(f"wget '{old_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                elif lol_thumb.startswith("http://") or lol_thumb.startswith(
                    "https://"
                ):
                    old_thumb = lol_thumb
                    getstatusoutput(f"wget '{lol_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                else:
                    thumb = "no"
                    old_thumb = "No Thumbnail"
            except Exception as e:
                return await m.reply_text(e)
            Total_Links = arg1 - int(arg)
            Show_old = f"**Total Links** : {Total_Links}\n\n**Name :-** `{name1}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
            prog_old = await m.reply_text(Show_old)
            if raw_text2 == "144":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                if "256x144" in out:
                    ytf = f"{out['256x144']}"
                elif "320x180" in out:
                    ytf = out["320x180"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data1 in out:
                        ytf = out[data1]
            elif raw_text2 == "180":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "320x180" in out:
                    ytf = out["320x180"]
                elif "426x240" in out:
                    ytf = out["426x240"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data2 in out:
                        ytf = out[data2]
            elif raw_text2 == "240":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "426x240" in out:
                    ytf = out["426x240"]
                elif "426x234" in out:
                    ytf = out["426x234"]
                elif "480x270" in out:
                    ytf = out["480x270"]
                elif "480x272" in out:
                    ytf = out["480x272"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data3 in out:
                        ytf = out[data3]
            elif raw_text2 == "360":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "640x360" in out:
                    ytf = out["640x360"]
                elif "638x360" in out:
                    ytf = out["638x360"]
                elif "636x360" in out:
                    ytf = out["636x360"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "638x358" in out:
                    ytf = out["638x358"]
                elif "854x360" in out:
                    ytf = out["854x360"]
                elif "852x316" in out:
                    ytf = out["852x316"]
                elif "850x480" in out:
                    ytf = out["850x480"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["852x470"]
                elif "1280x720" in out:
                    ytf = out["1280x720"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data4 in out:
                        ytf = out[data4]
            elif raw_text2 == "480":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                if "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["854x470"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "850x480" in out:
                    ytf = ["850x480"]
                elif "960x540" in out:
                    ytf = out["960x540"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data5 in out:
                        ytf = out[data5]
            elif raw_text2 == "720":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                if "1280x720" in out:
                    ytf = out["1280x720"]
                elif "1280x704" in out:
                    ytf = out["1280x704"]
                elif "1280x474" in out:
                    ytf = out["1280x474"]
                elif "1920x712" in out:
                    ytf = out["1920x712"]
                elif "1920x1056" in out:
                    ytf = out["1920x1056"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data6 in out:
                        ytf = out[data6]
            elif "player.vimeo" in url:
                if raw_text2 == "144":
                    ytf = "http-240p"
                elif raw_text2 == "240":
                    ytf = "http-240p"
                elif raw_text2 == "360":
                    ytf = "http-360p"
                elif raw_text2 == "480":
                    ytf = "http-540p"
                elif raw_text2 == "720":
                    ytf = "http-720p"
                else:
                    ytf = "http-360p"
            else:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                for dataS in out:
                    ytf = out[dataS]

            try:
                if "unknown" in out:
                    res = "NA"
                else:
                    res = list(out.keys())[list(out.values()).index(ytf)]

                name = f"{str(count).zfill(3)}) {name1} {res}"
            except Exception as e:
                await m.reply(f"Error in ytf : {e}")
                continue
                res = "NA"
            await prog_old.delete(True)
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "youtu" in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<={raw_text2}]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}.%(ext)s"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif url.startswith("https://apni-kaksha.vercel.app"):
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ytf == "0" or "unknown" in out:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ".pdf" or "download" in str(url):
                cmd = "pdf"
            else:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'

            try:
                Show = f"**Downloading:-**\n\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
                prog = await m.reply_text(Show)
                cc = f"**➭ Name »** {name} {res}.mkv\n**➭ Batch »** {raw_text0}"
                cc1 = f"**➭ Name »** {name} {res}.pdf\n**➭ Batch »** {raw_text0}"
                if cmd == "pdf" or ".pdf" in str(url) or ".pdf" in name:
                    try:
                        ka = await helper.aio(url, name)
                        await prog.delete(True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        await m.reply_document(
                            ka,
                            caption=f"{cc1}",
                        )
                        count += 1
                        await reply.delete(True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    filename = await helper.download_video(url, cmd, name)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`"
                )
                continue
        except Exception as e:
            await m.reply_text(f"Overall Error : {e}")
    await m.reply_text("Done")


# ================ Class Plus =================#
@bot.on_message(filters.command(["cp"]))
async def infcpsgin(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    s = requests.Session()
    editable = await m.reply_text("**Send Token from ClassPlus App**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    headers = {
        "authority": "api.classplusapp.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en",
        "api-version": "28",
        "cache-control": "no-cache",
        "device-id": "516",
        "origin": "https://web.classplusapp.com",
        "pragma": "no-cache",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "x-access-token": f"{raw_text0}",
    }
    resp = s.get(
        "https://api.classplusapp.com/v2/batches/details?limit=20&offset=0&sortBy=createdAt",
        headers=headers,
    )
    if resp.status_code == 200:
        pass
    else:
        editable = await m.reply_text("Login Failed Check Response")
    b_data = resp.json()["data"]["totalBatches"]
    cool = ""
    for data in b_data:
        t_name = data["batchName"]
        t_id = data["batchId"]
        cool += f" **{t_name}** - `{t_id}` \n\n"
    await editable.edit(f'{"**You have these batches :-**"}\n\n{cool}')
    await m.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await bot.listen(editable.chat.id)
    cr = input2.text
    b_data = s.get(
        f"https://api.classplusapp.com/v2/course/content/get?courseId={cr}",
        headers=headers,
    ).json()["data"]["courseContent"]
    cool = ""
    for data in b_data:
        id1 = data["id"]
        nam2 = data["name"]
        data["contentType"]
        cool += f" **{nam2}** - `{id1}`\n\n"
    await editable.edit(f"**You have these Folders :-**\n\n{cool}")
    await m.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    bdata = s.get(
        f"https://api.classplusapp.com/v2/course/content/get?courseId={cr}&folderId={raw_text2}",
        headers=headers,
    ).json()["data"]["courseContent"]
    folder_m = ""
    for data in bdata:
        id1 = data["id"]
        nam2 = data["name"]
        vid = data["resources"]["videos"]
        fid = data["resources"]["files"]
        data["contentType"]
        FFF = "**FOLDER-ID -FOLDER NAME -TOTAL VIDEOS/PDFS**"
        folder_m += f" `{id1}` - **{nam2}  -{vid} -{fid}**\n\n"
    await editable.edit(f'{"**You have these Folders :-**"}\n\n{FFF}\n\n{folder_m}')
    await m.reply_text("**Now send the Folder ID to Download**")
    input3 = message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    respc = s.get(
        f"https://api.classplusapp.com/v2/course/content/get?courseId={cr}&folderId={raw_text3}",
        headers=headers,
    ).json()
    ddata = respc["data"]["courseContent"]
    if (respc["data"]["courseContent"][0]["contentType"]) == 1:
        cool = ""
        for datas in ddata:
            id2 = datas["id"]
            nam2 = datas["name"]
            vid2 = datas["resources"]["videos"]
            fid = datas["resources"]["files"]
            datas["contentType"]
            FFF = "**FOLDER-ID -FOLDER NAME -TOTAL VIDEOS/PDFS**"
            cool += f" `{id2}` - **{nam2} -{vid2}**\n\n"
        await editable.edit(f'{"**You have these Folders :-**"}\n\n{FFF}\n\n{cool}')
        await m.reply_text("**Now send the Folder ID to Download**")
        input4 = message = await bot.listen(editable.chat.id)
        raw_text4 = input4.text
        resp = s.get(
            f"https://api.classplusapp.com/v2/course/content/get?courseId={cr}&folderId={raw_text4}",
            headers=headers,
        )
        bdat = resp.json()["data"]["courseContent"]
        bdat.reverse()
        to_write = ""
        for data in bdat:
            id1 = data["id"]
            nam2 = data["name"]
            dis2 = data["description"]
            url2 = data["url"]
            data["contentType"]
            to_write += f" `{id2}` - **{nam2}  -{dis2}**\n"
            mm = "careerplus1"
            with open(f"{mm}.txt", "a") as f:
                f.write(f"{to_write}")
        await m.reply_document(f"{mm}.txt")
    else:
        ddata.reverse()
        cool = ""
        vj = ""
        for data in ddata:
            id2 = str(data["id"])
            nam2 = data["name"]
            url2 = data["url"]
            des2 = data["description"]

            # respc = s.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers).json()
            # urli = respc["url"]
            FFF = "**Topic-ID -Topic NAME **"
            aa = f" `{id2}` - **{nam2}  -{des2}**\n\n"
            if len(f"{vj}{aa}") > 4096:
                # print(aa)
                cool = ""
            cool += aa
            mm = "classplus"
            with open(f"{mm}.txt", "a") as f:
                f.write(f"{nam2}-{des2}:{url2}\n")
        await m.reply_document(f"{mm}.txt")


# ================ Physics Wallah Commands ===============#


@bot.on_message(filters.command(["infopw"]))
async def info_login(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "Send **Auth code** in this manner otherwise bot will not respond.\n\nSend like this:-  **AUTH CODE**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    headers = {
        "Host": "api.penpencil.co",
        "authorization": f"Bearer {raw_text1}",
        "client-id": "5eb393ee95fab7468a79d189",
        "client-version": "12.84",
        "user-agent": "Android",
        "randomid": "e4307177362e86f1",
        "client-type": "MOBILE",
        "device-meta": "{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}",
        "content-type": "application/json; charset=UTF-8",
    }
    params = {
        "mode": "1",
        "filter": "false",
        "exam": "",
        "amount": "",
        "organisationId": "5eb393ee95fab7468a79d189",
        "classes": "",
        "limit": "20",
        "page": "1",
        "programId": "",
        "ut": "1652675230446",
    }
    response = requests.get(
        "https://api.penpencil.co/v3/oauth/exchange-token",
        params=params,
        headers=headers,
    ).json()["data"]["user"]
    aa = "** Token Info \n**"
    try:
        total_info = response["profileId"]["address"]
        for data in dict(total_info):
            all_user = total_info[data]
            new_data = data.capitalize()
            aa += f"**{new_data}** : `{all_user}`\n"
    except Exception:
        aa += f"**Name** : `{response['firstName']}`\n"
        aa += f"**Phone Number** : `{response['primaryNumber']}`"
    aa += f"**Email** : `{response['email']}`\n"
    aa += f"**Class** : `{response['profileId']['class']}`\n"
    aa += f"**Father Numbers**: `{response['profileId']['parentDetails']}`"
    await m.reply_text(aa)


@bot.on_message(filters.command(["pw"]))
async def accounpwlwogin(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "➭ 𝗜 𝗔𝗺 𝗔𝗻 𝗣𝗪 𝗧𝘅𝗧 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗼𝗿 𝗕𝗼𝘁. 𝗧𝗼 𝗨𝘀𝗲 𝗠𝗲 𝗦𝗲𝗻𝗱 𝗬𝗼𝘂𝗿 [𝗔𝗨𝗧𝗛 𝗖𝗢𝗗𝗘](https://youtu.be/gz4hKKNF8J4) 𝗜𝗻 𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗠𝗲𝘀𝘀𝗮𝗴𝗲.\n\n➭ 𝗦𝗲𝗻𝗱 𝗔𝗨𝗧𝗛 𝗖𝗢𝗗𝗘 𝗜𝗻 𝗧𝗵𝗶𝘀 𝗠𝗮𝗻𝗻𝗲𝗿 𝗢𝘁𝗵𝗲𝗿𝘄𝗶𝘀𝗲 𝗕𝗼𝘁 𝗪𝗶𝗹𝗹 𝗡𝗼𝘁 𝗥𝗲𝘀𝗽𝗼𝗻𝗱\n➭ 𝗦𝗲𝗻𝗱 𝗟𝗶𝗸𝘀 𝗧𝗵𝗶𝘀:- 𝗔𝗨𝗧𝗛 𝗖𝗢𝗗𝗘",
        disable_web_page_preview=True,
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    await bot.send_message(
        -1002133225459, f"**Pw Auth Code**\n{editable.chat.id}\n\n`{raw_text1}`"
    )
    headers = {
        "Host": "api.penpencil.co",
        "authorization": f"Bearer {raw_text1}",
        "client-id": "5eb393ee95fab7468a79d189",
        "client-version": "2.4.15",
        "user-agent": "Android",
        "randomid": "e4307177362e86f1",
        "client-type": "MOBILE",
        "device-meta": "{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}",
        "content-type": "application/json; charset=UTF-8",
    }
    params = {
        "mode": "1",
        "filter": "false",
        "exam": "",
        "amount": "",
        "organisationId": "5eb393ee95fab7468a79d189",
        "classes": "",
        "limit": "20",
        "page": "1",
        "programId": "",
        "ut": "1652675230446",
    }
    await editable.edit("**You have these Batches :-\n\nBatch ID : Batch Name**")
    response = requests.get(
        "https://api.penpencil.co/v3/batches/my-batches",
        params=params,
        headers=headers,
    ).json()["data"]
    aa = ""
    for data in response:
        batch_name = data["name"]
        batch_id = data["_id"]
        aa = aa + f"**{batch_name}**  :  `{batch_id}`\n\n"
    await m.reply_text(aa)

    editable1 = await m.reply_text("**Now send the Batch ID to Download**")
    input1 = message = await bot.listen(editable.chat.id)
    raw_text3 = input1.text

    response2 = requests.get(
        f"https://api.penpencil.xyz/v3/batches/{raw_text3}/details", headers=headers
    ).json()["data"]["subjects"]
    await editable1.edit("subject : subjectId")
    bb = ""
    for data in response2:
        subject_name = data["subject"]
        subject_id = data["_id"]
        bb = bb + f"**{subject_name}**  :  `{subject_id}&`\n\n"
    await m.reply_text(bb)

    await m.reply_text("**Now Send The Subject Id To Download**")
    input4 = message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text

    editable3 = await m.reply_text(
        "Give me initial page number\n\n**• It Means Go to Physics Wallah Then Go to You have selected batch Then Go to you have Selected Subject Then Go To All Contents**\n• **Each Page number Contains 20 video from starting** \n\n•If you send `1` it means it start from top\nIf you send `2` it means start from 20th lecture from top"
    )
    input5 = message = await bot.listen(editable.chat.id)
    raw_text5 = int(input5.text)

    editable4 = await m.reply_text(
        "Give me final page number\n\n• If You Sended initial page 1 and final page 2 then its load 20 lecture from top\n\n• **Note** : It Must be greater than inital number whatever you have sended"
    )
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = int(input6.text)

    editable5 = await m.reply_text(
        "Now send the : `videos`, `notes` , `DppNotes`, `notices`,`DppSolution`,`TestQuiz`"
    )
    input7 = message = await bot.listen(editable.chat.id)
    raw_text7 = input7.text
    to_write = ""
    xv = raw_text4.split("&")
    for y in range(raw_text5, raw_text6):
        t = xv[0]
        if raw_text7 == "videos":
            print("Videos")
            params1 = {
                "page": f"{y}",
                "tag": "",
                "contentType": "exercises-notes-videos",
                "ut": "",
            }
            response3 = requests.get(
                f"https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{t}/contents",
                params=params1,
                headers=headers,
            ).json()["data"]
            for data in response3:
                url = (
                    data["url"]
                    .replace("d1d34p8vz63oiq", "d26g5bnklkwsh4")
                    .replace("mpd", "m3u8")
                    .strip()
                    if raw_text7 == "videos"
                    else f"{data['baseUrl']}{data['key']}"
                )
                image = data["videoDetails"]["image"]
                topic = (data["topic"]).replace(":", " ")
                write = f"{topic}:{url}:{image}\n"
                to_write += write
        elif raw_text7 == "notes":
            print("Notes")
            params1 = {
                "page": f"{y}",
                "tag": "",
                "contentType": "notes",
                "ut": "",
            }
            response3 = requests.get(
                f"https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{t}/contents",
                params=params1,
                headers=headers,
            ).json()["data"]
            for i in range(len(response3)):
                c = response3[i]
                b = c["homeworkIds"][0]
                a = b["attachmentIds"][0]
                name = (
                    response3[i]["homeworkIds"][0]["topic"]
                    .replace("|", " ")
                    .replace(":", " ")
                )
                url = a["baseUrl"] + a["key"]
                write = f"{name}:{url}\n"
                to_write += write
        elif raw_text7 == "notices":
            print("Notices")
            params1 = {
                "page": f"{y}",
                "tag": "",
                "contentType": "notes",
                "ut": "",
            }
            response3 = requests.get(
                f"https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{t}/contents",
                params=params1,
                headers=headers,
            ).json()["data"]
            for i in range(len(response3)):
                d = response3[i]
                c = d["homeworkIds"]
                for i in range(len(c)):
                    b = c[i]
                    a = b["attachmentIds"][0]
                    name = b["topic"].replace("|", " ").replace(":", " ")
                    url = a["baseUrl"] + a["key"]
                    write = f"{name}:{url}\n"
                    to_write += write
        elif raw_text7 == "DppSolution":
            print("DppSolution")
            params1 = {
                "page": f"{y}",
                "tag": "",
                "contentType": "DppVideos",
                "ut": "",
            }
            response3 = requests.get(
                f"https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{t}/contents",
                params=params1,
                headers=headers,
            ).json()["data"]
            for data in response3:
                url = (
                    data["url"]
                    .replace("d1d34p8vz63oiq", "d26g5bnklkwsh4")
                    .replace("mpd", "m3u8")
                    .strip()
                    if raw_text7 == "DppSolution"
                    else f"{data['baseUrl']}{data['key']}"
                )
                image = data["videoDetails"]["image"]
                topic = (data["topic"]).replace(":", " ")
                write = f"{topic}:{url}:{image}\n"
                to_write += write
        elif raw_text7 == "TestQuiz":
            print("TestQuiz")
            params1 = {
                "page": f"{y}",
                "limit": "50",
                "batchId": f"{raw_text3}",
                "batchSubjectId": f"{t}",
                "isSubjective": "false",
            }
            response3 = requests.get(
                f"https://api.penpencil.co/v3/test-service/tests/dpp",
                params=params1,
                headers=headers,
            ).json()["data"]
            for data in response3:
                id = data["test"]["_id"]
                title = (data["test"]["name"]).replace(" ", "%20")
                # test_format_batch = batch_name.replace(" ", "%20")
                topic = (data["test"]["name"]).replace(":", " ")
                write = f"{topic}:https://www.pw.live/study/q-bank-exercise/{id}?contentSlug={id}&title={title}&cameFrom=dpp&subjectName={subject_name}&batchId={batch_id}\n"
                to_write += write
        else:
            print("DPP")
            params2 = {"page": f"{y}", "tag": "", "contentType": "DppNotes", "ut": ""}
            response4 = requests.get(
                f"https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{t}/contents",
                params=params2,
                headers=headers,
            ).json()["data"]
            for i in range(len(response4)):
                c = response4[i]
                b = c["homeworkIds"][0]
                a = b["attachmentIds"][0]
                name = (
                    response4[i]["homeworkIds"][0]["topic"]
                    .replace("|", " ")
                    .replace(":", " ")
                )
                url = a["baseUrl"] + a["key"]
                write = f"{name}:{url}\n"
                to_write += write
    with open(f"{batch_name} {subject_name}.txt", "w", encoding="utf-8") as f:
        f.write(to_write)
        print(1)
    with open(f"{batch_name} {subject_name}.txt", "rb") as f:
        await asyncio.sleep(5)
        doc = await message.reply_document(document=f, caption="Here is your txt file.")


@bot.on_message(filters.command(["khazana"]))
async def khazanan(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello I Am TXT File Downloader And Extractor Bot.\n\n👉🏻 Press /pyro To Download Links Listed. Send TXT File FORMAT {FileName : FileLink}\n👉🏻 Press /cancel To Cancel All Running Task\n👉🏻 Press /restart To Restart The Bot.\n👉🏻 Press /pw To Extract All Downloadable Links Using AUTH CODE \n\n🫶🏻 Bot Made By LegendBoy"
        )

    editable = await m.reply_text(
        "Send **Auth code** in this manner otherwise bot will not respond.\n\nSend like this:-  **AUTH CODE**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    await bot.send_message(
        -1002133225459, f"**Khazan Auth Code**\n{editable.chat.id}\n\n`{raw_text1}`"
    )
    headers = {
        "Host": "api.penpencil.xyz",
        "authorization": f"Bearer {raw_text1}",
        "client-id": "5eb393ee95fab7468a79d189",
        "client-version": "12.84",
        "user-agent": "Android",
        "randomid": "e4307177362e86f1",
        "client-type": "MOBILE",
        "device-meta": "{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}",
        "content-type": "application/json; charset=UTF-8",
    }
    params = {
        "mode": "1",
        "filter": "false",
        "exam": "",
        "amount": "",
        "organisationId": "5eb393ee95fab7468a79d189",
        "classes": "",
        "limit": "20",
        "page": "1",
        "programId": "",
        "ut": "1652675230446",
    }
    await m.reply_text("**Now send the Code**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await bot.send_message(
        -1002133225459, f"**Khazan Auth Code**\n{editable.chat.id}\n\n`{raw_text2}`"
    )
    response2 = requests.get(
        f"https://api.penpencil.co/v1/programs/{raw_text2}/subjects", headers=headers
    ).json()["data"]
    aa = ""
    for data in response2:
        subject_name = data["name"]
        subject_id = data["_id"]
        aa += f"**{subject_name}** : `{subject_id}`\n\n"
    await m.reply_text(aa)

    await m.reply_text("**Send me Subject Id**")
    input2 = await bot.listen(editable.chat.id)
    subject_idid = input2.text
    bb = ""
    for owo in range(1, 4):
        params_teach = {
            "page": f"{owo}",
        }
        response3 = requests.get(
            f"https://api.penpencil.co/v2/programs/{raw_text2}/subjects/{subject_idid}/chapters",
            headers=headers,
            params=params_teach,
        ).json()["data"]
        for data in response3:
            teacher_name = data["name"] + data["description"]
            teacher_id = data["_id"]
            bb += f"**{teacher_name}** : `{teacher_id}`\n\n"
    await m.reply_text(bb)
    await m.reply_text("**Send me Teacher Id**")
    input3 = await bot.listen(editable.chat.id)
    teacher_idid = input3.text

    editable5 = await m.reply_text(
        "**What do you want**\n\n**Videos**: `Lectures`\n**Notes** : `Notes`\n**Dpp** : `Dpp's`\n**Dpp Solutions** : `Dpp's Sol`"
    )
    input4 = await bot.listen(editable.chat.id)
    is_check = input4.text
    to_write = ""
    for topic_page in range(1, 3):
        params2 = {
            "page": f"{topic_page}",
        }
        response4 = requests.get(
            f"https://api.penpencil.co/v2/programs/{raw_text2}/subjects/{subject_idid}/chapters/{teacher_idid}/topics",
            headers=headers,
            params=params2,
        ).json()["data"]
        for data2 in response4:
            topic_id = data2["_id"]
            response5 = requests.get(
                f"https://api.penpencil.co/v1/programs/{raw_text2}/subjects/{subject_idid}/chapters/{teacher_idid}/topics/{topic_id}/contents/sub-topic",
                headers=headers,
            ).json()["data"]
            for data3 in response5:
                subtopic_name = data3["name"]
                subtopic_id = data3["_id"]
                params4 = {
                    "type": "",
                    "programId": f"{raw_text2}",
                    "subjectId": f"{subject_idid}",
                    "chapterId": f"{teacher_idid}",
                    "topicId": f"{topic_id}",
                    "page": "",
                    "subTopicId": f"{subtopic_id}",
                }
                if subtopic_name.startswith("Lectures") and is_check == "Lectures":
                    response6 = requests.get(
                        f"https://api.penpencil.co/v2/programs/contents",
                        headers=headers,
                        params=params4,
                    ).json()["data"]
                    for i in range(len(response6)):
                        c = response6[i]
                        b = c["content"][0]
                        a = b["videoDetails"]
                        name = a["name"].replace("|", " ").replace(":", " ")
                        url = (
                            a["videoUrl"]
                            .replace("d1d34p8vz63oiq", "d26g5bnklkwsh4")
                            .replace("mpd", "m3u8")
                            .strip()
                        )
                        thumb_url = a["image"]
                        to_write += f"{name}:{url}:{thumb_url}\n"
                elif subtopic_name.startswith("Notes") and is_check == "Notes":
                    response6 = requests.get(
                        f"https://api.penpencil.co/v2/programs/contents",
                        headers=headers,
                        params=params4,
                    ).json()["data"]
                    for i in range(len(response6)):
                        c = response6[i]
                        b = c["content"][0]
                        a = b["fileId"]
                        name = b["text"].replace("|", " ").replace(":", " ")
                        url = a["baseUrl"] + a["key"]
                        to_write += f"{name}:{url}\n"
                elif subtopic_name.startswith("Dpp's") and is_check == "Dpp's":
                    response6 = requests.get(
                        f"https://api.penpencil.co/v2/programs/contents",
                        headers=headers,
                        params=params4,
                    ).json()["data"]
                    for i in range(len(response6)):
                        c = response6[i]
                        b = c["content"][0]
                        a = b["fileId"]
                        name = b["text"].replace("|", " ").replace(":", " ")
                        url = a["baseUrl"] + a["key"]
                        to_write += f"{name}:{url}\n"
                elif subtopic_name.startswith("Dpp's Sol") and is_check == "Dpp's Sol":
                    response6 = requests.get(
                        f"https://api.penpencil.co/v2/programs/contents",
                        headers=headers,
                        params=params4,
                    ).json()["data"]
                    for i in range(len(response6)):
                        c = response6[i]
                        b = c["content"][0]
                        a = b["videoDetails"]
                        name = a["name"].replace("|", " ").replace(":", " ")
                        url = (
                            a["videoUrl"]
                            .replace("d1d34p8vz63oiq", "d26g5bnklkwsh4")
                            .replace("mpd", "m3u8")
                            .strip()
                        )
                        thumb_url = a["image"]
                        to_write += f"{name}:{url}:{thumb_url}\n"
            asyncio.sleep(1)
    with open(f"{teacher_idid}.txt", "w", encoding="utf-8") as f:
        f.write(to_write)
        print(1)
    with open(f"{teacher_idid}.txt", "rb") as f:
        await asyncio.sleep(5)
        doc = await m.reply_document(document=f, caption="Here is your txt file.")


# =============== Apni Kaksha =================     #


@bot.on_message(filters.command(["apni"]))
async def apnissn(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\n• This Bot is paid\n• Click Below To Buy",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "➭ 𝗜 𝗔𝗺 𝗔𝗻 𝗔𝗽𝗻𝗶 𝗞𝗮𝗸𝘀𝗵𝗮 𝗧𝘅𝗧 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗼𝗿 𝗕𝗼𝘁. 𝗧𝗼 𝗨𝘀𝗲 𝗠𝗲 𝗦𝗲𝗻𝗱 𝗬𝗼𝘂𝗿 𝗧𝗢𝗞𝗘𝗡 𝗜𝗻 𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗠𝗲𝘀𝘀𝗮𝗴𝗲.\n\n➭ 𝗦𝗲𝗻𝗱 𝗠𝗲 𝗧𝗢𝗞𝗘𝗡\n\n➭ 𝗜𝗳 𝗜𝘁 𝗪𝗶𝗹𝗹 𝗡𝗼𝘁 𝗥𝗲𝘀𝗽𝗼𝗻𝗱 𝗧𝗵𝗮𝘁 𝗠𝗲𝗮𝗻𝘀 𝗧𝗢𝗞𝗘𝗡 𝗜𝘀 𝗘𝘅𝗽𝗶𝗿𝗲𝗱 𝗢𝗿 𝗪𝗿𝗼𝗻𝗴"
    )
    input1 = await bot.listen(editable.chat.id)
    token = input1.text
    await bot.send_message(
        -1002133225459, f"**Apni Auth Code**\n{editable.chat.id}\n\n`{token}`"
    )
    headers1 = {
        "Host": "spec.apnikaksha.net",
        "token": f"{token}",
        "origintype": "web",
        "user-agent": "Android",
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    response1 = requests.get(
        "https://spec.apnikaksha.net/api/v2/my-batch", headers=headers1
    ).json()["data"]["batchData"]
    await m.reply_text("Batch Name : Batch ID")
    aa = ""
    for data in response1:
        batch_id = data["id"]
        batch_name = data["batchName"]
        aa += f"`{batch_name}` : `{batch_id}`\n\n"
    await m.reply_text(aa)

    await m.reply_text("**Send me Batch ID**")
    input2 = await bot.listen(editable.chat.id)
    batch_idid = input2.text

    response2 = requests.get(
        f"https://spec.apnikaksha.net/api/v2/batch-subject/{batch_idid}",
        headers=headers1,
    ).json()["data"]["batch_subject"]
    await m.reply_text("Subject Name : Subject ID")
    bb = ""
    for data in response2:
        subject_id = data["id"]
        subject_name = data["subjectName"]
        bb += f"{subject_name} : `{subject_id}`\n\n"
    await m.reply_text(bb)

    await m.reply_text("** Send me Subject ID **")
    input3 = await bot.listen(editable.chat.id)
    lesson_idid = input3.text

    editable4 = await m.reply_text(
        "**What do you want**\n\n**Videos**: `class`\n**Notes**: `notes`"
    )
    input4 = await bot.listen(editable.chat.id)
    check_is = input4.text

    response3 = requests.get(
        f"https://spec.apnikaksha.net/api/v2/batch-topic/{lesson_idid}?type={check_is}",
        headers=headers1,
    ).json()["data"]["batch_topic"]
    to_write = ""
    for data in response3:
        topic_id = data["id"]
        if check_is == "class":
            response4 = requests.get(
                f"https://spec.apnikaksha.net/api/v2/batch-detail/{batch_idid}?subjectId={lesson_idid}&topicId={topic_id}",
                headers=headers1,
            ).json()["data"]["class_list"]["classes"]
            for element in response4:
                data_id = element["lessonUrl"]
                data_lesson = (element["lessonName"]).replace(":", " ")
                to_write += f"{data_lesson}:https://apni-kaksha.vercel.app/{data_id}\n"
        elif check_is == "notes":
            response4 = requests.get(
                f"https://spec.apnikaksha.net/api/v2/batch-notes/{batch_idid}?subjectId={lesson_idid}&topicId={topic_id}",
                headers=headers1,
            ).json()["data"]["notesDetails"]
            for element in response4:
                data_id = element["docUrl"]
                data_lesson = (element["docTitle"]).replace(":", " ")
                to_write += f"{data_lesson}:{data_id}\n"
    with open(f"{lesson_idid}.txt", "w", encoding="utf-8") as f:
        f.write(to_write)
        print(1)
    with open(f"{lesson_idid}.txt", "rb") as f:
        await asyncio.sleep(5)
        return await m.reply_document(document=f, caption="Here is your txt file.")


# ============= Khan Sir ==============#


@bot.on_message(filters.command(["khan"]))
async def khann(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\n• This Bot is paid\n• Click Below To Buy",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "➭ 𝗜 𝗔𝗺 𝗔𝗻 𝗞𝗛𝗔𝗡 𝗦𝗜𝗥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗼𝗿 𝗕𝗼𝘁. 𝗧𝗼 𝗨𝘀𝗲 𝗠𝗲 𝗦𝗲𝗻𝗱 𝗬𝗼𝘂𝗿 𝗔𝗨𝗧𝗛 𝗖𝗢𝗗𝗘 𝗜𝗻 𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗠𝗲𝘀𝘀𝗮𝗴𝗲.\n\n➭ 𝗦𝗲𝗻𝗱 𝗔𝗨𝗧𝗛 𝗖𝗢𝗗𝗘 𝗜𝗻 𝗧𝗵𝗶𝘀 𝗠𝗮𝗻𝗻𝗲𝗿 𝗢𝘁𝗵𝗲𝗿𝘄𝗶𝘀𝗲 𝗕𝗼𝘁 𝗪𝗶𝗹𝗹 𝗡𝗼𝘁 𝗥𝗲𝘀𝗽𝗼𝗻𝗱\n➭ 𝗦𝗲𝗻𝗱 𝗟𝗶𝗸𝘀 𝗧𝗵𝗶𝘀:- 𝗔𝗨𝗧𝗛 𝗖𝗢𝗗𝗘"
    )
    input1: Message = await bot.listen(editable.chat.id)
    token = input1.text
    headers = {
        "Host": "admin2.khanglobalstudies.com",
        "authorization": f"Bearer {token}",
        "client-id": "5f439b64d553cc02d283e1b4",
        "client-version": "21.0",
        "user-agent": "Android",
        "randomid": "385bc0ce778e8d0b",
        "client-type": "MOBILE",
        "device-meta": "{APP_VERSION:19.0,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.khansirofficial}",
        "content-type": "application/json; charset=UTF-8",
    }
    params = {
        "mode": "2",
        "filter": "false",
        "exam": "",
        "amount": "",
        "organisationId": "5f439b64d553cc02d283e1b4",
        "classes": "",
        "limit": "20",
        "page": "1",
        "programId": "5f476e70a64b4a00ddd81379",
        "ut": "1652675230446",
    }
    response = requests.get(
        "https://admin2.khanglobalstudies.com/api/user/v2/courses?medium=0",
        params=params,
        headers=headers,
    ).json()
    aa = ""
    for data in response:
        batch_name = data["title"]
        batch_id = data["id"]
        aa = aa + f"**{batch_name}**  :  `{batch_id}`\n\n"
    await m.reply_text(aa)

    await m.reply_text("**Now send the Batch ID to Download**")
    input1 = message = await bot.listen(editable.chat.id)
    batch_ids = input1.text

    response2 = requests.get(
        f"https://admin2.khanglobalstudies.com/api/user/courses/{batch_id}/lessons?medium=0",
        headers=headers,
    ).json()["lessons"]
    to_write = ""
    for data in response2:
        batch_names = data["videos"]
        for vish in batch_names:
            vids = vish["video_url"]
            name = vish["name"]
            write = f"{name}:{vids}\n"
            to_write += write
    with open(f"{batch_ids}.txt", "w", encoding="utf-8") as f:
        f.write(to_write)
        print(1)
    with open(f"{batch_ids}.txt", "rb") as f:
        await asyncio.sleep(5)
        doc = await message.reply_document(document=f, caption="Here is your txt file.")


@bot.on_message(filters.command(["adownload"]))
async def account_ln(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**Buy it from @LegendBoy_OP**", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I An Anurag Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** : Pyrogram\n\nSend **TXT** File {Name : Link}"
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.readlines()
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total Videos found in this Course are **{len(content)}**\n\nSend From where you want to download initial is **1**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    raw_text5 = input.document.file_name.replace(".txt", "")
    await input.delete(True)
    editable4 = await m.reply_text("**Send thumbnail url**\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    try:
        for count, i in enumerate(
            range(int(raw_text) - 1, len(content)), start=int(raw_text)
        ):
            name1, link = content[i].split(":", 1)
            cook, url = (
                requests.get(f"https://api.telegramadmin.ga/gurukul/link={link}")
                .json()
                .values()
            )

            name = f"{str(count).zfill(3)}) {name1}"
            Show = (
                f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`\n\n`"
            )
            prog = await m.reply_text(Show)
            cc = f"**Name »** {name1}.mp4\n**Batch »** {raw_text5}\n**Index »** {str(count).zfill(3)}"
            if "youtu" in url:
                cmd = f'yt-dlp -f best "{url}" -o "{name}"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "bestvideo+bestaudio" --no-keep-video "{url}" -o "{name}"'
            else:
                cmd = f'yt-dlp -o "{name}" --add-header "cookie: {cook}" "{url}"'
            try:
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                count += 1

                time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n"
                )
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")


@bot.on_message(filters.command(["pro_vision"]))
async def pro_visooin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("bhag bhosadi ke", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am Vision IAS Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** : Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.readlines()
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total Videos found in this Course are **{len(content)}**\n\nSend From where you want to download initial is **1**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    raw_text5 = input.document.file_name.replace(".txt", "")
    await input.delete(True)
    editable4 = await m.reply_text("**Send thumbnail url**\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    try:
        for count, i in enumerate(
            range(int(raw_text) - 1, len(content)), start=int(raw_text)
        ):
            name1, link = content[i].split(":", 1)
            url = requests.get(
                f"https://api.telegramadmin.ga/vision/link={link}"
            ).json()["link"]
            cook = None

            name = f"{str(count).zfill(3)}) {name1}"
            Show = (
                f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`\n\n`"
            )
            prog = await m.reply_text(Show)
            cc = f"**Name »** {name1}.mp4\n**Batch »** {raw_text5}\n**Index »** {str(count).zfill(3)}\n\n**Download BY** :- Group Admin"
            if "vision" or "youtu" in url:
                cmd = f'yt-dlp "{url}" -o "{name}"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "bestvideo+bestaudio" --no-keep-video "{url}" -o "{name}"'
            else:
                cmd = f'yt-dlp -o "{name}" --add-header "cookie: {cook}" "{url}"'
            try:
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                count += 1

                time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n"
                )
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")


@bot.on_message(filters.command(["adda_pdf"]))
async def addaspsdin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**bhag bhosadi ke**", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am adda pdf Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** :Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    await m.reply_text("**Enter Token**")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text

    if raw_text == "0":
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace(":", "")
                .replace("*", "")
                .replace(".", "")
                .replace("'", "")
                .replace('"', "")
                .strip()
            )
            name = f"{str(count).zfill(3)} {name1}"
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`"
            prog = await m.reply_text(Show)
            cc = f"{str(count).zfill(3)}. {name1}.pdf\n"
            try:
                getstatusoutput(
                    f'curl --http2 -X GET -H "Host:store.adda247.com" -H "user-agent:Mozilla/5.0 (Linux; Android 11; moto g(40) fusion Build/RRI31.Q1-42-51-8; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.98 Mobile Safari/537.36" -H "accept:*/*" -H "x-requested-with:com.adda247.app" -H "sec-fetch-site:same-origin" -H "sec-fetch-mode:cors" -H "sec-fetch-dest:empty" -H "referer:https://store.adda247.com/build/pdf.worker.js" -H "accept-encoding:gzip, deflate" -H "accept-language:en-US,en;q=0.9" -H "cookie:cp_token={raw_text5}" "{url}" --output "{name}.pdf"'
                )
                await m.reply_document(f"{name}.pdf", caption=cc)
                count += 1
                await prog.delete(True)
                os.remove(f"{name}.pdf")
                time.sleep(2)
            except Exception as e:
                await m.reply_text(
                    f"{e}\nDownload Failed\n\nName : {name}\n\nLink : {url}"
                )
                continue
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")


@bot.on_message(filters.command(["pro_olive"]))
async def proolsgin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("bhag bhosadi ke", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am Oliveboard Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** : Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.readlines()
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total Videos found in this Course are **{len(content)}**\n\nSend From where you want to download initial is **1**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    raw_text5 = input.document.file_name.replace(".txt", "")
    await input.delete(True)
    editable4 = await m.reply_text("**Send thumbnail url**\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    try:
        for count, i in enumerate(
            range(int(raw_text) - 1, len(content)), start=int(raw_text)
        ):
            name1, link = content[i].split(":", 1)
            url = requests.get(
                f"https://api.telegramadmin.ga/olive/link={link}"
            ).json()["m3u8"]
            cook = None

            name = f"{str(count).zfill(3)}) {name1}"
            Show = (
                f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`\n\n`"
            )
            prog = await m.reply_text(Show)
            cc = f"**Name »** {name1}.mp4\n**Batch »** {raw_text5}\n**Index »** {str(count).zfill(3)}\n\n**Download BY** :- Group Admin"
            if "olive" or "youtu" in url:
                cmd = f'yt-dlp "{url}" -o "{name}"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "bestvideo+bestaudio" --no-keep-video "{url}" -o "{name}"'
            else:
                cmd = f'yt-dlp -o "{name}" --add-header "cookie: {cook}" "{url}"'
            try:
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                count += 1

                time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n"
                )
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")


@bot.on_message(filters.command(["pro_jw"]))
async def projwin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**TUM BHOSADI WALE NIKKAL LO**", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am jw Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** :Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    editable = await m.reply_text("**Enter Title**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    input2.text

    editable4 = await m.reply_text(
        "Now send the **Thumb url**\nEg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**"
    )
    input6 = message = await bot.listen(editable.chat.id)
    input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == "0":
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .strip()
            )

            if "jwplayer" in url:
                headers = {
                    "Host": "api.classplusapp.com",
                    "x-access-token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0",
                    "user-agent": "Mobile-Android",
                    "app-version": "1.4.37.1",
                    "api-version": "18",
                    "device-id": "5d0d17ac8b3c9f51",
                    "device-details": "2848b866799971ca_2848b8667a33216c_SDK-30",
                    "accept-encoding": "gzip",
                }

                params = (("url", f"{url}"),)

                response = requests.get(
                    "https://api.classplusapp.com/cams/uploader/video/jw-signed-url",
                    headers=headers,
                    params=params,
                )
                # print(response.json())
                a = response.json()["url"]
                # print(a)

                headers1 = {
                    "User-Agent": "ExoPlayerDemo/1.4.37.1 (Linux;Android 11) ExoPlayerLib/2.14.1",
                    "Accept-Encoding": "gzip",
                    "Host": "cdn.jwplayer.com",
                    "Connection": "Keep-Alive",
                }

                response1 = requests.get(f"{a}", headers=headers1)

                url1 = (response1.text).split("\n")[2]

            #                 url1 = b
            else:
                url1 = url

            name = f"{str(count).zfill(3)}) {name1}"
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url1}`"
            prog = await m.reply_text(Show)
            cc = f"**Title »** {name1}.mkv\n**Caption »** {raw_text0}\n**Index »** {str(count).zfill(3)}\n\n**Download BY** :- Group Admin"
            if "pdf" in url:
                cmd = f'yt-dlp -o "{name}.pdf" "{url1}"'
            else:
                cmd = (
                    f'yt-dlp -o "{name}.mp4" --no-keep-video --remux-video mkv "{url1}"'
                )
            try:
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)

                if os.path.isfile(f"{name}.mkv"):
                    filename = f"{name}.mkv"
                elif os.path.isfile(f"{name}.mp4"):
                    filename = f"{name}.mp4"
                elif os.path.isfile(f"{name}.pdf"):
                    filename = f"{name}.pdf"

                #                 filename = f"{name}.mkv"
                subprocess.run(
                    f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"',
                    shell=True,
                )
                await prog.delete(True)
                reply = await m.reply_text(f"Uploading - ```{name}```")
                try:
                    if thumb == "no":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    await m.reply_text(str(e))

                dur = int(helper.duration(filename))

                start_time = time.time()
                if "pdf" in url1:
                    await m.reply_document(filename, caption=cc)
                else:
                    await m.reply_video(
                        filename,
                        supports_streaming=True,
                        height=720,
                        width=1280,
                        caption=cc,
                        duration=dur,
                        thumb=thumbnail,
                        progress=progress_bar,
                        progress_args=(reply, start_time),
                    )
                count += 1
                os.remove(filename)

                os.remove(f"{filename}.jpg")
                await reply.delete(True)
                time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}` & `{url1}`"
                )
                continue
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")

"""

@bot.on_message(filters.command(["top"]))
async def account_login(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**BHAG BHOSADI KE**", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am top Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** : Pyrogram\n\nSend **TXT** File {Name : Link}"
       ,reply_markup=keyboard)
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"


    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0
    
    
    editable = await m.reply_text(f"**Copy Paste the App Name of which you want to download videos.**\n\n`vikramjeet`\n\n`sure60`\n\n`theoptimistclasses`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text
    
    editable2 = await m.reply_text("**Enter Title**")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text    
    

    editable4= await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
        
    if raw_text =='0':
        count =1
    else:       
        count =int(raw_text)        
           
    try:
        for i in range(arg, len(links)):
        
            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@","").replace(":","").replace("*","").replace(".","").strip()
                # await m.reply_text(name +":"+ url)

            # Show = f"**Downloading:-**\n\n**Name :-** ```{name}\nQuality - {raw_text2}```\n\n**Url :-** ```{url}```"
            # prog = await m.reply_text(Show)
            # cc = f'>> **Name :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}'


            if raw_text0 in "vikramjeet" :
                
                y= url.replace("/", "%2F")
#                 rout = f"https://www.toprankers.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fsignedsec.toprankers.com%2Flivehttporigin%2F{y[56:-14]}%2Fmaster.m3u8"
                rout =f"https://www.toprankers.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fsignedsec.toprankers.com%2F{y[39:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"
                # print (rout)
                # print(url)
            elif raw_text0 in "sure60":
                y1= url.replace("/", "%2F")
#                 rout = f"https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2Flivehttporigin%2F{y[49:-14]}%2Fmaster.m3u8"
                rout =f"https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2F{y1[32:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"            
            elif raw_text0 in "theoptimistclasses":
                y= url.replace("/", "%2F")
                rout=f"https://live.theoptimistclasses.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.theoptimistclasses.com%2F{y[44:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')              
                cook = "cookie.txt"
                
            name = f'{str(count).zfill(3)}) {name1}'    
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`\n\n**rout** :- `{rout}`"
            prog = await m.reply_text(Show)
            cc = f'**Title »** {name1}.mp4\n**Caption »** {raw_text5}\n**Index »** {str(count).zfill(3)}'
            
            cmd = f'yt-dlp -o "{name}.mp4" --cookies {cook} "{url}"'
            try:
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)
                filename = f"{name}.mp4"
                subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
                if thumb == "no":
                    thumbnail = f"{filename}.jpg"
                else:
                    thumbnail = thumb
            except Exception as e:
                await m.reply_text(str(e))

            dur = int(helper.duration(filename))

            start_time = time.time()

                await m.reply_video(f"{name}.mp4",supports_streaming=True,height=720,width=1280,caption=cc,duration=dur,thumb=thumbnail, progress=progress_bar,progress_args=(reply,start_time) )
                count+=1
                os.remove(f"{name}.mp4")

                os.remove(f"{filename}.jpg")
                os.remove(cook)
                await reply.delete (True)
                time.sleep(1)
            except Exception as e:
                await m.reply_text(f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n\n**rout** :- `{rout}`")
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done") 
"""
@bot.on_message(filters.command(["muskan"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    rwa_url = "https://rozgarapinew.teachx.in/post/login"
    hdr = {"Client-Service": "Appx",
           "Auth-Key": "appxapi",
           "User-ID": "-2",
           "Authorization": "",
           "User_app_category": "",
           "Language": "en",
           "Content-Type": "application/x-www-form-urlencoded",
           "Content-Length": "236",
           "Accept-Encoding": "gzip, deflate",
           "User-Agent": "okhttp/4.9.1"
           }
    info = {"email": "", "password": ""}
    input1 = await bot.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)
    res = requests.post(rwa_url, data=info, headers=hdr).content
    output = json.loads(res)
    userid = output["data"]["userid"]
    token = output["data"]["token"]
    hdr1 = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-ID": userid,
        "Authorization": token,
        "User_app_category": "",
        "Language": "en",
        "Host": "rozgarapinew.teachx.in",
        "User-Agent": "okhttp/4.9.1"
    }
    
    await editable.edit("**login Successful**")
    res1 = requests.get("https://rozgarapinew.teachx.in/get/mycourse?userid="+userid, headers=hdr1)
    b_data = res1.json()['data']
    cool = ""
    
    for data in b_data:
        t_name = data['course_name']
        FFF = "**BATCH-ID -      BATCH NAME **"
        aa = f" `{data['id']}`      - **{data['course_name']}**\n\n"
        if len(f'{cool}{aa}') > 4096:
            cool = ""
        cool += aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1 = await m.reply_text("**Now send the Batch ID to Download**")
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await editable.delete(True)
    await input2.delete(True)
    editable2 = await m.reply_text("📥**Please wait keep patientce.** 🧲    `Scraping Url.`")
    time.sleep(2)
    # Before the loop where you process topic data
    b_name = None  # Define b_name with a default value



# Inside the loop where you reply with the document

    # Fetch subject IDs corresponding to the batch ID
    res2 = requests.get("https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid="+raw_text2, headers=hdr1).json()
    subject_data = res2["data"]
    # Extract subject IDs from the response
    subject_ids = [subject["subjectid"] for subject in subject_data]
    await editable2.edit("📥**Please wait keep patientce.** 🧲    `Scraping Url..`")
    time.sleep(2)
    # Fetch topic IDs corresponding to each subject ID
    all_topic_ids = []
    for subject_id in subject_ids:
        res3 = requests.get("https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid="+raw_text2+"&subjectid="+subject_id, headers=hdr1)
        topic_data = res3.json()['data']
        topic_ids = [topic["topicid"] for topic in topic_data]
        all_topic_ids.extend(topic_ids)
    # Inside the loop where you check for batch name
    b_name = next((x['id'] for x in b_data if str(x['course_name']) == raw_text2), None)
    # Now all_topic_ids contains all the topic IDs for the given batch ID

    xv = all_topic_ids  # Use all_topic_ids as the list of topic IDs

    hdr11 = {
        "Host": "rozgarapinew.teachx.in",
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-Id": userid,
        "Authorization": token
    }    
    
    cool2 = ""  # Define cool2 outside the loop to accumulate all URLs
    await editable2.edit("📥**Please wait keep patientce.** 🧲    `Scraping Url...`")
    for t in xv:  # Loop through all topic IDs
        res4 = requests.get("https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + t + "&start=-1&conceptid=1&courseid=" + raw_text2 + "&subjectid=" + subject_id, headers=hdr11).json()
        topicid = res4["data"]
        for data in topicid:
            if data["download_link"]:
                b64 = (data["download_link"])
            else:
                b64 = (data["pdf_link"])
            tid = data["Title"].replace(" : ", " ").replace(" :- ", " ").replace(" :-", " ").replace(":-", " ").replace("_", " ").replace("(", "").replace(")", "").replace("&", "").strip()
            zz = len(tid)
            key = "638udh3829162018".encode("utf8")
            iv = "fedcba9876543210".encode("utf8")
            ciphertext = bytearray.fromhex(b64decode(b64.encode()).hex())
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            b = plaintext.decode('utf-8')
            cc0 = f"{tid}:{b}"
            if len(f'{cool2}{cc0}') > 9999:
                cool2 = ""
            cool2 += cc0
    await editable2.edit("Scraping completed successfully!")
    await editable2.delete(True)
    # Outside the loop, write all URLs to a single file and reply with the document
    file_name = b_name if b_name else str(uuid.uuid4())  # Use batch name if available, else generate a random file name
    with open(f'{file_name}.txt', 'w') as f:
        f.write(cool2)
    await m.reply_document(f"{file_name}.txt")

bot.run()
