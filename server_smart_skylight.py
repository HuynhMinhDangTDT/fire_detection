import socket
import time
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def server():
    count = 0
    email_sender = "bennohz554@gmail.com" #Email người gửi
    email_password = "sxsr winn thun opiv" #Nhập pass của tụi em vô đợt anh có làm cho tụi em 
    # email_receiver = "nguyengiaphucvl2019@gmail.com" #Email người nhận
    email_receiver = ["nguyengiaphucvl2019@gmail.com","bennohz554@gmail.com","vndang00@gmail.com"] #Email người nhận

    subject = "Cảnh báo hiện phát hiện cháy"
    
    msg = MIMEMultipart()
    # msg["To"] = email_receiver
    msg["To"] = ", ".join(email_receiver)
    msg["From"] = email_sender
    msg["subject"] = subject

    while True:
        # Initialize variables
        saving_host = "172.20.10.3"
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
                msg_ready = MIMEText('Cảnh báo hiện tại phát hiện đám cháy tại nhà bạn cần xem xét kỹ lưỡng sao đó gọi cho 114')

                image_open = open('fire_detect_image.jpg', 'rb').read()
                image_ready = MIMEImage(image_open,'jpg', name = 'Nguon chay')

                msg.attach(msg_ready)
                msg.attach(image_ready)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
            yield listdata
            # yield content
            # yield message

                
            print("Closing connection")
            sock.close()


if __name__ == "__main__":
    server()
