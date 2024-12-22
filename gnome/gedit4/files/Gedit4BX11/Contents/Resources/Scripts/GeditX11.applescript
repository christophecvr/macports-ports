#!/usr/bin/env osascript
use framework "Foundation"
use scripting additions

--global GeditExec and set GeditExec to <...>does not work use property to declare and use a global value at top level.
property GeditExec : "export PATH=/opt/geditb/bin:/opt/geditb/sbin:$PATH;exec gedit"

-- when using open command without file.
-- when clicking on application in finder.
on run
	set text item delimiters to linefeed
	-- We log some actions into ~/Library/Logs/aGeditX11.log
	set myHomePath to system attribute "HOME"
	set myLogFile to myHomePath & "/Library/Logs/aGeditX11.log" as text
	set myFile to open for access (myLogFile) with write permission
	set eof myFile to 0
	write "We can use this to log Gedit3 starter actions" to myFile starting at eof
	close access myFile
	set envPWD to {}
	set envPWD to system attribute "PWD"
	-- if is true Gedit is launched from terminal with open command
	if envPWD is not equal to {} and envPWD is not equal to "" then
		set AppArgs to (current application's NSProcessInfo's processInfo's arguments) as list
		set AppArgsNumbers to count of AppArgs
		set AppXargs to {}
		if AppArgsNumbers is greater than 1 then
			set AppArgsCnt to 0
			repeat with I in AppArgs
				set AppArgsCnt to (AppArgsCnt + 1)
				if AppArgsCnt is greater than 1 then
					set end of AppXargs to quoted form of text of I as text
				end if
			end repeat
			-- open command used no file but there are arguments set
			set text item delimiters to " "
			do shell script GeditExec & " " & AppXargs & " &> /dev/null &"
			set text item delimiters to linefeed
		else
			-- open command used no file or argument set
			do shell script GeditExec & " &> /dev/nul &"
		end if
		--else gedit is launched by click on the application in finder
	else
		do shell script GeditExec & " &> /dev/null &"
	end if
end run

-- when using open command with a file to open
-- When opening selected files in finder with Gedit3
on open SelFiles
	set text item delimiters to linefeed
	-- We log some actions into ~/Library/Logs/aGeditX11.log	
	set myHomePath to system attribute "HOME"
	set myLogFile to myHomePath & "/Library/Logs/aGeditX11.log" as text
	set myFile to open for access (myLogFile) with write permission
	set eof myFile to 0
	write "We can use this to log Gedit3 starter actions" to myFile starting at eof
	close access myFile
	set envPWD to {}
	set envPWD to system attribute "PWD"
	-- if is true when Gedit3 is launched from terminal with open
	if envPWD is not equal to {} and envPWD is not equal to "" then
		set AppArgs to (current application's NSProcessInfo's processInfo's arguments) as list
		set AppArgsNumbers to count of AppArgs
		set AppXargs to {}
		if AppArgsNumbers is greater than 1 then
			set AppArgsCnt to 0
			repeat with I in AppArgs
				set AppArgsCnt to (AppArgsCnt + 1)
				if AppArgsCnt is greater than 1 then
					set end of AppXargs to quoted form of text of I as text
				end if
			end repeat
		end if
		repeat with I in SelFiles
			set aSelFile to quoted form of text of POSIX path of I as text
			if AppArgsNumbers is greater than 1 then
				set text item delimiters to " "
				-- open command used in terminal with file(s) and arguments.
				do shell script GeditExec & " " & aSelFile & " " & AppXargs & " &> /dev/null &"
				set text item delimiters to linefeed
			else
				-- open command used in terminal with one or more files. No arguments.
				do shell script GeditExec & " " & aSelFile & " &> /dev/null &"
			end if
		end repeat
		-- the else will be used when using Gedit 3 to open selected files in finder
	else
		repeat with I in SelFiles
			set aSelFile to quoted form of text of POSIX path of I as text
			-- opening one or more selected files in finder with Gedit.
			do shell script GeditExec & " " & aSelFile & " &> /dev/null &"
		end repeat
	end if
end open
