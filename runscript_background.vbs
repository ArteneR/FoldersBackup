Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
WScript.Sleep(12000)
strArgs = "cmd /c py backup_folders.py"
oShell.Run strArgs, 0, false
