# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 23:01:48 2018

@author: Ben Zhao
"""
import discord
import asyncio
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import os


####################################################################
# Setup
####################################################################
client = discord.Client()

# jobber numbers
number_channel_id = 475656157130915851
# Jobber lists
list_channel_id = 475656194120220672
# jobber graphs
graph_channel_id = 475656217449201664
# Bot command and Message
bot_channel_id = 477596596863762443

tracker_list = {
                5001832: ("Consider it Drunk", "CiS"),
                5001162: ("Untameable", "LB"),
                5001968: ("Pokemon", "CtA"),
                5002158: ("Ship Faced", "PO"),
                5002112: ("Throwing Ape Ship", "APE"),
                5000200: ("The Midnight Society", "BRENDA"),
                #5001156: ("Oath of Peace", "KtP"),
                # 5000435: ("The Southsea Bandits", "TSB"),
                # 5001229: ("Elysium", "ELSM"),
                # 5001155: ("Inglorious Basterds", "IB"),
                #5001990: ("The Organization", "GW")
                }

destination = "./MEL_TRIPLEDROP/"

n_data_points = 200

if not os.path.exists(destination):
    os.makedirs(destination)


####################################################################
# Functions
####################################################################
async def cade_data_function():
    await client.wait_until_ready()
    num_channel = discord.Object(id=str(number_channel_id))
    list_channel = discord.Object(id=str(list_channel_id))
    graph_channel = discord.Object(id=str(graph_channel_id))

    while not client.is_closed:
        now_time = datetime.utcnow().strftime('%d/%m/%y-%H:%M:%S')
        
        record_holder = {}
        number_holder = {}
        jobber_holder = {}

        for (crew_id, (crew_name, crew_short)) in tracker_list.items():
            print(crew_id, crew_name, crew_short)
            with open("%s%s_job.csv" % (destination, crew_short), "r") as crew_file:
                crew_reader = csv.reader(crew_file, delimiter=',', quotechar='\"')
                index = []
                last_row = None
                record_holder[crew_name] = []
                for row in crew_reader:
                    record_holder[crew_name].append(int(row[2]))
                    index.append(int(row[1]))
                    last_row = row
                number_holder[crew_name] = last_row[3:]
                jobber_holder[crew_name] = int(last_row[2])

        plt.figure()
        for crew, data in record_holder.items():
            label = "%s - %i"%(crew, jobber_holder[crew])
            plt.plot(index[-n_data_points:], data[-n_data_points:], label=label)
        
        plt.legend()
        plt.title(destination.split('/')[1])
        plt.ylabel('Jobbers')
        plt.xlabel('Minutes')

        plt.savefig("%splot.png" % destination)
        plt.close('all')
        
        # await client.send_message(num_channel, now_time)
        # await client.send_message(num_channel, number_holder)

        # await client.send_message(list_channel, now_time)
        # await client.send_message(list_channel, jobber_holder)

        await client.send_message(graph_channel, now_time)
        await client.send_file(graph_channel, "%splot.png" % destination)
        
        sleeptime = 60 - datetime.utcnow().second + 30
        await asyncio.sleep(sleeptime)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    bot_channel = discord.Object(id=str(bot_channel_id))
    await client.send_message(bot_channel, "Ready")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    bot_channel = discord.Object(id=str(bot_channel_id))

    if message.content.startswith('!hello'):
        bot_channel = discord.Object(id=str(bot_channel_id))
        await client.send_message(bot_channel, "Hello")


    if message.content.startswith('!reset'):
        await client.send_message(bot_channel, "Restarting...")
        force_shutdown()


def force_shutdown():
    raise SystemExit


def handle_exit():
    print("Handling")
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(asyncio.wait_for(t, 5,
                                                            loop=client.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass


####################################################################
# MAIN
#################################################################### 
with open('token.txt', 'r') as tokenfile:
    token = tokenfile.read().replace('\n', '')

# client.loop.create_task(cade_data_function())
# client.run(token)

while True:
    client.loop.create_task(cade_data_function())
    try:
        client.loop.run_until_complete(client.start(token))
    except SystemExit:
        print('SystemExit')
        handle_exit()
        break
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        print("Program ended")
        break

    print("Bot restarting")
    client = discord.Client(loop=client.loop)
