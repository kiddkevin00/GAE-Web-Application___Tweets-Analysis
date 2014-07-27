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

save_file_name = "default"
SAVE_PATH = "data/"

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
		global save_file_name

		try:
			if type(data) is str:
				#print data
				tweet =  data.split(',"text":"')[1].split('","source":')[0]
				created_at = data.split('"created_at":"')[1].split('","id":')[0]
				#print tweet
				#print created_at
			relativePath = os.path.join(SAVE_PATH, save_file_name+".txt")   
			# "a+" : append  
			with open(relativePath, "a+") as output_file:
				file_size = os.stat(relativePath).st_size
				print "current size : " + str(file_size)
				# set file size < 1000B(1KB)
				if file_size < 1000:
					output_file.write("Tweet : "+tweet + "\n")
					output_file.write("Created at : " + created_at+"\n")
					output_file.write("\n")
				else:
					print "exceed the file size limit !!"
					# need to disconncect with tweepy, still figuring out..
					pass	
		except BaseException, e:
			print "failed ondata: ", str(e)
			#time.sleep(5)
		return True
	def on_error(self, status):
		print "error", status

def main():
	global save_file_name
	global SAVE_PATH

	print "This tool can can help you retreive Twitter's data through Twitter API"
	print "starting.."

	save_file_name = raw_input("Please enter a file name to save as : ")

	relativePath = os.path.join(SAVE_PATH, save_file_name+".txt")   
	if os.path.exists(relativePath):
		os.remove(relativePath)

	# keyword for searching  
	keyword = raw_input("What do you wanna search this time?  ")

	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[keyword])
	# the following line actually can't work
	twitterStream.disconnect()

	print "This is the end of the program"

if __name__ == "__main__":
	main()
