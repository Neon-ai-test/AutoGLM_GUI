@echo off
echo Creating AutoGLM Desktop Application shortcut...
echo.

REM Get the current directory
set CURRENT_DIR=%cd%

REM Create a VBScript to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\AutoGLM Desktop.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CURRENT_DIR%\start_autoglm_desktop.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "AutoGLM Desktop Application" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Execute the VBScript
cscript //nologo CreateShortcut.vbs

REM Clean up
del CreateShortcut.vbs

echo.
echo Shortcut created on your desktop!
echo You can now double-click the "AutoGLM Desktop" shortcut to launch the application.
pause