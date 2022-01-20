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

To start them: `docker-compose -f docker-compose.dev.yml up`

To stop them: `docker-compose -f docker-compose.dev.yml down`

#### Without docker
You're by yourself on this one.  If you don't want to use Docker, you'll just have to either install it manually or use a cloud service for testing.

## Deployment
TBD