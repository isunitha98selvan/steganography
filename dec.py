#code for decryption
import cv2
import numpy as np
from PIL import Image

def check_range(value):
	if value in range(64):
		return 3
	else:
		return 3

def decrypt(carrier_pixel_block):
	gx  = carrier_pixel_block[0][0]
	gur = carrier_pixel_block[0][1]
	gbl = carrier_pixel_block[1][0]
	gbr = carrier_pixel_block[1][1]
 
	bin_gx=list(format(gx,'08b'))

	d1=abs((int(gur)-int(gx)))
	d2=abs((int(gbr)-int(gx)))
	d3=abs((int(gbl)-int(gx)))
   
	# t1=check_range(d1)
	# t2=check_range(d2)
	# t3=check_range(d3)
	t1=2
	#calculate lower bouembed youtube video on sitend
	l1 = int(format(gur, '08b')[-t1:])
	l2 = int(format(gbl, '08b')[-t1:])
	l3 = int(format(gbr, '08b')[-t1:])

	s1 = int(d1-l1)
	s2 = int(d2-l2)
	s3 = int(d3-l3)

	bin_s1 = list(format(s1,'08b')[-2:])
	bin_s2 = list(format(s2,'08b')[-2:])
	bin_s3 = list(format(s3,'08b')[-2:])

	final_bin = bin_gx[-2:]+bin_s1 + bin_s2 +bin_s3
	new_gx   = ''.join(final_bin)
	return int(new_gx,2)

def main():
	encrypted_image_name='Check2.png'
	
	# secret_image = np.zeros([length,width],dtype=np.uint8)
	img=cv2.imread(encrypted_image_name)
	#print(img) 
	encrypted_image_matrix = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	i=j=0
	temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
	print(temp)
	print(decrypt(temp))
	exit()
	print('Image:')
	print('Length: ' +str(len(encrypted_image_matrix)) +'  width: ' + str(len(encrypted_image_matrix[0])))
	#print(encrypted_image_matrix)
	i=0
	j=0
	count=0
	row_number=0
	row_cover=col_cover=0
	while i<length and j<width : #Traversing the cover image matrix
		temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
		secret_image[row_cover][col_cover] = decrypt(temp)
		col_cover+=1
		if col_cover == width:
			col_cover=0
			row_cover+=1
		j+=2
		if j >= width:
			i+=2
			j=0
		# if count == 1432 * 2:
		#     row=np.array(row,dtype="int")
		#     secret_image=np.matrix(row)
		#     count=0
		#     row_number+=1
		#     #print(secret_image)
		#     row=[]
	# print(row)
	# print(secret_image)
	# secret_image=np.matrix(row)
	print(secret_image)
	print(len(secret_image))
	img = Image.fromarray(secret_image)
	img.show()
	#print(row)
	print(i,j)

if __name__=='__main__':
	main()