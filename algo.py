from PIL import Image

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
# Same for blue n green




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
