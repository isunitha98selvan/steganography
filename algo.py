from PIL import Image
from math import abs
import numpy as np
class IMG:
	def __init__(self):
		self.carrier_image=None
		self.cover_image=None
		self.file_supported=['JPEG','PNG','TIFF','BMP']  #check if it is a valid image
		self.image_mode=None

	def open_image(self,image_name):
		self.carrier=Image.open(image_name,'r')
		width,height=self.carrier.size
		self.image_mode = ''.join(self.fg.getbands())

		if self.carrier.format in self.file_supported:
			print("Image format: ",self.carrier.format)
			print("Image size: ",width,"x",height)
		else:
			print("Unsupported file type!")

	def check_size(self):
		size_cover= os.path.getsize(self.cover_image)*8
		size_carrier=os.path.getsize(self.carrier_image)*8
		if size_carrier*3 <=2* size_cover:
			print("Unable to fit data in carrier image!")

def image_to_matrix(file_name):
	img = Image.open(file_name,'r')
	arr = np.array(img)
	return arr.tolist()

def set_bit(oldByte, newBit):

	temp = list(bin(old_byte))
	temp[-1] = new_bit
	return int(''.join(temp),2)		

def getPixelValue(rgbList):
	return rgbList[0],rgbList[1],rgbList[2]

def embedding(carrier_pixel_block,cover_pixel_block,k=3):  #Assuming the pixel block is a list of list with the inner list having the RGB values
	gx = carrier_pixel_block[0][0]
	gur = carrier_pixel_block[0][1]
	gbl = carrier_pixel_block[1][0]
	gbr = carrier_pixel_block[1][1]
	gxR,gxG,gxB = getPixelValue(gx) #Assuming it's all integers
	cvR,cvG,cvB = getPixelValue(cover_pixel_block[0][0])
	L = int(format(gxR, '08b')[-1] + format(gxG, '08b')[-1] + format(gxB, '08b')[-1])
	S = int(format(cvR, '08b')[-1] + format(cvG, '08b')[-1] + format(cvB, '08b')[-1])
	newgxR = set_bit(gxR,int(format(cvR, '08b')[-1]))
	newgxB = set_bit(gxB,int(format(cvB, '08b')[-1]))
	newgxG = set_bit(gxG,int(format(cvG, '08b')[-1]))
	d = L-S
	#red
	if d> pow(2,k-1) and 0<= newgxR + pow(2,k) and newgxR + pow(2,k)<=255:
		newgxR = newgxR + pow(2,k)
	elif d< -pow(2,k-1) and 0<= newgxR - pow(2,k) and newgxR - pow(2,k)<=255:
		newgxR = newgxR - pow(2,k)
	else:
		newgxR = newgxR
	#blue
	if d> pow(2,k-1) and 0<= newgxB + pow(2,k) and newgxB + pow(2,k)<=255:
		newgxB = newgxB + pow(2,k)
	elif d< -pow(2,k-1) and 0<= newgxB - pow(2,k) and newgxB - pow(2,k)<=255:
		newgxB = newgxB - pow(2,k)
	else:
		newgxB = newgxB
	#green
	if d> pow(2,k-1) and 0<= newgxG + pow(2,k) and newgxG + pow(2,k)<=255:
		newgxG = newgxG + pow(2,k)
	elif d< -pow(2,k-1) and 0<= newgxG - pow(2,k) and newgxG - pow(2,k)<=255:
		newgxG = newgxG - pow(2,k)
	else:
		newgxG = newgxG

	gurR,gurG,gurB = getPixelValue(gur)
	CVurR,CVurG,CVurB = getPixelValue(cover_pixel_block[0][1])
	d1_red=abs(newgxR-gurR)
	d1_green=abs(newgxG-gurG)
	d1_blue=abs(newgxB-gurB)

	gblR,gblG,gblB = getPixelValue(gbl)
	CVblR,CVblG,CVblB = getPixelValue(cover_pixel_block[1][0])
	d2_red=abs(newgxR-gblR)
	d2_green=abs(newgxG-gblG)
	d2_blue=abs(newgxB-gblB)

	gbrR,gbrG,gbrB = getPixelValue(gbr)
	CVbrR,CVbrG,CVbrB = getPigbrRxelValue(cover_pixel_block[1][1])
	d3_red=abs(newgxR-gbrR)
	d3_green=abs(newgxG-gbrG)
	d3_blue=abs(newgxB-gbrB)

	t1_red=no_of_bits_to_hide(d1_red)
	t1_blue=no_of_bits_to_hide(d1_blue)
	t1_green=no_of_bits_to_hide(d1_green)

	l1_red = int(format(gurR, '08b')[-t1_red:])
	s1_red = int(format(CVurR,'08b')[-t1_red:])
	l1_green = int(format(gurG, '08b')[-t1_green:])
	s1_green = int(format(CVurG,'08b')[-t1_green:])
	l1_blue = int(format(gurB, '08b')[-t1_blue:])
	s1_blue = int(format(CVurB,'08b')[-t1_blue:])

	t2_red=no_of_bits_to_hide(d2_red)
	t2_blue=no_of_bits_to_hide(d2_blue)
	t2_green=no_of_bits_to_hide(d2_green)

	l2_red = int(format(gblR, '08b')[-t2_red:])
	s2_red = int(format(CVblR,'08b')[-t2_red:])
	l2_green = int(format(gblG, '08b')[-t2_green:])
	s2_green = int(format(CVblG,'08b')[-t2_green:])
	l2_blue = int(format(gblB, '08b')[-t2_blue:])
	s2_blue = int(format(CVblB,'08b')[-t2_blue:])

	t3_red=no_of_bits_to_hide(d3_red)
	t3_blue=no_of_bits_to_hide(d3_blue)
	t3_green=no_of_bits_to_hide(d3_green)

	l3_red = int(format(gbrR, '08b')[-t3_red:])
	s3_red = int(format(CVbrR,'08b')[-t3_red:])
	l3_green = int(format(gbrG, '08b')[-t3_green:])
	s3_green = int(format(CVbrG,'08b')[-t3_green:])
	l3_blue = int(format(gbrB, '08b')[-t3_blue:])
	s3_blue = int(format(CVbrB,'08b')[-t3_blue:])

	d1_red_new=l1_red+s1_red
	d1_blue_new=l1_blue+s1_blue
	d1_green_new=l1_green+s1_green

	d2_red_new=l2_red+s2_red
	d2_blue_new=l2_blue+s2_blue
	d2_green_new=l2_green+s2_green
	
	d3_red_new=l3_red+s3_red
	d3_blue_new=l3_blue+s3_blue
	d3_green_new=l3_green+s3_green

	new2gurR = newgxR - d1_red_new
	new2gurG = newgxG - d1_green_new
	new2gurB = newgxB - d1_blue_new

	new3gurR = newgxR + d1_red_new
	new3gurG = newgxG + d1_green_new
	new3gurB = newgxB + d1_blue_new

	new2gbrR = newgxR - d2_red_new
	new2gbrG = newgxG - d2_green_new
	new2gbrB = newgxB - d2_blue_new

	new3gbrR = newgxR + d2_red_new
	new3gbrG = newgxG + d2_green_new
	new3gbrB = newgxB + d2_blue_new

	new2gblR = newgxR - d3_red_new
	new2gblG = newgxG - d3_green_new
	new2gblB = newgxB - d3_blue_new

	new3gblR = newgxR + d3_red_new
	new3gblG = newgxG + d3_green_new
	new3gblB = newgxB + d3_blue_new

	# For gur
	if abs(gurR - new2gurR) < abs(gurR - new3gurR) and 0<=new2gurR and new2gurR<=255:
		newgurR = new2gurR
	else:
		newgurR = new3gurR

	if abs(gurG - new2gurG) < abs(gurG - new3gurG) and 0<=new2gurG and new2gurG<=255:
		newgurG = new2gurG
	else:
		newgurG = new3gurG

	if abs(gurB - new2gurB) < abs(gurB - new3gurB) and 0<=new2gurB and new2gurB<=255:
		newgurB = new2gurB
	else:
		newgurB = new3gurB

	# For gbr
	if abs(gbrR - new2gbrR) < abs(gbrR - new3gbrR) and 0<=new2gbrR and new2gbrR<=255:
		newgbrR = new2gbrR
	else:
		newgbrR = new3gbrR

	if abs(gbrG - new2gbrG) < abs(gbrG - new3gbrG) and 0<=new2gbrG and new2gbrG<=255:
		newgbrG = new2gbrG
	else:
		newgbrG = new3gbrG

	if abs(gbrB - new2gbrB) < abs(gbrB - new3gbrB) and 0<=new2gbrB and new2gbrB<=255:
		newgbrB = new2gbrB
	else:
		newgbrB = new3gbrB

	# For gbl
	if abs(gblR - new2gblR) < abs(gblR - new3gblR) and 0<=new2gblR and new2gblR<=255:
		newgblR = new2gblR
	else:
		newgblR = new3gblR

	if abs(gblG - new2gblG) < abs(gblG - new3gblG) and 0<=new2gblG and new2gblG<=255:
		newgblG = new2gblG
	else:
		newgblG = new3gblG

	if abs(gblB - new2gblB) < abs(gblB - new3gblB) and 0<=new2gblB and new2gblB<=255:
		newgblB = new2gblB
	else:
		newgblB = new3gblB

	stego_pixel_block = [[newgxR,newgxG,newgxB],[newgurR,newgurG,newgurB],[newgblR,newgblG,newgblB],[newgbrR,newgbrG,newgbrB]]

def no_of_bits_to_hide(value):
	#using quantisation range for variant 1
	if value in range(64):
		return 3
	else:
		return 4
		
#converts plaintext to 8-bit binary format
def convert_to_binary(data):
	data_binary=' '.join(format(ord(x), '08b') for x in data)
	print(data_binary)
	return data_binary

def main():
	#carrier image
	carrier_image_name=input("Enter the file name of the carrier image: ")
	carrier_image_matrix = image_to_matrix(carrier_image_name)
	cover_image_name=input("Enter the file name of the cover image: ")
	cover_image_matrix = image_to_matrix(cover_image_name)
	
	# img=Image.open(image_name,'r')
	# width,height=img.size
	# new_img=img.copy() 
	# #data to be encypted
	# file_name= input("Enter file name to be encrypted: ")
	# f=open(file_name,"r")
	# data=f.read()
	# binary_data=convert_to_binary(data)
	
	#check if carrier image is big enough

	hide_seek(new_img,data)

	new_img.save('encrypted.jpg')

if __name__=='__main__':
	main()
