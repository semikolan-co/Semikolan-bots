import discord
import os
import requests
import json
from keep_alive import keep_alive 
from datetime import date,datetime,timedelta
import pytz
from dateutil import tz
import os

# Environment variables include
# bot token
# clist username and api key
# discord channel id
# discord role id to tag

clistUsername = os.environ["username"]
clistApiKey = os.environ["api_key"]
channelId = os.environ["channel_id"]
roleId = os.environ["role_id"]

def utctoist(datestring):
  datetime_object = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S') +  timedelta(hours=5,minutes=30)
  ist = datetime_object.strftime('%Y-%m-%dT%H:%M:%S')
  return ist

client = discord.Client()
def get_quote():
   IST = pytz.timezone('Asia/Kolkata')
   dt = str(datetime.now(IST))[:10]
   response = requests.get("https://clist.by:443/api/v2/contest/?start__gt="+str(dt)+"T00%3A00%3A00&order_by=start&username="+clistUsername+"&api_key="+clistApiKey)
   json_data = json.loads(response.text)
   print(json_data)
   with open ("sample.json", "w") as outfile:
    json.dump(json_data,outfile)

def get_hackathons():
  

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  channel = client.get_channel(channelId)
  #await channel.send('hello')
  curr_date = 'ini'
  while True:
    IST = pytz.timezone('Asia/Kolkata')
    last_date = str(datetime.now(IST))[:10]
    while last_date != curr_date:
      f = open('sample.json',)
      data = json.load(f)
      print('********************')
      get_quote()
      msg = True
      for ind_data in data['objects']:

        # format- 2021-09-08T10:30:00
        
        ind_data['start'] = utctoist(ind_data['start'])
        
        print(ind_data['start'][:10])
        print(ind_data['start'][11:])
        if(str(datetime.now(IST))[:10]==ind_data['start'][:10]):
        # if('2021-09-10'==ind_data['start'][:10]):
          if msg:
            await channel.send('>>> Hello <@&'+roleId+'> ,these are all the contests happening today: ')
            msg = False
          await channel.send(">>> ```"+ind_data['event']+'\n'+ind_data['host']+'\n'+ind_data['start'][11:]+' IST```'+'\n'+ind_data['href'])
      curr_date = str(datetime.now(IST))[:10]
      if msg:
        await channel.send('>>> Hey <@&'+roleId+'> , there are no contests starting today!')
keep_alive()
get_quote()
client.run(os.getenv("TOKEN"))
