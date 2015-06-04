; example1.nsi
!include x64.nsh 
SetCompressor /SOLID /FINAL LZMA
;--------------------------------

; The name of the installer
Name "Elite Merchant"

; The file to write
OutFile "EliteMerchantInstaller.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\Elite Merchant"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

InstallDirRegKey HKLM "Software\EliteMerchant" "Install_Dir"

Function .onInit
        ${If} ${RunningX64}
        ${EnableX64FSRedirection}
        ${else}
        MessageBox MB_OK "Sorry this application runs only on x64 machines"
        Abort
        ${EndIf}
        StrCpy '$INSTDIR' '$PROGRAMFILES\EliteMerchant'

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
Section "Elite Merchant (required)" ;No components page, name is not important
  SectionIn RO
  
  SetOutPath $INSTDIR\platforms
  File src\dist\platforms\*

  SetOutPath $INSTDIR\requests
  File src\dist\requests\*
  
  SetOutPath $INSTDIR\imageformats
  File src\dist\imageformats\*
  
  SetOutPath $INSTDIR\mediaservice
  File src\dist\mediaservice\*
  
  SetOutPath $INSTDIR\sounds
  File src\dist\sounds\*
  
  SetOutPath $INSTDIR
  File src\dist\*
  
  WriteRegStr HKLM SOFTWARE\Software\EliteMerchant "Install_Dir" "$INSTDIR"
  
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteMerchant" "DisplayName" "Elite Merchant"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteMerchant" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteMerchant" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteMerchant" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
SectionEnd ; end the section

Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Elite Merchant"
  CreateShortcut "$SMPROGRAMS\Elite Merchant\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortcut "$SMPROGRAMS\Elite Merchant\Elite Merchant.lnk" "$INSTDIR\EliteMerchant.exe" "--UI" "$INSTDIR\EliteMerchant.exe" 0
  
SectionEnd


Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EliteMerchant"
  DeleteRegKey HKLM SOFTWARE\EliteDB

  ; Remove files and uninstaller
  Delete $INSTDIR\*
  Delete $INSTDIR\sounds\*
  Delete $INSTDIR\mediaservice\*
  Delete $INSTDIR\imageformats\*
  Delete $INSTDIR\platforms\*
  Delete $INSTDIR\requests\*

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Elite Merchant\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\Elite Merchant"
  RMDir "$INSTDIR\sounds"
  RMDir "$INSTDIR\mediaservice"
  RMDir "$INSTDIR\imageformats"
  RMDir "$INSTDIR\platforms"
  RMDir "$INSTDIR\requests"
  RMDir "$INSTDIR"

SectionEnd