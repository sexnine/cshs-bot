Discord bot for the r/cshighschoolers Discord Server :)

[![CodeFactor](https://www.codefactor.io/repository/github/sexnine/cshs-bot/badge)](https://www.codefactor.io/repository/github/sexnine/cshs-bot)

### Made using
![Python](https://img.shields.io/badge/-Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-white?style=for-the-badge&logo=docker)
![MongoDB](https://img.shields.io/badge/-MongoDB-10aa50?style=for-the-badge&logo=mongodb&logoColor=white)
![Pycord](https://img.shields.io/badge/-Pycord-5865f2?style=for-the-badge&logo=discord&logoColor=white)
...and loss of sleep

## Development
Make sure you have Python 3.10 installed, also would be good to have both Docker and docker-compose.

### Setting up
- Make a new venv and install all the required packages with `pip install -r requirements.txt`
- Follow the example in the `bot.env` file and set those environment variables (not in the file, like actual envs)
- Make a copy of the example config files (in `config/examples`) into the `config/` directory and fill in the fields for any of the cogs you will be using

### Testing
I would recommend running the python code in your env and having only the MongoDB service running while you develop.

#### Enabling only the MongoDB instance for testing
Copy `.example.env` to `.env` and change any of the fields if you wish. 

To start it: `docker-compose -f docker-compose.dev.yml up mongo`

To stop it: `docker-compose -f docker-compose.dev.yml down mongo`

#### Using docker for both the bot and MongoDB
Copy `.example.env` to `.env` and change any of the fields if you wish. 

Copy `bot.example.env` to `bot.env` and fill in the required fields.

To start them: `docker-compose -f docker-compose.dev.yml up --build`

To stop them: `docker-compose -f docker-compose.dev.yml down`

#### Without docker
You're by yourself on this one.  If you don't want to use Docker, you'll just have to 
either install it manually or use a cloud service for testing.

## Deployment

### Deploying with Docker
The cshs-bot docker image is available at `ghcr.io/sexnine/cshs-bot`.

You need to have a MongoDB instance setup for the bot to work.
I would recommend using the official [mongo docker image](https://hub.docker.com/_/mongo).

After you set up the MongoDB instance, you can actually run the bot.  
Make sure to set all the environment variables needed (see `bot.example.env` for an example) and
bind `/app/config` to a directory on your host system to lot lose any data.

#### An example run command
```shell
docker run ghcr.io/sexnine/cshs-bot:latest \
 -e DISCORD_TOKEN=ODk0ODQzNz00ODA4MzY2NTky.YVv6LA.UtT44GEnbk9qukTL5UtDVrcoYZw \
 -e MONGO_URI=mongodb://username:password@localhost:27017/ \
 -e DB_NAME=bot \
 -v ./config:/app/config
```

### After deploying
The owner of the bot will be able to remotely adjust the config of the bot.  You can add other owners, change what cogs get loaded on startup, prefixes and more.

DM the bot `-help config` for help.

⚠ Currently, the bot will not load any more modules (cogs) when you edit the config.
For these changes to be applied, you will have to restart the bot.