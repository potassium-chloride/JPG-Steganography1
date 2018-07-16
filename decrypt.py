#!/usr/bin/env python3
from PIL import Image, ImageDraw
import sys

image=Image.open(sys.argv[1])
width = image.size[0]
height = image.size[1]
s=""
buff=""
pix = image.load()

ri=Image.open("R2.png")
rpix=ri.load()
rsize=int(ri.size[0]/2)

rmR=0
rmG=0
kp=0
for i in range(ri.size[0]):
	for j in range(ri.size[1]):
		rmR+=rpix[i, j][0]
		rmG+=rpix[i, j][1]
		kp+=1

def detectR(x,y):
	mR=-rmR;
	mG=-rmG;
	for i in range(ri.size[0]):
		for j in range(ri.size[1]):
			mR += pix[x-rsize+i, y-rsize+j][0]
			mG += pix[x-rsize+i, y-rsize+j][1]
	mR/=kp
	mG/=kp
	S=0
	for i in range(ri.size[0]):
		for j in range(ri.size[1]):
			R = pix[x-rsize+i, y-rsize+j][0]-mR
			G = pix[x-rsize+i, y-rsize+j][1]-mG
			A = rpix[i,j][3]
			C = rpix[i,j][0]*A
			C2= rpix[i,j][1]*A
			S+=C*R+C2*G
	return S

step=74
arr=[]

def isSTOPsignal():
	if(len(arr)<24):
		return False
	mval=sum(arr)/len(arr)
	tmp=""
	for i in arr[-12:]:
		if(mval>i):tmp+="1"
		else:tmp+="0"
	return tmp.count("10"*len(arr))>0

print("Start decrypt...")

for i in range(rsize+2,width-rsize-2,step):
	for j in range(rsize+2,height-rsize-2,step):
		arr.append(detectR(i,j))
		if(isSTOPsignal()):break

mval=sum(arr)/len(arr)

for i in arr:
	if(mval>i):buff+="1"
	else:buff+="0"

print("Raw data: "+buff)
nbuff=""
for i in buff:
	nbuff+=i
	if(len(nbuff)==8):
		s+=chr(int(nbuff,2))
		nbuff=""

print("Vague decrypted text: "+s)

realsize=int(input("Enter real size: "))

nbuff=""
s=""
for i in range(realsize):
	nbuff+=str(round((int(buff[i]=='1')+int(buff[i+realsize]=='1')+int(buff[i+2*realsize]=='1'))/3))
	if(len(nbuff)==8):
		s+=chr(int(nbuff,2))
		nbuff=""

print("\nResult: \""+s+"\"")
