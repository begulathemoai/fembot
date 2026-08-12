# The cutest discord bot

will do a lot of more or less cool stuff (when everything from the second version will have been reimplemented) like :
- [ ] personal channels
- [x] music playback in VCs (kinda bad tho) with a (bad) playlist system
- [ ] downloading from yt and other platforms with the goat yt-dlp
- [ ] timeouts limited to a singular channel
- [x] replying to random and not-so-random messages without being mentionned(can be disabled)
- [x] chatgpt but better :pray:
- [x] replying with random copypastas to the word "kirk"
- [ ] message aliasing (you specify an alias and a message and when that alias is input the bot sends the message) (NEW)
- [x] allowing you (yes, YOU) to larp as a dev
- [x] randomly error out
- [ ] get you "banned" from YT cuz ain't no way i'm implementing PO token bullshit for a shitpost bot
- [x] not have an automatic system to clear the cache
- [ ] allow you to become one of its fans
- [ ] wack it
- [x] garmin support (members with no perms can timeout someone else for a minute, can be disabled but is funny)
- [ ] youtube search
- [ ] have 1000 loc in the main file (no that was the second ver)
- [x] use a sqlite database to store guild settings
- [x] allow you to ban users from it
- [x] allow them to say "i've been banned from fembot™ :bangbang:"
- [x] do bad jokes in french
- [x] bully people for not removing tracking from yt links


this is the third ~~rewrite~~ version of fembot <br>
the first was in JS (ew)<br>
the second was in python but was *bad*<br>
this one is in python and is *less bad*

this is my own bad code, no ai was used (tho the ruff linter saved my ass multiple times) (more like tuff linter)
<br><br><br><br><br><br><br>
this may come as a surprise to many but this bot is currently french<br>
i'll add translation strings & an english translation later (famous last words)<br>
also this program is linux only (more like everything other than windows only) cuz i use env vars & directories that only exist on linux (`$XDG_DATA_HOME`)<br>

# Setup
1. Make sure you have the `uv` package manager installed
2. Clone this repo
3. Open the root folder of the repo
4. Run `uv sync`
5. Input your discord token through `FEM_BOT_TOKEN` by using an .env file in the project root
6. Start fembot with `uv run fembot`
7. ???
8. Profit

## Config options
All global config is done through env vars, passed either when launching the script <br>
 or through an `.env` file placed in the project root (or where you plan to be running the script).<br><br>
`FEM_BOT_TOKEN` - Self explanatory : your bot's token.<br>
`TEST_SERVER_ID` - If defined, and different from -1, fembot will only operate in this guild.<br>
`OWNER_ID` - The user id of the bot's owner (grants the highest available permissions).<br>
`BOT_BANNED_USERS` - A colon-separated list of all of the ids of users banned from the bot.<br>
`GUILD_WHITELIST` - A colon-separated list of all of the ids of guilds fembot is allowed to operate in.<br>
