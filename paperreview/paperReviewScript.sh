#!/usr/bin/env bash

CLASS = "cs491x"


# GET INPUT INFORMATION
echo "Week of the paper review, followed by [Enter]:"
read WEEK

echo "Name of paper, followed by [Enter]:"
read PAPERNAME

echo "Name of the review, followed by [Enter]:"
read REVIEWNAME

# cp template folder to new location
if [[ ! -d "wk$WEEK" ]]; then
	echo "Creating Week Directory..."
	mkdir -p "wk$WEEK"
fi

if [[ ! -d "wk$WEEK/$PAPERNAME" ]]; then
	# create paper directory
	echo "Copying Review Files..."
	cp -r template "wk$WEEK/$PAPERNAME"
	echo "Renaming Review Files"
	mv "wk$WEEK/$PAPERNAME/FraserLuke.tex" "wk$WEEK/$PAPERNAME/$REVIEWNAME.tex"
else
	echo "Error: Review already exists"
	exit -1
fi

echo "Done!"
exit 1