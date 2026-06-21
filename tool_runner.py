# tool_runner.py

import json
# Import mock datasets that simulate a database
from mock_data import CUSTOMERS, ORDERS


# Fetch a customer by matching against multiple possible identifiers
def get_customer(query: str) -> str:
    # Normalize input for consistent matching (ignore case + extra spaces)
    query = query.strip().lower()

    # Iterate through all customers in the dataset
    for customer in CUSTOMERS.values():
        # Match against customer_id, email, or name
        if (
            query == customer["customer_id"].lower()
            or query == customer["email"].lower()
            or query == customer["name"].lower()
        ):
            # Return the matched customer as a JSON string
            return json.dumps(customer)

    # Return a structured validation error if no match is found
    return json.dumps({
        "error": {
            "type": "validation",
            "retryable": False,
            "message": (
                f"No customer found matching '{query}'. The input may be "
                "misspelled or in the wrong format. Customer IDs follow the "
                "format CUST-XXXX. You can also search by full name or email "
                "address. Ask the customer to verify their details and try again."
            )
        }
    })


# Fetch an order using its order ID
def lookup_order(order_id: str) -> str:
    # Normalize input (strip spaces + standardize casing)
    order_id = order_id.strip().upper()

    # Check if the order exists in the dataset
    if order_id in ORDERS:
        # Return the order details as a JSON string
        return json.dumps(ORDERS[order_id])

    # Return a structured validation error if the order is not found
    return json.dumps({
        "error": {
            "type": "validation",
            "retryable": False,
            "message": (
                f"No order found with ID '{order_id}'. The input may be "
                "misspelled or in the wrong format. Order IDs follow the "
                "format ORD-XXXX. Ask the customer to verify their order ID "
                "and try again."
            )
        }
    })


# Central dispatcher that routes tool calls to the correct function
def run_tool(tool_name: str, tool_input: dict) -> str:
    # Route to the appropriate tool based on its name
    if tool_name == "get_customer":
        return get_customer(tool_input["query"])
    elif tool_name == "lookup_order":
        return lookup_order(tool_input["order_id"])
    else:
        # Handle unknown tool calls safely with a structured error
        return json.dumps({
            "error": {
                "type": "validation",
                "retryable": False,
                "message": f"Tool '{tool_name}' is not recognised."
            }
        })