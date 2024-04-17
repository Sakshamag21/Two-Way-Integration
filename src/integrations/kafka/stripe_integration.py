import stripe
import json
import os

from dotenv import load_dotenv
load_dotenv()

secret_key = os.getenv("SECRET_KEY")

stripe.api_key = secret_key

def process_message(msg):
    try:
        event = json.loads(msg.value())
        event_type = event.get('event')
        name = event.get('name')
        email = event.get('email')
        
        if event_type == 'customer_created':
            name = event.get('name')
            email = event.get('email')
            existing_customers = stripe.Customer.list(email=email, limit=1).data
            if existing_customers:
                print("Customer already exists:")
                print(existing_customers[0])
            else:
                new_customer = stripe.Customer.create(email=email, name=name)
                print("New customer created:")
                
        elif event_type == 'customer_retrieved':
            customer = stripe.Customer.list(email=email, limit=1).data[0]
            print("Customer retrieved:")
            print(customer)
        elif event_type == 'customer_updated':
            name = event.get('name')
            email = event.get('email')
            previous_email = event.get('previous_email')
            customer = stripe.Customer.list(email=previous_email, limit=1).data[0]
            stripe.Customer.modify(customer.id, email=email, name=name)
            print("Customer updated")
        elif event_type == 'customer_deleted':
            email = event.get('email')
            customer = stripe.Customer.list(email=email, limit=1).data[0]
            stripe.Customer.delete(customer.id)
            print("Customer deleted")
        else:
            print(f"Unknown event type: {event_type}")

    except Exception as e:
        print(f"Error processing message: {e}")
