import sys
from pytube import *
import ffmpeg
import os

def progress(stream = None, chunk = None, file_handle = None, remaining = None):
	percent = (100*(file_size-remaining))/file_size
	print("{:00.2f} % downloaded ".format(percent) , '{:.2f}'.format((file_size-remaining)/(1024**2)),'MB',' out of ' , '{:.2f}'.format(file_size/(1024**2)),'MB' ,sep="  ")

def yt_downloader():
	link=input("Enter the video link :: ").strip()
	print ("Accessing YouTube URL...")
	try:
		yt=YouTube(link,on_progress_callback=progress)
	except:
		print('!!  ERROR  !!')
		print('::  Check your connection  ::')
		print('::  Check the url of the link  ::')
		exit(0)
	name=yt.title
	audio=yt.streams.filter(only_audio=True,type='audio',subtype='mp4').all()
	sel=1
	if (len(audio)>1):
		for audio_t in audio :
			print ("::::::::::"+str(sel)+"::::::::::")
			print(audio_t)
		sel=int(input("??  Enter choice  ??  "))
	print ("Downloading : {}...".format(name))
	stream_to_be_downloaded=audio[sel-1]
	global file_size
	file_size = stream_to_be_downloaded.filesize
	print ('File size %.2f MB'.format((file_size)/(1024**2)))
	stream_to_be_downloaded.download(filename='audio')
	audio_to_be_converted=ffmpeg.input('audio.mp4')
	ultimate_file=ffmpeg.output(audio_to_be_converted,name,format='mp3')
	ultimate_file.run()
	os.remove('audio.mp4')


if __name__ == '__main__':
	yt_downloader()

