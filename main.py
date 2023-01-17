import time, os, io, sys
from pypresence import Presence
cid = "783900573388111922"

RPC = Presence(cid)
RPC.connect()
print("Programa Iniciado.\n\n")

RPC.update(
	state="Nenhum player aberto",
	details="<Esperando por player>",
	large_image='cardinal_anime',
	large_text="Cardinal",
	small_text="<Nenhum player disponível>",
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

	elif "No players found" in getplaying:
		isplaying = "Stopped"
		songArtist = "<Não estou tocando>"
		songName = "<Esperando por player>"


	else:
		isplaying = "Stopped"
		songArtist = "<Não estou tocando>"
		songName = "<Esperando por player>"




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
		buttons=[{'label': 'Meu Github', 'url': 'https://github.com/hayukimori'}]
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
		print("\n\nSinal de saída Ctrl+C detectado. Saindo...\n\nObrigada por usar o programa!!!")
		time.sleep(1)
		os.system("clear")
		sys.exit(0)

	

'''
while True:
	sinfo = getSong()

	RPC.update(
		state=sinfo['songArtist'],
		details=sinfo['songName'],
		large_image='cardinal_anime',
		large_text=sinfo['isplaying'],
		small_text=sinfo['songArtist'],
		start=time.time()
		)

	print("==========================")
	print(f"SS:\t{sinfo['isplaying']}")
	print(f"SN:\t{sinfo['songName']}")
	print(f"SA:\t{sinfo['songArtist']}")
	print("==========================")

	time.sleep(.8)
	os.system("clear")
'''