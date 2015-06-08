del EliteMerchantInstaller*.exe
cd src
rmdir /Q /S dist
python3 setup.py py2exe
ren dist\main.exe EliteMerchant.exe
cd ..
makensis EliteMerchant.nsi
python3 renameInstaller.py
