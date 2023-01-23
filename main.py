#!/usr/bin/env python

import time, os, io, sys
from pypresence import Presence
from urllib.parse import unquote
cid = "783900573388111922"

# Função pra pegar a música e retornar as infos em dict
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

# Início do programa, pelo amor de deus, não sei como fazer isso funcionar corretamente

connected = False
running = False


def try_to_connect():
	global RPC
	global connected
	global running

	while connected == False and running == False:

		try:
			RPC = Presence(cid)
			RPC.connect()
			connected = True

			print("aprich started.\n\n")


			RPC.update(
				state="Nenhum player aberto",
				details="<Waiting for Player>",
				large_image='cardinal_anime',
				large_text="Cardinal",
				small_text="<No disponible players>",
			)
			
			running = True
			
		except ConnectionRefusedError:
			print("Erro de conexão com o discord, tentando novamente....")
			connected = False

		except Exception as e:
			print(str(e))
			print("algum erro desconhecido ocorreu, tentando novamente...")
			connected = False




# Pequena gambiarra pra atualizar e deixar algo na "ram", só pra iniciar o RPC.update()
ram = getSong()

# Verifica se a música é a mesma da var "ram"
def haschanged() -> bool:
	global ram

	if getSong() == ram:
		return False
	else:
		ram = getSong()
		return True


# Atualiza as informações, no geral
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


	# Implementação que ainda não funciona como deveria
	ctr = (
		connected == True,
		running == True
		)

	if all(ctr):
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

	else:
		print("Not connected or not running yet... try again")

# atualização só pra não quebrar com a "ram"
updateSong()

while True:
	if not connected:
		# aquela função la no começo com while not connected
		try_to_connect()
	else:
		try:
			# verifica se mudou e então atualiza com o updateSong()
			if haschanged():
				os.system("clear")
				updateSong()
				
		# Caso use Ctrl+C durante o código
		except KeyboardInterrupt:
			os.system("clear")
			print("================================")
			print("\nClosing...\n\nThanks for using my little script <3\nPT_BR: Obrigada por usar meu pequeno script <3 !!!\n")
			print("================================")
			
			time.sleep(1.5)
			os.system("clear")
			sys.exit(0)
