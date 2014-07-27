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

STORE_DATA_PATH = "data/"

# define a seperator for reading file contents
def isa_group_separator(line):
	return line=='\n'

# define a parent key(similar to Primary Key) for each entity 
def parent_key(key):
	return ndb.Key("TweetsGroup", key)

# define the model for Datastore 
class Tweet(ndb.Model):
	creat_at = ndb.StringProperty(indexed = False)
	tweet = ndb.StringProperty(indexed = False)

# define the main page
class MainHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug("here is MainHandler..")
		submitted_keyword = self.request.get("keyword")
		logging.debug("keyword : "+submitted_keyword)
		if (submitted_keyword):
			tweet_query = Tweet.query(ancestor=parent_key(submitted_keyword))	
			tweets = tweet_query.fetch()
			logging.debug(len(tweets))
			for tweet in tweets:
				logging.debug(tweet)



		template_values = {

		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

#define a page for storing data
class TweetStore(webapp2.RequestHandler):
	def get(self):
		global STORE_DATA_PATH
		logging.debug("here is TweetStore..")
		for file in os.listdir(STORE_DATA_PATH):
			# assign parent key for each entity 
			tweet_parent_name = file[:-4]

			tweets = []
			logging.debug("file name : " + file)
			with open(STORE_DATA_PATH + file, "r") as infile:
				# similar to "GROUP BY", but search for the same key sequentially
				# Here grouping the not empty lines together   
				for key, group in itertools.groupby(infile, isa_group_separator):
					if not key:
						tweet = Tweet(parent=parent_key("key04"))
						for item in group:
							field, value = item.split(" : ")
							# strip all the white_space
							value = value.strip()
							# can't use "," to seperate varible like "print" does
							logging.debug(field + value)
							if field == "Tweet":
								tweet.tweet = value
							elif field == "Created at":
								tweet.creat_at = value
							else: 
								self.redirect("/?error=1")
						tweets.append(tweet)
						logging.debug(len(tweets))
			ndb.put_multi(tweets)
		self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/savedata', TweetStore)
], debug=True)
