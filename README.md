#yolov5 setup

Set up for computer has GPU
B1:
  Create environment ```conda create -n vehicle_detection python=3.8```

B2:
  activate environment:  ```conda activate vehicle_detection```
  install pytorch : ```conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia```
  git clone https://github.com/ultralytics/yolov5.git
  cd yolov5
   
  pip install opencv-python
  pip install pandas
  pip install requests
  pip install PyYAML
  pip install tqdm
  pip install matplotlib
  pip install seaborn


B3:
  https://github.com/roxa-delphi/yolov5_test/blob/main/test.py
  cd (target-dirctory)
  python test.py

B4:
  test result:
  run in terminal ```python real_time_counting.py```


Set up for computer only use CPU

B1:
  Create environment ```conda create -n vehicle_detection python=3.8```
B2:
  activate environment:  ```conda activate vehicle_detection```
  run in terminal 
  ```cd yolov5```
  ```git clone https://github.com/ultralytics/yolov5.git```
  ```pip install -r requirements.txt```
B3:
  test result:
  ```cd yolov5```
  run in terminal ```python real_time_counting.py```

Warning must be change Path/model be for run ```real_time_counting.py```
--> model = torch.hub.load('path_to\\yolov5', 'custom', path='runs/train/exp15/weights/best.pt', source='local', force_reload=True)

Train Custom data
First create file dataset has validation and image

Format repare dataset for training of yolov5
mydata
  ---images
    ---train (put file.jpg//png//...)
    ---valid  (put file.jpg//png//...) (20% of dataset)
  ---labels
    ---train (put file.txt)
    ---valid  (put file.txt) (20% of dataset)

Labels is validation folder

put folder mydata to yolov5 folder

if your validation is VOC file (file.xml) --> you must be change format to file.txt
Run ```xml2yolov5.py```

Auto seperate file from dataset folder to train and validation
Run ```yolov5_format_dataset.py```

Create file data train.yaml

train: C:\Users\PC\Desktop\local\car_bike_detection\car_bike_detection\xml_to_textYolo\yolov5\mydata\images\train
val: C:\Users\PC\Desktop\local\car_bike_detection\car_bike_detection\xml_to_textYolo\yolov5\mydata\images\valid

nc: 4
names: ['car','motorcycle','truck','bus']

put to yolov5/data

config file model pretrain (Ex: yolov5x.yml)
This file is in models folder

```
# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license

# Parameters
nc: 4  # number of classes ```Change number of class training```
depth_multiple: 1.33  # model depth multiple
width_multiple: 1.25  # layer channel multiple
anchors:
  - [10,13, 16,30, 33,23]  # P3/8
  - [30,61, 62,45, 59,119]  # P4/16
  - [116,90, 156,198, 373,326]  # P5/32

# YOLOv5 v6.0 backbone
backbone:
  # [from, number, module, args]
  [[-1, 1, Conv, [64, 6, 2, 2]],  # 0-P1/2
   [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
   [-1, 3, C3, [128]],
   [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
   [-1, 6, C3, [256]],
   [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
   [-1, 9, C3, [512]],
   [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
   [-1, 3, C3, [1024]],
   [-1, 1, SPPF, [1024, 5]],  # 9
  ]

# YOLOv5 v6.0 head
head:
  [[-1, 1, Conv, [512, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 6], 1, Concat, [1]],  # cat backbone P4
   [-1, 3, C3, [512, False]],  # 13

   [-1, 1, Conv, [256, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 4], 1, Concat, [1]],  # cat backbone P3
   [-1, 3, C3, [256, False]],  # 17 (P3/8-small)

   [-1, 1, Conv, [256, 3, 2]],
   [[-1, 14], 1, Concat, [1]],  # cat head P4
   [-1, 3, C3, [512, False]],  # 20 (P4/16-medium)

   [-1, 1, Conv, [512, 3, 2]],
   [[-1, 10], 1, Concat, [1]],  # cat head P5
   [-1, 3, C3, [1024, False]],  # 23 (P5/32-large)

   [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
  ]
```

Train Models
After prepare all of setup we now can train the model
```bash
python train.py --data train.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128
                                                                 yolov5s                    64
                                                                 yolov5m                    40
                                                                 yolov5l                    24
                                                                 yolov5x                    16
```
after finish trainning
run file ```danh_gia_model.py``` for showing the result of the models --> you can stop training if you see the result value converging in chart.

Run
```bash
python detect.py --weights yolov5s.pt --source 0                               # webcam
                                               img.jpg                         # image
                                               vid.mp4                         # video
                                               screen                          # screenshot
                                               path/                           # directory
                                               list.txt                        # list of images
                                               list.streams                    # list of streams
                                               'path/*.jpg'                    # glob
                                               'https://youtu.be/LNwODJXcvt4'  # YouTube
                                               'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
``` 
for testing the result.

Or you can run file ```real_time_counting.py``` for testing this project.

Reference
https://github.com/ultralytics/yolov5
https://github.com/ultralytics/yolov5/issues/388
https://github.com/ultralytics/yolov5/issues/36

For more information please contact me
Email: vndang00@gmail.com