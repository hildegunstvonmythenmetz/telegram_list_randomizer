## List Randomizer Telegram Bot

You can use this bot to shuffle a list or to pick a random item from the list. It works automatically, no need to add it anywhere. Simple type the bots name ... in any chat followed by the list. The items should be seperated by spaces. Then choose if you want to shuffle the list or pick an item from it.
 
### Deployment

The bot gets automatically deployed to heroku.

### Run the bot locally

In order for the bot to be able to run the 'LIST_RANDOMIZER_TOKEN' environment var must be set to a valid api key. The corresponding bot should be in ininline mode. 

 - `git clone https://github.com/hildegunstvonmythenmetz/telegram_list_randomizer`
 - `cd telegram_list_randomizer`
 - `pip install -r requirements.txt`
 - `python bot.py`

### Features
 
 - Shuffle a list
 - Pick a random element from a list
