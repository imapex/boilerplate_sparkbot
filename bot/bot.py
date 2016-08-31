#! /usr/bin/python
'''
    boilerplate_sparkbot

    This is a sample boilerplate application that provides the framework to quickly
    build and deploy an interactive Spark Bot.

    There are different strategies for building a Spark Bot.  This boilerplate is
    expects that a dedicated Spark Account be provided for the bot.  This is as
    opposed to leveraging a Bot service from a seperate Spark Account.

    This Bot will use a provided Spark Account (identified by the Developer Token)
    and create a webhook to receive all messages sent to the account.   You will
    specify a set of command words that the Bot will "listen" for.  Any other message
    sent to the bot will result in the help message being sent back.

    The bot is designed to be deployed as a Docker Container, and can run on any
    platform supporting Docker Containers.  Mantl.io is one example of a platform
    that can be used to run the bot.

    There are several pieces of information needed to run this application.  These
    details are provided Environment Variables to the application.

    If you are running the python application directly, you can set them like this:

    # Details on the Cisco Spark Account to Use
    export SPARK_BOT_EMAIL=myhero.demo@domain.com
    export SPARK_BOT_TOKEN=adfiafdadfadfaij12321kaf

    # Public Address and Name for the Spark Bot Application
    export SPARK_BOT_URL=http://myhero-spark.mantl.domain.com
    export SPARK_BOT_APP_NAME="imapex bot"

    If you are running the bot within a docker container, they would be set like this:
    # ToDo - Add docker run command

'''


__author__ = 'hapresto'


from flask import Flask, request, Response
import requests, json, re
from spark_utilities import *

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
    post_data = request.get_json(force=True)
    # Uncomment to debug
    # sys.stderr.write("Webhook content:" + "\n")
    # sys.stderr.write(str(post_data) + "\n")

    # Take the posted data and send to the processing function
    process_incoming_message(post_data)
    return ""


# Quick REST API to have bot send a message to a user
@app.route("/hello/<email>", methods=["GET"])
def message_email(email):
    '''
    Kickoff a 1 on 1 chat with a given email
    :param email:
    :return:
    '''
    send_message_to_email(email, "Hello!")
    return "Message sent to " + email


# Function to take action on incoming message
def process_incoming_message(post_data):
    # Determine the Spark Room to send reply to
    room_id = post_data["data"]["roomId"]

    # Get the details about the message that was sent.
    message_id = post_data["data"]["id"]
    message = get_message(message_id)
    # Uncomment to debug
    # sys.stderr.write("Message content:" + "\n")
    # sys.stderr.write(str(message) + "\n")

    # First make sure not processing a message from the bot
    if message["personEmail"] == bot_email:
        return ""

    # Log details on message
    sys.stderr.write("Message from: " + message["personEmail"] + "\n")

    # Find the command that was sent, if any
    command = ""
    for c in commands.items():
        if message["text"].find(c[0]) == 0:
            command = c[0]
            sys.stderr.write("Found command: " + command + "\n")
            # If a command was found, stop looking for others
            break

    # Take action based on command
    # If no command found, send help
    if command in ["","/help"]:
        reply = send_help(post_data)
    elif command in ["/echo"]:
        reply = send_echo(message)

    send_message_to_room(room_id, reply)


# Sample command function that just echos back the sent message
def send_echo(incoming):
    # Get sent message
    message = incoming["text"]
    return message


# Construct a help message for users.
def send_help(post_data):
    message = "Hello!  "
    message = message + "I understand the following commands:  \n"
    for c in commands.items():
        message = message + "* **%s**: %s \n" % (c[0], c[1])
    return message



if __name__ == '__main__':
    # Entry point for bot
    import os, sys

    # Retrieve needed details from environment for the bot
    bot_email = os.getenv("SPARK_BOT_EMAIL")
    spark_token = os.getenv("SPARK_BOT_TOKEN")
    bot_url = os.getenv("SPARK_BOT_URL")
    bot_app_name = os.getenv("SPARK_BOT_APP_NAME")

    # Make sure all required details were provided
    if bot_email == None or spark_token == None or bot_url == None or bot_app_name == None:
        sys.exit("Missing required argument")

    # Write the details out to the console
    sys.stderr.write("Spark Bot Email: " + bot_email + "\n")
    sys.stderr.write("Spark Token: REDACTED\n")
    sys.stderr.write("Spark Bot URL (for webhook): " + bot_url + "\n")
    sys.stderr.write("Spark Bot App Name: " + bot_app_name + "\n")

    # Set Authorization Header for Spark REST API Requests
    spark_headers["Authorization"] = "Bearer " + spark_token

    # Create Web Hook to recieve ALL messages
    global_webhook_id = setup_webhook("", bot_url, bot_app_name)
    sys.stderr.write("Global MyHero Web Hook ID: " + global_webhook_id + "\n")

    app.run(debug=True, host='0.0.0.0', port=int("5000"))

