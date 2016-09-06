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
echo "  - The name of your GitHub Repo and Local Code Directory that will be deleted"
read GITHUBREPO
echo

echo "Are you sure you want to delete your GitHub Repo $GITHUBUSER/$GITHUBREPO?"
echo "Type 'yes' to delete"
read ANSWER

if [ $ANSWER != "yes" ]
then
    echo "Exiting without deleting anything"
    exit 0
fi

echo "Beginning the cleanup process"
echo " "

echo "Deleting the Repo on GitHub"
curl -u $GITHUBUSER:$GITHUBPASS -X DELETE https://api.github.com/repos/$GITHUBUSER/$GITHUBREPO

echo "Deleting the local copy"
cd ../../
rm -Rf $GITHUBREPO

echo " "
echo " "
echo "The GitHub repo https://github.com/$GITHUBUSER/$GITHUBREPO has been deleted."
echo "The local instance has also been deleted."
echo " "

