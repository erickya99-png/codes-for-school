import socket
import sys
import threading
import time

# Set server address and port
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Non-privileged port


def start_server() -> None:
    """Run the TCP server and handle one client connection."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Server is listening on {HOST}:{PORT}...")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    print(f"Server received: {data.decode()}")
                    response = "Hello from server!"
                    conn.sendall(response.encode())
                    print("Response sent to client.")
                else:
                    print("No data received.")
    except Exception as e:
        print(f"Server error: {e}")


def start_client() -> None:
    """Connect to the TCP server, send a message, and print the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            message = "Hello from client!"
            client_socket.sendall(message.encode())
            print(f"Sent: {message}")

            data = client_socket.recv(1024)
            print(f"Received from server: {data.decode()}")
            print("Client disconnecting gracefully.")
    except ConnectionRefusedError:
        print("Could not connect. Is the server running?")
    except Exception as e:
        print(f"Client error: {e}")


def run_demo() -> None:
    """Run a simple demo by starting the server in a thread and then the client."""
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    start_client()
    server_thread.join(timeout=1)


def print_usage() -> None:
    print("Usage: python \"test for CYB333 Security Automation.py\" [server|client|demo]")
    print("  server - run as server")
    print("  client - run as client")
    print("  demo   - run server and client in the same script for one exchange")


if __name__ == "__main__":
    mode = "demo"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode in ("server", "s"):
        start_server()
    elif mode in ("client", "c"):
        start_client()
    elif mode == "demo":
        run_demo()
    else:
        print_usage()