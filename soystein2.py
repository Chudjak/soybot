import discord
from discord import app_commands
import asyncio
import datetime
import os
import random
import sys
import requests
import re
import difflib
from bs4 import BeautifulSoup
from io import BytesIO
import random
import json
soy_spam_prevention = datetime.datetime.now() - datetime.timedelta(seconds=30)
soy_random_spam = datetime.datetime.now() - datetime.timedelta(seconds=7)
messages = []
dictionary = {}



# Set the bot token
TOKEN = open("token.txt", "r").readline()

# Create a Discord client with the required intents
intents = discord.Intents.all()
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await tree.sync(guild=discord.Object(id=672761536477134860))
    print("Command tree LOADED!")
    print('------')
    
@tree.command(name = "taggedsoy", description = "Got a specific gem in mind?", guild=discord.Object(id=672761536477134860))
async def first_command(interaction, tag: str):
    global soy_spam_prevention
    current_time = datetime.datetime.now()
    if current_time < soy_spam_prevention + datetime.timedelta(seconds=30):
        await interaction.response.send_message('No spam, darlings.')
        return
    soy_spam_prevention = datetime.datetime.now()
    response = requests.get('https://booru.soy/random_image/view/' + tag)
    soup = BeautifulSoup(response.text, 'html.parser')
    # find the image URL in the HTML
    print('the tag is ' + tag)
    source_element = soup.find('source', {'type': ['video/mp4','video/webm']})
    if source_element is not None:
        image_url = soup.find('source', {'type': ['video/mp4','video/webm']})['src']
    else: 
        image_url = soup.find('img', {'id': 'main_image'})['src']
        
    # fix the url
    image_url = 'https://booru.soy' + image_url
    print('the fixed image url is ' + image_url)
    
    if image_url:
        await interaction.response.send_message('Here is your '+tag+random.choice([' gem!',' coal!',' dust!',' diamond!']))
        await interaction.channel.send(image_url)
    
@tree.command(name = "help", description = "I fucking hate you.", guild=discord.Object(id=672761536477134860))
async def first_command(interaction):
    await interaction.response.send_message(random.choice(['No gems for troons.', 'The Sommunity (Soy Community) is a term that broadly refers to those involved in the wider soyjak culture. ', 'Soyjak.party, also known as The Party, the \'Party, the \'arty, soy spinoff, soyfag.sharty, soyshart.farty, the \'sharty, and countless other names is an imageboard primarily dedicated to datamining.', 'I know where you live.', 'The Five Board Plan was a major restructuring of soyjak.party boards that occurred on 11th November, 2022 under a policy of board consolidation, with further reforms delievered over the next two days.']))
    
@tree.command(name = "mute", description = "Duckman posting ponies again? Don't you worry.", guild=discord.Object(id=672761536477134860)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction, target: discord.Member, time: int):
    '''# Check if the user has the required role
    if interaction.user.id == 1040033235075346543:  # replace with the user's ID
        await interaction.response.send_message("Matrixlets seething over pythonchads.")
        return matrix bots can't use slash commands afaik'''
    user = interaction.user
    if user.guild_permissions.manage_roles:
        # Get the mute duration
        mute_duration = time

        # Get the mute role
        mute_role = discord.utils.get(target.guild.roles, name='Omega Faggot')

        # Add the mute role to the user
        await target.add_roles(mute_role)
        
        # Record the start time of the mute
        mute_start_time = datetime.datetime.now()

        # Send a confirmation message
        with open('ADMIN ABUSE.ogg', 'rb') as f:
            await interaction.response.send_message(f'{target.mention} was muted for {mute_duration} {"minutes" if mute_duration > 1 else "minute"}!', file=discord.File(f))
        # Display information about the mute in the console
        if mute_duration == 1:
            print(f'{target.name} was muted by {user.name} for {mute_duration} minute')
        else:
            print(f'{target.name} was muted by {user.name} for {mute_duration} minutes')
        
        # Check if the duration of the mute has passed
        while True:
            # Get the current time
            current_time = datetime.datetime.now()

            # Check if the current time is greater than the start time plus the duration of the mute
            if current_time > mute_start_time + datetime.timedelta(minutes=mute_duration):
                # Remove the mute role from the user
                await target.remove_roles(mute_role)

                # Send a notification message
                await interaction.channel.send(f'{target.mention} has been FREED.')

                # Display information about the unmute in the console
                print(f'{target.name} was FREED after {mute_duration} {"minutes" if mute_duration > 1 else "minute"}!')

                # Break out of the loop
                break
            # Sleep for 1 minute
            await asyncio.sleep(60)
    else:
        # The user does not have the required role, send an error message
        await interaction.response.send_message('HWNBAG.')

@tree.command(name = "markov", description = "We miss you mommi", guild=discord.Object(id=672761536477134860)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    def generate_markov_chain(num_words):
        # Load the dictionary from the JSON file
        with open("dictionary.json", "r") as f:
            word_counts = json.load(f)

        # Generate a list of tuples containing the words and their probabilities
        word_probs = []
        for word, count in word_counts.items():
            total = 0
            for value in count.values():
                total += value
            word_probs.append((word, total / sum(word_counts["counts"].values())))

        # Generate a random starting word
        trve = random.choices(list(word_counts["counts"]), weights=list(word_counts["counts"].values()))[0]
        trve = trve.capitalize()
        chain = [trve]

        # Generate the rest of the chain
        for i in range(num_words):
            next_words = word_counts
            total_count = sum(next_words["counts"].values())
            rand = random.uniform(0, total_count)
            for next_word, count in next_words["counts"].items():
                if rand < count:
                    break
                rand -= count
            chain.append(next_word)
            word = next_word

        # Return the resulting chain
        chain_real = ' '.join(chain)
        return chain_real
    chain_length = random.randint(2, 25)
    markov_chain = generate_markov_chain(chain_length)
    await interaction.response.send_message(markov_chain)

@tree.command(name = "soy", description = "Peruse some gems.", guild=discord.Object(id=672761536477134860)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    if interaction.channel.id == 1040031774803230720:
        return
    global soy_random_spam
    current_time = datetime.datetime.now()
    if current_time < soy_random_spam + datetime.timedelta(seconds=7):
        await interaction.response.send_message('No spam, darlings.')
        return
    soy_random_spam = datetime.datetime.now()
    # send a request to the "Random" button URL and parse the HTML
    response = requests.get('https://booru.soy/random_image/view')
    soup = BeautifulSoup(response.text, 'html.parser')
    # find the image URL in the HTML
    try:
        image_url = soup.find('img', {'id': 'main_image'})['src']
    except:
        await interaction.response.send_message("It's over...")
    image_url = soup.find('img', {'id': 'main_image'})['src']
    # fix the url
    image_url = 'https://booru.soy' + image_url
    if image_url:
        # get the image's extension
        _, extension = os.path.splitext(image_url)
        # send the image to the Discord channel
        response = requests.get(image_url)
        file = discord.File(fp=BytesIO(response.content), filename='image' + extension)
        await interaction.response.send_message(f'Prediction: {random.choice(["NAS","IAS","Coal","Gem","Dust","Brimstone","Gemerald","I look like this","Literally me","Gemmish"])}', file=file)

@client.event
async def on_message(message):
    if message.content.startswith('!restart'):
        if message.author.id == 1040033235075346543:  # replace with the user's ID
            await message.channel.send("Matrixlets seething over pythonchads.")
            return
        if 'Admin' in [role.name for role in message.author.roles]:
            await message.channel.send('Restarting...')
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            # The user does not have the required role, send an error message
            await message.channel.send('HWNBAG.')
    if message.content == '!help':
        await message.channel.send("My commands are !mute, !soy and !restart.")
    # Add the message to a list of messages
    message_str = str(message.content)
    def preprocess_text(text):
        words = re.findall(r"\b[^\W\d_]+\b", text)

        # Create an empty dictionary to store the word counts
        word_counts = {}

        # Iterate over the words and update the word counts
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        return word_counts
    def save_to_file(array_item):
        with open("dictionary.json", "r") as f:
            # Check if the array itself exists
            file_contents = f.read()
            if not file_contents:
                data = {}
            else:
                # If the file is not empty, load the contents into a dictionary
                data = json.loads(file_contents)
            if "counts" not in data:
                # If the key does not exist, create it and set it to an empty dictionary
                data["counts"] = {}
            # Get the current counts dictionary
            counts = data["counts"]
            # Iterate over the words in the message
            for word in array_item:
                # Increment the count for the word
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
            # Open the JSON file for writing
            with open("dictionary.json", "w") as f:
                # Write the modified contents to the file
                json.dump(data, f)
    dictionary = preprocess_text(message_str)
    save_to_file(dictionary)
    def generate_markov_chain(num_words):
        # Load the dictionary from the JSON file
        with open("dictionary.json", "r") as f:
            word_counts = json.load(f)

        # Generate a list of tuples containing the words and their probabilities
        word_probs = []
        for word, count in word_counts.items():
            total = 0
            for value in count.values():
                total += value
            word_probs.append((word, total / sum(word_counts["counts"].values())))

        # Generate a random starting word
        trve = random.choices(list(word_counts["counts"]), weights=list(word_counts["counts"].values()))[0]
        trve = trve.capitalize()
        chain = [trve]

        # Generate the rest of the chain
        for i in range(num_words):
            next_words = word_counts
            total_count = sum(next_words["counts"].values())
            rand = random.uniform(0, total_count)
            for next_word, count in next_words["counts"].items():
                if rand < count:
                    break
                rand -= count
            chain.append(next_word)
            word = next_word

        # Return the resulting chain
        chain_real = ' '.join(chain)
        return chain_real
# Start the Discord bot
client.run(TOKEN)


# Run the event loop indefinitely
while True:
    try:
        asyncio.run(client.start(TOKEN))
    except Exception as e:
        print(e)