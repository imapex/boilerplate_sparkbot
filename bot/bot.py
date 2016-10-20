#! /usr/bin/python
"""
    boilerplate_sparkbot

    This is a sample boilerplate application that provides the framework to quickly
    build and deploy an interactive Spark Bot.

    There are different strategies for building a Spark Bot.  You can either create
    a new dedicated Spark Account for the bot, or create an "Bot Account" underneath
    another Spark Account.  Either type will work with this boilerplate, just be sure
    to provide the correct token and email account in the configuration.

    This Bot will use a provided Spark Account (identified by the Developer Token)
    and create a webhook to receive all messages sent to the account.   You will
    specify a set of command words that the Bot will "listen" for.  Any other message
    sent to the bot will result in the help message being sent back.

    The bot is designed to be deployed as a Docker Container, and can run on any
    platform supporting Docker Containers.  Mantl.io is one example of a platform
    that can be used to run the bot.

    There are several pieces of information needed to run this application.  These
    details can be provided as Environment Variables to the application.  The Spark
    token and email address can alternatively be provided/updated via an POST request to /config.

    If you are running the python application directly, you can set them like this:

    # Details on the Cisco Spark Account to Use
    export SPARK_BOT_EMAIL=myhero.demo@domain.com
    export SPARK_BOT_TOKEN=adfiafdadfadfaij12321kaf

    # Public Address and Name for the Spark Bot Application
    export SPARK_BOT_URL=http://myhero-spark.mantl.domain.com
    export SPARK_BOT_APP_NAME="imapex bot"

    If you are running the bot within a docker container, they would be set like this:
    # ToDo - Add docker run command
    docker run -it --name sparkbot \
    -e "SPARK_BOT_EMAIL=myhero.demo@domain.com" \
    -e "SPARK_BOT_TOKEN=adfiafdadfadfaij12321kaf" \
    -e "SPARK_BOT_URL=http://myhero-spark.mantl.domain.com" \
    -e "SPARK_BOT_APP_NAME='imapex bot'" \
    sparkbot

    # ToDo - API call for configuring the Spark info

    In cases where storing the Spark Email and Token as Environment Variables could
    be a security risk, you can alternatively set them via a REST request.

    curl -X POST http://localhost:5000/config \
        -d "{\"SPARK_BOT_TOKEN\": \"<TOKEN>\", \"SPARK_BOT_EMAIL\": \"<EMAIL>"}"

    You can read the configuration details with this request

    curl http://localhost:5000/config

"""

from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
import os
import sys
import json

# Create the Flask application that provides the bot foundation
app = Flask(__name__)


# The list of commands the bot listens for
# Each key in the dictionary is a command
# The value is the help message sent for the command
commands = {
    "/echo": "Reply back with the same message sent.",
    "/help": "Get help."
}


# Not strictly needed for most bots, but this allows for requests to be sent
# to the bot from other web sites.  "CORS" Requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,Key')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Entry point for Spark Webhooks
@app.route('/', methods=["POST"])
def process_webhook():
    # Check if the Spark connection has been made
    if spark is None:
        sys.stderr.write("Bot not ready.  \n")
        return "Spark Bot not ready.  "

    post_data = request.get_json(force=True)
    # Uncomment to debug
    # sys.stderr.write("Webhook content:" + "\n")
    # sys.stderr.write(str(post_data) + "\n")

    # Take the posted data and send to the processing function
    process_incoming_message(post_data)
    return ""


# Config Endpoint to set Spark Details
@app.route('/config', methods=["GET", "POST"])
def config_bot():
    if request.method == "POST":
        post_data = request.get_json(force=True)
        # Verify that a token and email were both provided
        if "SPARK_BOT_TOKEN" not in post_data.keys() or "SPARK_BOT_EMAIL" not in post_data.keys():
            return "Error: POST Requires both 'SPARK_BOT_TOKEN' and 'SPARK_BOT_EMAIL' to be provided."

        # Setup Spark
        spark_setup(post_data["SPARK_BOT_EMAIL"], post_data["SPARK_BOT_TOKEN"])

    # Return the config detail to API requests
    config_data = {
        "SPARK_BOT_EMAIL": bot_email,
        "SPARK_BOT_TOKEN": spark_token,
        "SPARK_BOT_URL": bot_url,
        "SPARKBOT_APP_NAME": bot_app_name
    }
    config_data["SPARK_BOT_TOKEN"] = "REDACTED"     # Used to hide the token from requests.
    return json.dumps(config_data)


# Quick REST API to have bot send a message to a user
@app.route("/hello/<email>", methods=["GET"])
def message_email(email):
    """
    Kickoff a 1 on 1 chat with a given email
    :param email:
    :return:
    """
    # Check if the Spark connection has been made
    if spark is None:
        sys.stderr.write("Bot not ready.  \n")
        return "Spark Bot not ready.  "

    # send_message_to_email(email, "Hello!")
    spark.messages.create(toPersonEmail=email, markdown="Hello!")
    return "Message sent to " + email


# Health Check
@app.route("/health", methods=["GET"])
def health_check():
    """
    Notify if bot is up
    :return:
    """
    return "Up and healthy"


# Function to Setup the WebHook for the bot
def setup_webhook(name, targeturl):
    # Get a list of current webhooks
    webhooks = spark.webhooks.list()

    # Look for a Webhook for this bot_name
    # Need try block because if there are NO webhooks it throws an error
    try:
        for h in webhooks:  # Efficiently iterates through returned objects
            if h.name == name:
                sys.stderr.write("Found existing webhook.  Updating it.\n")
                wh = spark.webhooks.update(webhookId=h.id, name=name, targetUrl=targeturl)
                # Stop searching
                break
        # If there wasn't a Webhook found
        if wh is None:
            sys.stderr.write("Creating new webhook.\n")
            wh = spark.webhooks.create(name=name, targetUrl=targeturl, resource="messages", event="created")
    except:
        sys.stderr.write("Creating new webhook.\n")
        wh = spark.webhooks.create(name=name, targetUrl=targeturl, resource="messages", event="created")

    return wh


# Function to take action on incoming message
def process_incoming_message(post_data):
    # Determine the Spark Room to send reply to
    room_id = post_data["data"]["roomId"]

    # Get the details about the message that was sent.
    message_id = post_data["data"]["id"]
    message = spark.messages.get(message_id)
    # Uncomment to debug
    # sys.stderr.write("Message content:" + "\n")
    # sys.stderr.write(str(message) + "\n")

    # First make sure not processing a message from the bot
    if message.personEmail in spark.people.me().emails:
        # Uncomment to debug
        # sys.stderr.write("Message from bot recieved." + "\n")
        return ""

    # Log details on message
    sys.stderr.write("Message from: " + message.personEmail + "\n")

    # Find the command that was sent, if any
    command = ""
    for c in commands.items():
        if message.text.find(c[0]) != -1:
            command = c[0]
            sys.stderr.write("Found command: " + command + "\n")
            # If a command was found, stop looking for others
            break

    reply = ""
    # Take action based on command
    # If no command found, send help
    if command in ["", "/help"]:
        reply = send_help(post_data)
    elif command in ["/echo"]:
        reply = send_echo(message)

    # send_message_to_room(room_id, reply)
    spark.messages.create(roomId=room_id, markdown=reply)


# Sample command function that just echos back the sent message
def send_echo(incoming):
    # Get sent message
    message = extract_message("/echo", incoming.text)
    return message


# Construct a help message for users.
def send_help(post_data):
    message = "Hello!  "
    message = message + "I understand the following commands:  \n"
    for c in commands.items():
        message = message + "* **%s**: %s \n" % (c[0], c[1])
    return message


# Return contents following a given command
def extract_message(command, text):
    cmd_loc = text.find(command)
    message = text[cmd_loc + len(command):]
    return message


# Setup the Spark connection and WebHook
def spark_setup(email, token):
    # Update the global variables for config details
    globals()["spark_token"] = token
    globals()["bot_email"] = email

    sys.stderr.write("Spark Bot Email: " + bot_email + "\n")
    sys.stderr.write("Spark Token: REDACTED\n")

    # Setup the Spark Connection
    globals()["spark"] = CiscoSparkAPI(access_token=globals()["spark_token"])
    globals()["webhook"] = setup_webhook(globals()["bot_app_name"], globals()["bot_url"])
    sys.stderr.write("Configuring Webhook. \n")
    sys.stderr.write("Webhook ID: " + globals()["webhook"].id + "\n")


if __name__ == '__main__':
    # Entry point for bot
    # Retrieve needed details from environment for the bot
    bot_email = os.getenv("SPARK_BOT_EMAIL")
    spark_token = os.getenv("SPARK_BOT_TOKEN")
    bot_url = os.getenv("SPARK_BOT_URL")
    bot_app_name = os.getenv("SPARK_BOT_APP_NAME")

    # bot_url and bot_app_name must come in from Environment Variables
    if bot_url is None or bot_app_name is None:
            sys.exit("Missing required argument.  Must set 'SPARK_BOT_URL' and 'SPARK_BOT_APP_NAME' in ENV.")

    # Write the details out to the console
    sys.stderr.write("Spark Bot URL (for webhook): " + bot_url + "\n")
    sys.stderr.write("Spark Bot App Name: " + bot_app_name + "\n")

    # Placeholder variables for spark connection objects
    spark = None
    webhook = None

    # Check if the token and email were set in ENV
    if spark_token is None or bot_email is None:
        sys.stderr.write("Spark Config is missing, please provide via API.  Bot not ready.\n")
    else:
        spark_setup(bot_email, spark_token)
        spark = CiscoSparkAPI(access_token=spark_token)

    app.run(debug=True, host='0.0.0.0', port=int("5000"))
