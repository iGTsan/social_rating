#!/bin/bash

# Reset head and index, keep working directory changes
git reset --keep 

# Pull latest changes, overwriting local
git pull origin main

# Reapply stashed changes if any
if [[ $(git stash list) != "" ]]; then
  git stash pop
fi