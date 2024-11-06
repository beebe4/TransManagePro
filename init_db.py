from database import get_db_connection

def init_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        with open('schema.sql', 'r') as f:
            schema = f.read()
            cur.execute(schema)
        conn.commit()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_database()
