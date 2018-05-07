from selenium import webdriver
import cv2
import time
import pytesseract
import os
from PIL import Image
#from pytesseract import image_to_string
import pytesseract
import argparse
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
import datetime




DRIVER = 'C:/chromedriver.exe'
driver = webdriver.Chrome(DRIVER)
driver.get('https://web.whatsapp.com')

def isNotEmpty(s):
    return bool(s and s.strip())

def diff_times_in_seconds(t1, t2):
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( t2_secs - t1_secs- 15)
newSlot = True

while 1:
	screenshot = driver.save_screenshot('my_screenshot.png')
	image = cv2.imread('my_screenshot.png')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	Y, X = image.shape[:2]
	equ = cv2.equalizeHist(gray)
	#print('Y is', Y, 'X is ',X)
	crop_img = gray[Y-355:Y-305, X-460:X-350]
	cv2.imwrite('my_screenshot_bw.png',crop_img)
	# cv2.imshow('image',crop_img) #enable or disable this to check if the online part is in view or not
	# cv2.waitKey(0)
	text = pytesseract.image_to_string(Image.open('my_screenshot_bw.png'))
	os.remove('my_screenshot.png')
	os.remove('my_screenshot_bw.png')

	if ('online' in text) and newSlot==True:
		print('came online at', datetime.datetime.now().time())
		start_time = datetime.datetime.now().time()
		newSlot=False

	elif 'online' not in text and (newSlot==False):
		end_time = datetime.datetime.now().time()
		print('duration online: ',diff_times_in_seconds(start_time,end_time), ' seconds')
		newSlot=True

	time.sleep(1)


#driver.quit()