#! /usr/bin/env bash

echo "This script will uninstall your bot from the Cisco DevNet Mantl Sandbox"
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
echo
echo "Mantl/Marathon application of: "
echo "   $docker_username/$bot_name from https://mantlsandbox.cisco.com/marathon "
echo " will be destroyed."
echo "App details: "
echo

curl -k -X GET -u $mantl_user:$mantl_password https://$control_address:8080/v2/apps/$docker_username/$bot_name \
-H "Content-type: application/json" | python -m json.tool

echo
echo "Is this correct?  yes/no"
echo
read ANSWER

if [ $ANSWER != "yes" ]
then
    echo "Exiting without removing anything"
    exit 0
fi

echo
echo "Uninstalling the bot at $docker_username/$bot_name"
curl -k -X DELETE -u $mantl_user:$mantl_password https://$control_address:8080/v2/apps/$docker_username/$bot_name \
-H "Content-type: application/json"
echo

