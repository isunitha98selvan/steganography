from PIL import Image

def hide_seek(new_img,message):
    #list of pixel values
    pix_val = list(new_img.getdata()) 

#converts plaintext to 8-bit binary format
def convert_to_binary(data):
    data_binary=' '.join(format(ord(x), '08b') for x in data)
    print(data_binary)
    return data_binary

def main():
    #carrier image
    image_name=input("Enter name of the image: ")
    img=Image.open(image_name,'r')
    width,height=img.size
    new_img=img.copy() 
    print("Reading image...")
    print("Image format: ",img.format)
    print("Image size: ",width,"x",height)
   
    #data to be encypted
    file_name= input("Enter file name to be encrypted: ")
    f=open(file_name,"r")
    data=f.read()
    binary_data=convert_to_binary(data)
    
    #check if carrier image is big enough

    hide_seek(new_img,data)

    new_img.save('encrypted.jpg')

if __name__=='__main__':
    main()
