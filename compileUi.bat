@echo off
echo "Generating MainWindow.ui"
call pyuic5 src\ui\MainWindow.ui > src\ui\MainWindowUI.py

echo "Generating Options.ui"
call pyuic5 src\ui\Options.ui > src\ui\OptionsUI.py

echo "Generating EdceVerification.ui"
call pyuic5 src\ui\EdceVerification.ui > src\ui\EdceVerificationUI.py

echo "Generating SearchTab.ui"
call pyuic5 src\ui\SearchTab.ui > src\ui\SearchTabUI.py

echo "Generating Status.ui"
call pyuic5 src\ui\Status.ui > src\ui\StatusUI.py

