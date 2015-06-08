import os

with open(os.path.join("src", "version.txt"), "rb") as file:
	line = file.read().decode("LATIN-1").replace("\n", "").replace("\r", "").replace(" ", "")
	os.rename("EliteMerchantInstaller.exe", "EliteMerchantInstaller_v{0}.exe".format(line))
	