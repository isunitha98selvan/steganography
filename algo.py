from PIL import Image
import numpy as np
import cv2

class IMG:
	def __init__(self):
		self.carrier_image=None
		self.cover_image=None
		self.file_supported=['JPEG','PNG','TIFF','BMP']  #check if it is a valid image
		self.image_mode=None

	def open_image(self,image_name):
		self.carrier=Image.open(image_name).convert('LA')
		self.carrier.save("carrier.png")
		width,height=self.carrier.size
		self.image_mode = ''.join(self.fg.getbands())

		if self.carrier.format in self.file_supported:
			print("Image format: ",self.carrier.format)
			print("Image size: ",width,"x",height)
		else:
			print("Unsupported file type!")

	def check_size(self):
		size_cover= os.path.getsize(self.cover_image)*801001000.
		size_carrier=os.path.getsize(self.carrier_image)*8
		if size_carrier*3 <=2* size_cover:
			print("Unable to fit data in carrier image!")

def abs(x):
	if x>=0:
		return x
	return -1*x

def image_to_matrix(file_name):
	img = Image.open(file_name,'r')
	arr = np.array(img)
	return arr.tolist()

def set_bit(oldByte, newBit):

	temp = list(bin(oldByte))
	temp[-1] = str(newBit)
	
	return int(''.join(temp),2)


def getPixelValue(rgbList):
	return rgbList[0],rgbList[1],rgbList[2]

def embedding(carrier_pixel_block,cover_pixel,k=3):  #Assuming the pixel block is a list of list with the inner list having the RGB values
	gx =  carrier_pixel_block[0][0]
	gur = carrier_pixel_block[0][1]
	gbl = carrier_pixel_block[1][0]
	gbr = carrier_pixel_block[1][1]
	cv  = cover_pixel
	# gxR,gxG,gxB = getPixelValue(gx) #Assuming it's all integers
	# cvR,cvG,cvB = getPixelValue(cover_pixel_block[0][0])
	# L = int(format(gxR, '08b')[-1] + format(gxG, '08b')[-1] + format(gxB, '08b')[-1])
	# S = int(format(cvR, '08b')[-1] + format(cvG, '08b	')[-1] + format(cvB, '08b')[-1])
	print("gx= ",gx)
	bin_gx=list(format(gx,'08b'))
	bin_gur=list(format(gur,'08b'))
	bin_gbl=list(format(gbl,'08b'))
	bin_gbr=list(format(gbr,'08b'))

	bin_cv=list(format(cv,'08b'))
	L = int(format(gx,'08b')[-3:])
	bin_gx[-1]=1
	bin_gx[-2]=bin_cv[0]
	bin_gx[-3]=bin_cv[1]
	
	new_gx = ''.join(bin_gx)		
	L = int(format(gx,'08b')[-3:])
	S = int(format(new_gx,'08b')[-3:])

	d = L-S
	
	if d> pow(2,k-1) and 0<= newgx + pow(2,k) and newgx + pow(2,k)<=255:
		newgx = newgx + pow(2,k)
	elif d< -pow(2,k-1) and 0<= newgx - pow(2,k) and newgx - pow(2,k)<=255:
		newgx = newgx - pow(2,k)
	else:
		newgx = newgx
	# #blue
	# if d> pow(2,k-1) and 0<= newgxB + pow(2,k) and newgxB + pow(2,k)<=255:
	# 	newgxB = newgxB + pow(2,k)
	# elif d< -pow(2,k-1) and 0<= newgxB - pow(2,k) and newgxB - pow(2,k)<=255:
	# 	newgxB = newgxB - pow(2,k)
	# else:
	# 	newgxB = newgxB
	# #green
	# if d> pow(2,k-1) and 0<= newgxG + pow(2,k) and newgxG + pow(2,k)<=255:
	# 	newgxG = newgxG + pow(2,k)
	# elif d< -pow(2,k-1) and 0<= newgxG - pow(2,k) and newgxG - pow(2,k)<=255:
	# 	newgxG = newgxG - pow(2,k)
	# else:
	# 	newgxG = newgxG

	CVur=cover_pixel_block[0][1]
	d1=abs(newgx-gur)
	# d1_green=abs(newgxG-gurG)
	# d1_blue=abs(newgxB-gurB)

	# gbl,gblG,gblB = getPixelValue(gbl)
	CVbl=cover_pixel_block[1][0]
	d2=abs(newgx-gbl)
	# d2_green=abs(newgxG-gblG)
	# d2_blue=abs(newgxB-gblB)

	# gbrR,gbrG,gbrB = getPixelValue(gbr)
	CVbr=cover_pixel_block[1][1]
	d3=abs(newgxR-gbrR)
	# d3_green=abs(newgxG-gbrG)
	# d3_blue=abs(newgxB-gbrB)

	t1=no_of_bits_to_hide(d1)
	# t1_blue=no_of_bits_to_hide(d1_blue)
	# t1_green=no_of_bits_to_hide(d1_green)

	l1 = int(format(gur, '08b')[-t1:])
	s1 = int(format(CVur,'08b')[-t1:])
	# l1_green = int(format(gurG, '08b')[-t1_green:])
	# s1_green = int(format(CVurG,'08b')[-t1_green:])
	# l1_blue = int(format(gurB, '08b')[-t1_blue:])
	# s1_blue = int(format(CVurB,'08b')[-t1_blue:])

	t2=no_of_bits_to_hide(d2)
	# t2_blue=no_of_bits_to_hide(d2_blue)
	# t2_green=no_of_bits_to_hide(d2_green)

	l2 = int(format(gbl, '08b')[-t2:])
	s2 = int(format(CVbl,'08b')[-t2:])
	# l2_green = int(format(gblG, '08b')[-t2_green:])
	# s2_green = int(format(CVblG,'08b')[-t2_green:])
	# l2_blue = int(format(gblB, '08b')[-t2_blue:])
	# s2_blue = int(format(CVblB,'08b')[-t2_blue:])

	t3=no_of_bits_to_hide(d3)
	# t3_blue=no_of_bits_to_hide(d3_blue)
	# t3_green=no_of_bits_to_hide(d3_green)

	l3= int(format(gbr, '08b')[-t3:])
	s3= int(format(CVbr,'08b')[-t3:])
	# l3_green = int(format(gbrG, '08b')[-t3_green:])
	# s3_green = int(format(CVbrG,'08b')[-t3_green:])
	# l3_blue = int(format(gbrB, '08b')[-t3_blue:])
	# s3_blue = int(format(CVbrB,'08b')[-t3_blue:])

	d1_new=l1+s1
	# d1_blue_new=l1_blue+s1_blue
	# d1_green_new=l1_green+s1_green

	d2_new=l2+s2
	# d2_blue_new=l2_blue+s2_blue
	# d2_green_new=l2_green+s2_green
	
	d3_new=l3+s3
	# d3_blue_new=l3_blue+s3_blue
	# d3_green_new=l3_green+s3_green

	new2gur = newgx - d1_new
	# new2gurG = newgxG - d1_green_new
	# new2gurB = newgxB - d1_blue_new

	new3gur = newgx + d1_new
	# new3gurG = newgxG + d1_green_new
	# new3gurB = newgxB + d1_blue_new

	new2gbr = newgx - d2_new
	# new2gbrG = newgxG - d2_green_new
	# new2gbrB = newgxB - d2_blue_new

	new3gbr = newgx + d2_new
	# new3gbrG = newgxG + d2_green_new
	# new3gbrB = newgxB + d2_blue_new

	new2gbl = newgx - d3_new
	# new2gblG = newgxG - d3_green_new
	# new2gblB = newgxB - d3_blue_new

	new3gbl = newgx + d3_new
	# new3gblG = newgxG + d3_green_new
	# new3gblB = newgxB + d3_blue_new

	# For gur
	if abs(gur - new2gur) < abs(gur - new3gur) and 0<=new2gur and new2gur<=255:
		newgur = new2gur
	else:
		newgur = new3gur

	# if abs(gur - new2gur) < abs(gur - new3gur) and 0<=new2gur and new2gur<=255:
	# 	newgurG = new2gurG
	# else:
	# 	newgurG = new3gurG

	# if abs(gurB - new2gurB) < abs(gurB - new3gurB) and 0<=new2gurB and new2gurB<=255:
	# 	newgurB = new2gurB
	# else:
	# 	newgurB = new3gurB

	# For gbr
	if abs(gbr - new2gbr) < abs(gbr - new3gbr) and 0<=new2gbr and new2gbr<=255:
		newgbr = new2gbr
	else:
		newgbr = new3gbr

	# if abs(gbrG - new2gbrG) < abs(gbrG - new3gbrG) and 0<=new2gbrG and new2gbrG<=255:
	# 	newgbrG = new2gbrG
	# else:
	# 	newgbrG = new3gbrG

	# if abs(gbrB - new2gbrB) < abs(gbrB - new3gbrB) and 0<=new2gbrB and new2gbrB<=255:
	# 	newgbrB = new2gbrB
	# else:
	# 	newgbrB = new3gbrB

	# For gbl
	if abs(gbl - new2gbl) < abs(gbl - new3gbl) and 0<=new2gbl and new2gbl<=255:
		newgbl = new2gbl
	else:
		newgbl = new3gbl

	# if abs(gblG - new2gblG) < abs(gblG - new3gblG) and 0<=new2gblG and new2gblG<=255:
	# 	newgblG = new2gblG
	# else:
	# 	newgblG = new3gblG

	# if abs(gblB - new2gblB) < abs(gblB - new3gblB) and 0<=new2gblB and new2gblB<=255:
	# 	newgblB = new2gblB
	# else:
	# 	newgblB = new3gblB

	stego_pixel_block = [newgx,newgur,newgblR,newgbrR]
	return stego_pixel_block

def no_of_bits_to_hide(value):
	#using quantisation range for variant 1
	if value in range(64):
		return 3
	else:
		return 4

def array2PIL(arr, size):
    mode = 'RGB'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

#converts plaintext to 8-bit binary format
def convert_to_binary(data):
	data_binary=' '.join(format(ord(x), '08b') for x in data)
	# print(data_binary)
	return data_binary

def main():
	#carrier image
	# carrier_image_name=input("Enter the file name of the carrier image: ")
	carrier_image_name='food.jpg'
	img=cv2.imread(carrier_image_name)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	cv2.imwrite('greyscale.jpg',img)
	# img =  io.imread(carrier_image_name, as_grey=True)
	# grey = Image.fromarray(img)
	# grey.save('GREY.png')
	print(img)
	carrier_image_matrix = image_to_matrix(carrier_image_name)
	print('Length: ' +str(len(carrier_image_matrix)) +'  width: ' + str(len(carrier_image_matrix[0])))
	final_image_matrix = np.zeros((len(carrier_image_matrix), len(carrier_image_matrix[0]), 3), dtype=np.uint8)

	# cover_image_name=input("Enter the file name of the cover image: ")
	cover_image_name='pic2.jpeg'
	cover_image_matrix = image_to_matrix(cover_image_name)
	# print(cover_image_matrix)
	print('Length: ' + str(len(cover_image_matrix)) +'  width: ' + str(len(cover_image_matrix[0])))
	if len(carrier_image_matrix)*3 <=2* len(cover_image_matrix) or len(carrier_image_matrix[0])*3 <=2* len(cover_image_matrix[0]) :
		print("Unable to fit data in carrier image!")
	else:
		print("Able to fit data in carrier image!")
	
	row_cover = col_cover = 0
	i=j=0
	while i<len(cover_grey_image_matrix) and j<len(cover_grey_image_matrix[0]):
		temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
		cover = cover_grey_image_matrix[row_cover][col_cover]
		row_cover+=1
		col_cover+=1
		if col_cover==len(cover_grey_image_matrix[0]):
			col_cover=0
		i+=2
		j+=2
		temp2 = embedding(temp,cover)
		final_image_matrix[i][j] = temp2[0][0]
		final_image_matrix[i][j+1] = temp2[0][1]
		final_image_matrix[i+1][j] = temp2[1][0]
		final_image_matrix[i+1][j+1] = temp2[1][1]

	
	# width=str(len(cover_image_matrix[0]))
	# print(width)
	# data = []
	# final_image=[]
	# count=0
	# for i in final_image_matrix:
	# 	count+=1
	# 	data.append(i)
	# 	if count==width:
	# 		final_image.append(data)
	# 		data=[]
	# 		print(final_image)
	# print(final_image)
	new_im = Image.fromarray(final_image,'RGB')
	final_image_matrix[i+1][j+1] = temp3[1][1]
	c=0
	for i in range(len(cover_image_matrix),len(carrier_image_matrix)):
		for j in range(len(cover_image_matrix[0]),len(carrier_image_matrix[0])):
			final_image_matrix[i][j] = carrier_image_matrix[i][j]
			if c==0:
				c=1

	# print(carrier_image_matrix[0])
	# print(final_image_matrix[0])
	img = Image.fromarray(final_image_matrix, 'RGB')
	img.save('Attempt1.png')
	# width=str(len(cover_image_matrix[0]))
	# print(width)
	# data = []
	# final_image=[]
	# count=0
	# for i in final_image_matrix:
	# 	count+=1
	# 	data.append(i)
	# 	if count==width:
	# 		final_image.append(data)
	# 		data=[]
	# 		print(final_image)
	# print(final_image)
	new_im.show()
	# img=Image.open(image_name,'r')
	# width,height=img.size
	# new_img=img.copy() 
	# #data to be encypted
	# file_name= input("Enter file name to be encrypted: ")
	# f=open(file_name,"r")
	# data=f.read()
	# binary_data=convert_to_binary(data)
	
	#check if carrier image is big enough

	# hide_seek(new_img,data)

	# new_img.save('encrypted.jpg')

if __name__=='__main__':
	main()
