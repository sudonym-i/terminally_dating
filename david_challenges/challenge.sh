
#!/bin/bash

# Accept prompt as first argument
PROMPT="$1"

rm -f challenge.py
touch challenge.py
echo "# $PROMPT" > challenge.py
echo "" >> challenge.py
nvim challenge.py
