#code for decryption

def check_range(value):
    if value in range(64):
        return 3
    else:
        return 4

def decrypt(carrier_pixel_block):
    gx=carrier_pixel_block[0][0]
    gxR,gxB,gxG=getPixelValue(gx)

    d1_red=abs(gurR-gxR)
    d1_blue=abs(gurB-gxB)
    d1_green=abs(gurG-gxG)

    d2_red=abs(gbrR-gxR)
    d2_blue=abs(gbrB-gxB)
    d2_green=abs(gbrG-gxG)

    d3_red=abs(gblR-gxR)
    d3_blue=abs(gblB-gxB)
    d3_green=abs(gblG-gxG)

    t1_red=check_range(d1_red)
    t1_blue=check_range(d1_blue)
    t1_green=check_range(d1_green)

    t2_red=check_range(d2_red)
    t2_blue=check_range(d2_blue)
    t2_green=check_range(d2_green)

    t3_red=check_range(d3_red)
    t3_blue=check_range(d3_blue)
    t3_green=check_range(d3_green)

    #calculate lower bound
    l1_red = int(format(gurR, '08b')[-t1_red:])
	l1_green = int(format(gurG, '08b')[-t1_green:])
	l1_blue = int(format(gurB, '08b')[-t1_blue:])

    l2_red = int(format(gblR, '08b')[-t2_red:])
	l2_green = int(format(gblG, '08b')[-t2_green:])
	l2_blue = int(format(gblB, '08b')[-t2_blue:])

    l3_red = int(format(gbrR, '08b')[-t3_red:])
	l3_green = int(format(gbrG, '08b')[-t3_green:])
	l3_blue = int(format(gbrB, '08b')[-t3_blue:])

    s1_red=d1_red+l1_red
    s1_blue=d1_blue+l1_blue
    s1_green=d1_green+l1_green

    s2_red=d2_red+l2_red
    s2_blue=d2_blue+l2_blue
    s2_green=d2_green+l2_green

    s3_red=d3_red+l3_red
    s3_blue=d3_blue+l3_blue
    s3_green=d3_green+l3_green