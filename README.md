# Website Uptime Notifier Bot
## Бот для оповещения о работоспособности веб-сайта
Bot can be accessed at: @web_uptime_notifier_bot

- This is code for a telegram bot, which notifies its users when the website they are monitoring is down. Each user can add up to 5 website URL's. 
- The bot sends requests to each of URLs every 10s and notifies the user if the response code is not 200. 

- The bot is deployed on Railway
## commands
- /start: to start the bot
- /add <URL>: to add the website to monitoring list
- /delete <URL>: to delete the website from monitoring list
- /list: to get a list of all URLs currently monitored
