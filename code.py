from PIL import Image, ImageDraw 
from random import randint		
from re import findall


def stega_encrypt():						
	img = Image.open(input("Шлях до картинки: ")) 
	draw = ImageDraw.Draw(img)	   		
	width = img.size[0]  		   		
	height = img.size[1]		   	
	pix = img.load()				
	f = open('keys.txt','w')			

	for elem in ([ord(elem) for elem in input("text here: ")]):
		key = (randint(1,width-10),randint(1,height-10))		
		g, b = pix[key][1:3]
		draw.point(key, (elem,g , b))														
		f.write(str(key)+'\n')								
	
	print('Ключi записанi в keys.txt.')
	img.save("enc.png", "PNG")
	f.close()

def stega_decrypt():
    	
	a = []						    
	keys = []
	img = Image.open(input("Де ваша картинка розташована?: "))				
	pix = img.load()
	f = open(input('path to keys: '),'r')
	y = str([line.strip() for line in f])				
															
	for i in range(len(findall(r'\((\d+)\,',y))):
		keys.append((int(findall(r'\((\d+)\,',y)[i]),int(findall(r'\,\s(\d+)\)',y)[i]))) 	
	for key in keys:
		a.append(pix[tuple(key)][0])							
	return ''.join([chr(elem) for elem in a]).encode("cp1251").decode("utf8")	

print("="*10 + "ШИФРУЄМО ТЕКСТ" + "="*10)
stega_encrypt()
print("="*10 + "ДЕШИФРУЄМО ТЕКСТ" + "="*10)
print("Ваше повiдомлення: ", stega_decrypt())
