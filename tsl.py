import cv2
import numpy as np
import serial

def nothing(x):
    pass

image_x, image_y = 64,64

from keras.models import load_model
classifier = load_model('tsl_model.h5')
serialport = serial.Serial('/dev/cu.usbserial-1420', 9600)
def predictor_arduino():
	if 1:
		
		input=serialport.readline()
		v=input.decode("utf-8")
		#v="448,531,481,511,516"
		values=v.split(',')
	
		a1=int(values[0])
		a2=int(values[1])
		a3=int(values[2])
		a4=int(values[3])
		a5=int(values[4])

		open=600
		close=525

		if a1>530:
			a1=2
		elif 470<a1:
			a1=1
		else:
		 a1=0

		if a2>open:
			a2=2
		elif close<a2<open:
			a2=1
		else:
		 a2=0

		if a3>open:
			a3=2
		elif close<a3<open:
			a3=1
		else:
			a3=0   

		if a4>open:
			a4=2
		elif close<a4<open:
			a4=1
		else:
			a4=0   

		if a5>open:
			a5=2
		elif 570<a5<open:
			a5=1
		else:
			a5=0     

		pred="x"

		if a1>=1 and a2<=0 and a3<=0 and a4<=0 and a5<=0:
				pred="6"
		elif a1<=1 and a2<=0 and a3<=1 and a4<=1 and a5<=1:
				pred="0"
		elif a1<=1 and a2==2 and a3<=1 and a4<=2 and a5<=1:
			pred="1"
			
		elif (a2+a3) == 4 and a4<=1 and a1<=1 and a5<=1:
				pred="2"
			
		elif (a1+a2+a3) >= 5 and (a4+a5)<=3:
				pred="3"
			
		elif a1<2 and (a2+a3+a5+a5)>=7:
				pred="4"
			
		elif  (a1+a2+a3+a5+a5)==10:
				pred="5"

		elif (a1+a4+a5)<=1 and (a2+a3)>=2 :
				pred="8"

		elif a2>=1 and (a1+a3+a4)<=3 and a5<=1:
				pred="9"


		elif (a1+a5)>=2 and (a2+a3+a4)<=2:
				pred="Y"
			 		 
	return pred
def predictor():
       import numpy as np
       from keras.preprocessing import image
       test_image = image.load_img('1.png', target_size=(64, 64))
       test_image = image.img_to_array(test_image)
       test_image = np.expand_dims(test_image, axis = 0)
       result = classifier.predict(test_image)
       
       if result[0][0] == 1:
              return '0'
       elif result[0][1] == 1:
              return '1'
       elif result[0][2] == 1:
              return '2'
       elif result[0][3] == 1:
              return '3'
       elif result[0][4] == 1:
              return '4'
       elif result[0][5] == 1:
              return '5'
       elif result[0][6] == 1:
              return '6'
       elif result[0][7] == 1:
              return '7'
       elif result[0][8] == 1:
              return '8'
       elif result[0][9] == 1:
              return '9'
       

       

cam = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

cv2.namedWindow("test")

img_counter = 0

img_text = ''
img_2 = ''
while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame,1)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")


    img = cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    imcrop = img[102:298, 427:623]
    hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
    cv2.putText(frame, img_2, (100, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
    cv2.imshow("test", frame)
    cv2.imshow("mask", mask)
    
    #if cv2.waitKey(1) == ord('c'):
        
    img_name = "1.png"
    save_img = cv2.resize(mask, (image_x, image_y))
    cv2.imwrite(img_name, save_img)
    print("{} written!".format(img_name))
    img_text = predictor()
    img_2=predictor_arduino()
        

    if cv2.waitKey(1) == 27:
        break


cam.release()
cv2.destroyAllWindows()