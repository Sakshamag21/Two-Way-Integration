# Two Way Integration Project

This project demonstrates a two-way integration between a MySQL database and Stripe, utilizing Kafka messaging for communication. The integration allows for seamless synchronization of customer data between the two systems.

## Folder Structure:

- **src/**
  - **integrations/**
    - **kafka/**
      - `kafka_consumer.py`: Handles Kafka message consumption and processing.
      - `stripe_integration.py`: Manages interactions with Stripe API for customer operations.
  - **services/**
    - `inward_sync.py`: Handles webhook events and updates the MySQL database.
  - **utils/**
    - `database.py`: Contains database connection and query execution functions.
    - `random_number.py`: Generate random ids for the creation of customer.
- **api.py**: Contains Flask API endpoints for customer operations.
- **.env**: Environment variables file.
- **requirements.txt**: List of project dependencies.

## Features:

- **Modular Design:** Each component of the system is organized into separate modules, promoting code reusability and maintainability.
- **Integration Flexibility:** The architecture supports integration with multiple systems, including Stripe, Salesforce, and potentially others, by encapsulating integration logic within dedicated modules.
- **Scalability:** The system is designed to handle a growing volume of customer data and integrate seamlessly with other systems as the product evolves.
- **Configurability:** Environment variables stored in the `.env` file allow for easy configuration of API keys, database credentials, and other settings.
- **Documentation:** The project includes comprehensive documentation within the codebase, including docstrings, comments, and a README file to facilitate understanding and usage.

## Setup and Usage:

1. **Environment Setup:**
   - Install Python 3.x and ensure pip is installed.
   - Clone the project repository.

2. **Install Dependencies:**
   - Navigate to the project directory.
   - Run `pip install -r requirements.txt` to install project dependencies.

3. **Configuration:**
   - Update the `.env` file with appropriate environment variables, including API keys and database credentials.

4. **Run the Services:**
   - Start each component of the project by executing the corresponding Python scripts using command `python api.py` 

5. **Testing and Deployment:**
   - Visit `unitest` folder and run `testCase.py` 

## Contributing:

Contributions to the project are welcome! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

