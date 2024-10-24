# Remembrall Discord Bot

The **Remembrall Discord Bot** is a simple bot that allows users to set reminders using Discord commands. Users can set reminders either by specifying a duration (`/Remembrall in`) or by specifying a particular date and time (`/Remembrall on`). Reminders are stored in a database, and the bot will send a direct message to the user when the reminder is due.

## Features

- **Set reminders by duration**: Use `/Remembrall in` to set reminders after a specific amount of time (e.g., in 2 days, 4 hours).
- **Set reminders by date and time**: Use `/Remembrall on` to set reminders for a specific date, with an optional time.
- **Persistent storage**: Reminders are stored in a SQLite database to ensure that they are not lost when the bot is restarted.

## Usage

### Commands

1. **/Remembrall in [time] [message]**
   - Set a reminder after a certain amount of time.
   - Format for `time`: `Xd Xh Xm Xs` where `X` is a number representing days, hours, minutes, and seconds.
   - Example:
     ```
     /Remembrall in 2d 4h 5m "Book dentist appointment"
     ```

2. **/Remembrall on [DD/MM/YY] [message]**
   - Set a reminder on a specific date. You can optionally include the time in `HH:MM` format.
   - If no time is provided, the bot will default to `00:00`.
   - Example:
     ```
     /Remembrall on 25/10/24 14:50 "Meeting with team"
     ```

   - Example if no time is provided:
     ```
     /Remembrall on 25/10/24 "Book dentist appointment"
     ```
