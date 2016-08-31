import requests

# Spark REST API access details
spark_host = "https://api.ciscospark.com/"
spark_headers = {}
spark_headers["Content-type"] = "application/json"


# Spark Utility Functions
# The following functions provide basic interfaces to Spark features

#### Message Utilities
def send_message_to_email(email, message):
    spark_u = spark_host + "v1/messages"
    message_body = {
        "toPersonEmail" : email,
        "markdown" : message
    }
    page = requests.post(spark_u, headers = spark_headers, json=message_body)
    message = page.json()
    return message


def send_message_to_room(room_id, message):
    spark_u = spark_host + "v1/messages"
    message_body = {
        "roomId" : room_id,
        "markdown" : message
    }
    page = requests.post(spark_u, headers = spark_headers, json=message_body)
    message = page.json()
    return message


def get_message(message_id):
    spark_u = spark_host + "v1/messages/" + message_id
    page = requests.get(spark_u, headers = spark_headers)
    message = page.json()
    return message

#### Webhook Utilities
def current_webhooks():
    spark_u = spark_host + "v1/webhooks"
    page = requests.get(spark_u, headers = spark_headers)
    webhooks = page.json()
    return webhooks["items"]


def create_webhook(roomId, target, webhook_name = "New Webhook"):
    spark_u = spark_host + "v1/webhooks"
    spark_body = {
        "name" : webhook_name,
        "targetUrl" : target,
        "resource" : "messages",
        "event" : "created"
    }

    if (roomId != ""):
        {
            spark_body["filter"]: "roomId=" + roomId
        }

    page = requests.post(spark_u, headers = spark_headers, json=spark_body)
    webhook = page.json()
    return webhook


def update_webhook(webhook_id, target, name):
    spark_u = spark_host + "v1/webhooks/" + webhook_id
    spark_body = {
        "name" : name,
        "targetUrl" : target
    }
    page = requests.put(spark_u, headers = spark_headers, json=spark_body)
    webhook = page.json()
    return webhook


def delete_webhook(webhook_id):
    spark_u = spark_host + "v1/webhooks/" + webhook_id
    page = requests.delete(spark_u, headers = spark_headers)


def setup_webhook(room_id, target, name):
    webhooks = current_webhooks()
    webhook_id = ""
    # pprint(webhooks)

    # Legacy test for room based demo
    if (room_id != ""):
        # Look for a Web Hook for the Room
        for webhook in webhooks:
            if webhook["filter"] == "roomId=" + room_id:
                # print("Found Webhook")
                webhook_id = webhook["id"]
                break
    # For Global Webhook
    else:
        for webhook in webhooks:
            if webhook["name"] == name:
                # print("Found Webhook")
                webhook_id = webhook["id"]
                break

    # If Web Hook not found, create it
    if webhook_id == "":
        webhook = create_webhook(room_id, target, name)
        webhook_id = webhook["id"]
    # If found, update url
    else:
        webhook = update_webhook(webhook_id, target, name)

    # pprint(webhook)
    return webhook_id


#### Room Utilities
def current_rooms():
    spark_u = spark_host + "v1/rooms"
    page = requests.get(spark_u, headers = spark_headers)
    rooms = page.json()
    return rooms["items"]


def leave_room(room_id):
    # Get Membership ID for Room
    membership_id = get_membership_for_room(room_id)
    spark_u = spark_host + "v1/memberships/" + membership_id
    page = requests.delete(spark_u, headers = spark_headers)


def get_membership_for_room(room_id):
    spark_u = spark_host + "v1/memberships?roomId=%s" % (room_id)
    page = requests.get(spark_u, headers = spark_headers)
    memberships = page.json()["items"]

    return memberships

