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

def get_menu_message_input(recipient):
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
                    "text": "Choose an option"
                },
                "body": {
                    "text": "Choose from the following options"
                },
                "footer": {
                    "text": "Choose from the following options"
                },
                "action": {
                    "button": "Select",
                    "sections": [
                        {
                            "title": "Select an option",
                            "rows": [
                            {
                                "id": "1",
                                "title": "Option 1",
                                "description": "Option 1 description"
                            },
                            {
                                "id": "2",
                                "title": "Option 2",
                                "description": "Option 2 description"
                            }
                            ]
                        }
                    ]
                }
            }
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
                    "button": "Select any one",
                    "sections": [
                        {
                            "title": "Section 1",
                            "rows": [
                                {
                                    "id": "initiateTrade",
                                    "title": "Initiate a new trade",
                                },
                                {
                                    "id": "viewTradeHistory",
                                    "title": "View my trade history",
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
            "to": recipient,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": "Click here to raise a trade: https://owl-tolerant-accurately.ngrok-free.app/"
            }
        }
    )

def get_trade_details_text_message_input(trade_id, person_name, product_name, quantity, price):
    return "Name - " + person_name + " \n" + "Product - " + product_name + " \n" + "Quantity - " + quantity + " \n" + "Price - " + price + " \n" + "Trade ID - " + trade_id

def get_approve_trade_message_input(recipient, trade_id, person_name, product_name, quantity, price):
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
                    "text": "Approve a trade"
                },
                "body": {
                    "text": get_trade_details_text_message_input(trade_id, person_name, product_name, quantity, price)
                },
                "footer": {
                    "text": "Choose from the following options"
                },
                "action": {
                    "button": "Select any one",
                    "sections": [
                        {
                            "title": "Section 1",
                            "rows": [
                                {
                                    "id": "approveTrade_" + trade_id,
                                    "title": "Approve the trade",
                                },
                                {
                                    "id": "rejectTrade_" + trade_id,
                                    "title": "Reject the trade",
                                }
                            ]
                        }
                    ]
                }
            }
        }
    )

def get_trade_id_list_message_input(recipient):
    
    
    return json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual", 
        "to": recipient,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Trade IDs"
            },
            "body": {
                "text": "Select a trade ID to view details"
            },
            "footer": {
                "text": "Choose from the following options"
            },
            "action": {
                "button": "Select Trade",
                "sections": [
                    {
                        "title": "Available Trades",
                        "rows": rows
                    }
                ]
            }
        }
    })

def get_view_trade_history_message_input(recipient):
    trades = storage.get_all_trades()
    rows = []
    for trade in trades:
        rows.append({
            "id": f"viewTrade_{trade['id']}",
            "title": f"Trade ID: {trade['id']} - {trade['product_name']}"
        })
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
                    "text": "Deal ID"
                },
                "body": {
                    "text": "Select a deal ID to view the details"
                },
                "footer": {
                    "text": "Choose from the following options"
                },
                "action": {
                    "button": "Select any one",
                    "sections": [
                        {
                            "title": "Section 1",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )

def get_trade_details_message_input(recipient, trade_id):
    trade = storage.get_trade(trade_id)
    return get_text_message_input(recipient, get_trade_details_text_message_input(trade_id, trade["person_name"], trade["product_name"], trade["quantity"], trade["price"]))


