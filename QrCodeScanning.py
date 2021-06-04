import webbrowser
import codecs
import time
import os
from platform import release
import requests
from io import BytesIO

from pyzbar import pyzbar
from PIL import Image, ImageEnhance
import cv2 as cv

class DeQrCode:
    def __init__(self) -> None:
        self.str_out_logs = ""
        self.out_logs = ""
        self.out_log_pre = ""
        self.out_log_now = ""
        self.url_list = []
        self.len = 0
        self.cap = None
        
    def open_cam(self):
        self.cap = cv.VideoCapture(0)
    
    def read_from_cam(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                txt_list = pyzbar.decode(frame)
                # for txt in txt_list:
                #     barcodeData = txt.data.decode("utf-8")

                if len(txt_list) > 0:
                    barcodeData = txt_list[0].data.decode("utf-8")
                    self.url_list.append(barcodeData)

                    tmp_list = sorted(list(set(self.url_list)), key=self.url_list.index)

                    self.url_list = tmp_list
                    
                    
                if self.len != len(self.url_list):
                    print(self.url_list)
                    self.len = len(self.url_list)

                cv.imshow("camera", frame)
                if cv.waitKey(1) == 27:
                    break
                
                

    def out_put_to_log(self):
        with open("url list.log", 'w', encoding="utf-8") as f:
            f.writelines(self.url_list)
            
    def open_url(self):
        for url in self.url_list:
            time.sleep(1)
            webbrowser.open(url=url)
            
    def release(self):
        self.cap.release()
        cv.destroyAllWindows()
            


def get_ewm(img_adds):
    """ 读取二维码的内容： img_adds：二维码地址（可以是网址也可是本地地址 """
    if os.path.isfile(img_adds):
        # 从本地加载二维码图片
        img = Image.open(img_adds)
    else:
        # 从网络下载并加载二维码图片
        rq_img = requests.get(img_adds).content
        img = Image.open(BytesIO(rq_img))

    # img.show()  # 显示图片，测试用

    txt_list = pyzbar.decode(img)

    for txt in txt_list:
        barcodeData = txt.data.decode("utf-8")
        print(barcodeData)


def read_from_cam():
    cap = cv.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            txt_list = pyzbar.decode(frame)

            out_log = str()
            for txt in txt_list:
                barcodeData = txt.data.decode("utf-8")
                out_log += barcodeData

            cv.imshow("camera", frame)
            if cv.waitKey(1) == 27:
                break
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    # 解析本地二维码
    # get_ewm('F:\\QRCODE.BMP')
    # read_from_cam()

    # 解析网络二维码
    # get_ewm('https://gqrcode.alicdn.com/img?type=cs&shop_id=445653319&seller_id=3035998964&w=140&h=140&el=q&v=1')

    deQrCode = DeQrCode()
    deQrCode.open_cam()
    deQrCode.read_from_cam()
    deQrCode.release()
    deQrCode.open_url()
