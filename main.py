import redis
import logging
import os
from datetime import datetime

# --- Setup Logging ---
log_dir = "logs"
log_file = os.path.join(log_dir, "main.log")

# Create logs directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Configure logging to write to file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# --- Constants ---
CREDENTIALS_FILE = "credentials.txt"

# --- Read Credentials ---
def read_credentials(file_path):
    """Read and parse credentials from a file."""
    credentials = {}
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Credentials file {file_path} not found.")

        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Skip empty lines and comments
                try:
                    key, value = line.split("=", 1)
                    credentials[key.strip()] = value.strip()
                except ValueError:
                    logging.warning(f"Skipping malformed line: {line}")

        # Validate required credentials
        if "USERNAME" not in credentials or "PASSWORD" not in credentials:
            raise ValueError("USERNAME or PASSWORD not found in credentials file.")

        return credentials["USERNAME"], credentials["PASSWORD"]

    except Exception as e:
        logging.error(f"Failed to read credentials: {e}")
        raise

# --- Connect to Redis ---
def connect_to_redis(username, password, host, port):
    """Establish a connection to Redis with error handling."""
    try:
        r = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            ssl_cert_reqs=None
        )
        r.ping()  # Test connection
        logging.info("Successfully connected to Redis.")
        return r
    except redis.ConnectionError as e:
        logging.error(f"Redis connection failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected Redis error: {e}")
        raise

# --- Main Execution ---
if __name__ == "__main__":
    try:
        # Read credentials
        USERNAME, PASSWORD = read_credentials(CREDENTIALS_FILE)
        logging.info("Successfully read credentials.")

        # Connect to Redis (replace with your actual host and port)
        redis_conn = connect_to_redis(
            username=USERNAME,
            password=PASSWORD,
            host="your-redis-hostname",
            port=12345
        )

        # Your Redis operations here...
        logging.info("Redis connection is ready for use.")

    except FileNotFoundError as e:
        logging.error(f"Credentials file error: {e}")
    except ValueError as e:
        logging.error(f"Credentials error: {e}")
    except redis.ConnectionError:
        logging.error("Failed to connect to Redis. Check credentials and network.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
