#!/usr/bin/env python

import os
import time
import argparse
import pypresence


from urllib.parse import unquote, quote
from argparse import Namespace, ArgumentParser

ID = "783900573388111922"
DELAY = 1.5


ENABLE_PROJECT_GITHUB_BUTTON = False
IMAGE = "3dhp_black"


rpc = None
past_buf = None
curr_buf = None


class UserOptions:
	@staticmethod
	def get_args() -> Namespace:
		"""Function with all the argument configuration using the ``argparser``
		library that return the arguments given by the user in a ease to use
		``Namespace`` object.
		"""
		parser: ArgumentParser = ArgumentParser(description='Simple Script to show playing music on Discord')

		parser.add_argument('--enable-github-button', '-b', action=argparse.BooleanOptionalAction, default=False, help="Shows Aprich Project button linked to github")

		parser.add_argument('--image', '-i', type=str, default="3dhp_black", help="Default rich presence image.")
	
		return parser.parse_args()


class Display:
	@staticmethod
	def log(msg):
		print(f"\033[32mstatus ok:\033[m {msg}")

	@staticmethod
	def err(msg, err="error"):
		print(f"\033[31m{err}:\033[m {msg}")

	@staticmethod
	def status(ss, sn, sa):
		print(f"\033[34m\tstatus:\033[33m\t{ss}\033[m")
		print(f"\033[34m\tname:\033[33m\t{sn}\033[m")
		print(f"\033[34m\tartist:\033[33m\t{sa}\033[m")


class Discord:
	@staticmethod
	def connect(err_h=lambda err: None):
		try:
			rpc.connect()
		except Exception as err:
			return err_h(type(err))
		else:
			Display.log("connected with discord app")

	@staticmethod
	def update(state, details, large_image, large_text, small_text, buttons=[],
			   err_h=lambda err: None):
		try:
			rpc.update(state=state, details=details, large_image=large_image,
					   large_text=large_text, small_text=small_text,
					   buttons=buttons)
		except Exception as err:
			return err_h(type(err))
		else:
			Display.log("status updated")


class ErrHandler:
	@staticmethod
	def couldNotUpdate(err):
		Display.err("could not update the song status", err)
		Discord.connect(ErrHandler.couldNotConnect)
		return True

	@staticmethod
	def couldNotConnect(err):
		Display.err("discord not found", err)
		return True


def searchOnYoutube(songname, songartist) -> str:
	ysu = "https://youtube.com/search?q={query}"
	query = quote(str(songartist)+ " - " +str(songname))
	return str(ysu.format(query=query))




class Controllers:
	@staticmethod
	def getSong():
		isplaying: str = "Stopped"
		songName: str = None
		songArtist: str = None
		songYtsearch: str = None

		getplaying = os.popen("playerctl status").read()

		raw_meta = os.popen("playerctl metadata").read()
		linesplit = raw_meta.splitlines()

		if "Playing" in getplaying:
			isplaying = "Playing"
			for x in linesplit:
				if ":artist" in x:
					artist = x.split(":artist")
					songArtist = artist[1].replace(" "*14, "") + " "*2


			for y in linesplit:
				if ":title" in y:
					title = y.split(":title")
					songName = title[1].replace(" "*15, "") + " "*2

		elif "Stopped" in getplaying:
			isplaying = "Stopped"

		elif "Paused" in getplaying:
			isplaying = "Paused"
			for x in linesplit:
				if ":artist" in x:
					artist = x.split(":artist")
					songArtist = artist[1].replace(" "*14, "") + " "*2

			for y in linesplit:
				if ":title" in y:
					title = y.split(":title")
					songName = title[1].replace(" "*15, "") + " "*2

		else:
			isplaying = "Stopped"
			songArtist = "<Not playing>"
			songName = "<Waiting for Player>"

		if not all((songName, songArtist)):
			_raw = os.popen("playerctl metadata").read().splitlines()
			for line in _raw:
				if ":url" in line:
					raw_url = line.split(":url")
					url = raw_url[1].replace(" "*17, "") + " "*2
					url = unquote(url)

					rsn = url.split('/')[-1]
					isplaying = "Playing"
					songArtist = "<unknown>"
					songName = rsn
					songYtsearch = searchOnYoutube(songName, "*")

		else:
			songYtsearch = searchOnYoutube(songName, songArtist)



		return {"isplaying": isplaying, "songName": songName,
				"songArtist": songArtist, "youtubeSearch": songYtsearch}

	@staticmethod
	def hasChanded():
		global past_buf
		global curr_buf

		if curr_buf == past_buf:
			return False

		past_buf = curr_buf
		return True

	@staticmethod
	def updateSong():

		if past_buf is None:
			return

		sinfo = past_buf

		ss = sinfo['isplaying']
		sn = sinfo['songName']
		sa = sinfo['songArtist']
		su = sinfo['youtubeSearch']

		# Buttons
		rpbuttons = [{
				'label': "Search On Youtube",
				'url': su
			}
		]

		project_github_button = {
				'label': "Aprich Project",
				'url': 'https://github.com/hayukimori/aprich'
			}



		if ENABLE_PROJECT_GITHUB_BUTTON:
			rpbuttons.append(project_github_button)


		while Discord.update(sa, sn, IMAGE, ss, sa, buttons=rpbuttons, err_h=ErrHandler.couldNotUpdate):
			time.sleep(DELAY)

		Display.status(ss, sn, sa)

	@staticmethod
	def firstTime(err_h=lambda err: None):
		global rpc
		global curr_buf

		try:
			rpc = pypresence.Presence(ID)
			curr_buf = Controllers.getSong()
			Controllers.updateSong()

		except Exception as err:
			return err_h(type(err))

		else:
			Display.log("rich presence connected with discord")

	@staticmethod
	def eventLoop():
		global curr_buf

		while True:
			curr_buf = Controllers.getSong()

			if Controllers.hasChanded():
				Controllers.updateSong()

			time.sleep(DELAY)


def main():
	global ENABLE_PROJECT_GITHUB_BUTTON
	global IMAGE

	# Define default args based on cli args;
	newvars = UserOptions.get_args()
	ENABLE_PROJECT_GITHUB_BUTTON = newvars.enable_github_button
	IMAGE = newvars.image
	
	try:
		while Controllers.firstTime(ErrHandler.couldNotConnect):
			time.sleep(DELAY)
		Controllers.eventLoop()

	except KeyboardInterrupt as err:
		Display.err("interruped by user", type(err))
		rpc.close()


if __name__ == "__main__":
	main()
