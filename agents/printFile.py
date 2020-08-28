"""
A script to print printThis.pdf on print server cups_pdf.luked.com as user reciever with printer VPDF.

Functions
---------
printFile(fname: str)->None
    print file fname.
"""
import os #Allows sending commands to the bash terminal to send a print request to the server through the lp command.
def printFile(fname: str)->None:
    """
    IF fname does not end with ".pdf", add it to the end. Print file fname on server cups_pdf.luked.com as user reciever on printer VPDF, and return nothing. The printed output will be found on the server at /home/reciever/PDF.

    args:
        fname (str): The name of the file to be printed. If the file given does not end with ".pdf", the extension will be added automatically.
    """
    #Add the .pdf extension if not present to fname to get the full name of the file.
    if fname[-4:] != ".pdf":
        fname += ".pdf"
    #Print the file. Replace the value of 'reciever' with a user with an existing home directory. Replace the value of 'cups_pdf.luked.com' with the name and domain of the server. Replace 'VPDF' with the name of the desired printer.
    os.system("lp -U 'reciever' -h 'cups_pdf.luked.com' -d 'VPDF' " + fname)
    return None

#Print the file "printThis.pdf". 
printFile("printThis")
