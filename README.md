# boilerplate_sparkbot

# Description

This is a sample project that provides the foundation for a Spark Bot.  It includes several basic elements for the bot, allowing the developer to focus on the actions of the bot, not the bot operations.  

This Bot will use a provided Spark Account (identified by the Developer Token) and create a webhook to receive all messages sent to the account.   You will specify a set of command words that the Bot will "listen" for.  Any other message sent to the bot will result in the help message being sent back.

[imapex/boilerplate_sparkbot](https://github.com/imapex/boilerplate_spark) is a starting point application for the [imapex](http://imapex.io) team @ Cisco.

# Spark Account Requirements

There are two strategies for building a Spark Bot.  

1. **Dedicated Spark Account** for the bot.  Here you create a full Spark Account with a unique email address.  

2. **Bot App** within another Spark Account.  Here you create a new *Bot App* under your personal Spark Account.  

Bots created based on this boilerplate can leverage either type of strategy.  You'll just need to provide the correct email and token details when starting the bot code.  

## Dedicated Spark Account 
Create a new Cisco Spark account for your bot, and record it's email and token for use in development and deployment.

You can create new, free account at [CiscoSpark.com](http://ciscospark.com).  You'll need an email address for the bot that hasn't been used with another.  Many users create accounts on Gmail for their bots if you do not have a personal domain/email-host you can use.  

Once your new account is created, log into [developer.ciscospark.com](https://developer.ciscospark.com) to find the new accounts token.  Here is a screenshot of where to locate the information.  

![](readme_resources/spark_token.jpg)

## Bot App 
A newer feature within Cisco Spark, is the ability to create *Bot* apps within another account.  This has the advantage of no longer requiring unique email accounts for each and every new bot you create.  Bot app accounts work nearly the same as full accounts with only a few differences.  Check this [page](https://developer.ciscospark.com/bots.html) for details.  

To create a new Bot App account to use, here are the basic instructions.  

1.  Log into [developer.ciscospark.com](https://developer.ciscospark.com) with your own personal Spark account.  
2. Click on **My Apps** in the top menu, and create a new **Bot** (do not create a new integration).  

	![](readme_resources/spark_myapps1.jpg)
	---
	![](readme_resources/spark_newapp1.jpg)
	
3. Provide a *Display Name*, *Bot Username*, and *Icon* URL for your new bot.  The *Bot Username* needs to be unique within Spark, and can **NOT** be changed.  Click **Add Bot**

	![](readme_resources/spark_newbot1.jpg)
	
4. Record the *Access token* that is displayed on the next page, and **Save Changes**.  If you do NOT copy the token, you can regenerate it.  

	![](readme_resources/spark_newbot2.jpg)
	
5. Also note the **Bot Username** that is displayed.  This is the ***Bot Email*** that will be needed when setting up your boilerplate code.  

# Building your own Spark Bot

The purpose of this boilerplate is to make it quick and easy to create new Spark Bots by providing a foundation to manage the underlying webhook creation and message sending, and letting the developer focus on the features of the bot being created.  

To get started with your own SparkBot, follow this process.  

1. Download the setup script

	```
	# move to the directory where you store code for your projects
	# DO NOT create a folder for your new bot
	cd ~/coding 

	# Download the script
	wget https://github.com/imapex/boilerplate_sparkbot/raw/master/setup_and_install/new_bot_setup.sh 

	# Make the script executable 
	chmod +x new_bot_setup.sh 
	```
 
2. Run the `new_bot_setup.sh` script
	* Provide your GitHub Credentials
		* ***NOTE regarding GitHub 2 Factor Auth***
			* If you have 2FA enabled on your GitHub account, you will need to provide a *Personal Access Token* when prompted for your password
			* Tokens can be generated at [github.com/settings/tokens](https://github.com/settings/tokens)
			* The token must have a minimum of `repo` access, and `delete_repo` access to automate the creation and cleanup of your new bot
	* Provide a name for your new Spark Bot 
	  *(also used as GitHub Repo Name)*
	* The script will 
		* Download the boilerplate_sparkbot code
		* Create a new local directory for your bot with the boilerplate code
		* Delete the downloaded boilerplate code
		* Create a new GitHub Repo on your account for the bot 
		* Push up the boilerplate code to GitHub
3. Add your bot commands and features to the bot.py file 
	
	1. Add new commands to the command dictionary in bot/bot.py 

		```
		# The list of commands the bot listens for
		# Each key in the dictionary is a command
		# The value is the help message sent for the command
		commands = {
		    "/echo": "Reply back with the same message sent.",
		    "/help": "Get help."
		}
		```
		
	2. Create a new Python function for each of your commands.  The function should return the text that will be sent back in reply.  You can use the included 	`send_echo` function as an example.  

		```
		def send_echo(incoming):
		    # Get sent message
		    message = incoming["text"]
		    # Slice first 6 characters to remove command
		    message = message[6:]
		    return message	
		```
	
	3. Update the `if ...elif` section of the `process_incoming_message` function for your new command.  

		```
		# Some of function removed below
		def process_incoming_message(post_data):
		    # Take action based on command
		    # If no command found, send help
		    if command in ["","/help"]:
		        reply = send_help(post_data)
		    elif command in ["/echo"]:
		        reply = send_echo(message)
		
		    send_message_to_room(room_id, reply)	
		```
	
4. Build the Docker image for your new bot.  There are several methods available for this.  
	* Using a drone.io CICD Server
		* Included in the boilerplate code is a .drone.yml configuration that will build a new container and publish to a Docker Hub repository
		* You'll need to copy the drone-secrets-sample.yml file to drone-secrets.yml, provide your informaiton, and secure the file before builds will be successful 
		* **TODO - PROVIDE MORE DETAILS**
	* Alternatively you can locally build and push to Docker Hub, or create an automated build repository on Docker Hub
		* **TODO - Provide more details**
5. Deploy your Bot.  To fully function, you must deploy your bot where it is publically avialable on the Internet (Spark needs to be able to reach it with WebHooks)
	* The DevNet Mantl Sandbox is a free and available option that can be used
		* Included in the code is an installation script that will deploy your bot to the sandbox.  *This script assumes you've published a Docker image to hub.docker.com for your bot*
		* To install to the Sandbox

			```
			# From the root of your project... 
			cd setup_and_install 
			
			# Run the install script
			./bot_install_sandbox.sh 
			```
			
		* Answer the questions
		* A new Marathon app definition for your bot will be created and deployed to the DevNet Sandbox


## Deleting your SparkBot

Should you want to delete your SparkBot, a cleanup script is provided that will do much of the work for you.  

1.  From your Spark Bot's local root directory

	```
	setup_and_install/new_bot_cleanup.sh
	
	```
2. Provide your GitHub Credentials and the name of your Bot.  The script will 

	* Delete your repository from GitHub
	* Delete the local code from your workstation 

3.  You will manually need to 

	* Delete any running instances of your application 
		* If you have deployed to the DevNet Sandbox, an uninstall script is available `setup_and_install/bot_uninstall_sandbox.sh` 
	* Delete any Docker (or other container registry) Repositories for your Bot 
	* Clear any WebHooks from the Spark Account you created for your bot


# Spark Bot Installation and Details


## Environment

Prerequisites

* Python 2.7+
* [setuptools package](https://pypi.python.org/pypi/setuptools)

## Downloading

Provide instructions for how to obtain the software from this repository, if there are multiple options - please include
as many as possible

Option A:

If you have git installed, clone the repository

    git clone https://github.com/imapex/boilerplate_sparkbot

Option B:

If you don't have git, [download a zip copy of the repository](https://github.com/imapex/boilerplate_sparkbot/archive/master.zip)
and extract.

Option C:

The latest build of this project is also available as a Docker image from Docker Hub

    docker pull imapex/boilerplate_sparkbot:latest

## Installing

Provide instructions on how to install / use the application.  The details provided here relate to the boilerplate_sparkbot itself, be sure to update for any additions/changes your Bot requires.  

# Usage

The bot is designed to be deployed as a Docker Container, and can run on any platform supporting Docker Containers.  Mantl.io is one example of a platform that can be used to run the bot.

***NOTE: For full functionality, this bot needs to be installed in an environment where the bot application is available on the public internet in order for the Spark Cloud to be able to send WebHooks to the bot.  If you do NOT have an environment to use, the DevNet Sandbox Mantl cluster can be leveraged to host your bot.***  

### Deploying to a Mantl.io cluster 

**TODO - update with details on how to install to Mantl** 

### Locally building and running the Docker Container 

You can build and run the Spark Bot as a Docker Container locally with these commands.  

```
docker build -t sparkbot .
docker run -it --name sparkbot \
	-e "SPARK_BOT_EMAIL=myhero.demo@domain.com" \
	-e "SPARK_BOT_TOKEN=adfiafdadfadfaij12321kaf" \
	-e "SPARK_BOT_URL=http://myhero-spark.mantl.domain.com" \
	-e "SPARK_BOT_APP_NAME='imapex bot'" \
	sparkbot
```

### Running Python Code Locally 

There are several pieces of information needed to run this application.  These details are provided Environment Variables to the application.

If you are running the python application directly, you can set them like this:

```
# Details on the Cisco Spark Account to Use
export SPARK_BOT_EMAIL=myhero.demo@domain.com
export SPARK_BOT_TOKEN=adfiafdadfadfaij12321kaf

# Public Address and Name for the Spark Bot Application
export SPARK_BOT_URL=http://myhero-spark.mantl.domain.com
export SPARK_BOT_APP_NAME="imapex bot"

# Start the bot
python bot/bot.py

```



# Development

The purpose of this boilerplate, and all other boilerplates created by the imapex team, is to make it quick and easy to create new Spark Bots by providing a foundation to manage the underlying webhook creation and message sending, and letting the developer focus on the features of the bot being created.  

If you'd like to contribute to this boilerplate with bug fixes or enhancements, we welcome you to the team.  Simply fork the main [imapex/boilerplate_sparkbot](https://github.com/imapex/boilerplate_spark) repository, make your improvements, and send us a Pull Request.  

## Linting

We use flake 8 to lint our code. Please keep the repository clean by running:

    flake8

## Testing

**TODO - Create tests for SPARKBOT BOILERPLATE**

The IMAPEX team should attempt to have unittests with  100% code coverage. An example test suite is contained
within the tests.py file for the boilerplate application

The tests are can be run in the following ways::

    python tests.py


When adding additional code or making changes to the project, please ensure that unit tests are added to cover the
new functionality and that the entire test suite is run against the project before submitting the code.
Minimal code coverage can be verified using tools such as coverage.py.

For instance, after installing coverage.py, the toolkit can be run with the command::

    coverage run tests.py

and an HTML report of the code coverage can be generated with the command::

    coverage html


