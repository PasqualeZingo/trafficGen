import os
def printFile(fname: str):
	f = fname + ".pdf"
	os.system("lp -U 'reciever' -h 'cups_pdf.luked.com' -d 'VPDF' " + f)
	return None
printFile("printThis")
