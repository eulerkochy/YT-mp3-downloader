import sys
from pytube import *
import ffmpeg
import os

def progress(stream = None, chunk = None, file_handle = None, remaining = None):
	percent = (100*(file_size-remaining))/file_size
	print("{:00.2f} % downloaded ".format(percent) , '{:.2f}'.format((file_size-remaining)/(1024**2)),'MB',' out of ' , '{:.2f}'.format(file_size/(1024**2)),'MB' ,sep="  ")

def yt_download(url):
	link=url
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
	global total_size
	total_size+=file_size
	print ('File size {:.2f} MB'.format((file_size)/(1024**2)))
	stream_to_be_downloaded.download(filename='audio')
	audio_to_be_converted=ffmpeg.input('audio.mp4')
	ultimate_file=ffmpeg.output(audio_to_be_converted,name,format='mp3')
	ultimate_file.run()
	os.remove('audio.mp4')

def parse_playlist(playlist):
	''' This function parses the link of a playlist and returns the link of individual videos as a list'''
	links=[]
	ply=Playlist(playlist)
	ytb='https://www.youtube.com'
	for link in ply.parse_links():
		links.append(ytb+link)
	return links

def yt_download_playlist():
	playlist_link=input('Enter playlist link :: ')
	all_songs=parse_playlist(playlist_link)

	file_path=input('?? Save to ?? [  Enter relative path  ] [  Press ENTER to save in the current directory ] ')

	if (len(file_path)>0):
		if not os.path.exists(file_path):
			os.makedirs(file_path)
			print('Directory', file_path , 'created')
		else:
			print('Directory',file_path,'already exists!')

		os.chdir(file_path)

	playlist_name=input('[  Enter the name of the playlist ] ')

	if (len(playlist_name)==0):
		playlist_name='Random Jingles'

	if (len(playlist_name)>0):
		if not os.path.exists(playlist_name):
			os.makedirs(playlist_name)
			print('Playlist', playlist_name , 'created!')
		else:
			print('Playlist',playlist_name,'already exists!')

		os.chdir(playlist_name)

	global total_size
	total_size=0.0
	
	for song in all_songs:
		yt_download(song)
	
	print ('\nDownloaded {:d} songs. '.format(len(all_songs)),'Total size {:.2f} MB\n'.format((total_size)/(1024**2)))


if __name__ == '__main__':
	yt_download_playlist()

