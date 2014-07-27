#!/usr/bin/python
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from sys import argv
import time, os

ckey = "D4dctRLEnUieVGk5dXmdhFFqT"
csecret = "BHPGUHFKk66cRL40MR4rXec26DsrKtXa36iii92wyBZcrWZ9tb"
atoken = "1914184802-niSHlUKUWZaVO3h2seLSxIcrDnFy4zu5tJDNXGc"
asecret = "axdMrkkUavyI7UhUpiRdtLlZ1v2JqYPYPtubfj4mmuer9"

#SAVE_FILE_NAME = "tweet04.txt"

class listener(StreamListener):
	# keep looping on this function
	def on_data(self, data):
		# for getting user's input from cmd
		#input1, input2 = argv

		# for getting user's input during the runtime 
		#raw_input("what is this?")

		# can't save in a specified path, still figuring out..
		# , but can read from a specific path
		#save_file_path = "/Users/Marcus/Desktop/data/"

		# declate as global, which althorize the function can change 
		# the value locally
		global SAVE_FILE_NAME

		try:
			if type(data) is str:
				#print data
				tweet =  data.split(',"text":"')[1].split('","source":')[0]
				created_at = data.split('"created_at":"')[1].split('","id":')[0]
				#print tweet
				#print created_at
			# "a+" : append  
			with open(SAVE_FILE_NAME, "a+") as output_file:
				file_size = os.stat(SAVE_FILE_NAME)
				#output_file.write("here")
				print file_size.st_size
				# set file size < 1000B(1KB)
				if file_size.st_size < 1000:
					output_file.write("Tweet : "+tweet + "\n")
					output_file.write("Created at : " + created_at+"\n")
					output_file.write("\n")
				else:
					# need to disconncect with tweepy, still figuring out..
					pass	
		except BaseException, e:
			print "failed ondata: ", str(e)
			#time.sleep(5)
		return True
	def on_error(self, status):
		print "error", status

def main():
	global SAVE_FILE_NAME
	SAVE_FILE_NAME = raw_input("Please enter a file name to save as : ")
	if os.path.exists(SAVE_FILE_NAME):
		os.remove(SAVE_FILE_NAME)
	print "starting.."
	# keyword for searching  
	keyword = raw_input("What do you wanna search this time?\n")
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[keyword])
	# the following line actually can't work
	twitterStream.disconnect()
	print "This is the end of the program"

if __name__ == "__main__":
	main()