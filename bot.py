import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import aiosqlite
import re
import asyncio

# Create the bot
intents = discord.Intents.default()
intents.message_content = True  # Make sure the necessary intents are enabled

bot = commands.Bot(command_prefix='/', intents=intents)


# Function to parse a time string like "2d 4h 5m 30s"
def parse_time_string(time_string):
    time_regex = re.compile(r'(?:(\d+)d)?\s*(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?')
    match = time_regex.match(time_string)
    if not match:
        raise ValueError(
            "Invalid time format. Use the format: `Xd Xh Xm Xs` where X is a number. Example: `2d 4h 5m 30s`.")

    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0

    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


# Function to parse a date string like "DD/MM/YY" or "DD/MM/YYYY" with optional time
def parse_date_string(date_string):
    try:
        # Try parsing with full date and time (DD/MM/YYYY HH:MM)
        return datetime.strptime(date_string, "%d/%m/%Y %H:%M")
    except ValueError:
        try:
            # Try parsing with short year and time (DD/MM/YY HH:MM)
            return datetime.strptime(date_string, "%d/%m/%y %H:%M")
        except ValueError:
            try:
                # Try parsing with full date and no time (DD/MM/YYYY) and set time to 00:00 by default
                return datetime.strptime(date_string, "%d/%m/%Y")
            except ValueError:
                try:
                    # Try parsing with short year and no time (DD/MM/YY) and set time to 00:00 by default
                    return datetime.strptime(date_string, "%d/%m/%y")
                except ValueError:
                    raise ValueError(
                        "Invalid date format. Use `DD/MM/YY`, `DD/MM/YYYY`, or add time like `DD/MM/YYYY HH:MM` or `DD/MM/YY HH:MM`.")


# Create SQLite database for reminders
async def init_db():
    async with aiosqlite.connect("reminders.db") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS reminders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            channel_id INTEGER,
                            reminder_time TIMESTAMP,
                            message TEXT
                            )''')
        await db.commit()


@bot.event
async def on_ready():
    await init_db()
    check_reminders.start()
    print(f"Logged in as {bot.user}")


# Function to check if a string is in the format HH:MM (valid time)
def is_time_format(string):
    time_regex = re.compile(r'^\d{2}:\d{2}$')
    return bool(time_regex.match(string))


# Command to set a reminder
@bot.command(name="Remembrall")
async def remembrall(ctx, mode: str = None, *, message_input: str = None):
    if not mode or not message_input:
        await ctx.send("Missing arguments. Correct usage:\n"
                       "`/Remembrall in [time] [message]` where [time] is in the format `Xd Xh Xm Xs` (example: `2d 4h 5m 30s`).\n"
                       "`/Remembrall on [DD/MM/YY] [message]` or with optional time `DD/MM/YYYY HH:MM` or `DD/MM/YY HH:MM`.")
        return

    try:
        if mode == "in":
            time_input, message = message_input.split(' ', 1)
            delta = parse_time_string(time_input)
            reminder_time = datetime.now() + delta

        elif mode == "on":
            # Split the input into parts
            parts = message_input.split(' ')
            time_input = parts[0]  # First part is the date
            message = ' '.join(parts[1:])  # The rest is the message

            # Check if the second part is a time (HH:MM)
            if len(parts) > 1 and is_time_format(parts[1]):
                time_input += f" {parts[1]}"  # Add the time to the date
                message = ' '.join(parts[2:])  # Adjust the message

            else:
                time_input += " 00:00"  # No time provided, default to 00:00

            reminder_time = parse_date_string(time_input)

        else:
            raise ValueError("Invalid mode. Use `in` for durations or `on` for dates.")

        # Save the reminder to the database
        async with aiosqlite.connect("reminders.db") as db:
            await db.execute('''INSERT INTO reminders (user_id, channel_id, reminder_time, message) 
                                VALUES (?, ?, ?, ?)''', (ctx.author.id, ctx.channel.id, reminder_time, message))
            await db.commit()

        await ctx.send(f"Reminder set for {reminder_time}. You will receive a DM.")

    except ValueError as e:
        await ctx.send(f"Error: {str(e)}\n\nCorrect usage:\n"
                       "- `/Remembrall in [time] [message]` where [time] is in the format `Xd Xh Xm Xs` (example: `2d 4h 5m 30s`).\n"
                       "- `/Remembrall on [DD/MM/YY] [message]` or with optional time `DD/MM/YYYY HH:MM` or `DD/MM/YY HH:MM`.")


# Function to check reminders periodically and send messages
@tasks.loop(seconds=60)
async def check_reminders():
    now = datetime.now()
    async with aiosqlite.connect("reminders.db") as db:
        async with db.execute(
                "SELECT id, user_id, channel_id, reminder_time, message FROM reminders WHERE reminder_time <= ?",
                (now,)) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                reminder_id, user_id, channel_id, reminder_time, message = row
                user = await bot.fetch_user(user_id)
                await user.send(f"Reminder: {message}")

                # Delete the reminder after it has been sent
                await db.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
                await db.commit()


# Run the bot with your token
bot.run("Your_token")
