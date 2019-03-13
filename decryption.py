#code for decryption
import cv2
import numpy as np

def check_range(value):
    if value in range(64):
        return 3
    else:
        return 4

def decrypt(carrier_pixel_block):
    gx  = carrier_pixel_block[0][0]
    gur = carrier_pixel_block[0][1]
    gbl = carrier_pixel_block[1][0]
    gbr = carrier_pixel_block[1][1]

    bin_gx=list(format(gx,'08b'))

    d1=abs(gur-gx)
    d2=abs(gbr-gx)
    d3=abs(gbl-gx)
   
    t1=check_range(d1)
    t2=check_range(d2)
    t3=check_range(d3)

    #calculate lower bound
    l1 = int(format(gur, '08b')[-t1:])
    l2 = int(format(gbl, '08b')[-t2:])
    l3 = int(format(gbr, '08b')[-t3:])

    s1 = d1-l1
    s2 = d2-l2
    s3 = d3+l3

    bin_s1=list(format(s1,'08b'))
    bin_s2=list(format(s2,'08b'))
    bin_s3=list(format(s3,'08b'))


def main():
    encrypted_image_name='Attempt1.png'
    img=cv2.imread(encrypted_image_name)
    #print(img)
    encrypted_image_matrix = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    print('Carrier image:')
    print('Length: ' +str(len(encrypted_image_matrix)) +'  width: ' + str(len(encrypted_image_matrix[0])))
    print(encrypted_image_matrix)
    decrypt(encrypted_image_matrix)

if __name__=='__main__':
    main()