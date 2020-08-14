import os #Allows sending commands to the bash terminal.
def printFile(fname: str)->None:
	"""
	Prints a file.
	args:
		fname (str): The name of the file to be printed. Must not contain the .pdf extension.
	"""
	#Add the .pdf extension to fname to get the full name of the file.
	f = fname + ".pdf"
	#Print the file. Replace the value of 'reciever' with a user with an existing home directory. Replace the value of 'cups_pdf.luked.com' with the name and domain of the server. Replace 'VPDF' with the name of the desired printer.
	os.system("lp -U 'reciever' -h 'cups_pdf.luked.com' -d 'VPDF' " + f)
	return None

#Print the file "printThis.pdf". 
printFile("printThis")
