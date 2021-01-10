# OsrsHelper lite
Yet one more repository for OsrsHelper bots, I swear this is the last one. This project will deprecate both 
[OsrsHelper](https://github.com/Visperi/OsrsHelper) and 
[OsrsHelper-rewrite](https://github.com/Visperi/OsrsHelper-rewrite) 
as soon as this one has the most essential commands available. For more detailed reasoning for this, see 
section [Why more repositories](#Why-more-repositories?).

One of the main objectives of this project is to make it easier to control the commands. 
This is achieved by implementing modular structure for the bot commands by using cogs (extensions in discord.py syntax).
This feature makes it easy to extend the bot without need to touch its underlying code, or delete existing commands.


## About modularity
In this project the term modular means that any family of bot commands (sorted into cogs) can be enabled or disabled 
on the go, or even completely removed without any impact on the bot! New families of commands can easily be developed 
and added by anyone, as long as they follow the common cog structure. No fear of breaking the whole bot since 
the commands are isolated into their respective cogs!


## Setup
#### Requirements
| Software/Library        | Version | Documentation                                                  |
|:-----------------------:|:-------:|:--------------------------------------------------------------:|
| Python                  | 3.6+    | [Link](https://docs.python.org/3.6/)                           |
| discord.py              | 1.6+    | [Link](https://discordpy.readthedocs.io/en/stable/)            |
| aiohttp                 | 3.6.3+  | [Link](https://docs.aiohttp.org/en/stable/)                    |
| mathparse               | 0.1.5+  | [Link](https://github.com/gunthercox/mathparse)                |
| pytz                    | 2020.5+ | [Link](https://pypi.org/project/pytz/)                         |
| dateutil                | 2.7.2+  | [Link](https://dateutil.readthedocs.io/en/stable)              |
| BeautifulSoup           | 4.9.3+  | [Link](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| numpy                   | TBA     | [Link](https://numpy.org/doc/stable/)                          |
| tabulate                | TBA     | [Link](https://pypi.org/project/tabulate/)                     |

Since there is currently no any public invitation link, following steps are also needed:
1. Create a Discord app for the bot in their [Developer portal](https://discord.com/developers/applications)
2. Enable following intents in the bot settings in developer portal
    1. Presence intent
    2. Members intent
3. Set your Discord API keys in file `Data files/credentials.json`
    1. Remember to provide the right `EBotVersion` in the bottom line of `main.py`

When you meet the requirements and the API keys are set, start the bot by running `main.py`. 
This will initialize the bot and load all cogs in directory `cogs`. The bot should appear online in Discord and be 
ready to process commands.


## Managing cogs
Managing cogs through the bot commands happens with following command:
`!extension <operation> <cog_name>` (command prefix can vary from default settings)

`<cog_name>` is dot separated name of the cog like in regular Python imports. Currently it is supported to leave the 
ending `_cog` out from the name. For example cog `discord_cog.py` can be loaded with commands  
`!extension load cogs.discord_cog` and `!extension load cogs.discord`. 

`<operation>` is one of the following operations:
- `load`  Loads an extension
[docs](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=extension#discord.ext.commands.Bot.load_extension)
- `unload` Unloads an extension
[docs](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=extension#discord.ext.commands.Bot.unload_extension)
- `reload` Atomically reloads an extension. Equivalent of calling `unload` and then `load`
[docs](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=extension#discord.ext.commands.Bot.reload_extension)

These operations makes it possible to update cogs on the go, without a need to restart the whole bot every time.

### Enabling new cogs
**Remember to end the cog file name with `_cog.py` so it can be recognized as one**
1. Implement a new cog
2. Place it in directory `cogs` if automatic load is wanted on bot startup
3. Load the cog if bot is already running
### Disabling existing cogs
1. Unload the cog
2. Delete the cog file if not needed in the future

## Current status
- Basic layout and functionality **Done**
- Caching available for commands **TBD**
- Extension reloading on the go  **Done**
- Cog functionality
    - discord cog       **Started**
    - error handler cog **TBD**
    - fin exclusive cog **Done**
    - help cog          **TBD**
    - maintenance cog   **Basics done**
    - osrs cog          **TBD**


## Why more repositories?
After realising the OsrsHelper-rewrite and its MySQL database require too much effort compared to what are the actual 
needs of this scale project, I completely lost my motivation into developing that version. When I tried to get back 
into it, I started noticing more different kinds of flaws in the project design that I didn't like.

In the last months and years the Discord API and [discord.py](https://discordpy.readthedocs.io/en/latest/) have had 
rather big and meaningful updates. Many times I have noticed that developing OsrsHelper with very old discord.py 
(more than 3 years old!) has started encountering more and more often functional problems, and developing any 
new features is a pretty far-fetched dream.

All this lead into a decision to yet again start the bot from scratch, this time with no excessive scalability with 
relational database nor other things that only adds maintaining effort with no actual benefits.


## Licence
MIT License

Full licence: [LICENCE](/LICENCE)
