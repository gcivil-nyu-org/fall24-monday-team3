from dotenv import load_dotenv
import os
load_dotenv("database.env")
print("Database Name:", os.getenv('DATABASE_NAME'))
print("Database User:", os.getenv('DATABASE_USER'))
print("Database Host:", os.getenv('DATABASE_HOST'))
print("Database Port:", os.getenv('DATABASE_PORT'))