# OsrsHelper lite
Yet one more repository for OsrsHelper bots, I swear this is the last one. This project will deprecate both 
[OsrsHelper](https://github.com/Visperi/OsrsHelper) and 
[OsrsHelper-rewrite](https://github.com/Visperi/OsrsHelper-rewrite) 
and  as soon as this one has the most essential commands available.

One of the main objectives of this project is to make it easier to control the commands. 
This is achieved by implementing modular structure for the bot commands by using cogs (extensions in discord.py syntax).
This feature makes it easy to extend the bot without need to touch its underlying code, or delete existing commands.


## About modularity
In this project the term modular means that any family of bot commands (sorted into cogs) can be enabled or disabled 
on the go, or even completely removed without any impact on the bot! New families of commands can easily be developed 
and added by anyone, as long as they follow the common cog structure. No fear of breaking the whole bot since 
the commands are isolated in their respective cogs!


## Managing cogs
Managing cogs through the bot commands happens with following command:
`!extension <operation> <cog_namespace>`

Where `<operation>` is one of the following operations:
- `reload`
- `load`
- `unload`

### Enabling new cogs
**Remember to end the cog file name with `_cog.py`**
### Disabling existing cogs

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
    

## Setup
#### Requirements
| Software/Library        | Version |
|:-----------------------:|:-------:|
| Python                  | 3.6+    |
| discord.py              | 1.5.1+  |
| aiohttp                 | 3.6.3+  |
| BeautifulSoup           | 4       |
| numpy                   | any     |
| tabulate                | xxxxx   |

Since there is currently no any public invitation link, following steps are also needed:
1. Create a Discord app for the bot in their [Developer portal](https://discord.com/developers/applications)
2. Enable following intents in the bot settings in developer portal
    1. Presence intent
    2. Members intent
3. Set your Discord API keys in file `Data files/credentials.json`

When you meet the requirements and the API keys are set, the bot can be started by running `main.py`. 
This will initialize the bot and load all cogs in directory `cogs`. The bot should appear online in Discord and is 
ready to process commands.


## Why more repositories?
After realising the OsrsHelper-rewrite and MySQL database it needs had way too much work compared to what are the actual 
needs of this scale project, I completely lost my motivation into developing that project. When I tried to get back 
into it, I started noticing more and more different kinds of flaws in the project design that I didn't like.

In the last months and years the Discord API and [discord.py](https://discordpy.readthedocs.io/en/latest/) have had 
rather big and meaningful updates. Many times I have noticed that developing OsrsHelper with very old discord.py 
(more than 3 years old!) has started encountering more and more often functional problems, and developing any 
new features is a pretty far-fetched dream.

All this lead into a decision to yet again start the bot from scratch, this time with no excessive scalability with 
relational database nor other things that only add amount of work with no actual benefits.


## Licence
MIT License

Full licence: [LICENCE](/LICENCE)
