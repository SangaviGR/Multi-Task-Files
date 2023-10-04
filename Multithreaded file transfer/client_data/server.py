import socket
import threading
import os


#returns the host name of the current system
IP = socket.gethostbyname(socket.gethostname())

# random port number - to identify the process
PORT = 65534

SEPARATOR = "<SEPARATOR>"

# Path to the server folder
SERVER_DATA_PATH = "C://Users//DELL//Desktop//sem4//FILE//server_data"


def handle_client(conn, addr):
   print(f"[NEW CONNECTION] {addr} connected.")
   conn.send("OK#Connected to the File Server.".encode("ascii"))

   while True:
       
       #our socket is going to receive data with buffer size of 1024 bytes at a time.
       data = conn.recv(1024).decode("ascii")
       
       data = data.split("#")
       action = data[0]
           

       if action == "LIST":
           #prints a list of names of all the files present in the specified path
           files = os.listdir(SERVER_DATA_PATH)
               
           send_data = "OK#"

           if len(files) == 0:
               send_data += "The server directory is empty"
           else:
               send_data += "\n".join(f for f in files)
           conn.send(send_data.encode("ascii"))

       elif action == "UPLOAD":
           name = data[1]
           
           filepath = os.path.join(SERVER_DATA_PATH, name)
           print(filepath)
           with open(filepath, "w") as f:
                f.write(name)
           
           send_data = "OK#File uploaded successfully."
           conn.send(send_data.encode("ascii"))
           
       elif action == "DOWNLOAD":
           name = data[1]
           
           filepath = os.path.join(SERVER_DATA_PATH, name)
           print(filepath)
           filesize = os.path.getsize(filepath)
           
           
           send_data+= f"{filepath}{SEPARATOR}{filesize}"
           
           send_data = "OK#File downloaded successfully."
           conn.send(send_data.encode("ascii"))

       elif action == "DELETE":
           files = os.listdir(SERVER_DATA_PATH)
           send_data = "OK#"
           filename = data[1]
           filename = filename.split("/")[-1]

           if len(files) == 0:
               send_data += "The server directory is empty"
           else:
               if filename in files:
                   os.remove(f"{SERVER_DATA_PATH}//{filename}")
                   send_data += "File deleted successfully."
               else:
                   send_data += "File not found."

           conn.send(send_data.encode("ascii"))

       elif action == "LOGOUT":
           break
       elif action == "HELP":
           data = "OK#LIST: List all the files from the server.\nUPLOAD <path>: Upload a file to the server.\nDELETE <filename>: Delete a file from the server.\nLOGOUT: Disconnect from the server.\nHELP: List all the commands."
           conn.send(data.encode("ascii"))

   print(f"[DISCONNECTED] {addr} disconnected")
   conn.close()





if __name__ == "__main__":

       print("[STARTING] Server is starting")
       
       # create a socket object
       server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
       #binds it to a specific IP and port so that it can listen to incoming requests on that IP and port
       server.bind((IP, PORT))
       
       #Listen for connections made to the socket
       server.listen()
       
       print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

       while True:
           
           # used by a server to accept a connection request from a client.
           conn, addr = server.accept()
           
           # creates an instance of the threading.Thread class.
           thread = threading.Thread(target=handle_client, args=(conn, addr))
           
           # causes this thread to begin execution,
           thread.start()
           
           #return the number of active threads in the current thread's thread group
           print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")