#!/bin/bash

rm -f challenge.py
touch challenge.py
echo "$prompt" > challenge.py
nvim challenge.py
