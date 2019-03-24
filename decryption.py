#code for decryption
import cv2
import numpy as np
from PIL import Image
def check_range(value):
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
        
def decrypt(carrier_pixel_block,k=3):
    gx  = carrier_pixel_block[0][0]
    gur = carrier_pixel_block[0][1]
    gbl = carrier_pixel_block[1][0]
    gbr = carrier_pixel_block[1][1]
    # print("----")
    # print(gx,gur,gbl,gbr)
    
    new_gx = int(format(gx,'08b')[-k:],2)
    new_gur = int(format(gur, '08b')[-k:],2)
    new_gbl = int(format(gbr, '08b')[-k:],2)
    new_gbr = int(format(gbl, '08b')[-k:],2)

    # print("no.s",new_gx,new_gur,new_gbr,new_gbl)
    d1=abs(int(gur)-int(gx))
    d2=abs(int(gbr)-int(gx))
    d3=abs(int(gbl)-int(gx))
   
    # print("d= :",d1,d2,d3)
    t1=3
    t2=3
    t3=2
    l1 = check_range(d1)
    l2 = check_range(d2)
    l3 = check_range(d3)


    # print("l=",l1,l2,l3)
    s1 = int(d1-l1)
    s2 = int(d2-l2)
    s3 = int(d3-l3)

    # print("s= ",s1,s2,s3)
    
    bin_s1 = list(format(s1,'08b')[-t1:])
    bin_s2 = list(format(s2,'08b')[-t2:])
    bin_s3 = list(format(s3,'08b')[-t3:])
    # bin_gx = list(format(new_gx,'08b')[-2:])

    final_bin = bin_s1 + bin_s2 +bin_s3
    new_gx   = ''.join(final_bin)
    # print(int(new_gx),2)
    return int(new_gx,2)

def main():
    encrypted_image_name='Check3.png'
    img=cv2.imread(encrypted_image_name)
    
    ##print(img) 
    encrypted_image_matrix = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    i = len(encrypted_image_matrix)
    j = len(encrypted_image_matrix[0])
    i-=3
    j-=3
    temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
    len1 = decrypt(temp) # Embedding length of cover image
    print(len1)
    
    j-=2
    temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
    len2 = decrypt(temp) # Embedding length of cover image
    print(len2)
    j-=2
    
    temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
    wid1 = decrypt(temp) # Embedding length of cover image
    print(wid1)
    j-=2
    
    temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
    wid2 = decrypt(temp) # Embedding length of cover image
    print(wid2)

    length = int('%i%i' % (len1,len2))
    width = int('%i%i' % (wid1,wid2))
    print("Length,width= ",length,width)
    secret_image = np.zeros([length,width],dtype=int)

    print('Image:')
    print('Length: ' +str(len(encrypted_image_matrix)) +'  width: ' + str(len(encrypted_image_matrix[0])))
    print(encrypted_image_matrix)
    count=0
    row_number=0
    # for i in range(300,400):
    # 	print(secret_image[i].tolist())
    count=0
    row_cover=col_cover=0
    n=0
    i=0
    j=0
    while row_cover<length and col_cover<width: #Traversing the cover image matrix
        temp = [[encrypted_image_matrix[i][j],encrypted_image_matrix[i][j+1]],[encrypted_image_matrix[i+1][j],encrypted_image_matrix[i+1][j+1]]]
        #print(temp)
        secret_image[row_cover][col_cover] = decrypt(temp)
        #print(secret_image[row_cover][col_cover])
        col_cover+=1
        if col_cover == width:
            count+=1
            col_cover=0
            row_cover+=1
        j+=2
        if j >= width:
            i+=2
            j=0
        # count+=1
        n+=1
    #print(n)
    #print("count= ",count)
    #print(row_cover,col_cover)
    # for i in range(count):
    #  	print(secret_image[i].tolist())
    img = Image.fromarray(np.uint8(secret_image) , 'L')

    #img = Image.fromarray(secret_image,L)
    img.save("Cover.png")
    # img.show()
    
if __name__=='__main__':
    main()