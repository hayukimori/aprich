#!/usr/bin/env python

import time, os, io, sys
from pypresence import Presence
from urllib.parse import unquote
cid = "783900573388111922"

RPC = Presence(cid)
RPC.connect()
print("Programa Iniciado.\n\n")

RPC.update(
	state="Nenhum player aberto",
	details="<Waiting for Player>",
	large_image='cardinal_anime',
	large_text="Cardinal",
	small_text="<No disponible players>",
)




def getSong() -> dict:
	isplaying: str = "Stopped"
	songName: str = None
	songArtist: str = None

	getplaying = os.popen("playerctl status").read()

	# Metadata
	raw_meta = os.popen("playerctl metadata").read()
	linesplit = raw_meta.splitlines()


	# Playing status
	if "Playing" in getplaying:
		isplaying = "Playing"
		for x in linesplit:
			if ":artist" in x:
				artist = x.split(":artist")
				songArtist = artist[1].replace("              ", "")

		for y in linesplit:
			if ":title" in y:
				title = y.split(":title")
				songName = title[1].replace("               ", "")



	elif "Stopped" in getplaying:
		isplaying = "Stopped"


	elif "Paused" in getplaying:
		isplaying = "Paused"
		for x in linesplit:
			if ":artist" in x:
				artist = x.split(":artist")
				songArtist = artist[1].replace("              ", "")

		for y in linesplit:
			if ":title" in y:
				title = y.split(":title")
				songName = title[1].replace("               ", "")


	else:
		isplaying = "Stopped"
		songArtist = "<Not playing>"
		songName = "<Waiting for Player>"


	# Filter

	cnd = (
		songName == None,
		songArtist == None
		)

	if any(cnd):
		_raw = os.popen("playerctl metadata").read().splitlines()
		for line in _raw:
			if ":url" in line:
				raw_url = line.split(":url")
				url = raw_url[1].replace("                 ", '')
				url = unquote(url)

				rsn = url.split('/')[-1]
				
				songArtist = "<unknown>"
				songName = rsn


	return {
	'isplaying': isplaying, 
	'songName': songName, 
	'songArtist': songArtist
	}


getSong()
ram = getSong()



def haschanged() -> bool:
	global ram

	if getSong() == ram:
		return False
	else:
		ram = getSong()
		return True


def updateSong():
	try:
		sinfo = ram

		ss=sinfo['isplaying']
		sn=sinfo['songName']
		sa=sinfo['songArtist']

		if len(sn) < 2:
			sn = "Fail to read song title"

		if len(sa) < 2:
			sa = "Fail to read song title"



	except Exception as e:
		print(str(e))
		sinfo = {
			'isplaying': "Stopped",
			'songName': "None",
			'songArtist': "None"
		}
		ss=sinfo['isplaying']
		sn=sinfo['songName']
		sa=sinfo['songArtist']




	RPC.update(
		state=sa,
		details=sn,
		large_image='3dhp',
		large_text=ss,
		small_text=sa,
		buttons=[{'label': "Hayukimori's Github", 'url': 'https://github.com/hayukimori'}]
	)

	print("==========================")
	print(f"SS:\t{ss}")
	print(f"SN:\t{sn}")
	print(f"SA:\t{sa}")
	print("==========================")

updateSong()

while True:
	try:
		if haschanged():
			os.system("clear")
			updateSong()
	except KeyboardInterrupt:
		os.system("clear")
		print("================================")
		print("\nKeyboardInterrupt signal received\n. Closing...\n\nThanks for using my little script <3\n\n\nPT_BR: Obrigada por usar meu pequeno script <3 !!!")
		print("================================")
		
		time.sleep(1)
		os.system("clear")
		sys.exit(0)
