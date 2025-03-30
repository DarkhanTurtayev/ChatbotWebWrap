#!/bin/bash

detect_os() {
  case "$OSTYPE" in
    darwin*) echo "macOS" ;;
    msys*) echo "Windows" ;;
    *) echo "unknown" ;;
  esac
}

echo "Installing Python dependencies..."

if ! command -v pip &> /dev/null
then
    echo "pip not found, installing..."
    python -m ensurepip --upgrade
fi

pip install flask

echo "Creating SQLite database..."
python sql_table.py  

if [ $? -ne 0 ]; then
    echo "Database creation failed. Please check the sql_table.py script."
    exit 1
fi

echo "Starting ngrok..."

if [ "$(detect_os)" == "macOS" ]; then
    osascript -e 'tell application "Terminal" to do script "ngrok http 6000"'
elif [ "$(detect_os)" == "Windows" ]; then
    start cmd /k "ngrok http 6000"
else
    ./ngrok http 6000 &  
    echo "Else running"
fi

echo "Starting Flask server..."

python app.py  

echo "Setup complete!"