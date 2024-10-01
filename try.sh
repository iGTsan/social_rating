#!/bin/bash

# Pull latest changes, overwriting local
git pull

sudo docker compose up -d --build