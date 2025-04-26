import json

def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def get_greetings_message_input(recipient):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "Greetings from Traders"
                },
                "body": {
                    "text": "What would you like to do?"
                },
                "footer": {
                    "text": "Choose from the following options"
                },
                "action": {
                    "button": "Select any one option",
                    "sections": [
                        {
                            "title": "Section 1",
                            "rows": [
                                {
                                    "id": "1",
                                    "title": "Initiate a new trade",
                                    "description": "Initiate a new trade"
                                },
                                {
                                    "id": "2",
                                    "title": "View my trade history",
                                    "description": "View my trade history"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    )

def get_raise_trade_message_input(recipient):
    return json.dumps(
        {
            "recipient_type": "individual",
            "messaging_product": "whatsapp",
            "to": "PHONE_NUMBER",
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "header": {
                "type": "text",
                "text": "Flow message header"
                },
                "body": {
                "text": "Flow message body"
                },
                "footer": {
                "text": "Flow message footer"
                },
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_token": "AQAAAAACS5FpgQ_cAAAAAD0QI3s.",
                        "flow_id": "1",
                        "flow_cta": "Book!",
                        "flow_action": "navigate",
                        "flow_action_payload": {
                            "screen": "<SCREEN_NAME>",
                            "data":{ 
                                "product_name": "name",
                                "product_description": "description",
                                "product_price": 100
                            }
                        }
                    }
                }
            }
        }
    )

    
