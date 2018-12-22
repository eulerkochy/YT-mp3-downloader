import sys
from pytube import *
import ffmpeg
import os

def progress(stream = None, chunk = None, file_handle = None, remaining = None):
	percent = (100*(file_size-remaining))/file_size
	print("{:00.0f} % downloaded ".format(percent) , str(file_size-remaining)+' bytes' ,' out of ' , str(file_size)+' bytes' ,sep=" ||  ")

def yt_downloader():
	link=input("Enter the video link :: ").strip()
	print ("Accessing YouTube URL...")
	try:
		yt=YouTube(link,on_progress_callback=progress)
	except:
		print('<<  ERROR  >>')
		exit(0)
	name=yt.title
	audio=yt.streams.filter(only_audio=True).all()
	sel=1
	for audio_type in audio:
		print (":::::"+str(sel)+":::::")
		print(audio_type)
		sel+=1
	sel=int(input("Enter Choice :: "))
	print ("Downloading : {}...".format(name))
	stream_to_be_downloaded=audio[sel-1]
	global file_size
	file_size = stream_to_be_downloaded.filesize
	stream_to_be_downloaded.download(filename='audio')
	audio_to_be_converted=ffmpeg.input('audio.mp4')
	ultimate_file=ffmpeg.output(audio_to_be_converted,name,format='mp3')
	ultimate_file.run()
	os.remove('audio.mp4')


if __name__ == '__main__':
	yt_downloader()

