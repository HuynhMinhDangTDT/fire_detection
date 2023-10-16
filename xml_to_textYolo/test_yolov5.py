#動画ファイルでの検出テスト
#  python test.py

import sys
import cv2
import torch


#モデルの読み込みと設定
model = torch.hub.load('ultralytics/yolov5','yolov5s')
#model = torch.hub.load('ultralytics/yolov5','yolov5m')

model.conf = 0.3	#検出の下限値
#model.classes = [0]	#0:person クラスだけ
#print(model.names)


#動画ファイルの読み込み
camera = cv2.VideoCapture("2022_0121_090959_863.MOV")


#動画すべてのフレームで処理をする
while True:

  ret, img = camera.read()
  if not ret :
    while cv2.waitKey(100) == -1:	#動画ファイルの最後ではキーを押すと終了
      pass
    break

  results = model(img)		#default=640
#  results = model(img, size=320)
#  results = model(img, size=480)

  #検出情報の描画
  for *bb, conf, cls in results.xyxy[0]:

      s   = model.names[int(cls)]+":"+'{:.1f}'.format(float(conf)*100)
      cc  = (255,255,0)
      cc2 = (128,0,0)

      cv2.rectangle(
          img,
          (int(bb[0]), int(bb[1])),
          (int(bb[2]), int(bb[3])),
          color=cc,
          thickness=2,
          )

      cv2.rectangle(img, (int(bb[0]), int(bb[1])-20), (int(bb[0])+len(s)*10, int(bb[1])), cc, -1)
      cv2.putText(img, s, (int(bb[0]), int(bb[1])-5), cv2.FONT_HERSHEY_PLAIN, 1, cc2, 1, cv2.LINE_AA)

  #表示
  cv2.imshow('color',img)

  #"q"を押すと終了
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break


camera.release()
cv2.destroyAllWindows()