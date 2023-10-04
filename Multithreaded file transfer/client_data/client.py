import socket


#returns the host name of the current system
IP = socket.gethostbyname(socket.gethostname())

# random port number - to identify the process
PORT = 65534

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connection to IP on the PORT. 
client.connect((IP, PORT))


while True:
    
       #socket is going to receive data, in a buffer size of 1024 bytes at a time.
       data = client.recv(1024).decode("ascii")
       
       action , msg = data.split("#")


       if action == "DISCONNECTED":
           print(f"[SERVER]: {msg}")
           break
       
        
       elif action == "OK":
           print(f"{msg}")
      
#   Input action to be done

       data = input(">> ")
       data = data.split(" ")
       action = data[0]


# To send data from client socket to the server side.

       if action == "HELP":
           client.send(action.encode("ascii"))
           
       elif action == "DELETE":
           client.send(f"{action}#{data[1]}".encode("ascii"))    
           
       
       elif action == "DOWNLOAD":
           print(client.send(f"{action}#{data[1]}".encode("ascii")) )
       
       elif action == "LIST":
           client.send(action.encode("ascii"))
      
           
       elif action == "UPLOAD":
           path = data[1]
           
           filename = path.split("/")[-1]
           path = path.replace(f"/{filename}", "")
           send_data = f"{action}#{filename}#{path}"
           client.send(send_data.encode("ascii"))


       elif action == "LOGOUT":
            client.send(action.encode("ascii"))
            break
           

print("Disconnected from the server.")
client.close()