from flask import Flask
from threading import Thread
import discord
from replit import db

is_in_bal = False

app = Flask("")

@app.route("/")
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def embed(message, color, title, text):
  embed=discord.Embed(title=title, url="", description=text, color=color)
  embed.set_author(name="CircuitGuy", url="", icon_url=message.author.avatar_url)
  embed.set_footer(text="This has been requested by: " + message.author.name)
  return embed

def create_bal(person):
  db["balances"].append({"name": person, "balance": "0", "multiplier": "x1"})
def change_bal(person, changer, value):
  if changer != "name":
    for N in range(len(db["balances"])):
      if db["balances"][N]["name"] == person:
        db["balances"][N][changer] = value
def erase_bal(person):
  for N in range(len(db["balances"])):
    if db["balances"][N]["name"] == person:
      db["balances"].remove(db["balances"][N])
def check_bal(person):
  if person in str(db["balances"]):
    return True
  else:
    return False
def get_balance(person):
  for N in range(len(db["balances"])):
    if db["balances"][N]["name"] == person:
      return db["balances"][N]["balance"]
def get_multiplier(person):
  for N in range(len(db["balances"])):
    if db["balances"][N]["name"] == person:
      return db["balances"][N]["multiplier"]



"""
  if message.content.startswith("./admincontrol"):
    if db["allow_talk"] == 1:
      if message.author.name not in db["bans"]:
        adminsname = ""
        if message.author.name in db["admins"] or db["owner"]:
          if message.content.startswith("./admincontrol add"):
            adminsname = message.content[19:]
            adminsname = str(adminsname)
            if adminsname not in db["admins"]:
              db["admins"] = db["admins"] + " " + adminsname
              await message.channel.send("User " + adminsname + " has been added to the list of Admins\nList is now: " + db["admins"])
            else:
              await message.channel.send("User " + adminsname + " is allready in the admins list")
          if message.content.startswith("./admincontrol remove"):
            adminsname = message.content[21:]
            adminsname = str(adminsname)
            if adminsname in db["admins"]:
              db["admins"] = db["admins"].replace(adminsname, "")
              await message.channel.send("User " + adminsname + " has been removed from the list of admins\nList is now: " + db["admins"])
            else:
              await message.channel.send("User " + adminsname + " is not in the admins list")
          if message.content.startswith("./admincontrol list"):
            await message.channel.send("List of admins: " + db["admins"])
          if message.content.startswith("./admincontrol clear"):
            db["admins"] = ""
            await message.channel.send("List of admins: " + db["admins"])
        else:
            await message.channel.send("You do not have permissions to run this command - Ask admins to grant you permmision.")
  
  if message.content.startswith("./bancontrol"):
    if db["allow_talk"] == 1:
      if message.author.name not in db["bans"]:
        bansname = ""
        if message.author.name in db["admins"] or db["owner"]:
          if message.content.startswith("./bancontrol add"):
            bansname = message.content[16:]
            bansname = str(bansname)
            if bansname not in db["bans"]:
              db["bans"] = db["bans"] + " " + bansname
              await message.channel.send("User" + bansname + " has been added to the list of bans\nList is now: " + db["bans"])
            else:
              await message.channel.send("User " + bansname + " is allready in the bans list")
          if message.content.startswith("./bancontrol remove"):
            bansname = message.content[19:]
            bansname = str(bansname)
            if bansname in db["bans"]:
              db["bans"] = db["bans"].replace(bansname, "")
              await message.channel.send("User" + bansname + " has been removed from the list of bans\nList is now: " + db["bans"])
            else:
              await message.channel.send("User " + bansname + " is not in the bans list")
          if message.content.startswith("./bancontrol list"):
            await message.channel.send("List of bans: " + db["bans"])
          if message.content.startswith("./bancontrol clear"):
            db["bans"] = ""
            await message.channel.send("List of bans: " + db["bans"])
        else:
            await message.channel.send("You do not have permissions to run this command - Ask admins to grant you permmision.")
"""
