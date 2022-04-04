# This is the code for a Discord Bot designed to do various tasks on Discord and help you to fun the server

import os
import discord
import requests
from replit import db
import functions
import random

my_secret = os.environ["PASS"]
NinjaKey = db["NinjaKeyDB"]
client = discord.Client()

famous_quote_list = ['age', 'alone', 'amazing', 'anger'
'architecture', 'art', 'attitude', 'beauty'
'best', 'birthday', 'business', 'car'
'change', 'communications', 'computers', 'cool'
'courage', 'dad', 'dating', 'death'
'design', 'dreams', 'education', 'environmental'
'equality', 'experience', 'failure', 'faith'
'family', 'famous', 'fear', 'fitness'
'food', 'forgiveness', 'freedom', 'friendship'
'funny', 'future', 'god', 'good'
'government', 'graduation', 'great', 'happiness'
'health', 'history', 'home', 'hope'
'humor', 'imagination', 'inspirational', 'intelligence'
'jealousy', 'knowledge', 'leadership', 'learning'
'legal', 'life', 'love', 'marriage'
'medical', 'men', 'mom', 'money'
'morning', 'movies', 'success']

@client.event
async def on_ready():
  print("This bot logged in as {0.user}".format(client))



@client.event
async def on_message(message):
  global quote_type
  global famous_quote_list
  global NinjaKey

  if message.author == client.user:
    return
   
  if client.user.mentioned_in(message) and "@everyone" not in message.content:
    color = discord.Color.blue()
    await message.channel.send(embed=functions.embed(message, color, "Hello", "You mentioned me!\nI'm at ur service...\nType ./info or ./help for more info. Happing chatting.\n*BTW, I dont respond to @ everyone, so dont go pinging the whole server*"))
  
  text = message.content
  api_url = 'https://api.api-ninjas.com/v1/sentiment?text={}'.format(text)
  response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
  if response.status_code == requests.codes.ok:
    emotion = "{" + response.text[response.text.index("sentiment\": ") + 12:]
  else:
    print("Error:", response.status_code, response.text)
  if db["allow_sentiment"] == 1:
    if message.content.startswith(db["prefix"]) == False:
      if emotion == "{\"NEUTRAL\"}":
        pass
      elif emotion == "{\"WEAK_NEGATIVE\"}":
        await message.channel.send("Dont worry - It'll be fine.")
      elif emotion == "{\"NEGATIVE\"}":
        await message.channel.send("Calm down - your endagering the quietness of this server!")
      elif emotion == "{\"WEAK_POSITIVE\"}":
        await message.channel.send("Good for you!")
      elif emotion == "{\"POSITIVE\"}":
        await message.channel.send("Nice - way to go!")

  elif message.content.startswith(db["prefix"] + " ownerprint"):
    print(message.author)
    print(str(message.author))
  elif message.content.startswith(db["prefix"] + " rcash"):
    if "Banned" not in str(message.author.roles) and db["allow_talk"] == 1:
      if message.content.startswith(db["prefix"] + " rcash beg"):
        rgenerator = random.randint(0, 100)
        if rgenerator > 0 and rgenerator < 50:
          amount_given = 0
        elif rgenerator > 50 and rgenerator < 75:
          amount_given = 10
        elif rgenerator > 75 and rgenerator < 90:
          amount_given = 100
        elif rgenerator > 90 and rgenerator < 100:
          amount_given = 1000
        if functions.check_bal(str(message.author)) == False:
          functions.create_bal(str(message,author))
        amount_given = amount_given * functions.get_multiplier(str(message.author))
        functions.change_bal(str(message.author), "balance", functions.get_balance(str(message.author)) + amount_given)
        color = discord.Color.blue()
        await message.channel.send(embed=functions.embed(message, color, "Cash Game", "You wanted to beg from someone else, i'd reccomend getting a job, but ur the typer here.\nA passer by felt sorry for u and gave u: " + str(amount_given)))
      if message.content.startswith(db["prefix"] + " rcash balance"):
        color = discord.Color.blue()
        await message.channel.send(embed=functions.embed(message, color, "Cash Game", "You wanted to get ur balance in R cash, Well it is: "))
      
  elif message.content.startswith(db["prefix"] + " help"):
    if "Banned" not in str(message.author.roles) and db["allow_talk"] == 1:
      color = discord.Color.blue()
      await message.channel.send(embed=functions.embed(message, color, "Hello", "You asked for help!\nI'm at ur service...\nType ./info for a list of commands."))
  elif message.content.startswith(db["prefix"] + " ping"):
    if "Banned" not in str(message.author.roles) and db["allow_talk"] == 1:
      await message.channel.send("PONG!")
  elif message.content.startswith(db["prefix"] + " config"):
    if "Banned" not in str(message.author.roles):
      if "Admin" or "owner" in str(message.author.roles):
        if message.content.startswith(db["prefix"] + " config allowsentiment"):
          if db["allow_sentiment"] == 1:
            db["allow_sentiment"] = 0
          elif db["allow_sentiment"] == 0:
            db["allow_sentiment"] = 1
          else:
            db["allow_sentiment"] = 1
          color = discord.Color.orange()
          await message.channel.send(embed=functions.embed(message, color, "Settings...", "You asked for settings, to change api sentimental response\nWell it is now set to: " + str(db["allow_sentiment"])))
        elif message.content.startswith(db["prefix"] + " config allowapi"):
          if db["allow_api"] == 1:
            db["allow_api"] = 0
          elif db["allow_api"] == 0:
            db["allow_api"] = 1
          else:
            db["allow_api"] = 1
          color = discord.Color.orange()
          await message.channel.send(embed=functions.embed(message, color, "Settings...", "You asked for settings, to change api response for all commands\nWell it is now set to: " + str(db["allow_api"])))
        elif message.content.startswith(db["prefix"] + " config allowtalk"):
          if db["allow_talk"] == 1:
            db["allow_talk"] = 0
          elif db["allow_talk"] == 0:
            db["allow_talk"] = 1
          else:
            db["allow_talk"] = 1
          color = discord.Color.orange()
          await message.channel.send(embed=functions.embed(message, color, "Settings...", "You asked for settings, to change complete bot response for all commands *excluding config commands when your admin*\nWell it is now set to: " + str(db["allow_talk"])))
        elif message.content.startswith(db["prefix"] + " config apikey"):
          db["NinjaKeyDB"] = message.content[len(db["prefix"] + " config apikey "):]
          NinjaKey = db["NinjaKeyDB"]
          color = discord.Color.orange()
          await message.channel.send(embed=functions.embed(message, color, "Settings...", "You asked for settings, to change the key used to access Api Ninjas\nWell it is now set to: " + str(db["NinjaKeyDB"])))
        elif message.content.startswith(db["prefix"] + " config prefix"):
          if "owner" in str(message.author.roles):
            db["prefix"] = message.content[len(db["prefix"] + " config prefix "):].replace(" ", "")
            color = discord.Color.orange()
            await message.channel.send(embed=functions.embed(message, color, "Settings...", "You asked for settings, to change the the prefix for this discord bot\nWell it is now set to: " + db["prefix"]))
      elif db["allow_talk"] == 1:
        await message.channel.send("You asked for settings, But your not admin nor owner you dumbo!")
                                   
  elif message.content.startswith(db["prefix"] + " fun"):
    if "Banned" not in str(message.author.roles) and db["allow_talk"] == 1 and db["allow_api"] == 1:
      if message.content.startswith(db["prefix"] + " fun quote"):
        category =  message.content[len(db["prefix"] + " fun quote "):]
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          color = discord.Color.green()
          await message.channel.send(embed=functions.embed(message, color, "Famous Quotes", response.text[11:str(response.text).index("author") - 3]))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Famous Quotes", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun sentiment"):
        text = message.content[len(db["prefix"] + " fun sentiment "):]
        api_url = 'https://api.api-ninjas.com/v1/sentiment?text={}'.format(text)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          color = discord.Color.green()
          await message.channel.send(embed=functions.embed(message, color, "Manual Sentiment Api", "The quote you entered, \"" + text + "\" is classified as: {" + response.text[response.text.index("sentiment\": ") + 12:]))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Sentiment", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun bucket_list"):
        api_url = 'https://api.api-ninjas.com/v1/bucketlist'
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          color = discord.Color.green()
          await message.channel.send(embed=functions.embed(message, color, "Bucket List", response.text[8:response.text.index("}")]))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Bucket List", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun fact"):
        limit = 1
        api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          color = discord.Color.green()
          await message.channel.send(embed=functions.embed(message, color, "Fun Fact", response.text[9:-2]))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Fun Fact", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun dictionary"):
        word = message.content[len(db["prefix"] + " fun dictionary "):]
        api_url = 'https://api.api-ninjas.com/v1/dictionary?word={}'.format(word)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          if "\"valid\": true}" in response.text:
            meaning = response.text[14:response.text.index("word\": \"") - 3]
            if len(meaning) < 4000:
              color = discord.Color.green()
              await message.channel.send(embed=functions.embed(message, color, "Dictionary", meaning))
            else:
              color = discord.Color.red()
              await message.channel.send(embed=functions.embed(message, color, "Dictionary", "Word meaning too long to be sent to chat. Meaning is " + str(len(meaning)) + " charecters long - Srry!"))
          else:
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Dictionary", "The word - " + word + " - is invalid - Srry"))
        else:
            print("Error:", response.status_code, response.text)
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Dictionary", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun joke"):
        limit = 1
        api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          joke = response.text
          color = discord.Color.green()
          await message.channel.send(embed=functions.embed(message, color, "Joke", joke[9:-2]))
        else:
            print("Error:", response.status_code, response.text)
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Joke", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun hobby"):
        category = "general"
        api_url = 'https://api.api-ninjas.com/v1/hobbies?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          color = discord.Color.green()
          await message.channel.send(embed=functions.embed(message, color, "Hobby", response.text[9:response.text.index("link") - 3]))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Hobby", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun cats"):
        name = message.content[len(db["prefix"] + " fun cats "):]
        api_url = 'https://api.api-ninjas.com/v1/cats?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          answer = response.text
          while "[{\"" in answer:
            answer = answer.replace("[{\"", "")
          while "\": \"" in answer:
            answer = answer.replace("\": \"", " - ")
          while "\": " in answer:
            answer = answer.replace("\":", " - ")
          while "\", \"" in answer:
            answer = answer.replace("\", \"", "\n")
          while ", \"" in answer:
            answer = answer.replace(", \"", "\n")
          if len(answer[:-3]) > 6000:
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Cats", "Fact file is too long to be written to discord chat - Srry"))
          if answer != "[]" and not len(answer[:-3]) < 6000:
            color = discord.Color.green()
            await message.channel.send(embed=functions.embed(message, color, "Cats", answer[:-3]))
          else:
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Cats", "Invalid Cat"))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Cats", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
      elif message.content.startswith(db["prefix"] + " fun dogs"):
        name = message.content[len(db["prefix"] + " fun dogs "):]
        api_url = 'https://api.api-ninjas.com/v1/dogs?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': NinjaKey})
        if response.status_code == requests.codes.ok:
          answer = response.text
          while "[{\"" in answer:
            answer = answer.replace("[{\"", "")
          while "\": \"" in answer:
            answer = answer.replace("\": \"", " - ")
          while "\": " in answer:
            answer = answer.replace("\":", " - ")
          while "\", \"" in answer:
            answer = answer.replace("\", \"", "\n")
          while ", \"" in answer:
            answer = answer.replace(", \"", "\n")
          if len(answer[:-3]) > 6000:
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Dogs", "Fact file is too long to be written to discord chat - Srry"))
          if answer != "[]" and not len(answer[:-3]) < 6000:
            color = discord.Color.green()
            await message.channel.send(embed=functions.embed(message, color, "Dogs", answer[:-3]))
          else:
            color = discord.Color.red()
            await message.channel.send(embed=functions.embed(message, color, "Dogs", "Invalid Dog"))
        else:
          print("Error:", response.status_code, response.text)
          color = discord.Color.red()
          await message.channel.send(embed=functions.embed(message, color, "Dogs", "Api request has failed due to unknown reason - Srry\nError: " + str(response.status_code) + str(response.text)))
    elif db["allowapi"] == 0:
      await message.channel.send("Api repsonse is turned off. Tell your admin or owner to run " + db["prefix"] + " config allowapi, to toggle this again.")
  
  elif message.content.startswith(db["prefix"] + " info"):
    if "Banned" not in str(message.author.roles) and db["allow_talk"] == 1:
      if message.content == db["prefix"] + " info":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", This is the info center on how to use the rad bot. Mention this bot to get an introduction. Type ./help for a further intorduction. Type ./info <cmd> for more information on the command and it's sub commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="*The Commands*", value="**help\ninfo\nconfig\nfun\nmentionme\nping**", inline=False)
        await message.channel.send(embed=embed)
      elif message.content == db["prefix"] + " info help":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", this is a page dedicated to the help and indexing of this bot's commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="Help Command", value="Run this cmd to get more help.", inline=False)
        embed.add_field(name="Sub Commands", value="There are no sub-commands for this command.", inline=False)
        await message.channel.send(embed=embed)
      elif message.content == db["prefix"] + " info info":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", this is a page dedicated to the help and indexing of this bot's commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="Info Command", value="Run this to list all availible commands", inline=False)
        embed.add_field(name="Sub Commands", value="info <cmd> - Run to get a piece of info on a command, can get all possible commands by info", inline=False)
        await message.channel.send(embed=embed)
      elif message.content == db["prefix"] + " info config":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", this is a page dedicated to the help and indexing of this bot's commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="Config Command", value="Run this to configure this bot.", inline=False)
        embed.add_field(name="Sub Commands", value="config allowtalk - Run to toggle whether the bot can respond to any commands in this server except confg commands\nconfig allowsentiment - Run to toggle whether this bot should respond to any messages in chat depending on their sentimental level with an encouraging quote.\nconfig allowapi - Run to toggle whether this bot should respond to any commands that use the ApiNinjas API's. *Requests are not made if this is disabled*\nconfig prefix <new prefix> - Run to change the prefix of all commands. *Only owner can do this*", inline=False)
        await message.channel.send(embed=embed)
      elif message.content == db["prefix"] + " info fun":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", this is a page dedicated to the help and indexing of this bot's commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="Fun Command", value="Run this to entertain yourself.", inline=False)
        embed.add_field(name="Sub Commands", value="fun quote_play <tpye> - Return a famous quote, leave type empty for a random one\nfun quote_list - Return list of types for famous quote\nfun sentiment <text>- Return the sentiment of a piece of text, acute spelling is required\nfun bucket_list - Return a random thing to do\nfun fact - Return a fun fact\nfun dictionary <word> - Return the meaning of that word\nfun joke - Return a joke\nfun hobby - Return a hobby\nfun dogs <dog> - Return fact file of dog\nfun cats <cat> - Return fact file of cat", inline=False)
        await message.channel.send(embed=embed)
      elif message.content == db["prefix"] + " info mentionme":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", this is a page dedicated to the help and indexing of this bot's commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="Mention Me Command", value="Run this to get the attetion of everyone in the server, Be careful with this command as it can be a pain to others if spammed", inline=False)
        embed.add_field(name="Sub Commands", value="There are no sub-commands for this command.", inline=False)
        await message.channel.send(embed=embed)
      elif message.content == db["prefix"] + " info ping":
        embed=discord.Embed(title="Commands info", url="", description=message.author.name + ", this is a page dedicated to the help and indexing of this bot's commands", color=discord.Color.blue())
        embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
        embed.add_field(name="Ping Command", value="Run this fun command to get very nice 'PONG' back from the bot!", inline=False)
        embed.add_field(name="Sub Commands", value="There are no sub-commands for this command.", inline=False)
        await message.channel.send(embed=embed)
      else:
        await message.channel.send("Theres no help page on that...")
        
  elif message.content.startswith(db["prefix"] + " mentionme"):
    if "Banned" not in str(message.author.roles) and db["allow_talk"] == 1:
      color = discord.Color.green()
      await message.channel.send(embed=functions.embed(message, color, "Mentionme", "Hey @everyone pay attention to: " + message.author.mention))
  
  
  elif message.content.startswith(db["prefix"]):
    await message.channel.send("Thats not a command")

functions.keep_alive()
client.run(my_secret)