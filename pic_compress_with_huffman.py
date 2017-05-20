from PIL import Image as img
from colorama import Fore, Back, Style
import heapq
from collections import defaultdict
from matplotlib import pyplot as plt

def bin(num):
	if num == 0:
		return ""
	return bin(num//2) + str(num%2)
def to_bin(num):
	num = bin(num)
	if len(num) != 8:
		num = ('0'*(8-len(num)))+num
	return num

t1=False
while t1 != True:
	try:
		u_inp = input("Enter image location : ")
		im = img.open(u_inp).convert('LA') #convert normal pic to gray scale pic
		t1=True
	except Exception:
		print("Wrong Directory...")

pix = im.load()

print(Fore.LIGHTCYAN_EX + "\nCompressing in ((Huffman)) form ",end="")
for i in range(20):
	print(".",end="")
print(Style.RESET_ALL + "\n")
#just for fun

im_color_counter = []

for c in range(256):
	tmp2 = 0
	for c1 in range(im.height):
		for c2 in range(im.width):
			if pix[c2,c1][0] == c :
				tmp2+=1
	im_color_counter.append(tmp2)


def encode(frequency):
    heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    

data = []
for i in range(256):
	for q in range(0,im_color_counter[i]):
		data.append(i)

frequency = defaultdict(int)
for symbol in data:
    frequency[symbol] += 1

ftmp = 0
histo = []
huff = encode(frequency)
print ("Symbol{:->5}Weight{:->5}Huffman Code\n".format("",""))
for p in huff:
    print ("  {0:-<10}{1:-<13}{2}".format((str(p[0])),(str(frequency[p[0]])),(str(p[1]))))
    ftmp = ftmp + len(p[1])*frequency[p[0]] 
    histo.append((p[0],frequency[p[0]]))

print("\nNormal pic size = ",(im.height * im.width * 8))
print("Enocded pic size =",ftmp)

xes = []
for x in range(0,256):
	xes.append(x)
frq1 = (sorted(histo,key=lambda x:x[0]))
frq2 =[]
for i in range(0,256):
	frq2.append(frq1[i][1])
plt.plot(xes,frq2)
plt.show()
#from line xes=[]  is about plotting a histogram

