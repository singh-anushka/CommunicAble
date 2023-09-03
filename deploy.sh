#!/bin/bash
cd ~/CommunicAble
git stash
git pull origin master

cd backend
pipenv install
pipenv run uvicorn app.main:app --host 0.0.0.0 --port 8000

sudo service nginx restart