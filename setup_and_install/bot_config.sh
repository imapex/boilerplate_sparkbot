#! /usr/bin/env bash

echo "This script will reconfigure your bot on the Cisco DevNet Mantl Sandbox"
echo "This will need to be done anytime you restart your bot.  Typically after "
echo "adding a new feature.  "
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
echo "    * Letters and Numbers only.  No Punctuation "
read bot_name
echo
echo "What is the email address of your bot?  "
read bot_email
echo
echo "What is the token for your bot?  "
read -s bot_token
echo



echo " "
echo "***************************************************"
echo "Looking for your bot at $control_address.  "
curl -k -X GET -u $mantl_user:$mantl_password https://$control_address:8080/v2/apps/$docker_username/$bot_name \
-H "Content-type: application/json" \
| python -m json.tool
echo

echo
echo "The bot listed above will be configured with the specified email and token."
echo "  Is this correct?  yes/no"
echo
read ANSWER

if [ $ANSWER != "yes" ]
then
    echo "Exiting without configuring bot"
    exit 0
fi



BOT_URL="http://$docker_username-$bot_name.$mantl_domain"
echo "BOT Address: $BOT_URL"
echo

echo "Checking if Bot is up"
HTTP_STATUS=$(curl -sL -w "%{http_code}" "$BOT_URL/health" -o /dev/null)
echo "HTTP Status: $HTTP_STATUS"
while [ $HTTP_STATUS -ne 200 ]
do
    echo "Bot not up yet, checking again in 30 seconds. "
    sleep 30
    HTTP_STATUS=$(curl -sL -w "%{http_code}" "$BOT_URL" -o /dev/null)
    echo "HTTP Status: $HTTP_STATUS"
done
echo
echo "Bot is up.  Configuring Spark."
echo "Bot Configuration: "
curl -X POST $BOT_URL/config \
    -d "{\"SPARK_BOT_TOKEN\": \"$bot_token\", \"SPARK_BOT_EMAIL\": \"$bot_email\"}"
echo

