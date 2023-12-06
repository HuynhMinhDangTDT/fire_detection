import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import ImageGrab, Image
import time
import socket
import time
import sys
import os

# sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'yolov5'))

# from server_smart_skylight import server_sent


# sock = socket.socket()

# host = "192.168.1.7" #ESP32 IP in local network
# port = 8090            #ESP32 Server Port

# sock.connect((host, port))


# message = "Hello World"
# message_encode = message.encode()
# sock.send(message_encode)
def fire_detection(url_yolov5, path_weight):
    model = torch.hub.load(
        url_yolov5, "custom", path=path_weight, source="local", force_reload=True
    )

    CLASSES = ["lua"]

    # cap = cv2.VideoCapture('D:\\vehicle_detection\\highway.mp4')
    cap = cv2.VideoCapture(0)

    size = 416
    count = 0

    fps_start_time = time.time()
    fps = 0

    while cap.isOpened():
        ret, frame = cap.read()
        # fps_start_time = time.time()
        count += 1
        if count % 4 != 0:
            continue

        fps_end_time = time.time()
        fps_diff_time = fps_end_time - fps_start_time
        fps = 1 / fps_diff_time
        fps_start_time = fps_end_time
        fps_text = "FPS: {:.2f}ms".format(fps)
        frame = cv2.resize(frame, (600, 500))
        # cv2.line(frame, (79,cy1),(599,cy1), (0,0,255), 2)
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        converted = Image.fromarray(converted)
        results = model(converted)

        # a= results.pandas().xyxy[0].sort_values('xmin')  # sorted left-right
        # print(results.pandas().xyxy[0])
        for index, row in results.pandas().xyxy[0].iterrows():
            # print(row)
            x1 = int(row["xmin"])
            y1 = int(row["ymin"])
            x2 = int(row["xmax"])
            y2 = int(row["ymax"])
            id = row["class"]
            acuracy = row["confidence"]
            # print(id)
            if acuracy * 100 > 70:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # rectx1,recty1 =((x1+x2)/2,(y1+y2)/2)
                # rectcenter = int(rectx1),int(recty1)
                # cx = rectcenter[0]
                # cy = rectcenter[1]
                # cv2.circle(frame, (cx,cy), 3, (0,255,0), -1)
                server_sent(message="lua")
                cv2.putText(
                    frame,
                    str(CLASSES[id]) + ": " + str(round(acuracy, 2)),
                    (x1, y1),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 255, 0),
                    2,
                )
                cv2.putText(
                    frame,
                    fps_text,
                    (5, 30),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 0),
                    1,
                )

        cv2.imshow("result", frame)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    fire_detection(url_yolov5="", path_weight="")
