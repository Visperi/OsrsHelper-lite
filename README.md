# OsrsHelper lite
Yet one more repository for OsrsHelper bots, I swear this is the last one. This project will deprecate both 
[OsrsHelper-rewrite](https://github.com/Visperi/OsrsHelper-rewrite) and 
[OsrsHelper](https://github.com/Visperi/OsrsHelper) as soon as this one has the most essential commands available.

The aim of this project is to make it easy to control the commands. This is achieved by implementing modular structure 
for the bot commands by using cogs (extensions in discord.py syntax).


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


## Modular? What does it mean
In this project the modular means that any family of bot commands (sorted into cogs) can be enabled or disabled on the 
go, or even completely removed without any impact on the bot! New families of commands can easily be developed and 
added by any user, as long as they follow the common cog layout.


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
