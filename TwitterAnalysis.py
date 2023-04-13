#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep 30 19:18:02 2022

@author: pk673
"""

#Aim : Twitter analysis using Twitter API, NumPy, and Pandas to track global topics and city-specific trends, analyze following and followers counts of Twitter accounts, and retrieve previous tweets, identifying the top 5 trending topics in New York based on tweet volume

api_key=''
api_secret_key=''
access_token=''
access_token_secret=''

import numpy as np
import pandas as pd
import pip

pip install twitter

from twitter import Twitter 
from twitter import OAuth
from numpy import array
a=array([1,2,3])
a

#OAuth takes our 4 keys and access codes and authenticates them.
#Twitter uses the OAuth object to establish a connection to the twitter database.
oauth = OAuth(access_token, access_token_secret , api_key, api_secret_key)
api = Twitter(auth=oauth) #The variable api now is going to allow us to call functions that get data from twitter
help(api)

#What Topic is Trending Around World 
t_loc = api.trends.available()

from pandas.io.json import json_normalize
df_loc=json_normalize(t_loc)

#Which country has the most cities being tracked?
df_loc.country.value_counts()

#What if we wanted to search for a particular city, using a partial word?
dfNew=df_loc[df_loc['name'].str.contains('New')]

#Use the woeid to see what’s currently trending in any one city. Get the value for New York and put it in a variable ny.
ny=dfNew.loc[dfNew.name=='New York','woeid']
ny
type(ny)

ny.values[0]
type(ny.values[0])
ny_trend = api.trends.place(_id=ny.values[0])

ny2=dfNew.loc[373,'woeid']
dfNew[['name','woeid']]
type(ny2)
ny_trend2 = api.trends.place(_id=ny2)
 
#The values in the columns ”locations” and ”trends” are also JSON objects. The ”trends” column has the terms trending in New York.

dfny = json_normalize(ny_trend)

# Creating a New York Trends Table
dfny.trends
type(dfny.trends)

dftrends=json_normalize(dfny.trends.values[0])
nyjson=dfny.loc[0,'trends']
type(nyjson)

dftrends2 = json_normalize(nyjson)

#Saving/Reading a Pandas Table
dftrends.to_pickle('dftrends.pkl')

batman = pd.read_pickle('dftrends.pkl')

##Find the 5 topics with the highest tweet volumes (New York)
dftrends.columns
dftrends.nlargest(5,'tweet_volume')[['name','tweet_volume']]

sr = api.search.tweets(q='Trump',count = 100, tweet_mode='extended')
dfsr=json_normalize(sr)

dfst=json_normalize(dfsr.statuses.values[0])

#The table dfst is extremely large. It shows all the information a single tweet holds. The actual text message is in the column full text, 
dd = dfst.loc[0]
dd = dfst.full_text

#Following a Twitter Account
tjson=api.statuses.user_timeline(screen_name='realDonaldTrump',tweet_mode='extended',count=100)
dftrump=json_normalize(tjson)
dd = dftrump.full_text
dftrump.shape

#Followers of a Twitter Account
tfollow=api.followers.ids(screen_name='realDonaldTrump')
dffol = json_normalize(tfollow)
dffol2 = json_normalize(tfollow,'ids')

#followers of a twitter account

u0 = dffol2.loc[1,0]
u0
u0j=api.users.lookup(user_id=u0)
dfu0 = json_normalize(u0j)
#Using the id’s you can get the messages from a twitter account
tu0=api.statuses.user_timeline(id=u0,tweet_mode='extended',count=100)
dfu0t = json_normalize(tu0)
dd =dfu0t.full_text

#Even though the Twitter API allows us to get up 3200 tweets of a public user, the status call only allows us to receive up to 200 tweets at a time.
#The more recent 200 tweets will be given, but to get older tweets, we haveto make use of another parameter, named max id. Each tweet has a unique id:
dftrump['id']
#The id’s are in chronological order, the higher the id, the newer the tweet.
mid =dftrump['id'].min( )
#The id value in mid is the oldest tweet out of those 200 tweets.

#Get Previous tweets
mid=mid-1
tjson2=api.statuses.user_timeline(screen_name="realDonaldTrump",tweet_mode='extended',count=200, max_id=mid)
#max id parameter gets the tweets with id’s less than or EQUAL to the twitter id you provide in the parameter. That is why we decrease the mid variable by one value
dftrump2= json.normalize(tjson2)
mid_l=dftrump2['id'].max() #The mid l is less than mid.

#Get Previous Tweets - Loop
df = pd.DataFrame()
mid=0
for i in range(34) :
    if i ==0:
        tjsonn=api.statuses.usertimeline( screen_name="realDonaldTrump",tweet_mode='extended',count=200 )
    else :
        tjsonn=api.statuses.usertimeline( screen_name="realDonaldTrump",tweet_mode='extended',count=200, max_id= mid )
    if len(tjson) >0:
        dftrump=json.normalize(tjson)
        mid =dftrump['id'].min( )
        mid=mid-1
        df = pd.concat([df,dfttrump], ignore_index=True)

#We append dftrump to df every loop, dftrump takes on 200 rows at a time.


