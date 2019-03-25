from PIL import Image
import numpy as np
import cv2

def abs(x):
    if x>=0:
        return x
    return -1*x
def getLowerBoundAndBits(num):
    if num>=0 and num<=7:
        return 0,3
    if num>=8 and num<=15:
        return 8,3
    if num>=16 and num<=31:
        return 16,3
    if num>=32 and num<=63:
        return 32,3
    if num>=64 and num<=127:
        return 64,4
    if num<=255:
        return 128,4
    #print("Out of range")
    exit(0)

def embedding(carrier_pixel_block,cover_pixel,k=3):  #Assuming the pixel block is a list of list with the inner list having the RGB values

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
    bin_gx[-2]=bin_cv[1]

                
    new_gx = ''.join(bin_gx) # Combing the list to string
    
    S = int(new_gx[-k:])  # Extracting the decimal value of the k-bits of the embedded gx

    new_gx = int(new_gx,2) # New gx value obtained by converting from binary to decimal

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

    l1,t1 = getLowerBoundAndBits(d1)
    l2,t2 = getLowerBoundAndBits(d2)
    l3,t3 = getLowerBoundAndBits(d3)
        
    t1=3
    t2=3
    t3=2

    s1 = int(''.join(bin_cv[:t1]),2)
    s2 = int(''.join(bin_cv[t1:t1+t2]),2)
    s3 = int(''.join(bin_cv[t1+t2:t1+t2+t3]),2)
    # #print(s1,s2,s3)
    
    # bin_gur[-1]=bin_cv[2] # Embedding bits of secret data in the blocks
    # bin_gur[-2]=bin_cv[3]
    # new_gur = ''.join(bin_gur)  
    # s1 = int(new_gur[-t1:])
    # new_gur = int(new_gur,2)

    # bin_gbl[-1]=bin_cv[4]
    # bin_gbl[-2]=bin_cv[5]
    # new_gbl = ''.join(bin_gbl)
    # s3 = int(new_gbl[-t1:])
    # new_gbl = int(new_gbl,2)
    
    # bin_gbr[-1]=bin_cv[6]
    # bin_gbr[-2]=bin_cv[7]
    # new_gbr = ''.join(bin_gbr)
    # s2 = int(new_gbr[-t1:])
    # new_gbr = int(new_gbr,2)
    
    d1_new=l1+s1 # Computing the new distance values
    d2_new=l2+s2
    d3_new=l3+s3

    new2gur = new_gx - d1_new
    new3gur = new_gx + d1_new
    new2gbr = new_gx - d2_new
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

    stego_pixel_block = [[new_gx,new_gur],[new_gbl,new_gbr]]
    return stego_pixel_block

def no_of_bits_to_hide(value):
    #using quantisation range for variant 1
    if value in range(64):
        return 3
    else:
        return 4

#converts plaintext to 8-bit binary format
def convert_to_binary(data):
    data_binary=' '.join(format(ord(x), '08b') for x in data)
    return data_binary
def splitValues(num):
    return num//100,num%100
    

def main():
    #carrier image
    carrier_image_name='food.jpg'
    # carrier_image_name=input("Enter the file name of the carrier image: ")
    if carrier_image_name.split('.')[-1] not in ['jpg','jpeg','png']:
        print('Invalid file type!')
        print('\nProgram terminated')
        return
    grey_img=cv2.imread(carrier_image_name)  # Converting the RGB carrier image to grey scale
    carrier_grey_image_matrix = cv2.cvtColor(grey_img,cv2.COLOR_BGR2GRAY) #storing the image as a matrix

    cv2.imwrite('greyscaleCarrierImage.jpg',carrier_grey_image_matrix)
    
    print('\nCarrier image:')
    print('Length: ' + str(len(carrier_grey_image_matrix)) +'  width: ' + str(len(carrier_grey_image_matrix[0])))
    print('\n')
    
    # Creating the final image matrix for storing the secret data in carrier
    final_image_matrix = np.zeros((len(carrier_grey_image_matrix), len(carrier_grey_image_matrix[0])), dtype=np.uint8)
    cover_image_name='food2.jpeg'
    # cover_image_name=input("Enter the file name of the cover image: ")
    if cover_image_name.split('.')[-1] not in ['jpg','jpeg','png']:
        #print('Invalid file type!')
        #print('\nProgram terminated')
        return
    img2 = cv2.imread(cover_image_name)
    cover_grey_image_matrix = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('greyscale2.jpg',cover_grey_image_matrix)
    print('-------')
    print(cover_grey_image_matrix)
    n = 0
    #print(cover_image_matrix)
    print('\nCover image:')
    print('Length: ' +str(len(cover_grey_image_matrix)) +'  width: ' + str(len(cover_grey_image_matrix[0])))
    print('\n')
    print('Checking whether the cover image can be hid in the carrier image')
    # Check to see whether the secret data can be hid in the carrier image
    if len(carrier_grey_image_matrix)*3 <=2* len(cover_grey_image_matrix) or len(carrier_grey_image_matrix[0])*3 <=2* len(cover_grey_image_matrix[0]):
        print("Unable to fit data in carrier image!\n")
    else:
        print("Able to fit data in carrier image!\n")

    row_cover = col_cover = 0
    i=j=0
    # len1,len2 = splitValues(len(cover_grey_image_matrix))
    # #print(len1)
    # #print(len2)
    # wid1,wid2 = splitValues(len(cover_grey_image_matrix[0]))
    # #To store the length and width of the cover as first two secret data
    # temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
    # temp2 = embedding(temp,len1) # Embedding length of cover image
    # print(temp2)
    # final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
    # final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
    # final_image_matrix[i+1][j] = temp2[1][0]
    # final_image_matrix[i+1][j+1] = temp2[1][1]
    # #print("Final image: ",final_image_matrix)
    # k=2
    # #print(int((format(temp2[0][0],'08b')[-k:]),2))
    # #print(int((format(temp2[0][1], '08b')[-k:]),2))
    # #print(int((format(temp2[1][0], '08b')[-k:]),2))
    # #print(int((format(temp2[1][1], '08b')[-k:]),2))

    # j+=2
    # if j>=len(cover_grey_image_matrix[0]):
    # 		i+=2
    # 		j=0
    # temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
    # temp2 = embedding(temp,len2) # Embedding length of cover image
    # ##print(temp)
    # ##print(temp2)
    # final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
    # final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
    # final_image_matrix[i+1][j] = temp2[1][0]
    # final_image_matrix[i+1][j+1] = temp2[1][1]

    # j+=2
    # if j>=len(cover_grey_image_matrix[0]):
    # 		i+=2
    # 		j=0
    # temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
    # temp2 = embedding(temp,wid1) # Embedding length of cover image
    # final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
    # final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
    # final_image_matrix[i+1][j] = temp2[1][0]
    # final_image_matrix[i+1][j+1] = temp2[1][1]
    # j+=2
    # if j>=len(cover_grey_image_matrix[0]):
    # 		i+=2
    # 		j=0
    # temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
    # temp2 = embedding(temp,wid2) # Embedding length of cover image
    # final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
    # final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
    # final_image_matrix[i+1][j] = temp2[1][0]
    # final_image_matrix[i+1][j+1] = temp2[1][1]
    # j+=2
    # if j>=len(cover_grey_image_matrix[0]):
    # 		i+=2
    # 		j=0

    #print('Performing the embedding procedure........\n')
    while row_cover<len(cover_grey_image_matrix) : #Traversing the cover image matrix
        # Extraction of 2x2 non-overlapping matrix
        n+=1
        temp = [[carrier_grey_image_matrix[i][j],carrier_grey_image_matrix[i][j+1]],[carrier_grey_image_matrix[i+1][j],carrier_grey_image_matrix[i+1][j+1]]]
        cover = cover_grey_image_matrix[row_cover][col_cover]
        col_cover+=1
        if col_cover==len(cover_grey_image_matrix[0]):
            col_cover=0
            row_cover+=1
        j+=2
        if j>=len(cover_grey_image_matrix[0]):
            i+=2
            j=0
        temp2 = embedding(temp,cover) # Function that performs embedding is called
        if i==len(carrier_grey_image_matrix):
            break
        final_image_matrix[i][j] = temp2[0][0]  # The modified pixel values are stored in the final image matrix
        final_image_matrix[i][j+1] = temp2[0][1] # Values are in grey scale
        final_image_matrix[i+1][j] = temp2[1][0]
        final_image_matrix[i+1][j+1] = temp2[1][1]
    print("No. of pixel blocks: " )
    print(n)
    print(i,j)
    k=i
    print('row: ' + str(row_cover))
    print('col: ' + str(col_cover))
    print("-----")
    display_image = np.zeros((len(carrier_grey_image_matrix), len(carrier_grey_image_matrix[0])), dtype=np.uint8)

    for i in range(row_cover):
        for j in range(len(cover_grey_image_matrix[0])):
            display_image[i][j]=cover_grey_image_matrix[i][j]
    image = Image.fromarray(np.uint8(display_image),'L') # Storing the final image matrix as a grey scale image
    image.save('Checking.png')
    print('Embedding procedure completed!\n')

    for i in range(len(cover_grey_image_matrix)): # Traversing the block to right of the cover image in the carrier image
        for j in range(len(cover_grey_image_matrix[0]),len(carrier_grey_image_matrix[0])):
            final_image_matrix[i][j] = carrier_grey_image_matrix[i][j]

    # for i in range(len(cover_grey_image_matrix),len(carrier_grey_image_matrix)): # Traversing the remaining region of the carrier matrix
    #     for j in range(len(cover_grey_image_matrix[0]),len(carrier_grey_image_matrix[0])):
    #         if i>=k:
    #             final_image_matrix[i][j-len(cover_grey_image_matrix[0])] = carrier_grey_image_matrix[i][j-len(cover_grey_image_matrix[0])]
    #         else:
    #             final_image_matrix[i][j] = carrier_grey_image_matrix[i][j]


    print('Storing the result in Check3.png\n')
    img = Image.fromarray(np.uint8(final_image_matrix),'L') # Storing the final image matrix as a grey scale image
    img.save('Check3.png')
    print('Done!')
    print(len(final_image_matrix))
    print(len(final_image_matrix[0]))
if __name__=='__main__':
    main()
