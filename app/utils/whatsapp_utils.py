import logging
from flask import current_app, jsonify
import json
import requests
from app.utils.messages import get_greetings_message_input, get_text_message_input, get_menu_message_input,get_raise_trade_message_input, get_approve_trade_message_input
# from app.services.openai_service import generate_response
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def generate_response(response):
    # Return text in uppercase
    return response.upper()


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    # message_body = message["text"]["body"]

    # TODO: implement custom function here
    data = None
    if message["type"] == "interactive":
        handle_interactive_message(message)
    elif message["type"] == "text":
        handle_text_message(message)
    else:
        logging.error(f"Unsupported message type: {message['type']}")
        handle_retry_message(message)

def handle_text_message(message):
    response = generate_response(message["text"]["body"])
    if response.upper() == "MENU":
        data = get_menu_message_input(current_app.config["RECIPIENT_WAID"])
    elif response.upper() == "HI":
        data = get_greetings_message_input(current_app.config["RECIPIENT_WAID"])
    else:
        data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)

def handle_interactive_message(message):
    interactive = message["interactive"]
    if interactive["type"] == "list_reply":
        handle_list_reply(interactive)
    else:
        logging.error(f"Unsupported interactive type: {interactive['type']}")
        handle_retry_message(message)

def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )

def handle_retry_message(message):
    response = generate_response("Please try again")
    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)

def handle_list_reply(interactive):
    list_reply = interactive["list_reply"]
    if list_reply["id"] == "1":
        data = get_text_message_input(current_app.config["RECIPIENT_WAID"], list_reply["title"] + " selected")
        send_message(data)
    elif list_reply["id"] == "2":
        data = get_text_message_input(current_app.config["RECIPIENT_WAID"], list_reply["title"] + " selected")
        send_message(data)
    elif list_reply["id"] == "initiate_trade":
        data = get_raise_trade_message_input(current_app.config["RECIPIENT_WAID"])
        send_message(data)
    elif list_reply["id"] == "approve_trade":
        data = get_text_message_input(current_app.config["RECIPIENT_WAID"], "Trade approved")
        send_message(data)
    elif list_reply["id"] == "reject_trade":
        data = get_text_message_input(current_app.config["RECIPIENT_WAID"], "Trade rejected")
        send_message(data)
    else:
        logging.error(f"Unsupported list reply id: {list_reply['id']}")
        handle_retry_message(message)

def handle_trade_details_message(person_name, product_name, quantity, price):
    data = get_approve_trade_message_input(current_app.config["APPROVER_WAID"], person_name, product_name, quantity, price)
    send_message(data)


