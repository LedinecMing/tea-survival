def new_world(seed,il=[256,128,64,32,16,8,4,2]):
	from perlin import SimplexNoise
	import sys
	seed=str(seed)
	seed=sum([ord(i) for i in seed])
	print(seed)
	rgb=[]
	for l in il :
		for i in range(l):
			if len(rgb)<i+1:
				rgb.append([])
			for j in range(l):
				if len(rgb[i])<j+1:
					rgb[i].append([0,0,0])
				color=[abs(SimplexNoise().noise2(i*(il[0]/l)*seed,j*(il[0]/l)*seed)),0,0]
				for m in range(1,il[0]//l+1):
					for k in range(1,il[0]//l+1):
						try:
							rgb[i*m][j*k][0]+=color[0]
						except:
								print(i,j,m,k*m,j*k,l,len(rgb),len(rgb[i*m]))
								sys.exit()
								
	for i in rgb:
		i[j][0]//=len(il)
	for i in rgb:
		for j in range(len(rgb[0])):
			if round(i[j][0]*255)%256<200:
				i[j]='grass'
			elif round(i[j][0]*255)%256<255:
				i[j]='water'
	return rgb
if __name__=='__main__':
	print(new_world('j'))