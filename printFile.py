def printFile(fname: str):
	f = fname + ".pdf"
	os.system("lpr " + f)
	return None
