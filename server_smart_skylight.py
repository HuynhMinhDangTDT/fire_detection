import socket
import time
from email.message import EmailMessage
import ssl
import smtplib


# sock = socket.socket()

# host = "192.168.1.9" #ESP32 IP in local network
# port = 8090  #ESP32 Server Port

# def server_sent(message):
#     sock = socket.socket()

#     host = "192.168.1.9" #ESP32 IP in local network
#     port = 8090  #ESP32 Server Port

#     sock.connect((host, port))
#     message_encode = message.encode()
#     sock.send(message_encode)

#     print("Closing connection")
#     sock.close()

# def server_recive():

#     sock.connect((host, port))

#     while True:
#         while True:
#             time.sleep(1.5)
#             content = sock.recv(5)
#             # print(content)
#             if len(content) ==0:
#                 break
#             else:
#                 print(content)
#                 return content

#         print("Closing connection")
#         sock.close()

# count = 0
# email_sender = "mdthienxa@gmail.com"
# email_password = "ubkq irqt hhqj trpm"
# email_receiver = "vndang00@gmail.com"

# subject = "Cảnh báo hiện phát hiện cháy"
# body = """
# Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sao đó gọi cho 114
# """
# em = EmailMessage()
# em["From"] = email_sender
# em["To"] = email_receiver
# em["subject"] = subject
# em.set_content(body)

# context = ssl.create_default_context()

# while True:
#     sock = socket.socket()
#     host = "192.168.1.11"  # ESP32 IP in local network
#     port = 8090  # ESP32 Server Port
#     sock.connect((host, port))
#     while True:
#         message = ""
#         count += 1
#         if count % 4 != 0:
#             continue
#         try:
#             with open("log.txt", "r") as f:
#                 message = f.read()
#         except:
#             message = ""
#         # print(message)
#         message_encode = message.encode()
#         # sock.send(message_encode)

#         time.sleep(1.5)
#         content = sock.recv(5)
#         print(content)
#         content = content.decode("utf-8")
#         if len(content) == 0:
#             break
#         else:
#             # print(content)
#             # respond_data_to_web(content)
#             listdata = {
#                 "temperature": content,
#                 "message": message
#             }
#             sock.send(message_encode)
#             print(message_encode)
#         if message == "lua":
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#                 smtp.login(email_sender, email_password)
#                 smtp.sendmail(email_sender, email_receiver, em.as_string())
#         # yield listdata
#         # yield content
#         # yield message

            
#     print("Closing connection")
#     sock.close()
start_ip = 1
end_ip = 255
host = "192.168.1.3"  # ESP32 IP in local network
port = 8090  # ESP32 Server Port
sock = socket.socket()
try:
    sock.connect((host, port))
except:
    connection_established = False
    if not connection_established:
        for i in range(start_ip, end_ip + 1):
        # Construct the current IP address
            host = f"192.168.1.{i}"

            # Create a socket and attempt to connect
            sock = socket.socket()
            sock.settimeout(1)  # Set a timeout for the connection attempt
            try:
                sock.connect((host, port))
                print(f"Connected to {host}:{port}")
                saving_host = host
                connection_established = True
                # Perform any additional actions if the connection is successful
                # For example, you might break out of the loop or send/receive data
                break
            except socket.error as e:
                # Connection failed, continue to the next IP address
                print(f"Connection to {host} failed: {e}")
            finally:
                sock.close()
def server():
    count = 0
    email_sender = "" #Email người gửi
    email_password = "" #Nhập pass của tụi em vô đợt anh có làm cho tụi em 
    email_receiver = "" #Email người nhận

    subject = "Cảnh báo hiện phát hiện cháy"
    body = """
    Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sao đó gọi cho 114
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    
    while True:
        # Initialize variables
        sock = socket.socket()
        sock.connect((saving_host, port))
        while True:
            
            message = ""
            message_dieu_khien = ""
            count += 1
            if count % 4 != 0:
                continue
            try:
                with open("log.txt", "r") as f:
                    message = f.read()
            except:
                message = ""
                
            try:
                with open("log_dieu_khien.txt", "r") as f:
                    message_dieu_khien = f.read()
            except:
                message_dieu_khien = ""
                
                
            # print(message)
            message_encode = message.encode()
            # sock.send(message_encode)

            time.sleep(1.5)
            content = sock.recv(100)
            # print(content)
            content = content.decode("utf-8")
            print(content)
            mang_ket_qua = content.split(";")
            print(mang_ket_qua)
            if len(content) == 0:
                break
            else:
                # print(content)
                # respond_data_to_web(content)
                listdata = {
                    "temperature": mang_ket_qua[0],
                    "humidity": mang_ket_qua[1],
                    "photoresistor": mang_ket_qua[2],
                    "rain": mang_ket_qua[3],
                    "ultrasonic": mang_ket_qua[4],
                    "mode_dieu_khien": mang_ket_qua[5],
                    "message": message
                    
                }
                # print(type(mang_ket_qua[5]))
                sock.send(message_encode)
                
                print(message_encode)
            if message == "lua":
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
            yield listdata
            # yield content
            # yield message

                
            print("Closing connection")
            sock.close()


if __name__ == "__main__":
    server()
