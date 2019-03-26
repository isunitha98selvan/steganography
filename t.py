import cv2
import numpy as np
from PIL import Image
import os
import time

def main():
	root_dir = './Images/cover images'
	cover_images = []
	for filename in os.listdir(root_dir):
		cover_images.append(os.path.join(root_dir,filename))
		
	for i in range(len(cover_images)):
		cover_image_name=cover_images[i]
		img2 = cv2.imread(cover_image_name)
		cover_grey_image_matrix = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) # Converting the RGB cover image to grey scale
		cv2.imwrite('retrieved/Result' + str(i)+ '.png',cover_grey_image_matrix)
if __name__ == "__main__":
	main()
