import logging
import json

from flask import Blueprint, request, jsonify, current_app, render_template

from .decorators.security import signature_required
from .utils.whatsapp_utils import (
    process_whatsapp_message,
    is_valid_whatsapp_message,
)

webhook_blueprint = Blueprint("webhook", __name__)


def handle_message():
    """
    Handle incoming webhook events from the WhatsApp API.

    This function processes incoming WhatsApp messages and other events,
    such as delivery statuses. If the event is a valid message, it gets
    processed. If the incoming payload is not a recognized WhatsApp event,
    an error is returned.

    Every message send will trigger 4 HTTP requests to your webhook: message, sent, delivered, read.

    Returns:
        response: A tuple containing a JSON response and an HTTP status code.
    """
    body = request.get_json()
    # logging.info(f"request body: {body}")

    # Check if it's a WhatsApp status update
    if (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("statuses")
    ):
        logging.info("Received a WhatsApp status update.")
        return jsonify({"status": "ok"}), 200

    try:
        if is_valid_whatsapp_message(body):
            logging.info(f"request body: {body}")
            process_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), 400


# Required webhook verifictaion for WhatsApp
def verify():
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == current_app.config["VERIFY_TOKEN"]:
            # Respond with 200 OK and challenge token from the request
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400


@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    return verify()

@webhook_blueprint.route("/webhook", methods=["POST"])
@signature_required
def webhook_post():
    return handle_message()

@webhook_blueprint.route("/", methods=["GET"])
def show_order_form():
    """Display the order form."""
    return render_template("order_form.html")

@webhook_blueprint.route("/submit-order", methods=["POST"])
def handle_order():
    """Handle the order form submission."""
    try:
        person_name = request.form.get("person_name")
        product_name = request.form.get("product_name")
        quantity = request.form.get("quantity")
        
        # Log the order details
        logging.info(f"New order received - Person: {person_name}, Product: {product_name}, Quantity: {quantity}")
        
        # Here you can add additional processing like:
        # - Saving to a database
        # - Sending notifications
        # - Processing payment
        # - etc.
        
        return jsonify({
            "status": "success",
            "message": "Order received successfully",
            "order_details": {
                "person_name": person_name,
                "product_name": product_name,
                "quantity": quantity
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing order: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to process order"
        }), 500


