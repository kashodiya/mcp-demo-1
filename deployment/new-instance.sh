#!/bin/bash

# Create the ~/apps-bmo directory if it doesn't exist
if [ ! -d "$HOME/apps-bmo" ]; then
    mkdir "$HOME/apps-bmo"
fi

# Find the next available port number
start_port=7170
while [ -d "$HOME/apps-bmo/$start_port" ]; do
    start_port=$((start_port + 1))
done

# Create a new directory for the application
new_dir="$HOME/apps-bmo/$start_port"
mkdir "$new_dir"

# Clone the repository and install dependencies
git clone https://github.com/kashodiya/mcp-demo-1.git "$new_dir"
cd "$new_dir"
uv sync


# Generate a 6-digit random number string
RANDOM_NUMBER=$(printf "%06d" $((RANDOM % 1000000)))

# Create the start.sh file
cat << EOF > start.sh
export PASS=$RANDOM_NUMBER
uvicorn main:app --reload --port $start_port --host 0.0.0.0
EOF

# Make the start.sh file executable
chmod +x start.sh

echo "start.sh file created with password: $RANDOM_NUMBER"

echo App is installed in $new_dir. Run using start.sh.
