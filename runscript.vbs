Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
WScript.Sleep(5000)
strArgs = "cmd /c py backup_folders.py"
oShell.Run strArgs, 0, false