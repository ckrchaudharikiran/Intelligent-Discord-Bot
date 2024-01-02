
# Import necessary libraries
import discord  # Import Discord library
from discord.ext import commands  # Import commands extension from Discord library
import openai  # Import OpenAI library

# Replace with your Discord token
DISCORD_TOKEN = 'YOUR_DISCORD_TOKEN'

# Replace with your OpenAI API key
OPENAI_API_KEY = 'OPENAI_API_KEY'

# Set up the Discord bot with intents
intents = discord.Intents.default()  # Create a default instance of Discord Intents
intents.message_content = True  # Enable message content intent
intents.guilds = True  # Enable guilds intent
intents.members = True  # Enable members intent

# Create an instance of the bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Print a message when the bot is ready

# Event handler for processing messages
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself to prevent potential loops
    if message.author == bot.user:
        return  # Skip processing if the message is from the bot

    # Let the bot process commands
    await bot.process_commands(message)

# Command for asking a question using OpenAI GPT-3.5-turbo
@bot.command(name='ask')
async def ask_question(ctx, *, question):
    try:
        # Use OpenAI to get a response with the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # Set up system role message
                {"role": "user", "content": f"Question: {question}"},  # Set up user role message with the question
            ],
        )

        # Extract the message content
        response_content = response['choices'][0]['message']['content']

        # Send the response back to Discord
        for chunk in [response_content[i:i + 2000] for i in range(0, len(response_content), 2000)]:
            await ctx.send(chunk)  # Send the response in chunks to avoid exceeding Discord message limits

    except discord.errors.HTTPException as e:
        print(f"Failed to send message: {e}")  # Print an error message if sending the response fails

# Run the bot
bot.run(DISCORD_TOKEN)
