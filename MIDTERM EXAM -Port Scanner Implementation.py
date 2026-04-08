import socket
from datetime import datetime

def scan_ports(target_host, start_port, end_port):
    """
    Scan a range of ports on the target host.
    Args:
        target_host (str): The hostname or IP address to scan.
        start_port (int): The starting port number.
        end_port (int): The ending port number.
    """
    print(f"Scanning {target_host} from port {start_port} to {end_port}...")
    # Record start time
    start_time = datetime.now()

    # Loop through the port range
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set timeout to avoid hanging
            try:
                result = sock.connect_ex((target_host, port))
                # connect_ex returns 0 if port is open
                if result == 0:
                    print(f"[OPEN] Port {port}")
                else:
                    print(f"[CLOSED] Port {port}")
            except socket.gaierror:
                print(f"Hostname could not be resolved: {target_host}")
                break
            except socket.timeout:
                print(f"Timeout occurred for port {port}")
            except Exception as e:
                print(f"Error scanning port {port}: {e}")

    # Record end time
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Scanning completed in {duration}")

def validate_ports(start_port, end_port):
    """
    Validate port inputs.
    """
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
        raise ValueError("Ports must be in the range 1-65535.")
    if start_port > end_port:
        raise ValueError("Start port must be less than or equal to end port.")

if __name__ == "__main__":
    # User input for target host and port range
    target_host = input("Enter target host (127.0.0.1 or scanme.nmap.org): ").strip()
    try:
        start_port = int(input("Enter start port (e.g., 1): "))
        end_port = int(input("Enter end port (e.g., 1024): "))
        validate_ports(start_port, end_port)
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        exit()

    # Run the port scanner
    scan_ports(target_host, start_port, end_port)