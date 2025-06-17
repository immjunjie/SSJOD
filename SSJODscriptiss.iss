[Setup]
AppName=SSJOD
AppVersion=1.0
DefaultDirName={localappdata}\SSJOD
DefaultGroupName=SSJOD
OutputDir=Output
OutputBaseFilename=SSJOD-Setup
SetupIconFile=frontend\static\SSjodBoat.ico

[Files]
Source: "dist\SSjodex\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SSJOD"; Filename: "{app}\SSJOD.exe"
Name: "{autodesktop}\SSJOD"; Filename: "{app}\SSJOD.exe"

[Run]
Filename: "{app}\SSJOD.exe"; Description: "Launch SSJOD"; Flags: nowait postinstall skipifsilent