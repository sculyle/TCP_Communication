import socket
import threading # allows server shutdown via input (quit/ctrl+c)

host = ''  # Listen on all network interfaces
Port = 23456  # Assigned port number

# Connection Setup
def start_server():

    # Using sockets: https://docs.python.org/3/howto/sockets.html
    # Socket library documentation: https://docs.python.org/3/library/socket.html
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, Port))
    server_socket.listen(5)
    print(f"Server started - Listening on port {Port}...")
    
    # Connection (via thread)
    try:
        while True:
            client_socket, client_addr = server_socket.accept() # need both or cant close
            print(f"Connection from {client_addr} established")
            # threading documentation: https://docs.python.org/3/library/threading.html
            # threading research source: https://www.mandricmihai.com/2021/01/Python%20threads%20how%20to%20timeout%20and%20use%20KeyboardIntrerupt%20CTRL%20%20C.html
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("\nShutting down server")
    finally:
        server_socket.close()


# Input handling 
def handle_client(client_socket):
    moveon_check = True # allow to exit smooth (no breaks)

    try:
        while moveon_check == True:
            data = client_socket.recv(1024) # 2^10 buffer, https://stackoverflow.com/questions/7174927/when-does-socket-recvrecv-size-return
            command = data.decode().strip().upper()
            print(f"Received command: {command}")
            if command == "QUIT":
                response = "Closing connection"
                client_socket.sendall(response.encode())
                moveon_check = False
            elif command == "TIME":
                # Time pulled using "datetime" library
                # Documentation: https://docs.python.org/ko/3/library/datetime.html
                from datetime import datetime
                response = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                response = "Invalid command"
            client_socket.sendall(response.encode())
    finally:
        print("Closing client connection")
        client_socket.close() # avoid inf. loop

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True # daemon = background script
    server_thread.start()

    try:  # avoid inf. loop
        while True:
            command = input()
            if command.upper() == "QUIT":
                print("Stopping server...")
                break
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Stopping server.")
