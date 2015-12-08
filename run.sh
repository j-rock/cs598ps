#! /bin/bash
# Run the main classifier

if [ $# -eq 1 ]; then
    python src/py/main.py "$1"
elif [ $# -eq 3 ]; then
    python src/py/main.py "$1" "$2" "$3"
else
    python src/py/main.py
fi
