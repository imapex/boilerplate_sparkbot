# boilerplate_sparkbot

# Description

This is a sample project that provides the foundation for a Spark Bot.  It includes several basic elements for the bot, allowing the developer to focus on the actions of the bot, not the bot operations.  

This Bot will use a provided Spark Account (identified by the Developer Token) and create a webhook to receive all messages sent to the account.   You will specify a set of command words that the Bot will "listen" for.  Any other message sent to the bot will result in the help message being sent back.

[imapex/boilerplate_sparkbot](https://github.com/imapex/boilerplate_spark) is a starting point application for the [imapex](http://imapex.io) team @ Cisco.

# Spark Account Requirements

There are different strategies for building a Spark Bot.  This boilerplate expects that a dedicated Spark Account be provided for the bot.  This is as opposed to leveraging a Bot service from a seperate Spark Account.

Create a new Cisco Spark account for your bot, and record it's email and token for use in development and deployment.

**TODO - Add details on how to do this**



# Building your own Spark Bot

The purpose of this boilerplate is to make it quick and easy to create new Spark Bots by providing a foundation to manage the underlying webhook creation and message sending, and letting the developer focus on the features of the bot being created.  

To get started with your own SparkBot, follow this process.  

1. Clone the imapex repo 
2. Run the `new_bot_setup.sh` script
	* Provide your GitHub Credentials
	* Provide a name for your new Spark Bot 
	  *(also used as GitHub Repo Name)*
	* The script will 
		* Download the boilerplate_sparkbot code
		* Create a new local directory for your bot with the boilerplate code
		* Delete the downloaded boilerplate code
		* Create a new GitHub Repo on your account for the bot 
		* Push up the boilerplate code to GitHub
3. Add your bot commands and features to the bot.py file 
	***TODO - provide more details on this step***
4. Build the Docker image for your new bot
	* Using a drone.io CICD Server
		* Included in the boilerplate code is a .drone.yml configuration that will build a new container and publish to a Docker Hub repository
		* You'll need to copy the drone-secrets-sample.yml file to drone-secrets.yml, provide your informaiton, and secure the file before builds will be successful 
		* **TODO - PROVIDE MORE DETAILS**
	* Alternatively you can locally build and push to Docker Hub, or create an automated build repository on Docker Hub
		* **TODO - Provide more details**
5. Deploy your Bot.  To fully function, you must deploy your bot where it is publically avialable on the Internet (Spark needs to be able to reach it with WebHooks)
	* The DevNet Mantl Sandbox is a free and available option that can be used
		* Included in the code is an installation script called `bot_deploy_devnet.sh` that will walk through the deployment of your Bot to the DevNet Sandbox.  

**TODO - Create new_bot_setup script**

**TODO - Create bot_deploy_devnet.sh script**




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


