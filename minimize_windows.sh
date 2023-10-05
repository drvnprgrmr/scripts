#!/bin/bash

# Get list of visible windows ids
windows=$(xdotool search --onlyvisible ".*")

# Loop through each window
for win in $windows 
do
	# Get the window's desktop number
	win_desk=$(xdotool get_desktop_for_window $win 2>/dev/null)

	# Check if the window is in a valid desktop
	if (( $win_desk != -1 )); then

		# Minimize the window
		xdotool windowminimize $win
       	fi
	
done




