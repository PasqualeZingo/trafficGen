import os
def printFile(fname: str):
	f = fname + ".pdf"
	os.system("lp -U 'reciever' -h 'printer.luked.com' -d 'VPDF' " + f)
	return None

