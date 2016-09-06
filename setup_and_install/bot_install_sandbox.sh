#! /usr/bin/env bash

echo "This script will install your bot on the Cisco DevNet Mantl Sandbox"
echo
echo "The details on the Sandbox can be found at: "
echo "    https://devnetsandbox.cisco.com/ "
echo "You can access the Sandbox at: "
echo "    https://mantlsandbox.cisco.com "
echo "    user/pass: admin/1vtG@lw@y"
echo

control_address=mantlsandbox.cisco.com
mantl_user=admin
mantl_password=1vtG@lw@y
mantl_domain=app.mantldevnetsandbox.com

echo Please provide the following details on your bot.
echo "What is the your Docker Username?  "
read docker_username
echo
echo "What is the name of your bot?  "
read bot_name
echo
echo "What is the email address of your bot?  "
read bot_email
echo
echo "What is the token for your bot?  "
read -s bot_token
echo
echo "Your bot will be deployed based on the 'latest' tag of Docker Container at: "
echo "    https://hub.docker.com/r/$docker_username/$bot_name/"
echo "Is this correct?  yes/no"
echo
read ANSWER

if [ $ANSWER != "yes" ]
then
    echo "Exiting without installing bot"
    exit 0
fi

cp sample_marathon_app_def.json $docker_username-$bot_name-sandbox.json
sed -i "" -e "s/DOCKERUSER/$docker_username/g" $docker_username-$bot_name-sandbox.json
sed -i "" -e "s/DOCKERREPO/$bot_name/g" $docker_username-$bot_name-sandbox.json

sed -i "" -e "s/USERNAME/$docker_username/g" $docker_username-$bot_name-sandbox.json
sed -i "" -e "s/BOTNAME/$bot_name/g" $docker_username-$bot_name-sandbox.json
sed -i "" -e "s/BOTEMAIL/$bot_email/g" $docker_username-$bot_name-sandbox.json
sed -i "" -e "s/BOTTOKEN/$bot_token/g" $docker_username-$bot_name-sandbox.json
sed -i "" -e "s/APPDOMAIN/$mantl_domain/g" $docker_username-$bot_name-sandbox.json



echo " "
echo "***************************************************"
echo "Installing the Bot as  $docker_username/$bot_name"
curl -k -X POST -u $mantl_user:$mantl_password https://$control_address:8080/v2/apps \
-H "Content-type: application/json" \
-d @$docker_username-$bot_name-sandbox.json \
| python -m json.tool

echo "***************************************************"
echo

echo Installed

echo "Wait 2-3 minutes for your bot to deploy. "
echo "Your bot will be deployed to "
echo
echo "http://$docker_username-$bot_name.$mantl_domain/"
echo
echo "You should be able to send a message to yourself from the bot by using this call"
echo
echo "http://$docker_username-$bot_name.$mantl_domain/hello/<YOUR EMAIL ADDRESS>"
echo
echo "You can also watch the progress from the GUI at: "
echo
echo "https://$control_address/marathon"
echo
