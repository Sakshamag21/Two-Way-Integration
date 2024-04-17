from flask import Flask, request, jsonify
import json
import mysql.connector
import random


app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'zenskar_test'
}

sql_query_insert = """
INSERT INTO customer (ID,email, name)
VALUES (%s,%s, %s)
"""

sql_query_update = """
UPDATE customer
SET email = %s, name = %s
WHERE ID = %s
"""

sql_query_delete = """
DELETE FROM customer
WHERE ID = %s
"""

def generate_random_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def execute_query(query, values=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error executing query:", e)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def find_customer_id(email, name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID FROM customer WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print("Error finding customer ID:", e)
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    print("Received payload:", payload)
    
    event_data = json.loads(payload)

    event_type = event_data['type']
    event_object = event_data['data']['object']
    if event_type == 'customer.created':
        id=generate_random_id()
        execute_query(sql_query_insert, (id,event_object['email'], event_object['name']))
    elif event_type == 'customer.updated':
        print(event_object)
        customer_id = find_customer_id(event_object['email'], event_object['name'])
        if customer_id:
            execute_query(sql_query_update, (event_object['email'], event_object['name'], customer_id))
        else:
            print("Customer not found for update:", event_object['email'], event_object['name'])
    elif event_type == 'customer.deleted':
        customer_id = find_customer_id(event_object['email'], event_object['name'])
        print(customer_id)
        if customer_id:
            execute_query(sql_query_delete, (customer_id,))
        else:
            print("Customer not found for deletion:", event_object['email'], event_object['name'])
    else:
        print("Unhandled event type:", event_type)

    return jsonify({'received': True}), 200

if __name__ == '__main__':
    app.run(debug=True)
