import discord
import os
import time

client = discord.Client()

selected = 0

inp = ""
act = ""
name = ""

def embed_update():
    embed = discord.Embed(title="Cloudtodo", description="Create and manage your todolists!", color=0x00ff00)
    if selected == 1:
        embed.add_field(name="💠Create", value="Create a todolist", inline=False)
    else:
        embed.add_field(name="Create", value="Create a todolist", inline=False)
    if selected == 2:
        embed.add_field(name="💠View", value="View your todolists", inline=False)
    else:
        embed.add_field(name="View", value="View your todolists", inline=False)
    if selected == 3:
        embed.add_field(name="💠Delete", value="Delete a todolist", inline=False)
    else:
        embed.add_field(name="Delete", value="Delete a todolist", inline=False)
    if selected == 4:
        embed.add_field(name="💠List", value="List the contents of a todolist", inline=False)
    else:
        embed.add_field(name="List", value="List the contents  of a todolist", inline=False)
    if selected == 5:
        embed.add_field(name="💠Help", value="Help with cloudtodo", inline=False)
    else:
        embed.add_field(name="Help", value="Help with cloudtodo", inline=False)
    if selected == 6:
        embed.add_field(name="💠Add", value="Add an entry to an todolist", inline=False)
    else:
        embed.add_field(name="Add", value="Add an entry to an todolist", inline=False)
    if selected == 7:
        embed.add_field(name="💠Remove", value="Remove an entry from an todolist", inline=False)
    else:
        embed.add_field(name="Remove", value="Remove an entry from an todolist", inline=False)
    return embed

def ui(selected):
    global inp
    if selected == 1:
        embed = discord.Embed(title="Create", description="Create a todolist!", color=0x00ff00)
        if inp != "":
            embed.add_field(name="Name:", value="{}".format(inp), inline=False)
        else:
            embed.add_field(name="Name:", value="Waiting for input... Use $input", inline=False)
    if selected == 2:
        files = os.listdir()
        for x in files:
            if x.endswith(".todolist"):
                print(x)
            else:
                files.remove(x)
        if len(files) > 0:
            embed = discord.Embed(title="Cloudtodo", description="Your todolists:", color=0x00ff00)
            for x in files:
                if x.endswith(".todolist"):
                    print(x)
                    embed.add_field(name="{}".format(x), value="{}".format(x), inline=False)
        else:
            embed = discord.Embed(title="Cloudtodo", description="No todolists found! 😟", color=0x00ff00)
    if selected == 3:
        embed = discord.Embed(title="Delete", description="Delete a todolist!", color=0x00ff00)
        embed.add_field(name="Todolists", value="Available todolists:", inline=False)
        files = os.listdir()
        for x in files:
            if x.endswith(".todolist"):
                print(x)
            else:
                files.remove(x)
        if len(files) > 0:
            for x in files:
                if x.endswith(".todolist"):
                    embed.add_field(name="{}".format(x), value="{}".format(x), inline=False)
        else:
            print("No todolists found!")

        if inp != "":
            embed.add_field(name="Deleting:", value="{}".format(inp), inline=False)
        else:
            embed.add_field(name="Deleting:", value="Waiting for input... Use $input", inline=False)
    if selected == 4:
        embed = discord.Embed(title="List", description="List the contents of a todolist!", color=0x00ff00)
        embed.add_field(name="Todolists", value="Available todolists:", inline=False)
        files = os.listdir()
        for x in files:
            if x.endswith(".todolist"):
                print(x)
            else:
                files.remove(x)
        if len(files) > 0:
            for x in files:
                if x.endswith(".todolist"):
                    embed.add_field(name="{}".format(x), value="{}".format(x), inline=False)
        else:
            print("No todolists found!")

        if inp != "":
            embed.add_field(name="Listing:", value="{}".format(inp), inline=False)
        else:
            embed.add_field(name="Listing:", value="Waiting for input... Use $input", inline=False)

        
        
        
        

    return embed
   
    

@client.event
async def on_ready():
  print("ready as {0.user}".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" for commands"))



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content
    
    if msg.startswith('$help'):
        await message.channel.send("help | show this text \nstatus | shows the status of the bot \ntodo | starts the todo gui")

    if msg.startswith('$status'):
        await message.channel.send("{0.user} is online and ready!".format(client))
    
    if message.content.startswith('$todo'):
        send = await message.channel.send(embed=embed_update())	
        await send.add_reaction("❌")
        await send.add_reaction("⬆️")
        await send.add_reaction("⬇️")
        await send.add_reaction("✅")
    if message.content.startswith('$input'):
        global inp
        array = msg.split(" ", 1)
        try:
            array.remove('$input')
        except:
            print("An error occured, while trying to array the command")
        if len(array) > 0:
            inp = array[0]
        else:
            await message.channel.send("Invalide Syntax")





@client.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.emoji in ["❌", "⬆️", "⬇️", "✅"]:
        global selected
        global inp
        global name
        global act
        print(reaction.emoji)
        await reaction.remove(user)
        await reaction.message.add_reaction(reaction.emoji)
        if reaction.emoji == "❌":
            print("Aborting")
            await reaction.message.delete()
        if reaction.emoji == "⬆️":
            selected -= 1
            if selected < 0:
                selected = 0
            print(selected)
            await reaction.message.edit(embed=embed_update())
        if reaction.emoji == "⬇️":
            selected += 1
            print(selected)
            await reaction.message.edit(embed=embed_update())
        if reaction.emoji == "✅":
            print("Selected")
            try:
                if selected == 1:
                    while inp == "":
                        await reaction.message.edit(embed=ui(selected))
                    await reaction.message.edit(embed=ui(selected))
                    time.sleep(0.5)

                    if os.path.exists(inp + ".todolist"):
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} already exists.".format(inp), color=0x00ff00)
                    else:
                        todolist = open(inp + ".todolist", "w")
                        todolist.close()
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} created.".format(inp), color=0x00ff00)
                    inp = ""
                    selected = 0
                    await reaction.message.edit(embed=embed)
                    time.sleep(2)
                    await reaction.message.delete()
                
                if selected == 2:
                    await reaction.message.edit(embed=ui(selected))
                    time.sleep(6)
                    inp = ""
                    selected = 0
                    await reaction.message.delete()
                
                if selected == 3:
                    while inp == "":
                        await reaction.message.edit(embed=ui(selected))
                    await reaction.message.edit(embed=ui(selected))
                    time.sleep(0.5)

                    if os.path.exists(inp + ".todolist"):
                        os.remove(inp + ".todolist")
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} deleted".format(inp), color=0x00ff00)
                    else:
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} doesnt exist.".format(inp), color=0x00ff00)
                    inp = ""
                    selected = 0
                    await reaction.message.edit(embed=embed)
                    time.sleep(2)
                    await reaction.message.delete()

                if selected == 4:
                    while inp == "":
                        await reaction.message.edit(embed=ui(selected))
                    await reaction.message.edit(embed=ui(selected))
                    time.sleep(0.5)

                    if os.path.exists(inp + ".todolist"):
                        todolist = open(inp + ".todolist", "r")
                        awnser = todolist.read()
                        todolist.close()
                        embed = discord.Embed(title="Todolist {}:".format(inp), description="{}".format(awnser), color=0x00ff00)
                    else:
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} doesnt exist.".format(inp), color=0x00ff00)
                    inp = ""
                    selected = 0
                    await reaction.message.edit(embed=embed)
                    time.sleep(10)
                    await reaction.message.delete()
                if selected == 5:
                    embed = discord.Embed(title="Cloudtodo", description="Usage information:", color=0x00ff00)
                    embed.add_field(name="$todo", value="Opens the main menu", inline=False)
                    embed.add_field(name="$input <Value>", value="Allows the input of a value", inline=False)
                    embed.add_field(name="💠", value="The curser marks the selected thing", inline=False)
                    embed.add_field(name="⬆️", value="Moves the cursor up", inline=False)
                    embed.add_field(name="⬇️", value="Moves the cursor down", inline=False)
                    embed.add_field(name="✅", value="Selects", inline=False)
                    embed.add_field(name="❌", value="Cancels all actions", inline=False)
                    inp = ""
                    selected = 0
                    await reaction.message.edit(embed=embed)
                    time.sleep(12)
                    await reaction.message.delete()
                if selected == 6:
                    embed = discord.Embed(title="Add", description="Add an entry into a Todolist", color=0x00ff00)
                    await reaction.message.edit(embed=embed)
                    while name == "":
                        embed = discord.Embed(title="Add", description="Add an entry into a Todolist", color=0x00ff00) 
                        if inp != "" and name == "":
                            name = inp
                            inp = ""
                            embed.add_field(name="Name:", value="{}".format(name), inline=False)
                            embed.add_field(name="Entry:", value="Not defined...", inline=False)
                        else:
                            embed.add_field(name="Name:", value="Waiting for input... Use $input", inline=False)
                            embed.add_field(name="Entry:", value="Not defined...", inline=False)
                        await reaction.message.edit(embed=embed)

                    while act == "":
                        embed = discord.Embed(title="Add", description="Add an entry into a Todolist", color=0x00ff00)
                        if inp != "" and name != "":
                            act = inp
                            embed.add_field(name="Name:", value="{}".format(name), inline=False)
                            embed.add_field(name="Entry:", value="{}".format(act), inline=False)
                        else:
                            if os.path.exists(name + ".todolist"):
                                todolist = open(name + ".todolist", "r")
                                awnser = todolist.read()
                                todolist.close()
                                embed = discord.Embed(title="Contents of todolist {}:".format(name), description="{}".format(awnser), color=0x00ff00)
                            else:
                                embed = discord.Embed(title="Cloudtodo", description="Todolist {} doesnt exist.".format(inp), color=0x00ff00)
                            embed.add_field(name="Name:", value="{}".format(name), inline=False)
                            embed.add_field(name="Entry:", value="Waiting for input... Use $input", inline=False)
                        await reaction.message.edit(embed=embed)

                    await reaction.message.edit(embed=embed)
                    time.sleep(0.5)

                    if os.path.exists(name + ".todolist"):
                        todolist = open(name + ".todolist", "a")
                        todolist.write(act + "\n")
                        todolist.close()
                        embed = discord.Embed(title="Cloudtodo", description="Added entry {} into todolist!".format(act), color=0x00ff00)
                    else:
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} doesnt  exist.".format(name), color=0x00ff00)
                    inp = ""
                    act = ""
                    name = ""
                    selected = 0
                    await reaction.message.edit(embed=embed)
                    time.sleep(2)
                    await reaction.message.delete()
                if selected == 7:
                    embed = discord.Embed(title="Remove", description="Remove an entry from an Todolist", color=0x00ff00)
                    await reaction.message.edit(embed=embed)
                    while name == "":
                        embed = discord.Embed(title="Remove", description="Remove an entry from an Todolist", color=0x00ff00) 
                        if inp != "" and name == "":
                            name = inp
                            inp = ""
                            embed.add_field(name="Name:", value="{}".format(name), inline=False)
                            embed.add_field(name="Entry:", value="Not defined...", inline=False)
                        else:
                            embed.add_field(name="Name:", value="Waiting for input... Use $input", inline=False)
                            embed.add_field(name="Entry:", value="Not defined...", inline=False)
                        await reaction.message.edit(embed=embed)

                    while act == "":
                        embed = discord.Embed(title="Remove", description="Remove an entry from an Todolist", color=0x00ff00)
                        if inp != "" and name != "":
                            act = inp
                            embed.add_field(name="Name:", value="{}".format(name), inline=False)
                            embed.add_field(name="Entry:", value="{}".format(act), inline=False)
                        else:
                            embed.add_field(name="Name:", value="{}".format(name), inline=False)
                            embed.add_field(name="Entry:", value="Waiting for input... Use $input", inline=False)
                        await reaction.message.edit(embed=embed)

                    await reaction.message.edit(embed=embed)
                    time.sleep(0.5)


                    if os.path.exists(name + ".todolist"):
                        todolist = open(name + ".todolist", "r")
                        lines = todolist.readlines()
                        todolist.close()
                        todolist = open(name + ".todolist", "w")
                        for line in lines:
                            if line.strip("\n") != act:
                                todolist.write(line)
                        todolist.close()
                        embed = discord.Embed(title="Cloudtodo", description="Removed entry {} from todolist!".format(act), color=0x00ff00)
                    else:
                        embed = discord.Embed(title="Cloudtodo", description="Todolist {} doesnt  exist.".format(name), color=0x00ff00)

                    inp = ""
                    inp = ""
                    act = ""
                    name = ""
                    selected = 0
                    await reaction.message.edit(embed=embed)
                    time.sleep(2)
                    await reaction.message.delete()

            

            except:
                print("")

            
            


#❌⬆️⬇️✅💠





client.run('')
