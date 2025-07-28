"""
🌐 Open Source Project - Tele-Userbot (Note : this is bot ready code means you can import token and start second client for bot)
👨‍💻 Developer: Gagan
📂 Repo: https://github.com/devgaganin/tele-userbot
📜 License: MIT

Built with ❤️ for the Telegram community.
"""

import os
import io
import re
import time
import json
import math
import base64
import random, string
import socket
import hashlib
import logging
import asyncio
from datetime import datetime, timedelta

from urllib.parse import urlparse, quote_plus
from collections import defaultdict
from typing import Dict, List, Optional, Union
import aiohttp
import requests
import pytz
import qrcode
import feedparser
import whoisdomain as whois
from PIL import Image
from bs4 import BeautifulSoup
from pyfiglet import figlet_format
from googlesearch import search as google_search
from pyppeteer import launch
from pyrogram import Client, filters, enums, idle
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)
from pyrogram.errors import (
    FloodWait,
    RPCError,
    UserNotParticipant,
    ChatAdminRequired
)
from pyrogram.enums import ChatType
from pyrogram.raw.types import (
    InputPeerChannel,
    UpdateGroupCall,
    InputGroupCall,
)

from pyrogram.raw.functions.account import (
    UpdateProfile,
    UpdateUsername
)
from pyrogram.raw.functions.channels import EditTitle
from pyrogram.raw.functions.phone import (
    CreateGroupCall,
)

import sys
from config import API_ID, API_HASH, SESSION_STRING, UNPLASH_API as api_key

if not API_ID or not API_HASH or not SESSION_STRING:
    print("One of the required config values is missing: API_ID, API_HASH, or SESSION_STRING")
    sys.exit()

if not api_key:
    print("You can't use the .img command since the Unsplash API key is not provided in config")

app = Client(
    "ultra_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    workers=20
)
app.start_time = datetime.now()
print(f"👑 ULTRA USERBOT ONLINE — Start time: {app.start_time.strftime('%Y-%m-%d %H:%M:%S')}")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


MEDIA_DIR = "saved_media"
AUTO_REPLY_FILE = "auto_replies.json"
BLOCKED_USERS_FILE = "blocked_users.json"
NOTES_FILE = "notes.json"
REMINDERS_FILE = "reminders.json"
PROFILE_PICS_DIR = "profile_pics"
QUOTES_FILE = "quotes.json"
CUSTOM_COMMANDS_FILE = "custom_commands.json"
SCHEDULED_TASKS_FILE = "scheduled_tasks.json"
USER_DATA_FILE = "user_data.json"
GROUP_SETTINGS_FILE = "group_settings.json"


for directory in [MEDIA_DIR, PROFILE_PICS_DIR, "downloads", "temp"]:
    os.makedirs(directory, exist_ok=True)


auto_replies = {}
blocked_users = set()
notes = {}
reminders = {}
custom_quotes = {}
custom_commands = {}
scheduled_tasks = {}
user_data = {}
group_settings = {}
afk_mode = False
afk_reason = ""
afk_start_time = None
chat_titles = {}
spam_protection = {}
user_stats = defaultdict(lambda: {"messages": 0, "commands": 0})
active_filters = {}
rss_feeds = {}
rss_last_check = {}
custom_menus = {}
auto_reactions = {}
scheduled_messages = {}
user_aliases = {}
group_aliases = {}


def load_data():
    global auto_replies, blocked_users, notes, reminders, custom_quotes, custom_commands
    global scheduled_tasks, user_data, group_settings
    try:
        for file_path, variable in [
            (AUTO_REPLY_FILE, auto_replies),
            (BLOCKED_USERS_FILE, blocked_users),
            (NOTES_FILE, notes),
            (REMINDERS_FILE, reminders),
            (QUOTES_FILE, custom_quotes),
            (CUSTOM_COMMANDS_FILE, custom_commands),
            (SCHEDULED_TASKS_FILE, scheduled_tasks),
            (USER_DATA_FILE, user_data),
            (GROUP_SETTINGS_FILE, group_settings)
        ]:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(variable, set):
                        variable.clear()
                        variable.update(data)
                    else:
                        variable.clear()
                        variable.update(data)
    except Exception as e:
        logger.error(f"Error loading  {e}")


def save_data():
    try:
        mappings = [
            (AUTO_REPLY_FILE, auto_replies),
            (BLOCKED_USERS_FILE, list(blocked_users)),
            (NOTES_FILE, notes),
            (REMINDERS_FILE, reminders),
            (QUOTES_FILE, custom_quotes),
            (CUSTOM_COMMANDS_FILE, custom_commands),
            (SCHEDULED_TASKS_FILE, scheduled_tasks),
            (USER_DATA_FILE, user_data),
            (GROUP_SETTINGS_FILE, group_settings)
        ]
        
        for file_path, data in mappings:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving  {e}")


load_data()

# Split help text into categories
HELP_CATEGORIES = {
    "admin": """**👑 ADMINISTRATION:**
- `.ban [reply/user_id]` - Ban user
- `.unban [user_id]` - Unban user
- `.kick [reply/user_id]` - Kick user
- `.rmdel` - Kick deleted accounts 
- `.rmbots` - Kick bots
- `.promote [reply/user_id] [rank]` - Promote user
- `.demote [reply/user_id]` - Demote admin
- `.pin [reply]` - Pin message
- `.unpin [reply]` - Unpin message
- `.vc ` - VC on
- `.mute [reply/user_id] [time]` - Mute user
- `.unmute [reply/user_id]` - Unmute user
- `.purge [reply]` - Delete messages
- `.purgeall` - Nuke all messages 
- `.del [reply]` - Delete replied message
- `.lock [perm]` - Lock chat permissions
- `.unlock [perm]` - Unlock permissions
- `.admins` - List admins
- `.bots` - List bots
- `.users` - List users
- `.zombies` - Find deleted accounts
- `.settitle [title]` - Set chat title
- `.restoretitle` - Restore original title
- `.welcome [on/off] [msg]` - Welcome message
- `.goodbye [on/off] [msg]` - Goodbye message
- `.filter [trigger] [response]` - Add filter
- `.filters` - List filters
- `.stop [trigger]` - Remove filter""",

    "media": """**💾 MEDIA & STORAGE:**
- `.save [reply]` - Save media (forward/download)
- `.get [file_id]` - Get saved file
- `.files` - List saved files
- `.delmedia [file_id]` - Delete saved file
- `.cloud` - Cloud storage menu
- `.backup` - Backup all data
- `.restore` - Restore from backup""",

    "security": """**🛡️ PRIVACY & SECURITY:**
- `.block [reply/user_id]` - Block user
- `.unblock [user_id]` - Unblock user
- `.blocked` - List blocked users
- `.afk [reason]` - Set AFK mode
- `.unafk` - Disable AFK mode
- `.ghost [on/off]` - Ghost mode (invisible)
- `.antispam [on/off]` - Anti-spam protection
- `.captcha [on/off]` - CAPTCHA for new users
- `.report [reply]` - Report message
- `.whitelist [user_id]` - Whitelist user""",

    "automation": """**🤖 AUTOMATION & CUSTOM:**
- `.autoreply [trigger] [response]` - Set auto reply
- `.delreply [trigger]` - Delete auto reply
- `.addclean` - Auto clean system messages 
- `.remclean` - Disable Auto clean
- `.cleanstatus` - Addclean status
- `.replies` - List all auto replies
- `.alias [name] [command]` - Create command alias
- `.unalias [name]` - Remove alias
- `.aliases` - List aliases
- `.menu [name] [buttons]` - Create custom menu
- `.menus` - List menus
- `.reaction [trigger] [emoji]` - Auto reaction
- `.delreaction [trigger]` - del reaction
- `.schedule [time] [command]` - Schedule task
- `.unschedule [id]` - Cancel scheduled task
- `.tasks` - List scheduled tasks""",

    "notes": """**📝 NOTES & REMINDERS:**
- `.note [name] [content]` - Save a note
- `.getnote [name]` - Get a note
- `.delnote [name]` - Delete a note
- `.notes` - List all notes
- `.remind [time] [message]` - Set reminder
- `.reminders` - List all reminders
- `.todo [task]` - Add todo item
- `.todos` - List todo items
- `.done [id]` - Mark todo as done""",

    "search": """**🌐 SEARCH & TRANSLATION:**
- `.search [query]` - Search YouTube
- `.tr [lang] [text]` - Translate text
- `.wiki [query]` - Wikipedia search
- `.img [query]` - Image search
- `.weather [city]` - Weather information
- `.ud [word]` - Urban Dictionary
- `.define [word]` - Dictionary definition
- `.syn [word]` - Synonyms
- `.ant [word]` - Antonyms
- `.news [category]` - Latest news
- `.rss [url]` - Add RSS feed
- `.feeds` - List RSS feeds""",

    "profile": """**👤 PROFILE & PRESENCE:**
- `.setbio [text]` - Set profile bio
- `.setpic [reply/photo]` - Set profile picture
- `.setname [first] [last]` - Set name
- `.username [username]` - Set username
- `.qr [text]` - Generate QR code
- `.readqr [reply]` - Read QR code
- `.avatar [user_id]` - Get user avatar
- `.status [text]` - Set custom status
- `.clone [user_id]` - Clone profile
- `.revert` - Revert profile""",

    "fun": """**🎮 ENTERTAINMENT & FUN:**
- `.quote` - Random quote
- `.addquote [text]` - Add custom quote
- `.delquote [id]` - Delete custom quote
- `.myquotes` - List your quotes
- `.joke` - Random joke
- `.fact` - Random fact
- `.meme` - Random meme
- `.ascii [text]` - Convert text to ASCII art
- `.reverse [text]` - Reverse text
- `.mock [text]` - Mock text (aLtErNaTiNg cApS)
- `.vapor [text]` - Vaporwave text
- `.clap [text]` - Add claps between words
- `.emojify [text]` - Add random emojis
- `.spoiler [text]` - Create spoiler text
- `.password [length]` - Generate random password
- `.hash [text]` - Generate hash of text
- `.base64 [encode/decode] [text]` - Base64 encoding/decoding
- `.leet [text]` - 1337 speak
- `.flip [text]` - Flip text upside down
- `.cowsay [text]` - Cow says...
- `.roll [dice]` - Roll dice
- `.8ball [question]` - Magic 8 ball
- `.choose [option1|option2]` - Random choice""",

    "utils": """**⚙️ UTILITIES & TOOLS:**
- `.calc [expression]` - Calculator (works in reply too)
- `.ping` - Check bot response
- `.leave` - Leave current chat
- `.echo [text]` - Echo message
- `.type [text]` - Typing animation
- `.alive` - Bot status
- `.short [url]` - URL shortener
- `.expand [url]` - Expand short URL
- `.spb [user_id]` - Check SpamWatch
- `.whois [user_id]` - Advanced user info
- `.id [reply/user_id]` - Get IDs
- `.info [reply/user_id]` - Detailed user info
- `.stats` - Group statistics
- `.invite [user_id]` - Invite user to group
- `.export [chat_id]` - Export chat members
- `.import [file]` - Import members
- `.ss [url]` - Take website screenshot
- `.currency [amount] [from] [to]` - Currency converter
- `.time [location]` - Current time
- `.domain [domain]` - Domain info
- `.ip [ip]` - IP address info
- `.whoisdomain [domain]` - Whois domain lookup""",

    "dev": """**🔧 DEVELOPER & ADVANCED:**
- `.eval [code]` - Evaluate Python code
- `.exec [code]` - Execute Python code
- `.shell [command]` - Execute shell command
- `.restart` - Restart bot
- `.update` - Update bot
- `.logs` - Get bot logs
- `.sysinfo` - System information
- `.speedtest` - Network speed test
- `.pingall` - Ping all members
- `.broadcast [message]` - Broadcast message
- `.cleanup` - Clean up files
- `.debug [on/off]` - Debug mode""",

    "addons": """**📱 CUSTOM ADDONS:**
- `.addon [name]` - Load custom addon
- `.addons` - List available addons
- `.createaddon [name]` - Create new addon
- `.editaddon [name]` - Edit existing addon
- `.deleteaddon [name]` - Delete addon
- `.reloadaddons` - Reload all addons"""
}

MAIN_HELP = """**🚀 ULTRA USERBOT - PRO EDITION 🚀**

**📋 Available Categories:**
• `admin` - Administration commands
• `media` - Media & storage commands
• `security` - Privacy & security commands
• `automation` - Automation & custom commands
• `notes` - Notes & reminders
• `search` - Search & translation
• `profile` - Profile & presence
• `fun` - Entertainment & fun commands
• `utils` - Utilities & tools
• `dev` - Developer & advanced
• `addons` - Custom addons

**Usage:**
• `.help` - Show this menu
• `.help [category]` - Show specific category
• `.help all` - Show all commands (multiple messages)

**Examples:**
• `.help admin` - Show admin commands
• `.help fun` - Show fun commands"""

@app.on_message(filters.command("help", prefixes=".") & filters.me)
async def help_command(client: Client, message: Message):
    if len(message.command) > 1:
        category = message.command[1].lower()
        
        if category == "all":
            await message.edit_text("**🚀 Sending all help categories...**")
            await asyncio.sleep(1)
            
            for cat_name, cat_text in HELP_CATEGORIES.items():
                try:
                    await message.reply_text(cat_text, parse_mode=enums.ParseMode.MARKDOWN)
                    await asyncio.sleep(0.5) 
                except Exception as e:
                    await message.reply_text(f"Error sending {cat_name}: {str(e)}")
                    
            await message.edit_text("**✅ All help categories sent!**")
            
        elif category in HELP_CATEGORIES:
            try:
                await message.edit_text(HELP_CATEGORIES[category], parse_mode=enums.ParseMode.MARKDOWN)
            except Exception as e:
                await message.edit_text(f"Error: {str(e)}")
        else:
            available = ", ".join(HELP_CATEGORIES.keys())
            await message.edit_text(f"**❌ Invalid category!**\n\n**Available categories:**\n{available}\n\nUse `.help [category]` or `.help all`")
    else:
        try:
            await message.edit_text(MAIN_HELP, parse_mode=enums.ParseMode.MARKDOWN)
        except Exception as e:
            await message.edit_text(f"Error: {str(e)}")

# -------- BOT READY VERSION ----- 

@app.on_message(filters.command("helpx", prefixes=".") & filters.me)
async def help_paginated(client: Client, message: Message):
    """Alternative paginated help command"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Admin", callback_data="help_admin"),
         InlineKeyboardButton("💾 Media", callback_data="help_media")],
        [InlineKeyboardButton("🛡️ Security", callback_data="help_security"),
         InlineKeyboardButton("🤖 Automation", callback_data="help_automation")],
        [InlineKeyboardButton("📝 Notes", callback_data="help_notes"),
         InlineKeyboardButton("🌐 Search", callback_data="help_search")],
        [InlineKeyboardButton("👤 Profile", callback_data="help_profile"),
         InlineKeyboardButton("🎮 Fun", callback_data="help_fun")],
        [InlineKeyboardButton("⚙️ Utils", callback_data="help_utils"),
         InlineKeyboardButton("🔧 Dev", callback_data="help_dev")],
        [InlineKeyboardButton("📱 Addons", callback_data="help_addons")],
        [InlineKeyboardButton("📋 Show All", callback_data="help_all")]
    ])
    
    await message.edit_text(MAIN_HELP, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=keyboard)

# BOT READY VERSION ... (TEAM SPY)
@app.on_callback_query()
async def help_callback(client: Client, callback_query):
    if callback_query.data.startswith("help_"):
        category = callback_query.data.replace("help_", "")
        
        if category == "all":
            # Send all as separate messages
            await callback_query.message.edit_text("**🚀 Sending all help categories...**")
            for cat_name, cat_text in HELP_CATEGORIES.items():
                await callback_query.message.reply_text(cat_text, parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(0.5)
        elif category in HELP_CATEGORIES:
            await callback_query.message.edit_text(HELP_CATEGORIES[category], parse_mode=enums.ParseMode.MARKDOWN)
        
        await callback_query.answer()


def get_media_type(message: Message):
    if message.photo:
        return "photo"
    elif message.video:
        return "video"
    elif message.document:
        return "document"
    elif message.audio:
        return "audio"
    elif message.voice:
        return "voice"
    elif message.animation:
        return "animation"
    elif message.sticker:
        return "sticker"
    return None

async def check_admin(client: Client, chat_id: int, user_id: int):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except:
        return False

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def safe_eval(expression):
    """Safe evaluation of mathematical expressions"""

    expression = expression.replace(" ", "")
    

    allowed_chars = set('0123456789+-*/().%')
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")
    

    expression = expression.replace("%", "/100")
    

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception:
        raise ValueError("Invalid expression")

def mock_text(text):
    """Convert text to alternating caps (mocking)"""
    return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))

def vapor_text(text):
    """Convert text to vaporwave style"""
    vapor_map = {
        ' ': '　',
        '!': '！', '"': '＂', '#': '＃', '$': '＄', '%': '％', '&': '＆', "'": '＇',
        '(': '（', ')': '）', '*': '＊', '+': '＋', ',': '，', '-': '－', '.': '．',
        '/': '／', '0': '０', '1': '１', '2': '２', '3': '３', '4': '４', '5': '５',
        '6': '６', '7': '７', '8': '８', '9': '９', ':': '：', ';': '；', '<': '＜',
        '=': '＝', '>': '＞', '?': '？', '@': '＠', 'A': 'Ａ', 'B': 'Ｂ', 'C': 'Ｃ',
        'D': 'Ｄ', 'E': 'Ｅ', 'F': 'Ｆ', 'G': 'Ｇ', 'H': 'Ｈ', 'I': 'Ｉ', 'J': 'Ｊ',
        'K': 'Ｋ', 'L': 'Ｌ', 'M': 'Ｍ', 'N': 'Ｎ', 'O': 'Ｏ', 'P': 'Ｐ', 'Q': 'Ｑ',
        'R': 'Ｒ', 'S': 'Ｓ', 'T': 'Ｔ', 'U': 'Ｕ', 'V': 'Ｖ', 'W': 'Ｗ', 'X': 'Ｘ',
        'Y': 'Ｙ', 'Z': 'Ｚ', '[': '［', '\\': '＼', ']': '］', '^': '＾', '_': '＿',
        '`': '｀', 'a': 'ａ', 'b': 'ｂ', 'c': 'ｃ', 'd': 'ｄ', 'e': 'ｅ', 'f': 'ｆ',
        'g': 'ｇ', 'h': 'ｈ', 'i': 'ｉ', 'j': 'ｊ', 'k': 'ｋ', 'l': 'ｌ', 'm': 'ｍ',
        'n': 'ｎ', 'o': 'ｏ', 'p': 'ｐ', 'q': 'ｑ', 'r': 'ｒ', 's': 'ｓ', 't': 'ｔ',
        'u': 'ｕ', 'v': 'ｖ', 'w': 'ｗ', 'x': 'ｘ', 'y': 'ｙ', 'z': 'ｚ', '{': '｛',
        '|': '｜', '}': '｝', '~': '～'
    }
    
    result = ""
    for char in text:
        result += vapor_map.get(char, char)
    return result

def clap_text(text):
    """Add claps between words"""
    return " 👏 ".join(text.split())

def emojify_text(text):
    """Add random emojis to text"""
    emojis = ["😀", "😂", "🥰", "😎", "🤩", "😍", "🤗", "🤔", "😱", "🥳", "😭", "😡", "😴", "😈", "👻"]
    words = text.split()
    result = []
    for word in words:
        result.append(word)
        result.append(emojis[hash(word) % len(emojis)])
    return " ".join(result)

def spoiler_text(text):
    """Create spoiler text"""
    return f"||{text}||"

def generate_password(length=12):
    """Generate random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))


def leet_speak(text):
    """Convert text to 1337 speak"""
    leet_map = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
        'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7'
    }
    return ''.join(leet_map.get(c, c) for c in text)

def flip_text(text):
    """Flip text upside down"""
    flip_map = {
        'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ',
        'g': 'ƃ', 'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l',
        'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ',
        's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x',
        'y': 'ʎ', 'z': 'z', 'A': '∀', 'B': '𐐒', 'C': 'Ɔ', 'D': '◖',
        'E': 'Ǝ', 'F': 'Ⅎ', 'G': '⅁', 'H': 'H', 'I': 'I', 'J': 'ſ',
        'K': '⋊', 'L': '˥', 'M': 'W', 'N': 'N', 'O': 'O', 'P': 'Ԁ',
        'Q': 'Ό', 'R': 'ᴚ', 'S': 'S', 'T': '⊥', 'U': '∩', 'V': 'Λ',
        'W': 'M', 'X': 'X', 'Y': '⅄', 'Z': 'Z', '0': '0', '1': 'Ɩ',
        '2': 'ᄅ', '3': 'Ɛ', '4': 'ㄣ', '5': 'ϛ', '6': '9', '7': 'ㄥ',
        '8': '8', '9': '6', '.': '˙', ',': "'", '!': '¡', '?': '¿',
        '(': ')', ')': '(', '[': ']', ']': '[', '{': '}', '}': '{',
        '<': '>', '>': '<', '&': '⅋', '_': '‾'
    }
    return ''.join(flip_map.get(c, c) for c in text[::-1])

def cowsay(text):
    """Generate cowsay ASCII art"""
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    border = " " + "_" * (max_len + 2) + " "
    bottom_border = " " + "-" * (max_len + 2) + " "
    
    result = [border]
    for line in lines:
        padding = " " * (max_len - len(line))
        result.append(f"< {line}{padding} >")
    result.append(bottom_border)
    result.append("        \\   ^__^")
    result.append("         \\  (oo)\\_______")
    result.append("            (__)\\       )\\/\\")
    result.append("                ||----w |")
    result.append("                ||     ||")
    
    return "\n".join(result)

def roll_dice(dice_notation="1d6"):
    """Roll dice with notation like 2d6, 1d20, etc."""
    try:
        if 'd' in dice_notation:
            num, sides = map(int, dice_notation.split('d'))
        else:
            num, sides = 1, int(dice_notation)
        
        if num > 100 or sides > 1000:
            return "Too many dice or sides!"
        
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls)
        
        if len(rolls) == 1:
            return f"🎲 Rolled {rolls[0]} on a d{sides}"
        else:
            return f"🎲 Rolled {rolls} = {total} on {num}d{sides}"
    except:
        return "Invalid dice notation! Use format like 1d6, 2d20, etc."

def magic_8ball(question):
    """Magic 8 ball responses"""
    responses = [
        "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
        "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
        "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
        "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
        "Don't count on it", "My reply is no", "My sources say no",
        "Outlook not so good", "Very doubtful"
    ]
    return f"🎱 {random.choice(responses)}"

def random_choice(options):
    """Randomly choose from options"""
    choices = [opt.strip() for opt in options.split('|')]
    return f"🎲 I choose: {random.choice(choices)}"



@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_command(client: Client, message: Message):
    start = datetime.now()
    msg = await message.edit_text("Pinging...")
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await msg.edit_text(f"**Pong!🎈** `{latency}ms`")

@app.on_message(filters.command("alive", prefixes=".") & filters.me)
async def alive_command(client: Client, message: Message):
    from datetime import datetime

    try:
        uptime = datetime.now() - client.start_time
        days, seconds = uptime.days, uptime.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        await message.edit_text(
            f"**🚀 ULTRA USERBOT IS ALIVE!**\n⏱️ Uptime: `{uptime_str}`\n👑 Powered by Pyrogram royalty"
        )
    except Exception as e:
        await message.edit_text(f"❌ Error getting uptime:\n<code>{e}</code>")


@app.on_message(filters.command("id", prefixes=".") & filters.me)
async def id_command(client: Client, message: Message):
    chat_id = message.chat.id
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        await message.edit_text(f"**User ID:** `{user_id}`\n**Chat ID:** `{chat_id}`")
    else:
        await message.edit_text(f"**Chat ID:** `{chat_id}`")

@app.on_message(filters.command("ban", prefixes=".") & filters.me)
async def ban_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await message.edit_text("Reply to user or provide user ID")
    
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await message.edit_text(f"**Banned** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("kick", prefixes=".") & filters.me)
async def kick_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await message.edit_text("Reply to user or provide user ID")
    
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await client.unban_chat_member(message.chat.id, user_id)
        await message.edit_text(f"**Kicked** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("unban", prefixes=".") & filters.me)
async def unban_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if len(message.command) < 2:
        return await message.edit_text("Provide user ID to unban")
    
    user_id = message.command[1]
    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.edit_text(f"**Unbanned** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


@app.on_message(filters.command("rmdel", prefixes=".") & filters.me)
async def remove_deleted_accounts(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("❌ I'm not admin here!")

    zombies = []
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            zombies.append(member.user.id)

    if not zombies:
        return await message.edit_text("🧼 No deleted accounts found.")

    kicked = 0
    for user_id in zombies:
        try:
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            kicked += 1
        except Exception:
            continue

    await message.edit_text(f"🧟 Removed {kicked} deleted accounts!")


@app.on_message(filters.command("rmbots", prefixes=".") & filters.me)
async def remove_bots(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("❌ I'm not admin here!")

    bots = []
    async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
        bots.append(member.user.id)

    if not bots:
        return await message.edit_text("🤖 No bots found in chat.")

    removed = 0
    for user_id in bots:
        try:
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            removed += 1
        except Exception:
            continue

    await message.edit_text(f"🧹 Removed {removed} bots from chat!")



from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges

# 🎭 Role configs with full privileges, emoji, and description
ADMIN_ROLES = {
    "Admin": {
        "full": True,
        "emoji": "🔴",
        "desc": "Full control access"
    },
    "Godmode": {
        "full": True,
        "emoji": "🧨",
        "desc": "Nuclear override privileges"
    },
    "Overlord": {
        "full": True,
        "emoji": "☄️",
        "desc": "Supreme authority"
    },
    "Moderator": {
        "can_delete_messages": True,
        "can_restrict_members": True,
        "can_pin_messages": True,
        "emoji": "🛡️",
        "desc": "Moderation powers (delete, restrict, pin)"
    },
    "Minion": {
        "can_invite_users": True,
        "can_pin_messages": True,
        "emoji": "🪜",
        "desc": "Invite and pin access"
    },
    "Ghost": {
        "can_delete_messages": True,
        "can_manage_video_chats": True,
        "emoji": "👻",
        "desc": "Silent powers (delete, manage VC)"
    }
}

def get_admin_privileges(role: str) -> ChatPrivileges:
    config = ADMIN_ROLES.get(role.title(), {"full": True})
    if config.get("full"):
        return ChatPrivileges(
            can_manage_chat=True,
            can_change_info=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_video_chats=True
        )
    return ChatPrivileges(**{k: v for k, v in config.items() if isinstance(v, bool)})

def get_caption(role: str, user_id: int, action: str = "promote") -> str:
    config = ADMIN_ROLES.get(role.title(), {"emoji": "🔘", "desc": "Standard access"})
    if action == "promote":
        return f"{config['emoji']} **{role.upper()}** promoted `{user_id}`\n`{config['desc']}`"
    return f"🎭 `{user_id}` has been demoted. The throne is silent. 👑💀"

async def check_admin(client: Client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "owner")

@app.on_message(filters.command("promote", prefixes=".") & filters.me)
async def promote_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("❌ I'm not an admin here!")

    user_id = None
    role = "Admin"

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if len(message.command) > 1:
            role = " ".join(message.command[1:])
    elif len(message.command) > 2:
        user_id = int(message.command[1])
        role = " ".join(message.command[2:])
    elif len(message.command) > 1:
        user_id = int(message.command[1])
    else:
        return await message.edit_text("⚠️ Reply to user or provide user ID and role.")

    try:
        privileges = get_admin_privileges(role)
        await client.promote_chat_member(message.chat.id, user_id, privileges)
        await client.set_administrator_title(message.chat.id, user_id, role.title())
        await message.edit_text(get_caption(role, user_id, "promote"))
    except Exception as e:
        await message.edit_text(f"❌ Error:\n<code>{str(e)}</code>")

@app.on_message(filters.command("demote", prefixes=".") & filters.me)
async def demote_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("❌ I'm not an admin here!")

    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = int(message.command[1])
    else:
        return await message.edit_text("⚠️ Reply to a user or provide their ID to demote.")

    try:
        await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges())
        await client.set_administrator_title(message.chat.id, user_id, "")
        await message.edit_text(get_caption("Demoted", user_id, "demote"))
    except Exception as e:
        await message.edit_text(f"❌ Error while demoting:\n<code>{str(e)}</code>")

@app.on_message(filters.command("roles", prefixes=".") & filters.me)
async def roles_cmd(client: Client, message: Message):
    text = "🎭 **Available Roles:**\n\n"
    for role, config in ADMIN_ROLES.items():
        emoji = config.get("emoji", "🔘")
        desc = config.get("desc", "No description provided")
        text += f"{emoji} **{role}**\n`{desc}`\n\n"
    text += "**Usage:** `.promote <user> <role>`"
    await message.reply_text(text)





@app.on_message(filters.command("pin", prefixes=".") & filters.me)
async def pin_message(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if not message.reply_to_message:
        return await message.edit_text("Reply to a message to pin")
    
    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.id,
            disable_notification=False
        )
        await message.edit_text("**Pinned!**")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("unpin", prefixes=".") & filters.me)
async def unpin_message(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if not message.reply_to_message:
        return await message.edit_text("Reply to a pinned message to unpin")
    
    try:
        await client.unpin_chat_message(
            message.chat.id,
            message.reply_to_message.id
        )
        await message.edit_text("**Unpinned!**")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("mute", prefixes=".") & filters.me)
async def mute_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    user_id = None
    mute_time = 0
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if len(message.command) > 1:
            time_str = message.command[1]

            if time_str[-1] == 'm':
                mute_time = int(time_str[:-1]) * 60
            elif time_str[-1] == 'h':
                mute_time = int(time_str[:-1]) * 3600
            elif time_str[-1] == 'd':
                mute_time = int(time_str[:-1]) * 86400
            else:
                mute_time = int(time_str)
    elif len(message.command) > 2:
        user_id = message.command[1]
        time_str = message.command[2]
        if time_str[-1] == 'm':
            mute_time = int(time_str[:-1]) * 60
        elif time_str[-1] == 'h':
            mute_time = int(time_str[:-1]) * 3600
        elif time_str[-1] == 'd':
            mute_time = int(time_str[:-1]) * 86400
        else:
            mute_time = int(time_str)
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await message.edit_text("Reply to user or provide user ID and optional time")
    
    try:
        until_date = int(time.time() + mute_time) if mute_time > 0 else 0
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=client.get_chat(message.chat.id).permissions,
            until_date=until_date
        )
        time_text = f" for {mute_time//3600}h {mute_time%3600//60}m" if mute_time > 0 else ""
        await message.edit_text(f"**Muted** {user_id}{time_text}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("unmute", prefixes=".") & filters.me)
async def unmute_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await message.edit_text("Reply to user or provide user ID")
    
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=client.get_chat(message.chat.id).permissions
        )
        await message.edit_text(f"**Unmuted** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("purge", prefixes=".") & filters.me)
async def purge_messages(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if not message.reply_to_message:
        return await message.edit_text("Reply to start purging from")
    
    try:
        start_id = message.reply_to_message.id
        end_id = message.id
        deleted = 0
        
        for i in range(start_id, end_id + 1):
            try:
                await client.delete_messages(message.chat.id, i)
                deleted += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except:
                pass
        
        msg = await message.edit_text(f"**Purged {deleted} messages!**")
        await asyncio.sleep(3)
        await msg.delete()
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
import asyncio

# 🔧 Store enabled chat IDs
clean_enabled_chats = set()
clean_handler_ref = [None, None]

@app.on_message(filters.command("addclean", prefixes=".") & filters.me)
async def enable_clean_mode(client: Client, message: Message):
    global clean_handler_ref
    try:
        chat_id = message.chat.id
        if chat_id in clean_enabled_chats:
            return await message.edit_text("ℹ️ Clean mode is already active in this chat.")

        clean_enabled_chats.add(chat_id)

        if clean_handler_ref[0] is None:
            async def clean_service_message(client, msg):
                if msg.chat.id in clean_enabled_chats:
                    try:
                        await msg.delete()
                    except:
                        pass

            callback = lambda c, m: asyncio.create_task(clean_service_message(c, m))
            handler = MessageHandler(callback, filters.service)
            group = 99  # or any unique number
            app.add_handler(handler, group)
            clean_handler_ref = [handler, group]

        await message.edit_text("✅ Clean mode enabled in this chat. Service messages will auto-delete.")
    except Exception as e:
        await message.edit_text(f"⚠️ Error enabling clean mode:\n<code>{e}</code>")

@app.on_message(filters.command("remclean", prefixes=".") & filters.me)
async def disable_clean_mode(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        if chat_id not in clean_enabled_chats:
            return await message.edit_text("ℹ️ Clean mode is not active in this chat.")

        clean_enabled_chats.discard(chat_id)
        await message.edit_text("❎ Clean mode disabled in this chat. Service messages will remain.")
    except Exception as e:
        await message.edit_text(f"⚠️ Error disabling clean mode:\n<code>{e}</code>")

@app.on_message(filters.command("cleanstatus", prefixes=".") & filters.me)
async def check_clean_mode(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in clean_enabled_chats:
        await message.edit_text("🧼 Clean mode is <b>active</b> in this chat.")
    else:
        await message.edit_text("🧊 Clean mode is <b>disabled</b> in this chat.")




@app.on_message(filters.command("purgeall", prefixes=".") & filters.me)
async def nuke_chat(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        await message.edit_text("Purging all messages...")
        count = 0
        async for msg in client.get_chat_history(chat_id):
            try:
                await client.delete_messages(chat_id, msg.id)
                count += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except:
                pass
        confirmation = await message.edit_text(f"Nuked {count} messages 🦔👑👇")
        await asyncio.sleep(3)
        await confirmation.delete()
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")



@app.on_message(filters.command("del", prefixes=".") & filters.me)
async def delete_message(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to a message to delete")
    
    try:
        await client.delete_messages(
            message.chat.id,
            [message.reply_to_message.id, message.id]
        )
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("info", prefixes=".") & filters.me)
async def user_info(client: Client, message: Message):
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        user_id = message.from_user.id
    
    try:
        user = await client.get_users(user_id)
        chat_member = await client.get_chat_member(message.chat.id, user_id)
        
        info = f"**User Info:**\n"
        info += f"ID: `{user.id}`\n"
        info += f"Name: [{user.first_name}](tg://user?id={user.id})"
        if user.last_name:
            info += f" {user.last_name}"
        info += "\n"
        if user.username:
            info += f"Username: @{user.username}\n"
        info += f"Bot: {user.is_bot}\n"
        info += f"Verified: {user.is_verified}\n"
        info += f"Restricted: {user.is_restricted}\n"
        info += f"Scam: {user.is_scam}\n"
        info += f"Premium: {user.is_premium}\n"
        info += f"Status: {chat_member.status.value}"
        await message.edit_text(info)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("admins", prefixes=".") & filters.me)
async def list_admins(client: Client, message: Message):
    try:
        admins = []
        async for admin in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.user.is_bot:
                admins.append(f"[{admin.user.first_name}](tg://user?id={admin.user.id})")
        
        admin_list = "**Admins:**\n" + "\n".join(admins)
        await message.edit_text(admin_list)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("invite", prefixes=".") & filters.me)
async def invite_user(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if len(message.command) < 2:
        return await message.edit_text("Provide user ID to invite")
    
    user_id = message.command[1]
    try:
        await client.add_chat_members(message.chat.id, [user_id])
        await message.edit_text(f"**Invited** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("stats", prefixes=".") & filters.me)
async def chat_stats(client: Client, message: Message):
    try:
        chat = await client.get_chat(message.chat.id)
        stats = f"**Chat Stats:**\n"
        stats += f"Title: {chat.title}\n"
        stats += f"ID: `{chat.id}`\n"
        stats += f"Members: {chat.members_count}\n"
        stats += f"Type: {chat.type.value}"
        await message.edit_text(stats)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("leave", prefixes=".") & filters.me)
async def leave_chat(client: Client, message: Message):
    try:
        await message.edit_text("**Leaving chat...**")
        await client.leave_chat(message.chat.id)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("echo", prefixes=".") & filters.me)
async def echo_message(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide text to echo")
    
    text = message.text[6:]
    await message.edit_text(text)

@app.on_message(filters.command("type", prefixes=".") & filters.me)
async def type_animation(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide text to type")
    
    text = message.text[6:]
    typing_text = ""
    
    for char in text:
        typing_text += char
        await message.edit_text(typing_text)
        await asyncio.sleep(0.1)

@app.on_message(filters.command("lock", prefixes=".") & filters.me)
async def lock_chat(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    permissions = client.get_chat(message.chat.id).permissions
    

    if len(message.command) > 1:
        perm = message.command[1].lower()
        if perm == "messages":
            permissions.can_send_messages = False
        elif perm == "media":
            permissions.can_send_media_messages = False
        elif perm == "polls":
            permissions.can_send_polls = False
        elif perm == "other":
            permissions.can_send_other_messages = False
        elif perm == "web":
            permissions.can_add_web_page_previews = False
        elif perm == "change":
            permissions.can_change_info = False
        elif perm == "invite":
            permissions.can_invite_users = False
        elif perm == "pin":
            permissions.can_pin_messages = False
        else:
            return await message.edit_text("Invalid permission! Use: messages, media, polls, other, web, change, invite, pin")
    else:

        permissions = client.get_chat(message.chat.id).permissions
        permissions.can_send_messages = False
        permissions.can_send_media_messages = False
        permissions.can_send_polls = False
        permissions.can_send_other_messages = False
        permissions.can_add_web_page_previews = False
        permissions.can_change_info = False
        permissions.can_invite_users = False
        permissions.can_pin_messages = False
    
    try:
        await client.set_chat_permissions(
            message.chat.id,
            permissions=permissions
        )
        await message.edit_text("**Chat locked!**")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("unlock", prefixes=".") & filters.me)
async def unlock_chat(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    chat = await client.get_chat(message.chat.id)
    permissions = chat.permissions
    

    if len(message.command) > 1:
        perm = message.command[1].lower()
        if perm == "messages":
            permissions.can_send_messages = chat.permissions.can_send_messages or True
        elif perm == "media":
            permissions.can_send_media_messages = chat.permissions.can_send_media_messages or True
        elif perm == "polls":
            permissions.can_send_polls = chat.permissions.can_send_polls or True
        elif perm == "other":
            permissions.can_send_other_messages = chat.permissions.can_send_other_messages or True
        elif perm == "web":
            permissions.can_add_web_page_previews = chat.permissions.can_add_web_page_previews or True
        elif perm == "change":
            permissions.can_change_info = chat.permissions.can_change_info or True
        elif perm == "invite":
            permissions.can_invite_users = chat.permissions.can_invite_users or True
        elif perm == "pin":
            permissions.can_pin_messages = chat.permissions.can_pin_messages or True
        else:
            return await message.edit_text("Invalid permission! Use: messages, media, polls, other, web, change, invite, pin")
    else:

        permissions = client.get_chat(message.chat.id).permissions
    
    try:
        await client.set_chat_permissions(
            message.chat.id,
            permissions=permissions
        )
        await message.edit_text("**Chat unlocked!**")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("bots", prefixes=".") & filters.me)
async def list_bots(client: Client, message: Message):
    try:
        bots = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
            bots.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
        
        if bots:
            bot_list = "**Bots in chat:**\n" + "\n".join(bots)
        else:
            bot_list = "**No bots in chat**"
        await message.edit_text(bot_list)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("users", prefixes=".") & filters.me)
async def list_users(client: Client, message: Message):
    try:
        users = []
        async for member in client.get_chat_members(message.chat.id):
            if not member.user.is_bot:
                users.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
        
        if len(users) > 50:
            users = users[:50]
            user_list = f"**First 50 users in chat:**\n" + "\n".join(users)
        else:
            user_list = f"**Users in chat ({len(users)}):**\n" + "\n".join(users)
        await message.edit_text(user_list)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("zombies", prefixes=".") & filters.me)
async def find_zombies(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    try:
        zombies = []
        async for member in client.get_chat_members(message.chat.id):
            if member.user.is_deleted:
                zombies.append(str(member.user.id))
        
        if zombies:
            zombie_list = "**Deleted accounts found:**\n" + "\n".join([f"`{id}`" for id in zombies[:10]])
            if len(zombies) > 10:
                zombie_list += f"\n\nAnd {len(zombies) - 10} more..."
        else:
            zombie_list = "**No deleted accounts found**"
        await message.edit_text(zombie_list)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("settitle", prefixes=".") & filters.me)
async def set_chat_title(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if len(message.command) < 2:
        return await message.edit_text("Provide a title to set")
    
    title = " ".join(message.command[1:])
    try:

        if message.chat.id not in chat_titles:
            chat_titles[message.chat.id] = message.chat.title
        
        await client.set_chat_title(message.chat.id, title)
        await message.edit_text(f"**Chat title changed to:** {title}")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("restoretitle", prefixes=".") & filters.me)
async def restore_chat_title(client: Client, message: Message):
    if not await check_admin(client, message.chat.id, client.me.id):
        return await message.edit_text("I'm not admin here!")
    
    if message.chat.id not in chat_titles:
        return await message.edit_text("No original title stored for this chat")
    
    try:
        original_title = chat_titles[message.chat.id]
        await client.set_chat_title(message.chat.id, original_title)
        await message.edit_text(f"**Chat title restored to:** {original_title}")
        del chat_titles[message.chat.id]
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")


@app.on_message(filters.command("block", prefixes=".") & filters.me)
async def block_user(client: Client, message: Message):
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        return await message.edit_text("Reply to user or provide user ID")
    
    try:
        await client.block_user(user_id)
        blocked_users.add(str(user_id))
        save_data()
        await message.edit_text(f"**Blocked** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("unblock", prefixes=".") & filters.me)
async def unblock_user(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide user ID to unblock")
    
    user_id = message.command[1]
    try:
        await client.unblock_user(user_id)
        blocked_users.discard(str(user_id))
        save_data()
        await message.edit_text(f"**Unblocked** {user_id}!")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("blocked", prefixes=".") & filters.me)
async def list_blocked(client: Client, message: Message):
    if not blocked_users:
        return await message.edit_text("No blocked users")
    
    blocked_list = "**Blocked Users:**\n"
    for user_id in list(blocked_users)[:10]:
        try:
            user = await client.get_users(int(user_id))
            blocked_list += f"[{user.first_name}](tg://user?id={user.id}) - `{user_id}`\n"
        except:
            blocked_list += f"`{user_id}`\n"
    
    await message.edit_text(blocked_list)


@app.on_message(filters.command("afk", prefixes=".") & filters.me)
async def set_afk(client: Client, message: Message):
    global afk_mode, afk_reason, afk_start_time
    
    afk_mode = True
    afk_reason = " ".join(message.command[1:]) if len(message.command) > 1 else "AFK"
    afk_start_time = datetime.now()
    
    await message.edit_text(f"**AFK Mode Activated**\nReason: {afk_reason}")

@app.on_message(filters.command("unafk", prefixes=".") & filters.me)
async def unset_afk(client: Client, message: Message):
    global afk_mode, afk_reason, afk_start_time
    
    afk_mode = False
    afk_reason = ""
    afk_start_time = None
    
    await message.edit_text("**AFK Mode Deactivated**")


@app.on_message(filters.command("autoreply", prefixes=".") & filters.me)
async def set_auto_reply(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .autoreply [trigger] [response]")
    
    trigger = message.command[1].lower()
    response = " ".join(message.command[2:])
    
    auto_replies[trigger] = response
    save_data()
    await message.edit_text(f"Auto reply set for '{trigger}'")

@app.on_message(filters.command("delreply", prefixes=".") & filters.me)
async def delete_auto_reply(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide trigger to delete")
    
    trigger = message.command[1].lower()
    if trigger in auto_replies:
        del auto_replies[trigger]
        save_data()
        await message.edit_text(f"Deleted auto reply for '{trigger}'")
    else:
        await message.edit_text("Trigger not found")

@app.on_message(filters.command("replies", prefixes=".") & filters.me)
async def list_auto_replies(client: Client, message: Message):
    if not auto_replies:
        return await message.edit_text("No auto replies set")
    
    reply_list = "**Auto Replies:**\n"
    for trigger, response in auto_replies.items():
        reply_list += f"`{trigger}` → {response[:30]}{'...' if len(response) > 30 else ''}\n"
    
    await message.edit_text(reply_list)


@app.on_message(filters.regex(r"^\.save$") & filters.reply & filters.me)
async def save_media(client: Client, message: Message):
    replied = message.reply_to_message
    media_type = get_media_type(replied)
    
    if not media_type:
        return
    
    try:

        forwarded_msg = await replied.forward("me")
        message = await app.send_message("me", "saving bro!")
        await asyncio.sleep(2)
        await message.delete()
    except Exception as e:

        try:
            await message.edit_text(f"**Forward failed, downloading {media_type}...**")
            

            file_path = f"{MEDIA_DIR}/{media_type}_{replied.id}"
            if media_type == "photo":
                downloaded_path = await client.download_media(replied.photo.file_id, file_path + ".jpg")
            elif media_type == "video":
                downloaded_path = await client.download_media(replied.video.file_id, file_path + ".mp4")
            elif media_type == "document":
                downloaded_path = await client.download_media(replied.document.file_id, file_path + ".document")
            elif media_type == "audio":
                downloaded_path = await client.download_media(replied.audio.file_id, file_path + ".mp3")
            elif media_type == "voice":
                downloaded_path = await client.download_media(replied.voice.file_id, file_path + ".ogg")
            elif media_type == "animation":
                downloaded_path = await client.download_media(replied.animation.file_id, file_path + ".mp4")
            elif media_type == "sticker":
                downloaded_path = await client.download_media(replied.sticker.file_id, file_path + ".webp")
            else:
                return await message.edit_text("Unsupported media type!")
            

            await message.edit_text(f"**Uploading {media_type}...**")
            
            if media_type == "photo":
                await client.send_photo("me", downloaded_path, caption="Saved media")
            elif media_type == "video":
                await client.send_video("me", downloaded_path, caption="Saved media")
            elif media_type == "document":
                await client.send_document("me", downloaded_path, caption="Saved media")
            elif media_type == "audio":
                await client.send_audio("me", downloaded_path, caption="Saved media")
            elif media_type == "voice":
                await client.send_voice("me", downloaded_path, caption="Saved media")
            elif media_type == "animation":
                await client.send_animation("me", downloaded_path, caption="Saved media")
            elif media_type == "sticker":
                await client.send_sticker("me", downloaded_path, caption="Saved media")
            

            if os.path.exists(downloaded_path):
                os.remove(downloaded_path)
            
            await message.edit_text(f"**Saved {media_type}!** (Downloaded & Uploaded)")
            await asyncio.sleep(2)
            await message.delete()
            
        except Exception as upload_error:
            await message.edit_text(f"Error saving media: {str(upload_error)}")


@app.on_message(filters.command("setbio", prefixes=".") & filters.me)
async def set_bio(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide bio text")
    
    bio = " ".join(message.command[1:])
    try:
        await client.update_profile(bio=bio)
        await message.edit_text("**Bio updated successfully!**")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("setpic", prefixes=".") & filters.me & filters.reply)
async def set_profile_pic(client: Client, message: Message):
    if not message.reply_to_message.photo:
        return await message.edit_text("Reply to a photo to set as profile picture")
    
    try:

        file_path = await client.download_media(message.reply_to_message.photo.file_id)

        await client.set_profile_photo(photo=file_path)

        os.remove(file_path)
        await message.edit_text("**Profile picture updated successfully!**")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("setname", prefixes=".") & filters.me)
async def set_name(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .setname [first_name] [last_name]")
    
    first_name = message.command[1]
    last_name = " ".join(message.command[2:]) if len(message.command) > 2 else ""
    
    try:
        await client.update_profile(first_name=first_name, last_name=last_name)
        await message.edit_text("**Name updated successfully!**")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("username", prefixes=".") & filters.me)
async def set_username(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .username [username]")
    
    username = message.command[1]
    try:
        await client.update_username(username)
        await message.edit_text("**Username updated successfully!**")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")


@app.on_message(filters.command("calc", prefixes=".") & filters.me)
async def calculator(client: Client, message: Message):

    expression = ""
    if len(message.command) > 1:
        expression = " ".join(message.command[1:])
    elif message.reply_to_message:

        expression = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide expression to calculate or reply to a message with expression")
    
    if not expression:
        return await message.edit_text("No expression found!")
    
    try:
        result = safe_eval(expression)
        await message.edit_text(f"**Calculation:**\n{expression} = {result}")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("short", prefixes=".") & filters.me)
async def url_shortener(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide URL to shorten")
    
    url = message.command[1]
    try:

        api_url = f"http://tinyurl.com/api-create.php?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            short_url = response.text
            await message.edit_text(f"**Shortened URL:** {short_url}")
        else:
            await message.edit_text("Error shortening URL")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("qr", prefixes=".") & filters.me)
async def generate_qr(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide text to encode")
    
    text = " ".join(message.command[1:])
    try:

        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?data={text}&size=200x200"
        

        qr_path = f"{PROFILE_PICS_DIR}/qr_{int(datetime.now().timestamp())}.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(qr_url) as resp:
                if resp.status == 200:
                    with open(qr_path, 'wb') as f:
                        f.write(await resp.read())
                    

                    await message.reply_photo(
                        qr_path,
                        caption=f"**QR Code for:** {text}"
                    )
                    await message.delete()
                    

                    os.remove(qr_path)
                else:
                    await message.edit_text("Error generating QR code")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")
        
@app.on_message(filters.command("readqr", prefixes=".") & filters.me & filters.reply)
async def read_qr(client: Client, message: Message):
    if not message.reply_to_message.photo:
        return await message.edit_text("Reply to a QR code image")
    
    try:

        file_path = await client.download_media(message.reply_to_message.photo.file_id)
        

        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("https://api.qrserver.com/v1/read-qr-code/", files=files)
        
        os.remove(file_path)
        
        if response.status_code == 200:
            data = response.json()
            if data[0]['symbol'][0]['data']:
                decoded = data[0]['symbol'][0]['data']
                await message.edit_text(f"**Decoded QR Code:**\n{decoded}")
            else:
                await message.edit_text("Could not decode QR code")
        else:
            await message.edit_text("Error reading QR code")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("spb", prefixes=".") & filters.me)
async def spamwatch_check(client: Client, message: Message):
    if len(message.command) < 2:
        user_id = message.from_user.id
    else:
        user_id = message.command[1]
    
    try:
        user = await client.get_users(user_id)
        await message.edit_text(f"**SpamWatch Check for {user.first_name}:**\nNot integrated yet. Please add SpamWatch API integration.")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("whois", prefixes=".") & filters.me)
async def advanced_user_info(client: Client, message: Message):
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]
    else:
        user_id = message.from_user.id
    
    try:
        user = await client.get_users(user_id)
        chat_member = await client.get_chat_member(message.chat.id, user_id)
        
        info = f"**Advanced User Info:**\n"
        info += f"ID: `{user.id}`\n"
        info += f"Name: [{user.first_name}](tg://user?id={user.id})"
        if user.last_name:
            info += f" {user.last_name}"
        info += "\n"
        if user.username:
            info += f"Username: @{user.username}\n"
        info += f"Bot: {user.is_bot}\n"
        info += f"Verified: {user.is_verified}\n"
        info += f"Restricted: {user.is_restricted}\n"
        info += f"Scam: {user.is_scam}\n"
        info += f"Premium: {user.is_premium}\n"
        info += f"Status: {chat_member.status.value}"
        await message.edit_text(info)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")



@app.on_message(filters.command("search", prefixes=".") & filters.me)
async def search_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide search query.")

    query = " ".join(message.command[1:])
    await message.edit_text("🔍 Searching...")

    try:
        links = list(google_search(query, num_results=5))

        if not links:
            return await message.edit_text("No results found.")

        first_link = links[0]
        snippet = ""

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(first_link, timeout=10) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    texts = soup.stripped_strings
                    combined_text = " ".join(texts)
                    snippet = combined_text[:1000]
            except Exception as e:
                snippet = f"Could not scrape the first link: {e}"

        result_text = f"**🔎 Search Results for:** `{query}`\n\n"
        result_text += f"**📄 Snippet from:** [First Link]({first_link})\n"
        result_text += f"```{snippet}```\n\n"
        result_text += "**🔗 Other Results:**\n"
        for i, link in enumerate(links[1:], start=2):
            result_text += f"{i}. {link}\n"

        await message.edit_text(result_text, disable_web_page_preview=True)

    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


@app.on_message(filters.command("tr", prefixes=".") & filters.me)
async def translate_text(client: Client, message: Message):

    text = ""
    lang = "en"
    
    if len(message.command) > 2:
        lang = message.command[1]
        text = " ".join(message.command[2:])
    elif len(message.command) > 1:
        lang = message.command[1]
        if message.reply_to_message:
            text = message.reply_to_message.text or ""
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
        lang = "en"
    else:
        return await message.edit_text("Usage: .tr [lang] [text] or reply to message")
    
    if not text:
        return await message.edit_text("No text to translate!")
    
    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(text, dest=lang)
        await message.edit_text(
            f"**Translated to {lang}:**\n{result.text}\n\n"
            f"**Detected language:** {result.src}"
        )
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("wiki", prefixes=".") & filters.me)
async def wikipedia_search(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide search query")
    
    query = " ".join(message.command[1:])
    try:
        import wikipedia
        result = wikipedia.summary(query, sentences=3)
        await message.edit_text(f"**Wikipedia:** `{query}`\n\n{result}")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("img", prefixes=".") & filters.me)
async def image_search(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide search query")
    
    query = " ".join(message.command[1:])
    try: 
        url = f"https://api.unsplash.com/photos/random?query={query}&count=5&client_id={api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    images = []
                    for item in data:
                        images.append(item['urls']['regular'])
                    

                    await message.reply_photo(
                        images[0],
                        caption=f"**Image Search Results for:** `{query}`"
                    )
                    

                    for img_url in images[1:]:
                        await message.reply_photo(img_url)
                    
                    await message.delete()
                else:
                    await message.edit_text("Error fetching images")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


@app.on_message(filters.command("weather", prefixes=".") & filters.me)
async def weather_info(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide city name")
    
    city = " ".join(message.command[1:])
    url = f"https://wttr.in/{city}?format=j1"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await message.edit_text("Couldn't fetch weather data.")
                
                data = await resp.json()
                current = data['current_condition'][0]


                weather_report = f"**🌤 Weather in {city.title()}**\n"
                weather_report += f"🌡 Temperature: {current['temp_C']}°C (Feels like {current['FeelsLikeC']}°C)\n"
                weather_report += f"💧 Humidity: {current['humidity']}%\n"
                weather_report += f"💨 Wind: {current['windspeedKmph']} km/h ({current['winddir16Point']})\n"
                weather_report += f"🔍 Condition: {current['weatherDesc'][0]['value']}\n"
                weather_report += f"☁️ Cloud Cover: {current['cloudcover']}%\n"
                weather_report += f"🌅 Sunrise: {data['weather'][0]['astronomy'][0]['sunrise']}\n"
                weather_report += f"🌇 Sunset: {data['weather'][0]['astronomy'][0]['sunset']}"

                await message.edit_text(weather_report)
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


@app.on_message(filters.command("ud", prefixes=".") & filters.me)
async def urban_dictionary(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide a word to search")
    
    word = " ".join(message.command[1:])
    try:
        import urllib.parse
        url = f"http://api.urbandictionary.com/v0/define?term={urllib.parse.quote(word)}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['list']:
                definition = data['list'][0]
                result = f"**{word}**\n\n"
                result += f"{definition['definition'][:500]}{'...' if len(definition['definition']) > 500 else ''}\n\n"
                result += f"*Example:*\n{definition['example'][:300]}{'...' if len(definition['example']) > 300 else ''}"
                await message.edit_text(result)
            else:
                await message.edit_text("No definition found")
        else:
            await message.edit_text("Error fetching definition")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("define", prefixes=".") & filters.me)
async def dictionary_definition(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide a word to define")
    
    word = " ".join(message.command[1:])
    try:

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                result = f"**{entry['word']}**\n"
                if 'phonetic' in entry:
                    result += f"**Phonetic:** {entry['phonetic']}\n\n"
                if 'meanings' in entry and len(entry['meanings']) > 0:
                    meaning = entry['meanings'][0]
                    result += f"**Part of Speech:** {meaning['partOfSpeech']}\n"
                    if 'definitions' in meaning and len(meaning['definitions']) > 0:
                        definition = meaning['definitions'][0]
                        result += f"**Definition:** {definition['definition']}\n"
                        if 'example' in definition:
                            result += f"**Example:** {definition['example']}\n"
                await message.edit_text(result)
            else:
                await message.edit_text("No definition found")
        else:
            await message.edit_text("Error fetching definition")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("syn", prefixes=".") & filters.me)
async def synonyms(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide a word to find synonyms")
    
    word = " ".join(message.command[1:])
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                synonyms = []
                

                for meaning in entry.get('meanings', []):

                    synonyms.extend(meaning.get('synonyms', []))
                    

                    for definition in meaning.get('definitions', []):
                        synonyms.extend(definition.get('synonyms', []))
                
                if synonyms:

                    unique_synonyms = list(set(synonyms))[:10]
                    result = f"**Synonyms for {word}:**\n"
                    result += ", ".join(unique_synonyms)
                    await message.edit_text(result)
                else:
                    await message.edit_text(f"No synonyms found for {word}")
            else:
                await message.edit_text("No entry found for this word")
        else:
            await message.edit_text(f"Error fetching synonyms (HTTP {response.status_code})")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("ant", prefixes=".") & filters.me)
async def antonyms(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide a word to find antonyms")
    
    word = " ".join(message.command[1:])
    try:

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                antonyms = []
                for meaning in entry.get('meanings', []):
                    for definition in meaning.get('definitions', []):
                        antonyms.extend(definition.get('antonyms', []))
                
                if antonyms:
                    unique_antonyms = list(set(antonyms))[:10]
                    result = f"**Antonyms for {word}:**\n"
                    result += ", ".join(unique_antonyms)
                    await message.edit_text(result)
                else:
                    await message.edit_text(f"No antonyms found for {word}")
            else:
                await message.edit_text("No antonyms found")
        else:
            await message.edit_text("Error fetching antonyms")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


@app.on_message(filters.command("news", prefixes=".") & filters.me)
async def latest_news(client: Client, message: Message):
    category = "general"
    if len(message.command) > 1:
        category = message.command[1].lower()
    
    try:

        rss_urls = {
            "general": "http://feeds.bbci.co.uk/news/rss.xml",
            "world": "http://feeds.bbci.co.uk/news/world/rss.xml",
            "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
            "science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
            "health": "http://feeds.bbci.co.uk/news/health/rss.xml"
        }
        

        alt_rss = {
            "general": "https://rss.cnn.com/rss/edition.rss",
            "world": "https://rss.cnn.com/rss/edition_world.rss",
            "technology": "https://rss.cnn.com/rss/edition_technology.rss",
            "business": "https://rss.cnn.com/rss/money_latest.rss"
        }
        
        url = rss_urls.get(category, rss_urls["general"])
        

        feed = feedparser.parse(url)
        
        if feed.entries:
            result = f"**📰 Latest {category.title()} News:**\n\n"
            for i, entry in enumerate(feed.entries[:5], 1):
                title = entry.title
                link = entry.link
                summary = entry.get('summary', '')
                

                if summary:

                    summary = BeautifulSoup(summary, 'html.parser').get_text()
                    summary = summary[:150] + "..." if len(summary) > 150 else summary
                
                result += f"{i}. [{title}]({link})\n"
                if summary:
                    result += f"   {summary}\n"
                result += f"   📅 {entry.get('published', 'N/A')}\n\n"
            
            await message.edit_text(result, disable_web_page_preview=True)
        else:

            await scrape_news(message, category)
            
    except Exception as e:
        await message.edit_text(f"❌ Error fetching news: {str(e)}")

async def scrape_news(message: Message, category: str):
    """Fallback method using web scraping"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        

        search_query = f"{category} news" if category != "general" else "latest news"
        url = f"https://news.google.com/rss/search?q={search_query}&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(url)
        
        if feed.entries:
            result = f"**📰 Latest {category.title()} News (Google News):**\n\n"
            for i, entry in enumerate(feed.entries[:5], 1):
                title = entry.title
                link = entry.link
                source = entry.get('source', {}).get('title', 'Unknown')
                
                result += f"{i}. [{title}]({link})\n"
                result += f"   📰 Source: {source}\n"
                result += f"   📅 {entry.get('published', 'N/A')}\n\n"
            
            await message.edit_text(result, disable_web_page_preview=True)
        else:
            await message.edit_text("❌ No news found")
            
    except Exception as e:
        await message.edit_text(f"❌ Scraping failed: {str(e)}")


@app.on_message(filters.command("quicknews", prefixes=".") & filters.me)
async def quick_news(client: Client, message: Message):
    """Simple news using Google News RSS"""
    try:
        category = "general"
        if len(message.command) > 1:
            category = message.command[1].lower()
        

        if category == "general":
            url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
        else:
            url = f"https://news.google.com/rss/search?q={category}&hl=en-US&gl=US&ceid=US:en"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                result = f"**📰 {category.title()} News:**\n\n"
                for i, entry in enumerate(feed.entries[:5], 1):
                    result += f"{i}. [{entry.title}]({entry.link})\n\n"
                
                await message.edit_text(result, disable_web_page_preview=True)
            else:
                await message.edit_text("No news found")
        else:
            await message.edit_text(f"Error: HTTP {response.status_code}")
            
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")



@app.on_message(filters.command("note", prefixes=".") & filters.me)
async def save_note(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .note [name] [content]")
    
    note_name = message.command[1].lower()
    content = " ".join(message.command[2:])
    
    notes[note_name] = content
    save_data()
    await message.edit_text(f"Note '{note_name}' saved!")

@app.on_message(filters.command("getnote", prefixes=".") & filters.me)
async def get_note(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide note name")
    
    note_name = message.command[1].lower()
    if note_name in notes:
        await message.edit_text(f"**{note_name}:**\n{notes[note_name]}")
    else:
        await message.edit_text("Note not found")

@app.on_message(filters.command("delnote", prefixes=".") & filters.me)
async def delete_note(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide note name")
    
    note_name = message.command[1].lower()
    if note_name in notes:
        del notes[note_name]
        save_data()
        await message.edit_text(f"Note '{note_name}' deleted!")
    else:
        await message.edit_text("Note not found")

@app.on_message(filters.command("notes", prefixes=".") & filters.me)
async def list_notes(client: Client, message: Message):
    if not notes:
        return await message.edit_text("No notes saved")
    
    note_list = "**Saved Notes:**\n"
    for name in notes.keys():
        note_list += f"`{name}`\n"
    
    await message.edit_text(note_list)

@app.on_message(filters.command("remind", prefixes=".") & filters.me)
async def set_reminder(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .remind [minutes] [message]")
    
    try:
        minutes = int(message.command[1])
        reminder_text = " ".join(message.command[2:])
        

        reminder_id = str(len(reminders) + 1)
        reminders[reminder_id] = {
            "text": reminder_text,
            "time": minutes,
            "created": datetime.now().isoformat()
        }
        save_data()
        
        await message.edit_text(f"Reminder set for {minutes} minutes!")
        

        async def reminder_task():
            await asyncio.sleep(minutes * 60)
            if reminder_id in reminders:
                await message.reply_text(f"⏰ **Reminder:** {reminder_text}")

                reminders.pop(reminder_id, None)
                save_data()
        
        asyncio.create_task(reminder_task())
    except ValueError:
        await message.edit_text("Invalid time format. Use minutes as number")

@app.on_message(filters.command("reminders", prefixes=".") & filters.me)
async def list_reminders(client: Client, message: Message):
    if not reminders:
        return await message.edit_text("No active reminders")
    
    reminder_list = "**Active Reminders:**\n"
    for i, (id, reminder) in enumerate(reminders.items(), 1):
        reminder_list += f"{i}. {reminder['text']} (in {reminder['time']} min)\n"
    
    await message.edit_text(reminder_list)


@app.on_message(filters.command("quote", prefixes=".") & filters.me)
async def random_quote(client: Client, message: Message):
    try:

        apis = [
            "https://api.quotable.io/random",
            "https://zenquotes.io/api/random"
        ]
        
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if "quotable" in api_url:
                        quote = f"**{data['content']}**\n\n— {data['author']}"
                    else:
                        quote = f"**{data[0]['q']}**\n\n— {data[0]['a']}"
                    await message.edit_text(quote)
                    return
            except:
                continue
                

        if custom_quotes:
            import random
            quote_id = random.choice(list(custom_quotes.keys()))
            quote_data = custom_quotes[quote_id]
            await message.edit_text(f"**{quote_data['text']}**\n\n— {quote_data['author']}")
        else:
            await message.edit_text("Error fetching quote. Try again later.")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("addquote", prefixes=".") & filters.me)
async def add_custom_quote(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .addquote [text] or reply to message")
    

    if len(message.command) > 1:
        text = " ".join(message.command[1:])
        author = message.from_user.first_name
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
        author = message.reply_to_message.from_user.first_name
    else:
        return await message.edit_text("Provide quote text or reply to a message")
    
    if not text:
        return await message.edit_text("No text found!")
    

    quote_id = str(len(custom_quotes) + 1)
    custom_quotes[quote_id] = {
        "text": text,
        "author": author,
        "added_by": message.from_user.id,
        "added_at": datetime.now().isoformat()
    }
    save_data()
    
    await message.edit_text("**Quote added successfully!**")

@app.on_message(filters.command("delquote", prefixes=".") & filters.me)
async def delete_custom_quote(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Provide quote ID to delete")
    
    quote_id = message.command[1]
    if quote_id in custom_quotes:
        del custom_quotes[quote_id]
        save_data()
        await message.edit_text(f"**Quote {quote_id} deleted!**")
    else:
        await message.edit_text("Quote not found")

@app.on_message(filters.command("myquotes", prefixes=".") & filters.me)
async def list_my_quotes(client: Client, message: Message):
    user_quotes = {k: v for k, v in custom_quotes.items() if v["added_by"] == message.from_user.id}
    
    if not user_quotes:
        return await message.edit_text("You haven't added any quotes yet")
    
    quote_list = "**Your Quotes:**\n"
    for quote_id, quote_data in list(user_quotes.items())[:10]:
        quote_list += f"`{quote_id}.` {quote_data['text'][:50]}{'...' if len(quote_data['text']) > 50 else ''}\n"
    
    await message.edit_text(quote_list)

@app.on_message(filters.command("joke", prefixes=".") & filters.me)
async def random_joke(client: Client, message: Message):
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            data = response.json()
            joke = f"**{data['setup']}**\n\n{data['punchline']}"
            await message.edit_text(joke)
        else:
            await message.edit_text("Error fetching joke")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("fact", prefixes=".") & filters.me)
async def random_fact(client: Client, message: Message):
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            data = response.json()
            await message.edit_text(f"**Fact:** {data['text']}")
        else:
            await message.edit_text("Error fetching fact")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")



@app.on_message(filters.command("meme", prefixes=".") & filters.me)
async def custom_meme(client: Client, message: Message):
    try:

        if len(message.command) > 1:

            keywords = message.command[1:]
        elif message.reply_to_message and message.reply_to_message.text:

            keywords = message.reply_to_message.text.split()
        else:
            keywords = []

        urls_tried = set()
        meme_data = None

        if keywords:
            search_variants = ['-'.join(keywords)] + keywords

            for keyword in search_variants:
                url = f"https://api.apileague.com/retrieve-random-meme?keywords={keyword}"
                if url in urls_tried:
                    continue
                urls_tried.add(url)

                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if 'url' in data:
                        meme_data = data
                        break
        else:

            response = requests.get("https://api.apileague.com/retrieve-random-meme")
            if response.status_code == 200:
                meme_data = response.json()

        if meme_data:
            await message.reply_photo(
                photo=meme_data['url'],
                caption=f"**{meme_data.get('description', 'Meme')}**"
            )
            await message.delete()
        else:
            await message.edit_text("No meme found for given keywords.")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")


@app.on_message(filters.command("ascii", prefixes=".") & filters.me)
async def ascii_command(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.edit("Usage: `.ascii <text>` or reply to a message.")
        return

    if len(message.command) >= 2:
        text = " ".join(message.command[1:])
    elif message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    else:
        await message.edit("No valid text found to convert.")
        return

    try:
        ascii_art = figlet_format(text)
        if len(ascii_art) > 4096:
            ascii_art = ascii_art[:4093] + "..."
        await message.edit(f"```\n{ascii_art}\n```")
    except Exception as e:
        await message.edit(f"Error creating ASCII art: `{e}`")

@app.on_message(filters.command("reverse", prefixes=".") & filters.me)
async def reverse_text(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(text[::-1])

@app.on_message(filters.command("mock", prefixes=".") & filters.me)
async def mock_text_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(mock_text(text))

@app.on_message(filters.command("vapor", prefixes=".") & filters.me)
async def vapor_text_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(vapor_text(text))

@app.on_message(filters.command("clap", prefixes=".") & filters.me)
async def clap_text_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(clap_text(text))

@app.on_message(filters.command("emojify", prefixes=".") & filters.me)
async def emojify_text_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(emojify_text(text))

@app.on_message(filters.command("spoiler", prefixes=".") & filters.me)
async def spoiler_text_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(spoiler_text(text))

@app.on_message(filters.command("password", prefixes=".") & filters.me)
async def generate_password_command(client: Client, message: Message):
    length = 12
    if len(message.command) > 1:
        try:
            length = int(message.command[1])
            if length < 4:
                length = 4
            elif length > 100:
                length = 100
        except:
            pass
    
    password = generate_password(length)
    await message.edit_text(f"**Generated Password:** `{password}`")

@app.on_message(filters.command("hash", prefixes=".") & filters.me)
async def hash_text(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    sha1_hash = hashlib.sha1(text.encode()).hexdigest()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    
    result = f"**Hashes for:** `{text}`\n\n"
    result += f"**MD5:** `{md5_hash}`\n"
    result += f"**SHA1:** `{sha1_hash}`\n"
    result += f"**SHA256:** `{sha256_hash}`"
    
    await message.edit_text(result)

@app.on_message(filters.command("base64", prefixes=".") & filters.me)
async def base64_command(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .base64 [encode/decode] [text] or reply to message")
    
    operation = message.command[1].lower()
    text = " ".join(message.command[2:]) if len(message.command) > 2 else ""
    

    if not text and message.reply_to_message:
        text = message.reply_to_message.text or ""
    
    if not text:
        return await message.edit_text("No text found!")
    
    try:
        if operation == "encode":
            encoded = base64.b64encode(text.encode()).decode()
            await message.edit_text(f"**Base64 Encoded:**\n`{encoded}`")
        elif operation == "decode":
            decoded = base64.b64decode(text).decode()
            await message.edit_text(f"**Base64 Decoded:**\n`{decoded}`")
        else:
            await message.edit_text("Usage: .base64 [encode/decode] [text]")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("leet", prefixes=".") & filters.me)
async def leet_speak_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(leet_speak(text))

@app.on_message(filters.command("flip", prefixes=".") & filters.me)
async def flip_text_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    await message.edit_text(flip_text(text))

@app.on_message(filters.command("cowsay", prefixes=".") & filters.me)
async def cowsay_command(client: Client, message: Message):

    text = ""
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or ""
    else:
        return await message.edit_text("Provide text or reply to message")
    
    if not text:
        return await message.edit_text("No text found!")
    
    try:
        result = cowsay(text)
        await message.edit_text(f"```\n{result}\n```")
    except Exception as e:
        await message.edit_text(f"Error: {str(e)}")

@app.on_message(filters.command("roll", prefixes=".") & filters.me)
async def roll_dice_command(client: Client, message: Message):
    dice_notation = "1d6"
    if len(message.command) > 1:
        dice_notation = message.command[1]
    
    result = roll_dice(dice_notation)
    await message.edit_text(result)

@app.on_message(filters.command("8ball", prefixes=".") & filters.me)
async def magic_8ball_command(client: Client, message: Message):
    question = ""
    if len(message.command) > 1:
        question = " ".join(message.command[1:])
    elif message.reply_to_message:
        question = message.reply_to_message.text or ""
    
    if not question:
        return await message.edit_text("Ask a question!")
    
    result = magic_8ball(question)
    await message.edit_text(result)

@app.on_message(filters.command("choose", prefixes=".") & filters.me)
async def random_choice_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .choose [option1|option2|option3]")
    
    options = " ".join(message.command[1:])
    result = random_choice(options)
    await message.edit_text(result)


@app.on_message(filters.command("alias", prefixes=".") & filters.me)
async def create_alias(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .alias [name] [command]")
    
    alias_name = message.command[1].lower()
    command = " ".join(message.command[2:])
    

    if "aliases" not in user_data:
        user_data["aliases"] = {}
    
    user_data["aliases"][alias_name] = command
    save_data()
    
    await message.edit_text(f"**Alias '{alias_name}' created for command:** `{command}`")

@app.on_message(filters.command("unalias", prefixes=".") & filters.me)
async def remove_alias(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .unalias [name]")
    
    alias_name = message.command[1].lower()
    
    if "aliases" in user_data and alias_name in user_data["aliases"]:
        del user_data["aliases"][alias_name]
        save_data()
        await message.edit_text(f"**Alias '{alias_name}' removed!**")
    else:
        await message.edit_text("Alias not found!")

@app.on_message(filters.command("aliases", prefixes=".") & filters.me)
async def list_aliases(client: Client, message: Message):
    if "aliases" not in user_data or not user_data["aliases"]:
        return await message.edit_text("No aliases found!")
    
    alias_list = "**Your Aliases:**\n"
    for name, command in user_data["aliases"].items():
        alias_list += f"`{name}` → `{command}`\n"
    
    await message.edit_text(alias_list)

@app.on_message(filters.command("filter", prefixes=".") & filters.me)
async def add_filter(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .filter [trigger] [response]")
    
    trigger = message.command[1].lower()
    response = " ".join(message.command[2:])
    

    if message.chat.id not in active_filters:
        active_filters[message.chat.id] = {}
    
    active_filters[message.chat.id][trigger] = response
    await message.edit_text(f"**Filter added for '{trigger}'**")

@app.on_message(filters.command("filters", prefixes=".") & filters.me)
async def list_filters(client: Client, message: Message):
    if message.chat.id not in active_filters or not active_filters[message.chat.id]:
        return await message.edit_text("No filters found in this chat!")
    
    filter_list = "**Active Filters:**\n"
    for trigger, response in active_filters[message.chat.id].items():
        filter_list += f"`{trigger}` → {response[:30]}{'...' if len(response) > 30 else ''}\n"
    
    await message.edit_text(filter_list)

@app.on_message(filters.command("stop", prefixes=".") & filters.me)
async def remove_filter(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .stop [trigger]")
    
    trigger = message.command[1].lower()
    
    if message.chat.id in active_filters and trigger in active_filters[message.chat.id]:
        del active_filters[message.chat.id][trigger]
        await message.edit_text(f"**Filter '{trigger}' removed!**")
    else:
        await message.edit_text("Filter not found!")

@app.on_message(filters.command("schedule", prefixes=".") & filters.me)
async def schedule_task(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .schedule [time_in_minutes] [command]")
    
    try:
        minutes = int(message.command[1])
        command = " ".join(message.command[2:])
        

        task_id = str(len(scheduled_tasks) + 1)
        scheduled_tasks[task_id] = {
            "command": command,
            "time": minutes,
            "chat_id": message.chat.id,
            "created": datetime.now().isoformat()
        }
        save_data()
        
        await message.edit_text(f"**Task scheduled for {minutes} minutes!** (ID: {task_id})")
        

        async def execute_task():
            await asyncio.sleep(minutes * 60)
            if task_id in scheduled_tasks:

                try:

                    await message.reply_text(f"⏰ **Scheduled task executed:** {command}")

                    scheduled_tasks.pop(task_id, None)
                    save_data()
                except Exception as e:
                    logger.error(f"Error executing scheduled task: {e}")
        
        asyncio.create_task(execute_task())
    except ValueError:
        await message.edit_text("Invalid time format. Use minutes as number")

@app.on_message(filters.command("unschedule", prefixes=".") & filters.me)
async def unschedule_task(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .unschedule [task_id]")
    
    task_id = message.command[1]
    if task_id in scheduled_tasks:
        del scheduled_tasks[task_id]
        save_data()
        await message.edit_text(f"**Task {task_id} cancelled!**")
    else:
        await message.edit_text("Task not found!")

@app.on_message(filters.command("tasks", prefixes=".") & filters.me)
async def list_scheduled_tasks(client: Client, message: Message):
    if not scheduled_tasks:
        return await message.edit_text("No scheduled tasks!")
    
    task_list = "**Scheduled Tasks:**\n"
    for task_id, task in scheduled_tasks.items():
        task_list += f"`{task_id}.` {task['command']} (in {task['time']} min)\n"
    
    await message.edit_text(task_list)

@app.on_message(filters.command("todo", prefixes=".") & filters.me)
async def add_todo(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .todo [task]")
    
    task = " ".join(message.command[1:])
    

    if "todos" not in user_data:
        user_data["todos"] = []
    
    todo_id = len(user_data["todos"]) + 1
    user_data["todos"].append({
        "id": todo_id,
        "task": task,
        "completed": False,
        "created": datetime.now().isoformat()
    })
    save_data()
    
    await message.edit_text(f"**Todo added!** (ID: {todo_id})")

@app.on_message(filters.command("todos", prefixes=".") & filters.me)
async def list_todos(client: Client, message: Message):
    if "todos" not in user_data or not user_data["todos"]:
        return await message.edit_text("No todos found!")
    
    todo_list = "**Your Todos:**\n"
    for todo in user_data["todos"]:
        status = "✅" if todo["completed"] else "❌"
        todo_list += f"{status} `{todo['id']}.` {todo['task']}\n"
    
    await message.edit_text(todo_list)

@app.on_message(filters.command("done", prefixes=".") & filters.me)
async def mark_todo_done(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .done [todo_id]")
    
    try:
        todo_id = int(message.command[1])
        if "todos" in user_data:
            for todo in user_data["todos"]:
                if todo["id"] == todo_id:
                    todo["completed"] = True
                    save_data()
                    await message.edit_text(f"**Todo {todo_id} marked as done!**")
                    return
        await message.edit_text("Todo not found!")
    except ValueError:
        await message.edit_text("Invalid todo ID!")

@app.on_message(filters.command("rss", prefixes=".") & filters.me)
async def add_rss_feed(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .rss [feed_url]")
    
    feed_url = message.command[1]
    

    if "rss_feeds" not in user_data:
        user_data["rss_feeds"] = []
    
    user_data["rss_feeds"].append({
        "url": feed_url,
        "chat_id": message.chat.id,
        "added": datetime.now().isoformat()
    })
    save_data()
    
    await message.edit_text(f"**RSS feed added:** {feed_url}")

@app.on_message(filters.command("feeds", prefixes=".") & filters.me)
async def list_rss_feeds(client: Client, message: Message):
    if "rss_feeds" not in user_data or not user_data["rss_feeds"]:
        return await message.edit_text("No RSS feeds found!")
    
    feed_list = "**Your RSS Feeds:**\n"
    for i, feed in enumerate(user_data["rss_feeds"], 1):
        feed_list += f"`{i}.` {feed['url']}\n"
    
    await message.edit_text(feed_list)

@app.on_message(filters.command("menu", prefixes=".") & filters.me)
async def create_menu(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .menu [name] [button1|button2|button3]")
    
    menu_name = message.command[1]
    buttons_text = " ".join(message.command[2:])
    

    buttons = []
    for button_def in buttons_text.split('|'):
        if '=' in button_def:
            text, url = button_def.split('=', 1)
            buttons.append([InlineKeyboardButton(text.strip(), url=url.strip())])
    

    if "menus" not in user_data:
        user_data["menus"] = {}
    
    user_data["menus"][menu_name] = {
        "buttons": buttons,
        "created": datetime.now().isoformat()
    }
    save_data()
    
    await message.edit_text(f"**Menu '{menu_name}' created!**")

@app.on_message(filters.command("menus", prefixes=".") & filters.me)
async def list_menus(client: Client, message: Message):
    if "menus" not in user_data or not user_data["menus"]:
        return await message.edit_text("No menus found!")
    
    menu_list = "**Your Menus:**\n"
    for name in user_data["menus"].keys():
        menu_list += f"`{name}`\n"
    
    await message.edit_text(menu_list)

@app.on_message(filters.command("reaction", prefixes=".") & filters.me)
async def set_auto_reaction(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .reaction [trigger] [emoji]")
    
    trigger = message.command[1].lower()
    emoji = message.command[2]
    

    if "reactions" not in user_data:
        user_data["reactions"] = {}
    
    user_data["reactions"][trigger] = emoji
    save_data()
    
    await message.edit_text(f"**Auto reaction set for '{trigger}':** {emoji}")

@app.on_message(filters.command("delreaction", prefixes=".") & filters.me)
async def delete_auto_reaction(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .delreaction [trigger]")

    trigger = message.command[1].lower()

    if "reactions" in user_data and trigger in user_data["reactions"]:
        deleted_emoji = user_data["reactions"].pop(trigger)
        save_data()
        await message.edit_text(f"**Auto reaction removed for '{trigger}':** {deleted_emoji}")
    else:
        await message.edit_text(f"❌ No reaction found for trigger '{trigger}'")


@app.on_message(filters.text & filters.incoming & ~filters.me)
async def auto_reaction_handler(client: Client, message: Message):
    if "reactions" in user_data:
        text = message.text.lower()
        for trigger, emoji in user_data["reactions"].items():
            if re.search(r'\b' + re.escape(trigger) + r'\b', text):
                try:
                    await message.react([emoji])
                except:
                    pass
                break

@app.on_message(filters.command("ghost", prefixes=".") & filters.me)
async def ghost_mode(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .ghost [on/off]")
    
    mode = message.command[1].lower()
    if mode == "on":

        await message.edit_text("**Ghost mode activated!** (Implementation pending)")
    elif mode == "off":
        await message.edit_text("**Ghost mode deactivated!**")
    else:
        await message.edit_text("Usage: .ghost [on/off]")

@app.on_message(filters.command("antispam", prefixes=".") & filters.me)
async def antispam_protection(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .antispam [on/off]")
    
    mode = message.command[1].lower()
    if mode == "on":
        spam_protection[message.chat.id] = True
        await message.edit_text("**Anti-spam protection enabled!**")
    elif mode == "off":
        spam_protection[message.chat.id] = False
        await message.edit_text("**Anti-spam protection disabled!**")
    else:
        await message.edit_text("Usage: .antispam [on/off]")

@app.on_message(filters.command("captcha", prefixes=".") & filters.me)
async def captcha_protection(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .captcha [on/off]")
    
    mode = message.command[1].lower()
    if mode == "on":

        await message.edit_text("**CAPTCHA protection enabled!** (Implementation pending)")
    elif mode == "off":
        await message.edit_text("**CAPTCHA protection disabled!**")
    else:
        await message.edit_text("Usage: .captcha [on/off]")

@app.on_message(filters.command("welcome", prefixes=".") & filters.me)
async def set_welcome_message(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .welcome [on/off] [message]")
    
    mode = message.command[1].lower()
    welcome_msg = " ".join(message.command[2:])
    
    if message.chat.id not in group_settings:
        group_settings[message.chat.id] = {}
    
    if mode == "on":
        group_settings[message.chat.id]["welcome"] = welcome_msg
        group_settings[message.chat.id]["welcome_enabled"] = True
        await message.edit_text("**Welcome message enabled!**")
    elif mode == "off":
        group_settings[message.chat.id]["welcome_enabled"] = False
        await message.edit_text("**Welcome message disabled!**")
    else:
        await message.edit_text("Usage: .welcome [on/off] [message]")
    
    save_data()

@app.on_message(filters.command("goodbye", prefixes=".") & filters.me)
async def set_goodbye_message(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("Usage: .goodbye [on/off] [message]")
    
    mode = message.command[1].lower()
    goodbye_msg = " ".join(message.command[2:])
    
    if message.chat.id not in group_settings:
        group_settings[message.chat.id] = {}
    
    if mode == "on":
        group_settings[message.chat.id]["goodbye"] = goodbye_msg
        group_settings[message.chat.id]["goodbye_enabled"] = True
        await message.edit_text("**Goodbye message enabled!**")
    elif mode == "off":
        group_settings[message.chat.id]["goodbye_enabled"] = False
        await message.edit_text("**Goodbye message disabled!**")
    else:
        await message.edit_text("Usage: .goodbye [on/off] [message]")
    
    save_data()

@app.on_message(filters.command("cloud", prefixes=".") & filters.me)
async def cloud_storage_menu(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Upload File", callback_data="cloud_upload")],
        [InlineKeyboardButton("List Files", callback_data="cloud_list")],
        [InlineKeyboardButton("Download File", callback_data="cloud_download")],
        [InlineKeyboardButton("Delete File", callback_data="cloud_delete")]
    ])
    
    await message.edit_text("**☁️ Cloud Storage Menu**", reply_markup=keyboard)

@app.on_message(filters.command("backup", prefixes=".") & filters.me)
async def backup_data(client: Client, message: Message):
    try:

        backup_data = {
            "auto_replies": auto_replies,
            "blocked_users": list(blocked_users),
            "notes": notes,
            "reminders": reminders,
            "custom_quotes": custom_quotes,
            "custom_commands": custom_commands,
            "scheduled_tasks": scheduled_tasks,
            "user_data": user_data,
            "group_settings": group_settings,
            "timestamp": datetime.now().isoformat()
        }
        
        backup_file = f"backup_{int(datetime.now().timestamp())}.json"
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        

        await client.send_document("me", backup_file, caption="**UserBot Backup**")
        

        os.remove(backup_file)
        
        await message.edit_text("**Backup created and sent to Saved Messages!**")
    except Exception as e:
        await message.edit_text(f"**Error creating backup:** {str(e)}")

@app.on_message(filters.command("restore", prefixes=".") & filters.me)
async def restore_data(client: Client, message: Message):
    await message.edit_text("**Restore functionality needs implementation with file upload handling**")

@app.on_message(filters.command("debug", prefixes=".") & filters.me)
async def debug_mode(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .debug [on/off]")
    
    mode = message.command[1].lower()
    if mode == "on":

        logger.setLevel(logging.DEBUG)
        await message.edit_text("**Debug mode enabled!**")
    elif mode == "off":

        logger.setLevel(logging.INFO)
        await message.edit_text("**Debug mode disabled!**")
    else:
        await message.edit_text("Usage: .debug [on/off]")

@app.on_message(filters.command("sysinfo", prefixes=".") & filters.me)
async def system_info(client: Client, message: Message):
    try:
        import psutil
        import platform
        

        uname = platform.uname()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        info = "**System Information:**\n"
        info += f"System: {uname.system}\n"
        info += f"Node Name: {uname.node}\n"
        info += f"Release: {uname.release}\n"
        info += f"Version: {uname.version}\n"
        info += f"Machine: {uname.machine}\n"
        info += f"Processor: {uname.processor}\n"
        info += f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += f"Uptime: {uptime}\n\n"
        

        info += "**CPU Info:**\n"
        info += f"Physical cores: {psutil.cpu_count(logical=False)}\n"
        info += f"Total cores: {psutil.cpu_count(logical=True)}\n"
        info += f"Max Frequency: {psutil.cpu_freq().max:.2f}Mhz\n"
        info += f"Current Frequency: {psutil.cpu_freq().current:.2f}Mhz\n"
        info += f"CPU Usage: {psutil.cpu_percent()}%\n\n"
        

        svmem = psutil.virtual_memory()
        info += "**Memory Information:**\n"
        info += f"Total: {svmem.total / (1024**3):.2f} GB\n"
        info += f"Available: {svmem.available / (1024**3):.2f} GB\n"
        info += f"Used: {svmem.used / (1024**3):.2f} GB\n"
        info += f"Percentage: {svmem.percent}%\n"
        
        await message.edit_text(info)
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("speedtest", prefixes=".") & filters.me)
async def speed_test(client: Client, message: Message):
    await message.edit_text("**Running speed test...** (Implementation pending)")

@app.on_message(filters.command("logs", prefixes=".") & filters.me)
async def get_logs(client: Client, message: Message):
    try:

        await message.edit_text("**Logs functionality needs implementation**")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("restart", prefixes=".") & filters.me)
async def restart_bot(client: Client, message: Message):
    await message.edit_text("**Restarting bot...**")


    await asyncio.sleep(2)
    await message.edit_text("**Bot restarted!**")

@app.on_message(filters.command("update", prefixes=".") & filters.me)
async def update_bot(client: Client, message: Message):
    await message.edit_text("**Checking for updates...** (Implementation pending)")

@app.on_message(filters.command("cleanup", prefixes=".") & filters.me)
async def cleanup_files(client: Client, message: Message):
    try:

        cleaned = 0
        for root, dirs, files in os.walk("temp"):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    cleaned += 1
                except:
                    pass
        
        await message.edit_text(f"**Cleaned up {cleaned} temporary files!**")
    except Exception as e:
        await message.edit_text(f"**Error during cleanup:** {str(e)}")

@app.on_message(filters.command("broadcast", prefixes=".") & filters.me)
async def broadcast_message(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .broadcast [message]")
    
    broadcast_msg = " ".join(message.command[1:])

    await message.edit_text("**Broadcast functionality needs implementation**")



@app.on_message(filters.command("pingall", prefixes=".") & filters.me)
async def ping_all_members(client: Client, message: Message):
    """Ping all members in the current chat"""
    try:
        await message.edit_text("**🔄 Fetching chat members...**")
        
        chat_id = message.chat.id
        members = []
        mentions = []
        

        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)
        
        if not members:
            return await message.edit_text("**❌ No members found to ping!**")
        

        batch_size = 5
        total_batches = (len(members) + batch_size - 1) // batch_size
        
        await message.edit_text(f"**📢 Pinging {len(members)} members in {total_batches} batches...**")
        
        for i in range(0, len(members), batch_size):
            batch = members[i:i+batch_size]
            mention_text = " ".join([f"[{user.first_name}](tg://user?id={user.id})" for user in batch])
            
            if i == 0:
                await message.edit_text(f"**📢 Ping {(i//batch_size)+1}:**\n{mention_text}")
            else:
                await message.reply_text(f"**📢 Ping {(i//batch_size)+1}:**\n{mention_text}")
            

            await asyncio.sleep(1)
        
        await message.reply_text(f"**✅ Successfully pinged {len(members)} members!**")
        
    except FloodWait as e:
        await message.edit_text(f"**⚠️ Rate limited! Wait {e.value} seconds**")
    except Exception as e:
        await message.edit_text(f"**❌ Error:** `{str(e)}`")

@app.on_message(filters.command("export", prefixes=".") & filters.me)
async def export_chat_members(client: Client, message: Message):
    """Export chat members to a file"""
    try:
        await message.edit_text("**🔄 Exporting chat members...**")
        
        chat_id = message.chat.id
        chat_info = await client.get_chat(chat_id)
        members_data = []
        

        async for member in client.get_chat_members(chat_id):
            user = member.user
            member_info = {
                "id": user.id,
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "username": user.username or "",
                "phone_number": user.phone_number or "",
                "is_bot": user.is_bot,
                "is_verified": user.is_verified,
                "is_premium": user.is_premium,
                "status": str(member.status),
                "joined_date": member.joined_date.isoformat() if member.joined_date else "",
            }
            members_data.append(member_info)
        

        export_data = {
            "chat_info": {
                "id": chat_info.id,
                "title": chat_info.title or "",
                "type": str(chat_info.type),
                "members_count": len(members_data),
                "export_date": datetime.now().isoformat()
            },
            "members": members_data
        }
        

        filename = f"chat_export_{chat_id}_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        

        await message.edit_text(f"**📁 Exported {len(members_data)} members**")
        await client.send_document(
            chat_id,
            filename,
            caption=f"**📊 Chat Export**\n**Chat:** {chat_info.title}\n**Members:** {len(members_data)}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        

        os.remove(filename)
        
    except Exception as e:
        await message.edit_text(f"**❌ Export failed:** `{str(e)}`")

@app.on_message(filters.command("import", prefixes=".") & filters.me)
async def import_chat_members(client: Client, message: Message):
    """Import members from a JSON file to current chat"""
    try:

        if not message.reply_to_message or not message.reply_to_message.document:
            return await message.edit_text("**❌ Reply to a JSON export file to import members**")
        
        await message.edit_text("**🔄 Downloading and processing file...**")
        

        file_path = await client.download_media(message.reply_to_message)
        

        with open(file_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        members = import_data.get('members', [])
        chat_id = message.chat.id
        
        successful_adds = 0
        failed_adds = 0
        
        await message.edit_text(f"**🔄 Importing {len(members)} members...**")
        
        for i, member in enumerate(members):
            try:
                user_id = member.get('id')
                username = member.get('username')
                

                if username:
                    await client.add_chat_members(chat_id, f"@{username}")
                else:
                    await client.add_chat_members(chat_id, user_id)
                
                successful_adds += 1
                

                if (i + 1) % 10 == 0:
                    await message.edit_text(f"**🔄 Progress: {i+1}/{len(members)}\n✅ Added: {successful_adds}\n❌ Failed: {failed_adds}**")
                

                await asyncio.sleep(1)
                
            except FloodWait as e:
                await asyncio.sleep(e.value)
                continue
            except Exception:
                failed_adds += 1
                continue
        
        await message.edit_text(f"**📊 Import Complete**\n**✅ Successfully added:** {successful_adds}\n**❌ Failed to add:** {failed_adds}")
        

        os.remove(file_path)
        
    except Exception as e:
        await message.edit_text(f"**❌ Import failed:** `{str(e)}`")

@app.on_message(filters.command("ss", prefixes=".") & filters.me)
async def take_screenshot(client: Client, message: Message):
    """Take screenshot of a website using Pyppeteer"""
    if len(message.command) < 2:
        return await message.edit_text("**Usage:** `.screenshot [url]`")
    
    try:
        url = message.command[1]
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        await message.edit_text(f"**🔄 Taking screenshot of {url}...**")
        

        browser = await launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-gpu'
            ]
        )
        
        try:

            page = await browser.newPage()
            

            await page.setViewport({'width': 1920, 'height': 1080})
            

            await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            

            await page.goto(url, {'waitUntil': 'networkidle2', 'timeout': 30000})
            

            await asyncio.sleep(2)
            

            screenshot_path = f"screenshot_{int(time.time())}.png"
            await page.screenshot({
                'path': screenshot_path,
                'fullPage': True,
                'quality': 90
            })
            

            title = await page.title()
            

            await message.edit_text(f"**📸 Screenshot captured!**")
            await client.send_photo(
                message.chat.id,
                screenshot_path,
                caption=f"**🔗 URL:** {url}\n**📄 Title:** {title[:50]}{'...' if len(title) > 50 else ''}\n**📅 Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            

            os.remove(screenshot_path)
            
        finally:
            await browser.close()
            
    except Exception as e:
        await message.edit_text(f"**❌ Screenshot failed:** `{str(e)}`")

@app.on_message(filters.command("currency", prefixes=".") & filters.me)
async def currency_converter(client: Client, message: Message):
    """Convert currency using live exchange rates"""
    if len(message.command) < 4:
        return await message.edit_text("**Usage:** `.currency [amount] [from_currency] [to_currency]`\n**Example:** `.currency 100 USD EUR`")
    
    try:
        amount = float(message.command[1])
        from_curr = message.command[2].upper()
        to_curr = message.command[3].upper()
        
        await message.edit_text("**🔄 Getting exchange rates...**")
        

        async with aiohttp.ClientSession() as session:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if to_curr in data['rates']:
                        rate = data['rates'][to_curr]
                        converted = amount * rate
                        
                        await message.edit_text(
                            f"**💱 Currency Conversion**\n\n"
                            f"**Amount:** {amount:,.2f} {from_curr}\n"
                            f"**Converts to:** {converted:,.2f} {to_curr}\n"
                            f"**Exchange Rate:** 1 {from_curr} = {rate:.4f} {to_curr}\n"
                            f"**Last Updated:** {data['date']}"
                        )
                    else:
                        await message.edit_text(f"**❌ Currency '{to_curr}' not found!**")
                else:
                    await message.edit_text("**❌ Failed to fetch exchange rates!**")
                    
    except ValueError:
        await message.edit_text("**❌ Invalid amount! Please enter a valid number.**")
    except Exception as e:
        await message.edit_text(f"**❌ Error:** `{str(e)}`")

@app.on_message(filters.command("time", prefixes=".") & filters.me)
async def get_time(client: Client, message: Message):
    """Get current time for a specific location"""
    if len(message.command) < 2:
        return await message.edit_text("**Usage:** `.time [location]`\n**Example:** `.time New York`")
    
    try:
        location = " ".join(message.command[1:])
        await message.edit_text(f"**🔄 Getting time for {location}...**")
        

        async with aiohttp.ClientSession() as session:

            url = f"http://worldtimeapi.org/api/timezone"
            async with session.get(url) as response:
                if response.status == 200:
                    timezones = await response.json()
                    

                    location_lower = location.lower()
                    matching_tz = None
                    
                    for tz in timezones:
                        if location_lower in tz.lower():
                            matching_tz = tz
                            break
                    
                    if not matching_tz:

                        city_mapping = {
                            'new york': 'America/New_York',
                            'london': 'Europe/London',
                            'tokyo': 'Asia/Tokyo',
                            'dubai': 'Asia/Dubai',
                            'sydney': 'Australia/Sydney',
                            'paris': 'Europe/Paris',
                            'berlin': 'Europe/Berlin',
                            'moscow': 'Europe/Moscow',
                            'delhi': 'Asia/Kolkata',
                            'mumbai': 'Asia/Kolkata',
                            'kolkata': 'Asia/Kolkata',
                            'chennai': 'Asia/Kolkata',
                            'bangalore': 'Asia/Kolkata',
                        }
                        matching_tz = city_mapping.get(location_lower)
                    
                    if matching_tz:
                        url = f"http://worldtimeapi.org/api/timezone/{matching_tz}"
                        async with session.get(url) as tz_response:
                            if tz_response.status == 200:
                                time_data = await tz_response.json()
                                
                                datetime_str = time_data['datetime']
                                timezone = time_data['timezone']
                                utc_offset = time_data['utc_offset']
                                

                                dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                                
                                await message.edit_text(
                                    f"**🕐 Time Information**\n\n"
                                    f"**Location:** {location}\n"
                                    f"**Timezone:** {timezone}\n"
                                    f"**Current Time:** {dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                    f"**UTC Offset:** {utc_offset}\n"
                                    f"**Day of Year:** {time_data['day_of_year']}\n"
                                    f"**Week Number:** {time_data['week_number']}"
                                )
                            else:
                                await message.edit_text(f"**❌ Could not get time data for {location}**")
                    else:
                        await message.edit_text(f"**❌ Location '{location}' not found! Try a major city name.**")
                        
    except Exception as e:
        await message.edit_text(f"**❌ Error:** `{str(e)}`")

@app.on_message(filters.command("domain", prefixes=".") & filters.me)
async def domain_info(client: Client, message: Message):
    """Get comprehensive domain information"""
    if len(message.command) < 2:
        return await message.edit_text("**Usage:** `.domain [domain]`\n**Example:** `.domain google.com`")
    
    try:
        domain = message.command[1].replace('http://', '').replace('https://', '').split('/')[0]
        await message.edit_text(f"**🔄 Analyzing domain {domain}...**")
        
        domain_info = {}
        

        try:
            ip = socket.gethostbyname(domain)
            domain_info['ip'] = ip
        except:
            domain_info['ip'] = "Not found"
        

        try:
            w = whois.whois(domain)
            domain_info['registrar'] = w.registrar or "Not available"
            domain_info['creation_date'] = str(w.creation_date) if w.creation_date else "Not available"
            domain_info['expiration_date'] = str(w.expiration_date) if w.expiration_date else "Not available"
            domain_info['name_servers'] = w.name_servers if w.name_servers else ["Not available"]
        except:
            domain_info.update({
                'registrar': "Not available",
                'creation_date': "Not available", 
                'expiration_date': "Not available",
                'name_servers': ["Not available"]
            })
        

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{domain}", timeout=10) as response:
                    domain_info['http_status'] = response.status
                    domain_info['server'] = response.headers.get('server', 'Not available')
        except:
            domain_info['http_status'] = "Not available"
            domain_info['server'] = "Not available"
        

        ns_list = domain_info['name_servers']
        if isinstance(ns_list, list) and len(ns_list) > 1:
            ns_text = '\n'.join([f"• {ns}" for ns in ns_list[:5]])
        else:
            ns_text = str(ns_list[0]) if ns_list else "Not available"
        
        result = f"""**🌐 Domain Information**

**Domain:** {domain}
**IP Address:** {domain_info['ip']}
**HTTP Status:** {domain_info['http_status']}
**Server:** {domain_info['server']}

**📋 Registration Details**
**Registrar:** {domain_info['registrar']}
**Created:** {domain_info['creation_date']}
**Expires:** {domain_info['expiration_date']}

**🔧 Name Servers**
{ns_text}"""
        
        await message.edit_text(result)
        
    except Exception as e:
        await message.edit_text(f"**❌ Error analyzing domain:** `{str(e)}`")

@app.on_message(filters.command("ip", prefixes=".") & filters.me)
async def ip_info(client: Client, message: Message):
    """Get detailed IP address information"""
    if len(message.command) < 2:
        return await message.edit_text("**Usage:** `.ip [ip_address]`\n**Example:** `.ip 8.8.8.8`")
    
    try:
        ip = message.command[1]
        await message.edit_text(f"**🔄 Analyzing IP {ip}...**")
        

        async with aiohttp.ClientSession() as session:
            url = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data['status'] == 'success':
                        result = f"""**🌍 IP Address Information**

**IP:** {data['query']}
**ISP:** {data.get('isp', 'N/A')}
**Organization:** {data.get('org', 'N/A')}
**AS:** {data.get('as', 'N/A')}

**📍 Location**
**Country:** {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})
**Region:** {data.get('regionName', 'N/A')} ({data.get('region', 'N/A')})
**City:** {data.get('city', 'N/A')}
**ZIP Code:** {data.get('zip', 'N/A')}
**Coordinates:** {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}

**🕐 Time Zone**
**Timezone:** {data.get('timezone', 'N/A')}
**UTC Offset:** {data.get('offset', 'N/A')}

**🔍 Additional Info**
**Reverse DNS:** {data.get('reverse', 'N/A')}
**Mobile:** {'Yes' if data.get('mobile') else 'No'}
**Proxy:** {'Yes' if data.get('proxy') else 'No'}
**Hosting:** {'Yes' if data.get('hosting') else 'No'}"""
                        
                        await message.edit_text(result)
                    else:
                        await message.edit_text(f"**❌ Failed to get IP info:** {data.get('message', 'Unknown error')}")
                else:
                    await message.edit_text("**❌ Failed to fetch IP information!**")
                    
    except Exception as e:
        await message.edit_text(f"**❌ Error:** `{str(e)}`")

@app.on_message(filters.command("whoisdomain", prefixes=".") & filters.me)
async def whois_domain(client: Client, message: Message):
    """Get detailed WHOIS information for a domain"""
    if len(message.command) < 2:
        return await message.edit_text("**Usage:** `.whoisdomain [domain]`\n**Example:** `.whoisdomain google.com`")
    
    try:
        domain = message.command[1].replace('http://', '').replace('https://', '').split('/')[0]
        await message.edit_text(f"**🔄 Getting WHOIS data for {domain}...**")
        

        w = whois.query(domain)
        

        def format_date(date_obj):
            if isinstance(date_obj, list):
                return str(date_obj[0]) if date_obj else "Not available"
            return str(date_obj) if date_obj else "Not available"
        

        name_servers = w.name_servers
        if name_servers and isinstance(name_servers, list):
            ns_text = '\n'.join([f"• {ns}" for ns in name_servers[:8]])
        else:
            ns_text = str(name_servers) if name_servers else "Not available"
        

        def format_contact(contact_list):
            if contact_list and isinstance(contact_list, list):
                return contact_list[0] if contact_list[0] else "Not available"
            return str(contact_list) if contact_list else "Not available"
        
        result = f"""**📋 WHOIS Information**

**Domain:** {domain}
**Registrar:** {w.registrar or 'Not available'}
**WHOIS Server:** {w.whois_server or 'Not available'}

**📅 Important Dates**
**Created:** {format_date(w.creation_date)}
**Updated:** {format_date(w.updated_date)}
**Expires:** {format_date(w.expiration_date)}

**👤 Registrant**
**Name:** {w.name or 'Not available'}
**Organization:** {w.org or 'Not available'}
**Email:** {format_contact(w.emails)}

**🔧 Technical Details**
**Status:** {w.status or 'Not available'}
**DNSSEC:** {w.dnssec or 'Not available'}

**🌐 Name Servers**
{ns_text}

**🏢 Registrar Info**
**Registrar IANA ID:** {w.registrar_iana_id or 'Not available'}
**Registrar URL:** {w.registrar_url or 'Not available'}"""
        

        if len(result) > 4096:
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            await message.edit_text(parts[0])
            for part in parts[1:]:
                await message.reply_text(part)
        else:
            await message.edit_text(result)
            
    except Exception as e:
        await message.edit_text(f"**❌ WHOIS lookup failed:** `{str(e)}`")



async def get_chat_member_count(client: Client, chat_id: int) -> int:
    """Get total member count of a chat"""
    try:
        chat = await client.get_chat(chat_id)
        return chat.members_count or 0
    except:
        return 0
    
@app.on_message(filters.command("eval", prefixes=".") & filters.me)
async def evaluate_code(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .eval [code]")
    
    code = " ".join(message.command[1:])
    try:


        result = eval(code)
        await message.edit_text(f"**Result:**\n```\n{result}\n```")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("exec", prefixes=".") & filters.me)
async def execute_code(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .exec [code]")
    
    code = " ".join(message.command[1:])
    try:


        exec(code)
        await message.edit_text("**Code executed successfully!**")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("shell", prefixes=".") & filters.me)
async def execute_shell(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .shell [command]")
    
    command = " ".join(message.command[1:])
    try:


        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout or result.stderr
        await message.edit_text(f"**Shell Output:**\n```\n{output}\n```")
    except Exception as e:
        await message.edit_text(f"**Error:** {str(e)}")

@app.on_message(filters.command("addon", prefixes=".") & filters.me)
async def load_addon(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .addon [addon_name]")
    
    addon_name = message.command[1]
    await message.edit_text(f"**Loading addon '{addon_name}'...** (Implementation pending)")

@app.on_message(filters.command("addons", prefixes=".") & filters.me)
async def list_addons(client: Client, message: Message):
    await message.edit_text("**Available addons:** (Implementation pending)")

@app.on_message(filters.command("createaddon", prefixes=".") & filters.me)
async def create_addon(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .createaddon [addon_name]")
    
    addon_name = message.command[1]
    await message.edit_text(f"**Creating addon '{addon_name}'...** (Implementation pending)")

@app.on_message(filters.command("editaddon", prefixes=".") & filters.me)
async def edit_addon(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .editaddon [addon_name]")
    
    addon_name = message.command[1]
    await message.edit_text(f"**Editing addon '{addon_name}'...** (Implementation pending)")

@app.on_message(filters.command("deleteaddon", prefixes=".") & filters.me)
async def delete_addon(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit_text("Usage: .deleteaddon [addon_name]")
    
    addon_name = message.command[1]
    await message.edit_text(f"**Deleting addon '{addon_name}'...** (Implementation pending)")

@app.on_message(filters.command("reloadaddons", prefixes=".") & filters.me)
async def reload_addons(client: Client, message: Message):
    await message.edit_text("**Reloading all addons...** (Implementation pending)")


@app.on_message(
    filters.command("vc", prefixes=".") & 
    filters.me & 
    ~filters.private
)
async def start_vc_command(client: Client, message: Message):
    chat_id = message.chat.id
    

    peer = await client.resolve_peer(chat_id)
    

    result = await client.invoke(
        CreateGroupCall(
            peer=InputPeerChannel(
                channel_id=peer.channel_id,
                access_hash=peer.access_hash,
            ),
            random_id=client.rnd_id() // 9000000000,
        )
    )
    
    await message.edit("🎤 VC Started!")


@app.on_message(filters.command("pro", prefixes=".") & filters.me)
async def start_command(client: Client, message: Message):
    client.start_time = datetime.now()
    await message.reply_text(
        "🚀 **ULTRA USERBOT STARTED!** 🚀\n\n"
        "Use `.help` to see all available commands.\n"
        "This is a PRO edition with maximum features!\n\n"
        "**Features Include:**\n"
        "• Advanced Group Management\n"
        "• Media Saving & Cloud Storage\n"
        "• Privacy & Security Controls\n"
        "• Automation & Custom Commands\n"
        "• Search & Translation\n"
        "• Notes & Reminders\n"
        "• Profile Management\n"
        "• Entertainment & Fun\n"
        "• Developer Tools\n"
        "• Custom Addons\n"
    )
    
@app.on_message(filters.incoming & ~filters.me)
async def unified_message_handler(client: Client, message: Message):

    if message.from_user and str(message.from_user.id) in blocked_users:
        try:
            await message.delete()
        except:
            pass
        return
    

    if message.new_chat_members:
        for user in message.new_chat_members:

            if (message.chat.id in group_settings and 
                group_settings[message.chat.id].get("welcome_enabled", False)):
                welcome_msg = group_settings[message.chat.id].get("welcome", "Welcome to the group!")
                await message.reply_text(welcome_msg)
        

        if message.chat.id in group_settings and group_settings[message.chat.id].get("ghost_mode", False):
            try:
                await message.delete()
            except:
                pass
        return
    

    if message.text:
        text = message.text.lower()
        if message.chat.type == ChatType.PRIVATE:

            global afk_mode, afk_reason, afk_start_time
            
            if afk_mode and message.from_user:
                if afk_start_time:
                    afk_duration = datetime.now() - afk_start_time
                    duration_str = format_time(int(afk_duration.total_seconds()))
                else:
                    duration_str = "unknown time"
                
                await message.reply_text(
                    f"**I'm currently AFK**\n"
                    f"Reason: {afk_reason}\n"
                    f"Since: {duration_str} ago"
                )
                return
            

        for trigger, response in auto_replies.items():
            if re.search(r'\b' + re.escape(trigger) + r'\b', text):
                await message.reply_text(response)
                return
        

        if message.chat.id in active_filters:
            for trigger, response in active_filters[message.chat.id].items():
                if re.search(r'\b' + re.escape(trigger) + r'\b', text):
                    await message.reply_text(response)
                    return
                
                
        if "reactions" in user_data:
            for trigger, emoji in user_data["reactions"].items():
                pattern = r'\b{}\b'.format(re.escape(trigger))
                if re.search(pattern, text, re.IGNORECASE):
                    try:
                        await message.react([emoji])
                    except:
                        pass
                    break
                
async def main():
    await app.start()
    await idle()

if __name__ == "__main__":
    app.run(main())
    
# ------------------- REST FEATURES SOON PLEASE CONTRIBUTE TO MAKE IT MORE ADVANCE SPECIALLY RAW API Methods ---------------
