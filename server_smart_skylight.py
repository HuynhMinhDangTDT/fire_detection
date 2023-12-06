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


def server():
    count = 0
    email_sender = "mdthienxa@gmail.com"
    email_password = "gimf yhuc jtwz atok"
    email_receiver = "vndang00@gmail.com"

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
        sock = socket.socket()
        host = "192.168.1.18"  # ESP32 IP in local network
        port = 8090  # ESP32 Server Port
        sock.connect((host, port))
        while True:
            message = ""
            count += 1
            if count % 4 != 0:
                continue
            try:
                with open("log.txt", "r") as f:
                    message = f.read()
            except:
                message = ""
            # print(message)
            message_encode = message.encode()
            # sock.send(message_encode)

            time.sleep(1.5)
            content = sock.recv(5)
            # print(content)
            content = content.decode("utf-8")
            if len(content) == 0:
                break
            else:
                # print(content)
                # respond_data_to_web(content)
                listdata = {
                    "temperature": content,
                    "message": message
                }
                sock.send(message_encode)
            if message == "lua":
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
            yield listdata
            # yield content
            # yield message

                
        print("Closing connection")
        sock.close()


if __name__ == "__main__":
    server()
