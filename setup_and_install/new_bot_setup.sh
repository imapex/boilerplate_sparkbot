#!/usr/bin/env bash

# TODO - change the source branch from dev to master before publish

echo What is your GitHub Username?
read GITHUBUSER
echo
echo What is your GitHub Password?
read -s GITHUBPASS
echo
echo What is the name of your bot?
echo "  - A new GitHub repo will be created with this name"
read GITHUBREPO
echo

echo "Pulling down and prepping the code for the UI service."
wget https://github.com/imapex/boilerplate_sparkbot/archive/dev.zip

echo
echo Creating new directory ./$GITHUBREPO with bot code
mkdir
unzip -qq dev.zip -d ./$GITHUBREPO
rm dev.zip
cd ./$GITHUBREPO
# Move the files into the root of the repo and cleanup folder
mv boilerplate_sparkbot-dev/* ./
mv boilerplate_sparkbot-dev/\.* ./
rm -Rf boilerplate_sparkbot-dev
# Delete unneeded files from boilerplate
rm .drone.sec

echo
echo Creating new GitHub Repo
curl -u $GITHUBUSER:$GITHUBPASS -X POST \
    https://api.github.com/user/repos \
    -d '{"name": "'$GITHUBREPO'"}' \
    -o /dev/null

echo
echo "Setting up Local GitHub Repo and pushing to GitHub."
git init
git add .
git commit -m "First commit"
git remote add origin https://github.com/$GITHUBUSER/$GITHUBREPO.git
git push -u origin master

echo " "
echo " "
echo "Your new Spark Bot has been prepped in repo https://github.com/$GITHUBUSER/$GITHUBREPO."
echo "Now begin customizing the bot code in the file bot/bot.py"
echo "  "


