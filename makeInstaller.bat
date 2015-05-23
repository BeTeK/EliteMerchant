cd src
rmdir /Q /S dist
python3 setup.py py2exe
ren dist\main.exe EliteDB.exe
cd ..
makensis EliteDB.nsi
