Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
WScript.Sleep(300000)
strArgs = "cmd /c py backup_folders.py"
oShell.Run strArgs, 1, false
