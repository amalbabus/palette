import argparse
from collections import Counter
from PIL import Image,ImageFilter,ImageFont,ImageDraw
from decimal import Decimal
import pandas as pd
import prettytable
import math
from textwrap import wrap
import os
from tqdm import tqdm
import click

a=[]
b=[]
q=[]
v=[]
s=''
k=0.0

parser = argparse.ArgumentParser(description='Python Palette Maker')
parser.add_argument('image',help="image for extraction",metavar='image')
parser.add_argument('-p','--palette',help="v:vertical palette and h:horizontal palette",metavar='',choices=['v','h'])
parser.add_argument('-n','--nlargest',help="get first n common colors",metavar='',type=int)

args = parser.parse_args()
pt=prettytable.PrettyTable(['color','percentage','rgb'])
img=Image.open(args.image)
w,h=img.width,img.height
for i in tqdm(range(w),desc='Generating Table',unit='unit'):
	for j in range(h):
		d=i,j
		x,y,c=img.getpixel(d)
		a.append('#'+hex(x)[2:].rjust(2,'0')+hex(y)[2:].rjust(2,'0')+hex(c)[2:].rjust(2,'0'))
m=Counter(a).keys()
n=Counter(a).values()
if args.nlargest:
	lst=pd.Series(n)
	t=lst.nlargest(int(abs(args.nlargest)))
	res=t.index.values
else:
	lst=pd.Series(n)
	t=lst.nlargest(10)
	res=t.index.values
ty=''
for i in res:
	k=k+int(n[i])
for i in res:
	e=wrap(str(m[i][1:]),2)
	#ty+=str(int(e[0],16))+','+str(int(e[1],16))+','+str(int(e[2],16))
	pt.add_row([m[i],((float(n[i])/k)*100),(int(e[0],16),int(e[1],16),int(e[2],16))])
print("Palette generated")
print(pt)
if str(args.palette)=='v':
	x=100
	y=200
	#
	img=Image.new('RGB',(y,x),'white')
	for i in tqdm(res,desc='Generating Palette',unit='unit'):
		e=wrap(str(m[i][1:]),2)
		aa,bb,cc=int(e[0],16),int(e[1],16),int(e[2],16)
		for t in range(x):
			for j in range(y):
				img.putpixel((j,t),(aa,bb,cc,255))
		font=ImageFont.truetype('lucida.ttf',20)
		dr=ImageDraw.Draw(img)
		if (aa<127 and bb<127 and cc<127):
			dr.text((50,40),str(m[i]),font=font,fill='#ffffff')
		else:
			dr.text((50,40),str(m[i]),font=font,fill='#000000')
		img.save(str(i)+'.jpg')
	lis=[]

	for i in res:
		lis.append(str(i)+'.jpg')
	#print lis
	sd=100*int(len(res))
	newim=Image.new('RGB',(200,sd),'white')
	imgs=map(Image.open,lis)
	xx=0
	for im in imgs:
		newim.paste(im,(0,xx))
		xx+=100
	for i in lis:
		os.remove(i)
	nme=args.image[:-4]+'_palette.jpg'

	newim.save(nme)
	print('Palette saved to {}\\{}'.format(os.getcwd(),nme))
elif str(args.palette)=='h':
	x=100
	y=200
	img=Image.new('RGB',(x,y),'white')
	for i in tqdm(res,desc='Generating Palette',unit='unit'):
		e=wrap(str(m[i][1:]),2)
		aa,bb,cc=int(e[0],16),int(e[1],16),int(e[2],16)
		for t in range(x):
			for j in range(y):
				img.putpixel((t,j),(aa,bb,cc,255))
		font=ImageFont.truetype('lucida.ttf',20)
		dr=ImageDraw.Draw(img)
		if (aa<127 and bb<127 and cc<127):
			dr.text((10,90),str(m[i]),font=font,fill='#ffffff')
		else:
			dr.text((10,90),str(m[i]),font=font,fill='#000000')
		img.save(str(i)+'.jpg')
	lis=[]

	for i in res:
		lis.append(str(i)+'.jpg')
	#print lis
	sd=100*int(len(res))
	newim=Image.new('RGB',(sd,200),'white')
	imgs=map(Image.open,lis)
	xx=0
	for im in imgs:
		newim.paste(im,(xx,0))
		xx+=100
	for i in lis:
		os.remove(i)
	nme=args.image[:-4]+'_palette.jpg'

	newim.save(nme)
	print('Palette saved to {}\\{}'.format(os.getcwd(),nme))
else:
	pass