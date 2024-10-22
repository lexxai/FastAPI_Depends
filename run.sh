#!/bin/sh

sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

cd fastapi_learn
fastapi run main.py