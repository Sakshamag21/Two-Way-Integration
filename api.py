# api_service.py

from src.utils.random_number import generate_random_id
from src.utils.database import insert_query , update_query , delete_query

from multiprocessing import Process
import os


from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json

 
app = Flask(__name__)

kafka_conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(kafka_conf)
topic = 'customer_changes'

def send_to_kafka(event):
    print('msg created')
    producer.produce(topic, json.dumps(event).encode('utf-8'))
    producer.flush()

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    id = generate_random_id()
    name = data.get('name')
    email = data.get('email')
    print(id, name,email)
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
        
    customer_id=insert_query(id,name,email)
    print(customer_id)
    if(customer_id is not None):
        send_to_kafka({'event': 'customer_created', 'name': name,'email':email})
        return jsonify({'customer_id': 'done'}), 201
    else:
        return jsonify('not able to regsiter'), 500
    

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name and not email:
        return jsonify({'error': 'At least one field (name or email) is required to update'}), 400
    
    val= update_query(id,name,email)
    print(val,'val')
    if(val):
        send_to_kafka({'event': 'customer_updated', 'previous_email': val,'name':name,'email':email})
        return jsonify({'message': 'Customer updated successfully','name':name,'email':email}), 200
    else:
        return jsonify('Not able to update customer'), 500

    
        
    
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    
    email= delete_query(id)
    if(email):
        send_to_kafka({'event': 'customer_deleted',  'email': email})
        return jsonify({'message': 'Customer deleted successfully'}), 200
    else:
        return jsonify('Not able to delete customer'), 500
       

def start_consumer():
    os.system("python ./src/integrations/kafka/kafka_consumer.py")

if __name__ == '__main__':
    # Start the Kafka consumer process
    consumer_process = Process(target=start_consumer)
    consumer_process.start()

    # Start the Flask app
    app.run(debug=True)

    # Wait for both processes to finish
    consumer_process.join()