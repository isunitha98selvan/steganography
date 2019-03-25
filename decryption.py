#code for decryption
import cv2
import numpy as np
from PIL import Image
import os
def check_range(value):
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
		return 0
		
def decrypt(carrier_pixel_block,k=3): # The value of k has been set to 3

	# extracting the corresponding greyscale block value from the carrier pixel block
	gx  = carrier_pixel_block[0][0]
	gur = carrier_pixel_block[0][1]
	gbl = carrier_pixel_block[1][0]
	gbr = carrier_pixel_block[1][1]
	
	new_gx = int(format(gx,'08b')[-k:],2)
	new_gur = int(format(gur, '08b')[-k:],2)
	new_gbl = int(format(gbr, '08b')[-k:],2) # Extracting the decimal value of the k LSBs from each block
	new_gbr = int(format(gbl, '08b')[-k:],2)

	d1=abs(int(gur)-int(gx))
	d2=abs(int(gbr)-int(gx)) # Computing the corresponding distance values
	d3=abs(int(gbl)-int(gx))
   
	t1=3 # Setting the number of bits to extract
	t2=3
	t3=2

	l1 = check_range(d1)
	l2 = check_range(d2) # Obtaining the lower bounds of the corresponding range according to Type 1
	l3 = check_range(d3)

	s1 = int(d1-l1)
	s2 = int(d2-l2) # finding the value of Si which is difference between 
	s3 = int(d3-l3) # the distance and lower bound
  
	bin_s1 = list(format(s1,'08b')[-t1:])
	bin_s2 = list(format(s2,'08b')[-t2:]) # Extracting the decimal value of the ti-bits of Si
	bin_s3 = list(format(s3,'08b')[-t3:])

	final_bin = bin_s1 + bin_s2 +bin_s3 # Getting the binary value of the stored secret image pixel
	new_gx   = ''.join(final_bin)
	return int(new_gx,2)

def main():

	encrypted_images = []
	root_dir = '/home/rosa31/Desktop/6thSem/IAS/project/steganography/results'
	for filename in os.listdir(root_dir):
		encrypted_images.append(os.path.join(root_dir,filename))

	for image_index in range(len(encrypted_images)):
		encrypted_image_name= encrypted_images[image_index]

		img=cv2.imread(encrypted_image_name) # Reading the encrypted image
		
		encrypted_image_matrix = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		print('Dimensions of encrypted image: '+ str(image_index))

		print('Length: ' +str(len(encrypted_image_matrix)) +'  width: ' + str(len(encrypted_image_matrix[0])))
		print('\n')
		print('Decrypting the length and width values of cover image')
		i = len(encrypted_image_matrix)
		j = len(encrypted_image_matrix[0])
		i-=3
		j-=3
		temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
		len1 = decrypt(temp) # Getting the first two digits of length of secret image
		
		j-=2
		temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
		len2 = decrypt(temp) # Getting the next two digits of length of secret image
		j-=2
		
		temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
		wid1 = decrypt(temp) # Getting the first two digits of width of secret image
		j-=2
		
		temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
		wid2 = decrypt(temp) # Getting the last two digits of width of secret image
		
		length = int('%i%i' % (len1,len2))
		width = int('%i%i' % (wid1,wid2))  # Combining the two parts to get corresponding length and width
		
		secret_image = np.zeros([length,width],dtype=int)

		print('Dimensions of cover image:')
		print('Length: ' +str(length) +'  width: ' + str(width))
		
		print('')
		count=0
		row_cover=col_cover=0
		
		i=0
		j=0
		print('Performing the extraction procedure........\n')
		
		while row_cover<length and col_cover<width: #Traversing the secret image matrix
			# Extracting 2x2 non-overlapping matrix
			temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
			
			secret_image[row_cover][col_cover] = decrypt(temp) # Storing the value of decrypted pixel block
			
			col_cover+=1
			if col_cover == width:
				count+=1
				col_cover=0
				row_cover+=1
			j+=2
			if j >= len(encrypted_image_matrix[0]):
				i+=2
				j=0
			
		print('Embedding procedure succesfully completed!\n')
		
		img = Image.fromarray(np.uint8(secret_image) , 'L') # Convering matrix to image
		img.save('retrieved/Cover' + str(image_index)+ '.png')
		print('Done! The secret image has been retrieved and is stored in Cover' + str(image_index)+ '.png')	
if __name__=='__main__':
	main()