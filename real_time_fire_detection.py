import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "yolov5"))
import torch
from server_smart_skylight import server
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import ImageGrab, Image
import time
import multiprocessing
from multiprocessing import Pipe


def fire_detection(url_yolov5, path_weight):
    # url_yolov5 = "C:\\Users\\PC\\Desktop\\local_code\\thay_linh\\python_socket_sever_for_esp32\\yolov5"
    # path_weight = "runs/train/exp7/weights/best.pt"
    model = torch.hub.load(
        url_yolov5, "custom", path=path_weight, source="local", force_reload=True
    )

    CLASSES = ["lua"]

    USERNAME = "admin"
    PASSWORD = "ZSLHOS"
    IP = "192.168.1.17"
    PORT = "554"
    # cap = cv2.VideoCapture('D:\\vehicle_detection\\highway.mp4')
    try:
        # cap = cv2.VideoCapture("C:\\Users\\PC\\Desktop\\local_code\\thay_linh\\python_socket_sever_for_esp32\\test.mp4")
        URL = "rtsp://{}:{}@{}:{}/onvif1".format(USERNAME, PASSWORD, IP, PORT)
        try:
            cap = cv2.VideoCapture(URL, cv2.CAP_FFMPEG)
        except:
            cap = cv2.VideoCapture(0)
    except:
        try:
            os.remove("log.txt")
        except:
            pass
    # cap = cv2.VideoCapture(0)
    size = 416
    count = 0

    fps_start_time = time.time()
    fps = 0

    while cap.isOpened():
        ret, frame = cap.read()
        # fps_start_time = time.time()
        count += 1
        if count % 2 != 0:
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
                # try:
                #     server_sent(message = 'lua')
                # except:
                #     pass
                message = "lua"
            else:
                message = ""
                try:
                    os.remove("log.txt")
                except:
                    pass
            try:
                with open("log.txt", "w") as f:
                    f.write(message)
            except:
                pass
        cv2.imshow("result", frame)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            os.remove("log.txt")
            break

    cap.release()
    os.remove("log.txt")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    url_yolov5 = "C:\\Users\\PC\\Desktop\\local_code\\thay_linh\\python_socket_sever_for_esp32\\yolov5"
    path_weight = "runs/train/exp7/weights/best.pt"

    fire_detection(url_yolov5, path_weight)
    
    # task1 = multiprocessing.Process(target=server)
    # task1.start()

    # task2 = multiprocessing.Process(target=fire_detection(url_yolov5, path_weight))
    # task2.start()

    # task1.join()
    # task2.join()

    # task2.join()
    # fire_detection(url_yolov5 = '',path_weight = '')
