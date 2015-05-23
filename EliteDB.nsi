; example1.nsi
!include x64.nsh 

;--------------------------------

; The name of the installer
Name "Example1"

; The file to write
OutFile "EliteDBInstaller.exe"

; The default installation directory
InstallDir $PROGRAMFILES\EliteDB

; Request application privileges for Windows Vista
RequestExecutionLevel admin

InstallDirRegKey HKLM "Software\EliteDB" "Install_Dir"

Function .onInit
        ${If} ${RunningX64}
        ${DisableX64FSRedirection}
        ${else}
        MessageBox MB_OK "Sorry this application runs only on x64 machines"
        Abort
        ${EndIf}
        StrCpy '$INSTDIR' '$PROGRAMFILES\My Application'

FunctionEnd
;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "EliteDB (required)" ;No components page, name is not important
  SectionIn RO
  
  SetOutPath $INSTDIR
  
  File src\dist\*
  
  SetOutPath $INSTDIR\platforms
  File src\dist\platforms\*
  
  WriteRegStr HKLM SOFTWARE\Software\EliteDB "Install_Dir" "$INSTDIR"
  
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteDB" "DisplayName"EliteDB"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteDB" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteDB" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteDB" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
SectionEnd ; end the section

Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\EliteDB"
  CreateShortcut "$SMPROGRAMS\EliteDB\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortcut "$SMPROGRAMS\EliteDB\EliteDB.lnk" "$INSTDIR\EliteDB.exe" "--UI" "$INSTDIR\EliteDB.exe" 0
  
SectionEnd


Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteDB"
  DeleteRegKey HKLM SOFTWARE\EliteDB

  ; Remove files and uninstaller
  Delete $INSTDIR\*

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\EliteDB\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\EliteDB"
  RMDir "$INSTDIR"

SectionEnd