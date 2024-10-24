# Discord Remembrall Bot

This is a Discord bot that allows users to set reminders. You can set reminders either relative to the current time (e.g., in 2 days, 4 hours), or at a specific date and time.

## Features

- **Relative time reminders** (e.g., `/Remembrall in 2d 4h 5m 30s "Appointment with dentist"`)
- **Specific date reminders** (e.g., `/Remembrall on 25/10/2024 14:30 "Meeting with client"`)
- Reminders are stored in a SQLite database (`reminders.db`), and the data is persisted using Docker volumes.

## Add it to your server :

[Click here](https://short.silverspy.fr/Remembrall)

## Prerequisites

- You need a [Discord bot token](https://discord.com/developers/applications). Follow the instructions below to obtain it.
- Install [Docker](https://www.docker.com/get-started) and optionally [Docker Compose](https://docs.docker.com/compose/install/).

## Obtaining a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on **New Application** and give your application a name.
3. Under the **Bot** section, click **Add Bot**.
4. Reveal the **Token** and copy it. This token will be used to run your bot.

> **Important**: Keep your token secure. Never share it publicly. If it's exposed, you can regenerate it from the Developer Portal.

## Docker Installation

1. **Clone this repository**:

   ```bash
   git clone https://github.com/your-repo/discord-remembrall-bot.git
   cd discord-remembrall-bot
   ```

   Make sure to replace `your_discord_bot_token_here` in docker-compose with the actual bot token you obtained from the Discord Developer Portal.

3. **Build and run the bot using Docker Compose**:

   If you have Docker Compose installed, run the following command to build and start the bot:

   ```bash
   docker-compose up -d
   ```

   This command will:
   - Build the Docker image for the bot.
   - Start the bot in a container with the `reminders.db` persisted in the `data` folder.

4. **Check the logs** to make sure the bot is running correctly:

   ```bash
   docker logs discord-bot
   ```

5. **Stop the bot**:

   To stop the bot, run the following command:

   ```bash
   docker-compose down
   ```

## Usage

Once the bot is running, you can use the following commands:

- **Set a reminder relative to the current time**:
  ```
  /Remembrall in 2d 4h 5m 30s "Appointment with dentist"
  ```

- **Set a reminder for a specific date and time**:
  ```
  /Remembrall on 25/10/2024 14:30 "Meeting with client"
  ```

## Notes

- The bot stores all reminders in `reminders.db`, and this database is persisted using Docker volumes.
- The bot's time zone is hardcoded to **Europe/Paris**. All reminders will be processed in this time zone. (Need to fix)
