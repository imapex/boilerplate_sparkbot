#!/usr/bin/env bash

echo What is your GitHub Username?
read GITHUBUSER
echo
echo What is your GitHub Password?
echo "  ** If you have 2 Factor Auth configured, "
echo "     provide a Personal Access Token with repo and delete_repo access."
echo "     Tokens can be generated at https://github.com/settings/tokens **"
read -s GITHUBPASS
echo
echo What is the name of your bot?
echo "  - A new GitHub repo will be created with this name"
read GITHUBREPO
echo

echo "Pulling down and prepping the code for the UI service."
wget https://github.com/imapex/boilerplate_sparkbot/archive/master.zip

echo
echo Creating new directory ./$GITHUBREPO with bot code
mkdir
unzip -qq master.zip -d ./$GITHUBREPO
rm master.zip
cd ./$GITHUBREPO
# Move the files into the root of the repo and cleanup folder
mv boilerplate_sparkbot-master/* ./
mv boilerplate_sparkbot-master/\.* ./
rm -Rf boilerplate_sparkbot-master

# Delete Drone Build files from boilerplate
rm .drone.sec
rm .drone.yml
rm drone-secrets-sample.yml

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


