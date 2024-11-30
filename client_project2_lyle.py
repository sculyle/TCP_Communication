# referece sources for project: 
# tcp general - https://pymotw.com/2/socket/tcp.html
# sockets     - https://realpython.com/python-sockets/

import sys
import socket 

def start_client(server_ip, port_num):
    
    print("Starting client program...")
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Attempt connection to the server
        # Socket connection resource: https://stackoverflow.com/questions/7749341/basic-python-client-socket-example
        print(f"Connecting to: {server_ip} on port: {port_num}...")
        client_socket.connect((server_ip, port_num))
        print("SUCCESS - Connection established with the server")

        quit_check = True  # allow to exit smooth (no breaks)
        
        while quit_check == True: 
            # Prompt user for input  (removes need for threading)
            user_input = input("Client> ").strip()

            # Send command to server
            client_socket.sendall(user_input.encode())

            # Handle quit command to exit the client program
            # uniform reading 'upper': https://www.w3schools.com/python/ref_string_upper.asp (also used in server prog.)
            if user_input.upper() == "QUIT":
                print(f"Closing connection to: {server_ip}")
                quit_check = False

            response_from_client = client_socket.recv(1024).decode()
            print(f"Server> {response_from_client}")

    # Python OS observations: https://docs.python.org/3/library/exceptions.html
    # ^ applies to both connection error and keyboard inturrupt
    except ConnectionError as cerror:
        print(f"Connection error: {cerror}")
    except KeyboardInterrupt:
        print("\n Interrupt via keyboard -> Closing connection")

    finally:
        # CLose out the socket
        print("Exiting Program...")
        client_socket.close()

if __name__ == "__main__":

    # Get server IP from the command line
    server_ip = sys.argv[1]
    port_num = 23456  # Port number to connect to

    start_client(server_ip, port_num)
