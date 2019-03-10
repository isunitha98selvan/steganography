from PIL import Image
from math import abs

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

def set_bit(oldByte, newBit):

    temp = list(bin(old_byte))
	temp[-1] = new_bit
	return int(''.join(temp),2)		

def embedding(carrier_pixel_block,cover_pixel_block,k=3):
	gx = carrier_pixel_block[0][0]
	gur = carrier_pixel_block[0][1]
	gbl = carrier_pixel_block[1][0]
	gbr = carrier_pixel_block[1][1]
	gxR,gxB,gxG = getPixelValue(gx) #Assuming it's all integers
	cvR,cvB,cvG = getPixelValue(cover_pixel_block[0][0])
	L = int(format(gxR, '08b')[-1] + format(gxB, '08b')[-1] + format(gxG, '08b')[-1])
	S = int(format(cvR, '08b')[-1] + format(cvB, '08b')[-1] + format(cvG, '08b')[-1])
	newgxR = set_bit(gxR,int(format(cvR, '08b')[-1]))
	newgxB = set_bit(gxB,int(format(cvB, '08b')[-1]))
	newgxG = set_bit(gxG,int(format(cvG, '08b')[-1]))
	d = L-S
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

    gurR,gurB,gurG = getPixelValue(gur)
    d1_red=abs(newgxR-gurR)
    d1_green=abs(newgxG-gurG)
    d1_blue=abs(newgxB-gurB)

    gblR,gblB,gblG = getPixelValue(gbl)
    d2_red=abs(newgxR-gblR)
    d2_green=abs(newgxG-gblG)
    d2_blue=abs(newgxB-gblB)

    gbrR,gbrB,gbrG = getPixelValue(gbr)
    d3_red=abs(newgxR-gbrR)
    d3_green=abs(newgxG-gbrG)
    d3_blue=abs(newgxB-gbrB)

    t1_red=no_of_bits_to_hide(d1_red)
    t1_blue=no_of_bits_to_hide(d1_blue)
    t1_green=no_of_bits_to_hide(d1_green)

    t2_red=no_of_bits_to_hide(d2_red)
    t2_blue=no_of_bits_to_hide(d2_blue)
    t2_green=no_of_bits_to_hide(d2_green)

    t3_red=no_of_bits_to_hide(d3_red)
    t3_blue=no_of_bits_to_hide(d3_blue)
    t3_green=no_of_bits_to_hide(d3_green)

    #find lower bounds 
    #s1, s2, s3 are decimal values taken from cover image
    d1_red_new=l1_red+s1_red
    d1_blue_new=l1_blue+s1_blue
    d1_green_new=l1_green+s1_green

    d2_red_new=l2_red+s2_red
    d2_blue_new=l2_blue+s2_blue
    d2_green_new=l2_green+s2_green
    
    d3_red_new=l3_red+s3_red
    d3_blue_new=l3_blue+s3_blue
    d3_green_new=l3_green+s3_green

def no_of_bits_to_hide(value):
    #using quantisation range for varaint 1
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
	image_name=input("Enter name of the image: ")
	x=IMG()
	x.open_image(image_name)
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
