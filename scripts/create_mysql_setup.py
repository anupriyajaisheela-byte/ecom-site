import pymysql
import sys

# Configuration - update if you want different names
ROOT_USER = 'root'
ROOT_PASSWORD = 'dbms123'  # provided by user
HOST = '127.0.0.1'
PORT = 3306

DB_NAME = 'ecom_db'
APP_USER = 'ecom_user'
APP_PASSWORD = 'dbms123'

def main():
    try:
        conn = pymysql.connect(host=HOST, user=ROOT_USER, password=ROOT_PASSWORD, port=PORT)
    except Exception as e:
        print('Failed to connect to MySQL as root:', e)
        sys.exit(1)

    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            # Create user and grant privileges
            cur.execute(f"CREATE USER IF NOT EXISTS '{APP_USER}'@'localhost' IDENTIFIED BY %s;", (APP_PASSWORD,))
            cur.execute(f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* TO '{APP_USER}'@'localhost';")
            cur.execute("FLUSH PRIVILEGES;")
        conn.commit()
        print(f"Database `{DB_NAME}` and user `{APP_USER}` ensured.")
    except Exception as e:
        print('Error creating database or user:', e)
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
