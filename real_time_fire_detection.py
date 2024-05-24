import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "yolov5"))
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import ImageGrab, Image
import time
import multiprocessing
from multiprocessing import Pipe

def switch_camera(current_camera):
    return cap2 if current_camera == cap1 else cap1

def fire_detection(url_yolov5, path_weight, current_camera):
    img_counter = 0
    model = torch.hub.load(
        url_yolov5, "custom", path=path_weight, source="local", force_reload=True
    )
    USERNAME = "admin"
    PASSWORD = "ZSLHOS"
    IP = "192.168.1.100"
    PORT = "554"

    URL = "rtsp://{}:{}@{}:{}/onvif1".format(USERNAME, PASSWORD, IP, PORT)
    cap1 = cv2.VideoCapture(URL, cv2.CAP_FFMPEG)
    cap2 = cv2.VideoCapture(0)

    current_camera = cap1
    
    CLASSES = ["lua"]
    
    size = 416
    count = 0

    fps_start_time = time.time()
    fps = 0

    while True:
        ret, frame = current_camera.read()
        
        count += 1
        if count % 2 != 0:
            continue
        if not ret:
            print("Failed to capture frame")
            current_camera = switch_camera(current_camera)
            ret, frame = current_camera.read()
        
        fps_end_time = time.time()
        fps_diff_time = fps_end_time - fps_start_time
        fps = 1 / fps_diff_time
        fps_start_time = fps_end_time
        fps_text = "FPS: {:.2f}ms".format(fps)
        frame = cv2.resize(frame, (600, 500))
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        converted = Image.fromarray(converted)
        results = model(converted)

        for index, row in results.pandas().xyxy[0].iterrows():
            x1 = int(row["xmin"])
            y1 = int(row["ymin"])
            x2 = int(row["xmax"])
            y2 = int(row["ymax"])
            id = row["class"]
            acuracy = row["confidence"]

            if acuracy * 100 > 70:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
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
                message = "lua"
                try:
                    os.remove("log.txt")
                except:
                    pass
                try:
                    # img_name = "opencv_frame_{}.png".format(img_counter)
                    img_name = "fire_detect_image.jpg"
                    # cv2.imwrite(img_name, frame)
                    cv2.imwrite(filename=img_name, img=frame)
                    print("{} written!".format(img_name))
                    img_counter += 1
                    with open("log.txt", "w") as f:
                        # f.write("lua" if acuracy * 100 > 70 else "")
                        f.write(message)
                except:
                    pass
            else:
                message = ""
                try:
                    os.remove("log.txt")
                except:
                    pass
                try:
                    with open("log.txt", "w") as f:
                        # f.write("lua" if acuracy * 100 > 70 else "")
                        f.write(message)
                except:
                    pass

        cv2.imshow("result", frame)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            os.remove("log.txt")
            break
    
    current_camera.release()
    os.remove("log.txt")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    url_yolov5 = "D:\\Desktop_data\\local_code\\thay_linh\\python_socket_sever_for_esp32_from_git\\yolov5"
    path_weight = "runs/train/exp7/weights/best.pt"
    USERNAME = "admin"
    PASSWORD = "ZSLHOS"
    IP = "192.168.1.100"
    PORT = "554"

    URL = "rtsp://{}:{}@{}:{}/onvif1".format(USERNAME, PASSWORD, IP, PORT)
    cap1 = cv2.VideoCapture(URL, cv2.CAP_FFMPEG)
    cap2 = cv2.VideoCapture(0)

    current_camera = cap1

    fire_detection(url_yolov5, path_weight, current_camera)
