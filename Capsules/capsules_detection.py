import os
import cv2
import numpy as np
import os



##判斷是否為空膠囊函數
def empty_detection(img_path,img_file,im,im_gray):
        ##判斷空膠囊 需要提取藥丸 外殼的主輪廓 先做模糊
        im_blur = cv2.GaussianBlur(im_gray , (3,3) , 0)
        cv2.imshow('im_blur' , im_blur)

        ##二值化

        ret , im_bin = cv2.threshold(im_gray,
                                    210 , 255,
                                    cv2.THRESH_BINARY)
        cv2.imshow('im_bin' , im_bin)
        ##查找輪廓
        ###findCountours 改版後返回參數只有兩個
        cnts , hie = cv2.findContours(
                im_bin,
                cv2.RETR_CCOMP, ##提取兩層輪廓
                cv2.CHAIN_APPROX_NONE ##存儲所有輪廓做表點
        )
        ## 按週常進行過濾
        new_cnts = [] ##存放過濾後的輪廓
        for i in range(len(cnts)):
                cir_len = cv2.arcLength(cnts[i] , True) ##計算周常
                # print("cirlen:",cir_len)
                if cir_len > 1000:
                        new_cnts.append(cnts[i])
        ##繪製輪廓
        im_cnt = cv2.drawContours(im , new_cnts , -1,
                                (0,0,255) , 2)
        cv2.imshow('im_cnt' , im_cnt)
        if len(new_cnts) == 1: ##過濾後只剩一個輪廓 代表為空膠囊
                print("空膠囊",img_path)
                new_path = os.path.join("empty",img_file)
                os.rename(img_path , new_path)
                print("空膠囊成功移動至empty資料夾")
                return True
        else:
                return False
##判斷是否為有氣跑函數
def bub_detection(img_path,img_file,im,im_gray):
        img_blur = cv2.GaussianBlur(im_gray , (3,3) , 0)
        ##canny 邊緣提取
        im_canny = cv2.Canny(img_blur , 30 , 240) # 30:域值 240:模糊度
        cv2.imshow("im_canny" , im_canny)
        ##提取輪廓
        cnts , hie = cv2.findContours(
                im_canny,
                cv2.RETR_CCOMP, ##提取兩層輪廓
                cv2.CHAIN_APPROX_NONE ##存儲所有輪廓做表點
        )
        # print(len(cnts))
        # print(hie.shape)
        ##對輪廓進行篩選，過濾掉過大或過小的輪廓
        new_cnts = []
        for i in range(len(cnts)):
                area = cv2.contourArea(cnts[i])#計算面積
                cir_len = cv2.arcLength(cnts[i] , True) #計算周長

                if area >= 10000 or cir_len>=1000 or area < 5:
                        continue
                if hie[0][i][3] != -1: #有父輪廓 保留
                        new_cnts.append(cnts[i])
        im_cnt = cv2.drawContours(im , new_cnts , -1 , (0,0,255) , 1)
        cv2.imshow('im_cnt' , im_cnt)
        if len(new_cnts) > 0:
                print(img_path,":有氣泡")
                


##判斷是否為大小頭函數
def balance_detection(img_path,img_file,im,im_gray):
        pass



if __name__ == '__main__':
        imgdir = "images"
        img_files = os.listdir(imgdir)

        for img_file in img_files:
                img_path = os.path.join(imgdir, img_file)
                if os.path.isdir(img_path):
                        continue
                ###讀取圖像
                im = cv2.imread(img_path)
                im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                cv2.imshow('im', im)
                cv2.imshow('gray', im_gray)
                
                ##判斷是否為空膠囊
                is_empty = False
                is_empty = empty_detection(img_path
                                          ,img_file
                                          ,im
                                          ,im_gray)

        



                ##判斷是否有氣泡
                if not is_empty:#判斷如果不適空膠囊 在判斷是否有氣泡
                        is_bub = bub_detection(img_path
                                              ,img_file
                                              ,im
                                              ,im_gray)
                ##判斷是否為大小頭
                if (not is_empty) and (not is_bub):
                        balance_detection(img_path
                                         ,img_file
                                         ,im
                                         ,im_gray)

                cv2.waitKey()
                cv2.destroyAllWindows()
