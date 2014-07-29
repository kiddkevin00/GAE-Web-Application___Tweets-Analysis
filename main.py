#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os, urllib, time, itertools, logging

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb	
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

# (TODO) Must contain data in inside this file, don't know why..
STORE_DATA_PATH = "data/"

# define a seperator for reading file contents
def isa_group_separator(line):
	return line=='\n'

# define a parent key(similar to Primary Key) for each entity 
def parent_key(key):
	return ndb.Key("TweetsGroup", key)

# define the model for Datastore 
class Tweet(ndb.Model):
	created_at = ndb.StringProperty(indexed = False)
	tweet = ndb.StringProperty(indexed = False)

# define the main page
class MainHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug("here is MainHandler..")
		submitted_keyword = self.request.get("keyword")
		logging.debug("keyword : "+submitted_keyword)
		if (submitted_keyword):
			# TODO..
			caches = memcache.get(submitted_keyword) 

			tweet_query = Tweet.query(ancestor=parent_key(submitted_keyword))	
			tweets = tweet_query.fetch()
			logging.debug(len(tweets))
			for tweet in tweets:
				logging.debug(tweet)
		else: 
			logging.debug("no user's input")

		template_values = {

		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

# define a page for storing data
class TweetStore(webapp2.RequestHandler):
	def get(self):
		global STORE_DATA_PATH
		logging.debug("here is TweetStore..")
		selected_file = self.request.get("selected")
		logging.debug("Selected File : " + selected_file)
		save = self.request.get("save") 
		logging.debug("Save or not : " + save) 
		save_all = self.request.get("saveall")
		view_database = self.request.get("viewdb")

		view_tweets = []
		# view the data storing in the current Database..
		if (view_database == "true") and (selected_file): 
			tweet_query = Tweet.query(ancestor=parent_key(selected_file))	
			tweets_result = tweet_query.fetch()
			logging.debug("How many tweets store in this file at Database: " + str(len(tweets_result)))
			for tweet_result in tweets_result:
				logging.debug(tweet_result)
				view_tweet = []
				view_tweet.append(tweet_result.tweet)
				view_tweet.append(tweet_result.created_at)
				view_tweets.append(view_tweet)
				logging.debug("Number of tweets for preview : " + str(len(view_tweets)))

		# for storing and viewing files at the local directory 
		files = [] 
		for file in os.listdir(STORE_DATA_PATH):
			logging.debug("file name : " + file)

			# assign parent key for each entity 
			tweet_parent_name = file[:-4]

			save_tweets = []
			files.append(tweet_parent_name)
			if ((tweet_parent_name == selected_file) and (view_database != "true")):
				with open(STORE_DATA_PATH + file, "r") as infile:
					# similar to "GROUP BY", but search for the same key sequentially
					# Here groups the not empty lines together   
					for key, group in itertools.groupby(infile, isa_group_separator):
						if not key:
							tweet = Tweet(parent=parent_key(tweet_parent_name))
							view_tweet = []
							for item in group:
								field, value = item.split(" : ")
								# strip all the white_space
								value = value.strip()
								# can't use "," to seperate varible like "print" does
								logging.debug(field + " : " + value)
								if field == "Tweet":
									tweet.tweet = value
									view_tweet.append(value)
								elif field == "Created at":
									tweet.created_at = value
									view_tweet.append(value)
								else: 
									self.redirect("/?error=true")
							view_tweets.append(view_tweet)
							logging.debug("Number of tweets for preview : " + str(len(view_tweets)))
							if save == "true":
								save_tweets.append(tweet)
							logging.debug("Number of To_Save Tweets : " + str(len(save_tweets)))
				logging.debug("might save a file to Datastore..")
				ndb.put_multi(save_tweets)

			if (save_all == "true"):
				with open(STORE_DATA_PATH + file, "r") as infile:
					# similar to "GROUP BY", but search for the same key sequentially
					# Here groups the not empty lines together   
					for key, group in itertools.groupby(infile, isa_group_separator):
						if not key:
							tweet = Tweet(parent=parent_key(tweet_parent_name))
							for item in group:
								field, value = item.split(" : ")
								# strip all the white_space
								value = value.strip()
								# can't use "," to seperate varible like "print" does
								logging.debug(field + " : " + value)
								if field == "Tweet":
									tweet.tweet = value
								elif field == "Created at":
									tweet.created_at = value
								else: 
									self.redirect("/?error=true")
							save_tweets.append(tweet)
							logging.debug("Number of To_Save Tweets : " + str(len(save_tweets)))
				logging.debug("Save a file to Datastore..")
				ndb.put_multi(save_tweets)

		logging.debug("passing files paramter's size : " + str(len(files)))
		logging.debug("passing view_tweets paramter's size: " + str(len(view_tweets)))
		# logging.debug(view_tweets[0])
		template_values = {
			'files': files,
			'selected_file': selected_file,
			'view_tweets': view_tweets,
			'view_database': view_database
		}
		template = JINJA_ENVIRONMENT.get_template('data-save.html')
		self.response.write(template.render(template_values))
		#self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/data-save', TweetStore)
], debug=True)
