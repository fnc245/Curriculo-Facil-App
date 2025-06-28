; setup_script.iss
; Script para Inno Setup - Currículo Fácil

[Setup]
AppName=Currículo Fácil
AppVersion=2.0
AppPublisher=Francisco Neves Carvalho Filho
DefaultDirName={autopf}\CurriculoFacil
DefaultGroupName=Currículo Fácil
OutputBaseFilename=CurriculoFacil-v2.0-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\CurriculoFacil.exe

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

[Files]
; Pega TUDO da pasta de saída do PyInstaller e coloca no diretório de instalação do usuário.
Source: "dist\CurriculoFacil\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
; Cria a pasta para os currículos gerados, garantindo que ela exista na instalação.
Name: "{app}\curriculos_gerados"

[Icons]
Name: "{group}\Currículo Fácil"; Filename: "{app}\CurriculoFacil.exe"
Name: "{group}\{cm:ProgramOnTheWeb,Currículo Fácil}"; Filename: "https://github.com/fnc245"
Name: "{group}\{cm:UninstallProgram,Currículo Fácil}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Currículo Fácil"; Filename: "{app}\CurriculoFacil.exe"; Tasks: desktopicon

[Run]
; Executa a aplicação no final da instalação, se o usuário marcar a caixa.
Filename: "{app}\CurriculoFacil.exe"; Description: "{cm:LaunchProgram,Currículo Fácil}"; Flags: nowait postinstall shellexec