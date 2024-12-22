set AppleScript's text item delimiters to linefeed
tell application "Finder"
	set NewList to {}
	set SelList to text items of (selection as text)
	repeat with I in SelList
		set B to POSIX path of I
		set end of NewList to B
	end repeat
	return NewList as text
end tell
