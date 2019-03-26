from PIL import Image
import numpy as np
import cv2
import os

def abs(x): #Function to obtain absolute value
	if x>=0:
		return x
	return -1*x

def get_range(value): 
	# To get the lower bounds for Quantization ranges for Type 1
	if value in range(8):
		return 0
	elif value in range(8,16):
		return 8
	elif value in range(16,32):
		return 16
	elif value in range(32,64):
		return 32
	elif value in range(64,128):
		return 64
	elif value in range(128,255):
		return 128
	else:
		print("Error!")

def embedding(carrier_pixel_block,cover_pixel,k=3): # The value of k has been set to 3

	# extracting the corresponding greyscale block value from the carrier pixel block
	gx =  carrier_pixel_block[0][0]
	gur = carrier_pixel_block[0][1]
	gbl = carrier_pixel_block[1][0]
	gbr = carrier_pixel_block[1][1]
	cv  = cover_pixel

	bin_gx=list(format(gx,'08b')) # converting the integer greyscale value to binary
	bin_gur=list(format(gur,'08b'))
	bin_gbl=list(format(gbl,'08b'))
	bin_gbr=list(format(gbr,'08b'))
	bin_cv=list(format(cv,'08b'))
	
	L = int(format(gx,'08b')[-k:]) # Extracting the decimal value of the k LSBs of gx
	
	bin_gx[-1]=bin_cv[0]  # Embedding the first bit of the secret message in first LSB
	bin_gx[-2]=bin_cv[1]  # to obtain g'x

				
	new_gx = ''.join(bin_gx) # Combing the list to string
	
	S = int(new_gx[-k:])  # Extracting the decimal value of the k-bits of the g'x

	new_gx = int(new_gx,2) # New gx value obtained by converting g'x from binary to decimal

	d = L-S # Computing the value of d
	
	if d> pow(2,k-1) and 0<= new_gx + pow(2,k) and new_gx + pow(2,k)<=255:  # To get the optimized value of gx
		new_gx = new_gx + pow(2,k)
	elif d< -pow(2,k-1) and 0<= new_gx - pow(2,k) and new_gx - pow(2,k)<=255:
		new_gx = new_gx - pow(2,k)
	else:
		new_gx = new_gx

	d1=abs(new_gx-gur)  # Computing the corresponding distance values
	d2=abs(new_gx-gbr)
	d3=abs(new_gx-gbl)

	l1 = get_range(d1)  # Obtaining the lower bounds of the corresponding range according to Type 1
	l2 = get_range(d2)
	l3 = get_range(d3)
		
	t1=3 # Setting the number of bits to extract from cover pixel
	t2=3
	t3=2

	s1 = int(''.join(bin_cv[:t1]),2) 
	s2 = int(''.join(bin_cv[t1:t1+t2]),2) # Extracting the decimal value of the ti-bits of cover pixel
	s3 = int(''.join(bin_cv[t1+t2:t1+t2+t3]),2)
		
	d1_new=l1+s1 # Computing the new distance values
	d2_new=l2+s2
	d3_new=l3+s3

	new2gur = new_gx - d1_new
	new3gur = new_gx + d1_new
	new2gbr = new_gx - d2_new   # Finding the corresponding g' and g" values for all three blocks
	new3gbr = new_gx + d2_new
	new2gbl = new_gx - d3_new
	new3gbl = new_gx + d3_new
	
	# To obtain the optimized value for each block
	if abs(gur - new2gur) < abs(gur - new3gur) and 0<=new2gur and new2gur<=255: 
		new_gur = new2gur
	else:
		new_gur = new3gur

	if abs(gbr - new2gbr) < abs(gbr - new3gbr) and 0<=new2gbr and new2gbr<=255:
		new_gbr = new2gbr
	else:
		new_gbr = new3gbr

	if abs(gbl - new2gbl) < abs(gbl - new3gbl) and 0<=new2gbl and new2gbl<=255:
		new_gbl = new2gbl
	else:
		new_gbl = new3gbl

	stego_pixel_block = [[new_gx,new_gur],[new_gbl,new_gbr]] # Forming the new block
	return stego_pixel_block

# converts plaintext to 8-bit binary format
def convert_to_binary(data):
	data_binary=' '.join(format(ord(x), '08b') for x in data)
	return data_binary

# To get the first two digits and last two digits of a number respectively
def splitValues(num):
	return num//100,num%100
	

def main():
	carrier_images=[]
	cover_images=[]
	root_dir = '/home/rosa31/Desktop/6thSem/IAS/project/steganography/Images/carrier images'
	for filename in os.listdir(root_dir):
		carrier_images.append(os.path.join(root_dir,filename))

	root_dir = '/home/rosa31/Desktop/6thSem/IAS/project/steganography/Images/cover images'
	for filename in os.listdir(root_dir):
		cover_images.append(os.path.join(root_dir,filename))
	#carrier image
	cover_index = 0
	for carrier_index in range(len(carrier_images)):
		for ptr in range(10):

			carrier_image_name=carrier_images[carrier_index]
			print('Carrier image: ' + carrier_image_name)
			if carrier_image_name.split('.')[-1] not in ['jpg','jpeg','png','tiff']:
				print('Invalid file type!')
				print('\nProgram terminated')
				exit(0)

			grey_img=cv2.imread(carrier_image_name)  # Converting the RGB carrier image to grey scale
			carrier_grey_image_matrix = cv2.cvtColor(grey_img,cv2.COLOR_BGR2GRAY) # storing the image as a matrix

			cv2.imwrite('Images/greyScale/greyscaleCarrierImage' + str(carrier_index) + '.jpg',carrier_grey_image_matrix)
	
			print('\nCarrier image ' + str(carrier_index) + ' dimensions:')

			print('Length: ' + str(len(carrier_grey_image_matrix)) +'  width: ' + str(len(carrier_grey_image_matrix[0])))
			print('\n')
	
			# Creating the final image matrix for storing the secret data in carrier
			final_image_matrix = np.zeros((len(carrier_grey_image_matrix), len(carrier_grey_image_matrix[0])), dtype=np.uint8)
			cover_image_name=cover_images[cover_index]
			cover_index+=1
			print('Cover image: ' + cover_image_name)
			if cover_image_name.split('.')[-1] not in ['jpg','jpeg','png','tiff']:
				print('Invalid file type!')
				print('\nProgram terminated')
				exit(0)

			img2 = cv2.imread(cover_image_name)
			cover_grey_image_matrix = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) # Converting the RGB cover image to grey scale
			cv2.imwrite('Images/greyScale/greyscaleCoverImage' + str(carrier_index) + str(cover_index) +'.jpg',cover_grey_image_matrix)
			
			print('\nCover image: ' + str(cover_index))
			print('Length: ' +str(len(cover_grey_image_matrix)) +'  width: ' + str(len(cover_grey_image_matrix[0])))
			print('\n')
			print('Checking whether the cover image can be hid in the carrier image')


			# Check to see whether the secret data can be hid in the carrier image
			if len(carrier_grey_image_matrix) <=2* len(cover_grey_image_matrix) or len(carrier_grey_image_matrix[0]) <=2* len(cover_grey_image_matrix[0]):
				print("Unable to fit data in carrier image!\n")
				exit(0)
			else:
				print("Able to fit data in carrier image!\n")

			row_cover = col_cover = 0
			i=j=0
			print('Performing the embedding procedure........\n')
			
			while row_cover<len(cover_grey_image_matrix): #Traversing the cover image matrix
				# Extraction of 2x2 non-overlapping matrix
				temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
				cover = cover_grey_image_matrix[row_cover][col_cover]
				col_cover+=1
				if col_cover==len(cover_grey_image_matrix[0]):
					# print("col",col_cover)
					col_cover=0
					row_cover+=1
				temp2 = embedding(temp,cover) # Function that performs embedding is called
				
				
				final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
				final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
				final_image_matrix[i+1][j] = temp2[1][0]
				final_image_matrix[i+1][j+1] = temp2[1][1]
				j+=2
				if j==len(carrier_grey_image_matrix[0]):
					#print("j=",j)
					i+=2
					j=0
			
			k=i # storing row where cover image has been embedded till
	
			print('Embedding procedure completed!\n')

			for i in range(k,len(carrier_grey_image_matrix)):
				for j in range(len(carrier_grey_image_matrix[0])):
					final_image_matrix[i][j]=carrier_grey_image_matrix[i][j]
			i-=2
			j-=2
			len1,len2 = splitValues(len(cover_grey_image_matrix))
			
			wid1,wid2 = splitValues(len(cover_grey_image_matrix[0]))
			#To store the length and width of the cover as first two secret data
			temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
			temp2 = embedding(temp,len1) # Embedding length of cover image
			final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
			final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
			final_image_matrix[i+1][j] = temp2[1][0]
			final_image_matrix[i+1][j+1] = temp2[1][1]
			
			j-=2
			temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
			temp2 = embedding(temp,len2) # Embedding length of cover image
			final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
			final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
			final_image_matrix[i+1][j] = temp2[1][0]
			final_image_matrix[i+1][j+1] = temp2[1][1]
			j-=2
			
			temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
			temp2 = embedding(temp,wid1) # Embedding length of cover image
			final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
			final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
			final_image_matrix[i+1][j] = temp2[1][0]
			final_image_matrix[i+1][j+1] = temp2[1][1]
			j-=2
			
			temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
			temp2 = embedding(temp,wid2) # Embedding length of cover image
			final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
			final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
			final_image_matrix[i+1][j] = temp2[1][0]
			final_image_matrix[i+1][j+1] = temp2[1][1]
			
			print('Storing the result in Result_' + str(carrier_index) + '_' + str(cover_index) + '.png\n')
			img = Image.fromarray(np.uint8(final_image_matrix),'L') # Storing the final image matrix as a grey scale image
			img.save('results/Result_' + str(carrier_index) + '_' + str(cover_index) + '.png')
	print('Done!')
	
if __name__=='__main__':
	main()
