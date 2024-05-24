import socket
import time
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# start_ip = 1
# end_ip = 255
# host = "172.20.10.3"  # ESP32 IP in local network
# saving_host = "172.20.10.3"
# port = 8090  # ESP32 Server Port
# sock = socket.socket()
# try:
#     sock.connect((host, port))
# except:
#     connection_established = False
#     if not connection_established:
#         for i in range(start_ip, end_ip + 1):
#         # Construct the current IP address
#             host = f"172.20.10.{i}"

#             # Create a socket and attempt to connect
#             sock = socket.socket()
#             sock.settimeout(1)  # Set a timeout for the connection attempt
#             try:
#                 sock.connect((host, port))
#                 print(f"Connected to {host}:{port}")
#                 saving_host = "172.20.10.3"
#                 saving_host = host
#                 connection_established = True
#                 # Perform any additional actions if the connection is successful
#                 # For example, you might break out of the loop or send/receive data
#                 break
#             except socket.error as e:
#                 # Connection failed, continue to the next IP address
#                 print(f"Connection to {host} failed: {e}")
#             finally:
#                 sock.close()
# email_sender = "bennohz554@gmail.com" #Email người gửi
# email_password = "sxsr winn thun opiv" #Nhập pass của tụi em vô đợt anh có làm cho tụi em 
# email_receiver = ["nguyengiaphucvl2019@gmail.com","bennohz554@gmail.com"] #Email người nhận

# subject = "Cảnh báo hiện phát hiện cháy"
# body = """
# Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sao đó gọi cho 114
# """
# # em = EmailMessage()
# # em["From"] = email_sender
# # em["To"] = email_receiver
# # em["subject"] = subject
# # em.set_content(body)

# msg = MIMEMultipart()
# # msg["To"] = email_receiver
# msg["To"] = ", ".join(email_receiver)
# msg["From"] = email_sender
# msg["subject"] = subject

# msg_ready = MIMEText('Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sao đó gọi cho 114')

# image_open = open('fire_detect_image.jpg', 'rb').read()
# image_ready = MIMEImage(image_open,'jpg', name = 'Nguon chay')

# msg.attach(msg_ready)
# msg.attach(image_ready)

# context = ssl.create_default_context()

# # if message == "lua":
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, email_receiver, msg.as_string())
    
def server():
    count = 0
    email_sender = "bennohz554@gmail.com" #Email người gửi
    email_password = "sxsr winn thun opiv" #Nhập pass của tụi em vô đợt anh có làm cho tụi em 
    # email_receiver = "nguyengiaphucvl2019@gmail.com" #Email người nhận
    email_receiver = ["nguyengiaphucvl2019@gmail.com","bennohz554@gmail.com","huynhphuclinh@gmail.com"] #Email người nhận

    subject = "Cảnh báo phát hiện nguồn cháy"
    # body = """
    # Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sao đó gọi cho 114
    # """
    # em = EmailMessage()
    # em["From"] = email_sender
    # em["To"] = email_receiver
    # em["subject"] = subject
    # em.set_content(body)

    msg = MIMEMultipart()
    # msg["To"] = email_receiver
    msg["To"] = ", ".join(email_receiver)
    msg["From"] = email_sender
    msg["subject"] = subject

    
    while True:
        # Initialize variables
        saving_host = "192.168.1.103"
        port = 8090  # ESP32 Server Port
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
            message_dieu_khien_encode = message_dieu_khien.encode()
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
                sock.send(message_dieu_khien_encode)
                print(message_encode)
            if message == "lua":
                msg_ready = MIMEText('Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sau đó gọi cho 114')

                image_open = open('fire_detect_image.jpg', 'rb').read()
                image_ready = MIMEImage(image_open,'jpg', name = 'Nguon chay')

                msg.attach(msg_ready)
                msg.attach(image_ready)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, msg.as_string())
            yield listdata
            # yield content
            # yield message

                
            print("Closing connection")
            sock.close()


if __name__ == "__main__":
    server()
