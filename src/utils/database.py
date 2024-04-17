import mysql.connector

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'zenskar_test'
}

def check_existing_customer(email):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    query = "SELECT ID FROM customer WHERE email = %s"
    values = (email,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def insert_query(id, name, email):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    existing_customer = check_existing_customer(email)
    print(existing_customer)
    if existing_customer:
        print("Customer with email", email, "already exists with ID:", existing_customer[0])
        return existing_customer[0]
    
    query = "INSERT INTO customer (ID, name, email) VALUES (%s, %s, %s)"
    values = (id, name, email)
    try:
        cursor.execute(query, values)
        conn.commit()
        customer_id = cursor.lastrowid
        if customer_id is not None:
            print("Customer inserted with ID:", customer_id)
            return customer_id
        else:
            return None
    except Exception as e:
        print("Error executing insert query:", e)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def update_query(id,name,email):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM customer WHERE id = %s", (id,))
    previous_name, previous_email = cursor.fetchone()
    try:
        updates = []
        query = "UPDATE customer SET"
        params = []
        if name:
            query += " name = %s,"
            params.append(name)
            updates.append(f"Name updated from '{previous_name}' to '{name}'")
        if email:
            query += " email = %s,"
            params.append(email)
            updates.append(f"Email updated from '{previous_email}' to '{email}'")
        query = query.rstrip(',') + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, params)
        conn.commit()
        return previous_email
    except Exception as e:
        print("Error executing insert query:", e)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def delete_query(id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, email FROM customer WHERE id = %s", (id,))
        name, email = cursor.fetchone()
        cursor.execute("DELETE FROM customer WHERE id = %s", (id,))
        conn.commit()
        return email
    except Exception as e:
        print("Error executing insert query:", e)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()
