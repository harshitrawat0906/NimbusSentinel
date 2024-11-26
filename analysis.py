import pandas as pd
import re
from collections import defaultdict

# Sample restricted services
restricted_services = [
    '/identity/v3/auth/tokens',  # Example: Authentication service
    '/compute/v2.1/os-simple-tenant-usage',  # Example: Resource usage service
    '/networking/v2.0',  # Example: Networking service
]

# Create a function to parse the logs
def parse_logs(log_file_path):
    """
    Parse the logs and extract relevant fields.
    Assumes logs are in the format: <ip> - - [<timestamp>] "<method> <service> <http_version>" <status> <size> "-" "<user_agent>"
    """
    logs = []
    with open(log_file_path, 'r') as f:
        for line in f:
            # Regular expression to extract relevant parts of the log
            match = re.match(r'(?P<client_ip>\S+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<service>\S+) (?P<http_version>\S+)" (?P<status>\d+) (?P<size>\d+) "-" "(?P<user_agent>[^"]+)"', line)
            if match:
                logs.append(match.groupdict())
    return logs

# Function to track the number of access attempts and prepare data for DataFrame
def track_user_access(logs):
    """
    Track the number of access attempts per user (IP) and service.
    Returns a list of dictionaries for DataFrame creation.
    """
    access_tracker = defaultdict(lambda: defaultdict(int))
    
    # Track the access attempts per user and service
    for log in logs:
        client_ip = log['client_ip']
        service = log['service']
        access_tracker[client_ip][service] += 1

    # Convert the access tracker into a list of rows for DataFrame
    data = []
    for client_ip, services in access_tracker.items():
        for service, count in services.items():
            data.append({
                'User': client_ip,
                'Service': service,
                'Access Count': count
            })
    
    return data

# Function to generate the access table (DataFrame)
def generate_access_table(log_file_path):
    # Step 1: Parse the logs
    logs = parse_logs(log_file_path)
    
    # Step 2: Track user access
    access_data = track_user_access(logs)
    
    # Step 3: Create DataFrame from the access data
    df = pd.DataFrame(access_data)
    
    return df

# Example of how you would use this
if __name__ == "__main__":
    log_file_path = "access_logs.txt"  # Replace with the actual path to your log file
    access_table = generate_access_table("/var/log/apache2/horizon_access.log")
    
    # Display the table (or you can return it or save it as CSV)
    print(access_table)
