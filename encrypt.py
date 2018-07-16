#!/usr/bin/env python3
from PIL import Image, ImageDraw
import sys

image=Image.open(sys.argv[1])
txt=sys.argv[2]
width = image.size[0]
height = image.size[1]
draw = ImageDraw.Draw(image)

buff=""
for c in txt:
	tmp=bin(ord(c))[2:]
	tmp=(8-len(tmp))*'0'+tmp
	buff+=tmp

buff=3*buff

print("Size:",len(buff))
step=74
msize=int(width/step)*int(height/step)-2
print("Maxsize:",msize)
if(msize<len(buff)):
	print("Little picture. Exit")
	sys.exit(1)
else:
	print("OK")

ind=-1

pix = image.load()

ri=Image.open("R2.png")
rpix=ri.load()
rsize=int(ri.size[0]/2)

#encimg=Image.new("RGB", (image.width, image.height))
#draw = ImageDraw.Draw(encimg)

hideK=6

def addRed(x,y):
	global draw,pix,ri,rpix
	for i in range(ri.size[0]):
		for j in range(ri.size[1]):
			R = pix[x-rsize+i, y-rsize+j][0]
			G = pix[x-rsize+i, y-rsize+j][1]
			B = pix[x-rsize+i, y-rsize+j][2]
			C = rpix[i,j][0]
			C2= rpix[i,j][1]
			A = rpix[i,j][3]/hideK
			R=int((R*(255-A)+C*A)/255)
			G=int((G*(255-A)+C2*A)/255)
			draw.point((x-rsize+i, y-rsize+j), (R, G, B))

def addGreen(x,y):
	global draw,pix,ri,rpix
	for i in range(ri.size[0]):
		for j in range(ri.size[1]):
			R = pix[x-rsize+i, y-rsize+j][0]
			G = pix[x-rsize+i, y-rsize+j][1]
			B = pix[x-rsize+i, y-rsize+j][2]
			C = rpix[i,j][0]
			C2= rpix[i,j][1]
			A = rpix[i,j][3]/hideK
			G=int((G*(255-A)+C*A)/255)
			R=int((R*(255-A)+C2*A)/255)
			draw.point((x-rsize+i, y-rsize+j), (R, G, B))

def addBlue(x,y):
	global draw,pix,ri,rpix
	for i in range(ri.size[0]):
		for j in range(ri.size[1]):
			R = pix[x-rsize+i, y-rsize+j][0]
			G = pix[x-rsize+i, y-rsize+j][1]
			B = pix[x-rsize+i, y-rsize+j][2]
			C = max(rpix[i,j][0],rpix[i,j][1])
			A = rpix[i,j][3]/hideK
			B=int((B*(255-A)+C*A)/255)
			draw.point((x-rsize+i, y-rsize+j), (R, G, B))

print("Raw data: "+buff+"\n")

for i in range(rsize+2,width-rsize-2,step):
	for j in range(rsize+2,height-rsize-2,step):
		pix = image.load()
		ind+=1
		pers=int(100*ind/len(buff))
		if(pers<101):sys.stdout.write("Encrypting: "+"["+pers*"="+(100-pers)*"_"+"] "+str(pers)+"%\r")
		if(ind>len(buff)):
			cur=ind%2
			sys.stdout.write("Add middle data: "+"["+(pers-100)*"="+(200-pers)*"_"+"] "+str(pers-100)+"%   \r")
			if(cur==0):
				addRed(i,j)
			else:
				addGreen(i,j)
			if(ind>2*len(buff)):
				image.save("encrypted-"+sys.argv[1].replace(".png",".jpg"))
				print("Wrote                   "+100*" ")
				sys.exit(0)
		elif(ind==len(buff)):
			cur=ind%2
			if(cur==0):
				addRed(i,j)
			else:
				addGreen(i,j)
		else:
			cur=buff[ind]
			if(cur=='0'):
				addRed(i,j)
			else:
				addGreen(i,j)

image.save("encrypted-"+sys.argv[1].replace(".png",".jpg"))
print("Wrote                   "+100*" ")
sys.exit(0)

