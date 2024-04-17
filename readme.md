# Two-Way Integration Project

This project demonstrates a two-way integration between a MySQL database and Stripe, utilizing Kafka messaging for communication. The integration allows for seamless synchronization of customer data between the two systems.

## Components

### 1. API Service (`api.py`)

Exposes endpoints for creating, updating, and deleting customers in the MySQL database. It also publishes events related to these actions to a Kafka topic.

### 2. Kafka Consumer (`kafka_consumer.py`)

Listens for messages from the Kafka topic and processes them accordingly. In this case, it interacts with the Stripe API to create, update, or delete customers based on the received events.

### 3. Inward Sync Service (`inward_sync.py`)

Receives webhook events from Stripe and updates the MySQL database accordingly.

## Prerequisites

- Python 3.x
- Flask
- Confluent Kafka
- Stripe API
- MySQL Server
- Python libraries: `mysql-connector`, `stripe`, `dotenv`

## Setup

1. **MySQL Database Setup:** Ensure MySQL server is running and create a database named `zenskar_test`.
2. **Stripe API Setup:** Obtain a Stripe API key and set it as the `SECRET_KEY` environment variable in a `.env` file.
3. **Install Dependencies:** Run `pip install -r requirements.txt` to install required Python packages.
4. **Run the Services:** Start each component of the project by running the respective Python scripts (`api.py`, `kafka_consumer.py`, `inward_sync.py`).

## Usage

1. **API Service:**
   - Endpoint: `/customers`
   - Methods: 
     - `POST`: Create a new customer. Requires `name` and `email` fields in the request body.
     - `PUT`: Update an existing customer. Requires customer ID in the URL path and `name` or `email` fields in the request body.
     - `DELETE`: Delete a customer. Requires customer ID in the URL path.
     
2. **Kafka Consumer:** Listens for events from the Kafka topic `customer_changes` and interacts with the Stripe API accordingly.

3. **Inward Sync Service:** Exposes a webhook endpoint `/webhook` to receive events from Stripe and update the MySQL database accordingly.

## Workflow

1. When a customer is created, updated, or deleted via the API service, an event is published to the Kafka topic.
2. The Kafka consumer listens for these events and processes them.
3. For customer creation and update events, the consumer interacts with the Stripe API to create or update the corresponding customer.
4. The inward sync service receives webhook events from Stripe and updates the MySQL database accordingly.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

