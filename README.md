# TELE USERBOT

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)](https://pyrogram.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-@devgaganin-blue.svg)](https://t.me/devgaganin)

**A powerful, feature-rich Telegram userbot with 100+ commands for automation, media management, and enhanced Telegram experience.**

</div>

## ✨ Features

- 🔧 **100+ Commands** - Comprehensive command library
- 🤖 **Automation** - Auto replies, filters, scheduled tasks
- 💾 **Media Management** - Save, organize, and manage media files
- 🛡️ **Privacy & Security** - Ghost mode, anti-spam, user blocking
- 🎮 **Entertainment** - Games, jokes, ASCII art, and fun commands
- 🌐 **Search & Translation** - Multi-platform search and language tools
- 👑 **Administration** - Full group management capabilities
- 📝 **Notes & Reminders** - Personal productivity tools
- 🔌 **Custom Addons** - Extensible plugin system
- ⚡ **High Performance** - Fast and lightweight

## 📋 Complete Command List

### 👑 Administration Commands (22)
| Command | Usage | Description |
|---------|-------|-------------|
| `.ban` | `.ban [reply/user_id]` | Ban user from group |
| `.unban` | `.unban [user_id]` | Unban user from group |
| `.kick` | `.kick [reply/user_id]` | Kick user from group |
| `.promote` | `.promote [reply/user_id] [rank]` | Promote user to admin |
| `.demote` | `.demote [reply/user_id]` | Demote admin to member |
| `.pin` | `.pin [reply]` | Pin replied message |
| `.unpin` | `.unpin [reply]` | Unpin replied message |
| `.vc` | `.vc` | Turn on voice chat |
| `.mute` | `.mute [reply/user_id] [time]` | Mute user for specified time |
| `.unmute` | `.unmute [reply/user_id]` | Unmute user |
| `.purge` | `.purge [reply]` | Delete messages from replied message |
| `.del` | `.del [reply]` | Delete replied message |
| `.lock` | `.lock [permission]` | Lock chat permissions |
| `.unlock` | `.unlock [permission]` | Unlock chat permissions |
| `.admins` | `.admins` | List all group admins |
| `.bots` | `.bots` | List all bots in group |
| `.users` | `.users` | List all users in group |
| `.zombies` | `.zombies` | Find deleted accounts |
| `.settitle` | `.settitle [title]` | Set group title |
| `.restoretitle` | `.restoretitle` | Restore original title |
| `.welcome` | `.welcome [on/off] [msg]` | Set welcome message |
| `.goodbye` | `.goodbye [on/off] [msg]` | Set goodbye message |
| `.filter` | `.filter [trigger] [response]` | Add auto-response filter |
| `.filters` | `.filters` | List all active filters |
| `.stop` | `.stop [trigger]` | Remove filter |

### 💾 Media & Storage Commands (7)
| Command | Usage | Description |
|---------|-------|-------------|
| `.save` | `.save [reply]` | Save media file |
| `.get` | `.get [file_id]` | Retrieve saved file |
| `.files` | `.files` | List all saved files |
| `.delmedia` | `.delmedia [file_id]` | Delete saved media |
| `.cloud` | `.cloud` | Access cloud storage menu |
| `.backup` | `.backup` | Backup all userbot data |
| `.restore` | `.restore` | Restore from backup |

### 🛡️ Privacy & Security Commands (10)
| Command | Usage | Description |
|---------|-------|-------------|
| `.block` | `.block [reply/user_id]` | Block user |
| `.unblock` | `.unblock [user_id]` | Unblock user |
| `.blocked` | `.blocked` | List blocked users |
| `.afk` | `.afk [reason]` | Set AFK mode with reason |
| `.unafk` | `.unafk` | disable AFK mode |
| `.ghost` | `.ghost [on/off]` | Toggle ghost mode |
| `.antispam` | `.antispam [on/off]` | Toggle anti-spam protection |
| `.captcha` | `.captcha [on/off]` | Enable CAPTCHA for new users |
| `.report` | `.report [reply]` | Report message to admins |
| `.whitelist` | `.whitelist [user_id]` | Add user to whitelist |

### 🤖 Automation & Custom Commands (12)
| Command | Usage | Description |
|---------|-------|-------------|
| `.autoreply` | `.autoreply [trigger] [response]` | Set automatic reply |
| `.delreply` | `.delreply [trigger]` | Delete auto reply |
| `.replies` | `.replies` | List all auto replies |
| `.alias` | `.alias [name] [command]` | Create command alias |
| `.unalias` | `.unalias [name]` | Remove command alias |
| `.aliases` | `.aliases` | List all aliases |
| `.menu` | `.menu [name] [buttons]` | Create custom menu |
| `.menus` | `.menus` | List all custom menus |
| `.reaction` | `.reaction [trigger] [emoji]` | Set auto reaction |
| `.delreaction` | `.delreaction [trigger]` | Delete auto reaction |
| `.schedule` | `.schedule [time] [command]` | Schedule command execution |
| `.unschedule` | `.unschedule [id]` | Cancel scheduled task |
| `.tasks` | `.tasks` | List scheduled tasks |

### 📝 Notes & Reminders Commands (8)
| Command | Usage | Description |
|---------|-------|-------------|
| `.note` | `.note [name] [content]` | Save a note |
| `.getnote` | `.getnote [name]` | Retrieve saved note |
| `.delnote` | `.delnote [name]` | Delete note |
| `.notes` | `.notes` | List all saved notes |
| `.remind` | `.remind [time] [message]` | Set reminder |
| `.reminders` | `.reminders` | List all reminders |
| `.todo` | `.todo [task]` | Add task to todo list |
| `.todos` | `.todos` | List todo items |
| `.done` | `.done [id]` | Mark todo as completed |

### 🌐 Search & Translation Commands (11)
| Command | Usage | Description |
|---------|-------|-------------|
| `.search` | `.search [query]` | Search YouTube videos |
| `.tr` | `.tr [language] [text]` | Translate text |
| `.wiki` | `.wiki [query]` | Search Wikipedia |
| `.img` | `.img [query]` | Search images |
| `.weather` | `.weather [city]` | Get weather information |
| `.ud` | `.ud [word]` | Urban Dictionary lookup |
| `.define` | `.define [word]` | Dictionary definition |
| `.syn` | `.syn [word]` | Find synonyms |
| `.ant` | `.ant [word]` | Find antonyms |
| `.news` | `.news [category]` | Get latest news |
| `.rss` | `.rss [url]` | Add RSS feed |
| `.feeds` | `.feeds` | List RSS feeds |

### 👤 Profile & Presence Commands (10)
| Command | Usage | Description |
|---------|-------|-------------|
| `.setbio` | `.setbio [text]` | Set profile bio |
| `.setpic` | `.setpic [reply/photo]` | Set profile picture |
| `.setname` | `.setname [first] [last]` | Set display name |
| `.username` | `.username [username]` | Set username |
| `.qr` | `.qr [text]` | Generate QR code |
| `.readqr` | `.readqr [reply]` | Read QR code |
| `.avatar` | `.avatar [user_id]` | Get user avatar |
| `.status` | `.status [text]` | Set custom status |
| `.clone` | `.clone [user_id]` | Clone user profile |
| `.revert` | `.revert` | Revert profile changes |

### 🎮 Entertainment & Fun Commands (23)
| Command | Usage | Description |
|---------|-------|-------------|
| `.quote` | `.quote` | Get random quote |
| `.addquote` | `.addquote [text]` | Add custom quote |
| `.delquote` | `.delquote [id]` | Delete custom quote |
| `.myquotes` | `.myquotes` | List your quotes |
| `.joke` | `.joke` | Get random joke |
| `.fact` | `.fact` | Get random fact |
| `.meme` | `.meme` | Get random meme |
| `.ascii` | `.ascii [text]` | Convert text to ASCII art |
| `.reverse` | `.reverse [text]` | Reverse text |
| `.mock` | `.mock [text]` | Create mocking text |
| `.vapor` | `.vapor [text]` | Convert to vaporwave text |
| `.clap` | `.clap [text]` | Add claps between words |
| `.emojify` | `.emojify [text]` | Add random emojis |
| `.spoiler` | `.spoiler [text]` | Create spoiler text |
| `.password` | `.password [length]` | Generate random password |
| `.hash` | `.hash [text]` | Generate text hash |
| `.base64` | `.base64 [encode/decode] [text]` | Base64 encoding/decoding |
| `.leet` | `.leet [text]` | Convert to 1337 speak |
| `.flip` | `.flip [text]` | Flip text upside down |
| `.cowsay` | `.cowsay [text]` | ASCII cow says text |
| `.roll` | `.roll [dice]` | Roll dice |
| `.8ball` | `.8ball [question]` | Magic 8 ball |
| `.choose` | `.choose [option1\|option2]` | Random choice picker |

### ⚙️ Utilities & Tools Commands (22)
| Command | Usage | Description |
|---------|-------|-------------|
| `.calc` | `.calc [expression]` | Calculator |
| `.ping` | `.ping` | Check bot response time |
| `.leave` | `.leave` | Leave current chat |
| `.echo` | `.echo [text]` | Echo message |
| `.type` | `.type [text]` | Typing animation |
| `.alive` | `.alive` | Check bot status |
| `.short` | `.short [url]` | Shorten URL |
| `.expand` | `.expand [url]` | Expand shortened URL |
| `.spb` | `.spb [user_id]` | Check SpamWatch ban |
| `.whois` | `.whois [user_id]` | Advanced user information |
| `.id` | `.id [reply/user_id]` | Get user/chat IDs |
| `.info` | `.info [reply/user_id]` | Detailed user info |
| `.stats` | `.stats` | Group statistics |
| `.invite` | `.invite [user_id]` | Invite user to group |
| `.export` | `.export [chat_id]` | Export chat members |
| `.import` | `.import [file]` | Import member list |
| `.ss` | `.ss [url]` | Take website screenshot |
| `.currency` | `.currency [amount] [from] [to]` | Currency converter |
| `.time` | `.time [location]` | Get current time |
| `.domain` | `.domain [domain]` | Domain information |
| `.ip` | `.ip [ip_address]` | IP address lookup |
| `.whoisdomain` | `.whoisdomain [domain]` | Whois domain lookup |

### 🔧 Developer & Advanced Commands (12)
| Command | Usage | Description |
|---------|-------|-------------|
| `.eval` | `.eval [code]` | Evaluate Python code |
| `.exec` | `.exec [code]` | Execute Python code |
| `.shell` | `.shell [command]` | Execute shell command |
| `.restart` | `.restart` | Restart userbot |
| `.update` | `.update` | Update userbot |
| `.logs` | `.logs` | Get bot logs |
| `.sysinfo` | `.sysinfo` | System information |
| `.speedtest` | `.speedtest` | Network speed test |
| `.pingall` | `.pingall` | Ping all group members |
| `.broadcast` | `.broadcast [message]` | Broadcast message |
| `.cleanup` | `.cleanup` | Clean temporary files |
| `.debug` | `.debug [on/off]` | Toggle debug mode |

### 📱 Custom Addons Commands (6)
| Command | Usage | Description |
|---------|-------|-------------|
| `.addon` | `.addon [name]` | Load custom addon |
| `.addons` | `.addons` | List available addons |
| `.createaddon` | `.createaddon [name]` | Create new addon |
| `.editaddon` | `.editaddon [name]` | Edit existing addon |
| `.deleteaddon` | `.deleteaddon [name]` | Delete addon |
| `.reloadaddons` | `.reloadaddons` | Reload all addons |

**Total: 120+ Commands across 11 categories**

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Telegram API credentials
- Unsplash API key (optional, for image features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devgaganin/ultra-userbot.git
   cd ultra-userbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Edit `config.py` with your credentials:
   ```python
   # Telegram API Configuration
   API_ID = "your_api_id"
   API_HASH = "your_api_hash"
   SESSION_STRING = "your_session_string"
   
   # Optional: Unsplash API Key
   UNSPLASH_KEY = "your_unsplash_key"
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

### Getting Session String

You can get your session string using various methods:
- [Pyrogram Session String Generator](https://replit.com/@SpEcHiDe/GenerateStringSession)
- [Telegram Web Session](https://my.telegram.org/auth)

## 📖 Usage

### Basic Commands
```
.help                    # Show main help menu
.help [category]         # Show specific category commands
.help admin             # Show administration commands
.help all               # Show all commands in separate messages
```

### Example Commands
```
.ban @username          # Ban a user
.save                   # Save replied media
.tr en Hello           # Translate to English
.joke                  # Get a random joke
.calc 2+2              # Calculator
.weather London        # Get weather info
.remind 1h Meeting     # Set reminder
.quote                 # Random quote
```

## 🔧 Configuration

### Environment Variables
Create a `config.py` file with the following variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Telegram API ID from my.telegram.org | Yes |
| `API_HASH` | Telegram API Hash from my.telegram.org | Yes |
| `SESSION_STRING` | Pyrogram session string | Yes |
| `UNSPLASH_KEY` | Unsplash API key for image features | No |

### Custom Configuration
- Modify command prefixes in main code
- Add custom commands in the addons system
- Configure auto-replies and filters
- Set up custom menus and aliases

## 🏗️ Project Structure

```
ultra-userbot/
├── main.py              # Single file containing all bot functionality
├── config.py            # Configuration file
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

**Note**: This is an advanced standalone userbot - everything is contained in a single `main.py` file for simplicity and portability.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Areas for Contribution
- 🔌 **Raw API Usage** - Implement more Telegram Bot API features
- 🆕 **New Features** - Add new commands and functionality
- 🐛 **Bug Fixes** - Report and fix issues
- 📚 **Documentation** - Improve docs and examples
- 🧪 **Testing** - Help test new features and updates
- 🔄 **Module Updates** - Keep dependencies updated

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add proper error handling
- Include docstrings for new functions
- Test your changes thoroughly
- Update documentation if needed

## 📝 Module Updates Needed

This project needs updates in the following areas:

- [ ] **Raw API Integration** - More direct Telegram API usage
- [ ] **Async Optimization** - Better async/await implementation  
- [ ] **Database Integration** - SQLite/MongoDB support
- [ ] **Plugin System** - Enhanced addon architecture
- [ ] **Error Handling** - Comprehensive exception management
- [ ] **Logging System** - Better logging and debugging
- [ ] **Security Features** - Enhanced privacy and security
- [ ] **Performance** - Optimization and caching
- [ ] **UI/UX** - Better command interfaces
- [ ] **Documentation** - More examples and tutorials

## 🧪 Tested Version

- **Python**: 3.8, 3.9, 3.10, 3.11
- **Pyrogram**: 2.0+
- **Platform**: Linux, Windows, macOS
- **Telegram**: Latest stable version

## ⚠️ Disclaimer

- This is a **standalone userbot project** for personal use
- Use at your own risk and responsibility
- Follow Telegram's Terms of Service
- Not affiliated with Telegram
- Educational purposes only

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Developer**: [@devgaganin](https://github.com/devgaganin)
- **Telegram**: [@devgaganin](https://t.me/devgaganin)
- **Issues**: [Report Issues](https://github.com/devgaganin/tele-userbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/devgaganin/tele-userbot/discussions)

## 🌟 Support

If you find this project helpful, please:
- ⭐ Star the repository
- 🍴 Fork and contribute
- 📢 Share with others
- 🐛 Report issues
- 💡 Suggest new features

---

<div align="center">

**Made with ❤️ by [devgaganin](https://github.com/devgaganin)**

**[⬆ Back to Top](#-tele-userbot)**

</div>
