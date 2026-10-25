-- prints: path <tab> enabled <tab> x <tab> y <tab> w <tab> h   (one per line)
-- Closed menu items have no usable position, so every item carries the
-- position of its TOP-LEVEL menu bar title.
property maxDepth : 2

on run argv
	set appName to item 1 of argv
	set res to ""
	tell application "System Events"
		tell process appName
			repeat with mbi in (menu bar items of menu bar 1)
				set topName to name of mbi
				if topName is not missing value then
					if topName is not "Apple" then
						set {posX, posY} to position of mbi
						set {sizeW, sizeH} to size of mbi
						set res to res & topName & tab & "true" & tab & posX & tab & posY & tab & sizeW & tab & sizeH & linefeed
						try
							set res to res & my walk(menu 1 of mbi, topName, 1, posX, posY, sizeW, sizeH)
						end try
					end if
				end if
			end repeat
		end tell
	end tell
	return res
end run

on walk(theMenu, parentPath, level, posX, posY, sizeW, sizeH)
	set res to ""
	tell application "System Events"
		repeat with mi in (menu items of theMenu)
			set itemName to name of mi
			if itemName is not missing value then
				if itemName is not "" then
					set fullPath to parentPath & " > " & itemName
					set isOn to enabled of mi
					set res to res & fullPath & tab & isOn & tab & posX & tab & posY & tab & sizeW & tab & sizeH & linefeed
					if level < maxDepth then
						try
							set res to res & my walk(menu 1 of mi, fullPath, level + 1, posX, posY, sizeW, sizeH)
						end try
					end if
				end if
			end if
		end repeat
	end tell
	return res
end walk
