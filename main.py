import pygame as p
import pygame.locals as locals
import random,time,datetime
import pygame.gfxdraw
import sys
sys.setrecursionlimit(5000)
root=p.display.set_mode((2000,700))
p.init()
from PIL import Image
#Изображения
images={
'stone-axe':p.image.load('Images/tool_0000.png'),
'stone-pick':p.image.load('Images/tool_0001.png'),
'grass':p.transform.scale(p.image.load('Images/grass.png'),(128,128)),
'black-screen':p.image.load('Images/black.png'),
'white0.png':p.image.load('Images/white0.png'),
'white1.png':p.image.load('Images/white1.png'),
'tree':p.image.load('Images/tree.png')}
locate='main'
__version__='0.0.1'
class Button():
	def __init__(self,fromc,toc,loc,code):
		self.rect=[fromc,toc]
		self.loc=loc
		self.code=code
	def collide(self,point):
		#if point in self.rect: но без создания двумерного списка)
		if point[0]>self.rect[0][0]-1 and point[0]<self.rect[1][0]-1 and point[1]>self.rect[0][1]-1 and point[1]<self.rect[1][1]-1:
			return 1
		return 0
	def result(self):
		exec(self.code)
class Player():
	def __init__(self,hp,maxhp,attack,critchance,inventory,x,y):
		self.hp=hp
		self.maxhp=maxhp
		self.attack=attack
		self.inventory=inventory
		self.x,self.y=x,y
		self.spawn=[0,0]
	def regen(self,count):
		if not count+self.hp>self.maxhp:
			return exec('self.hp+=count')
		self.hp=self.maxhp
class World():
	def __init__(self,size,map=[]):
		self.size=size
		self.map=map
class Tile():
	def __init__(self,breaktime,tool,place):
		self.breaktime=breaktime
		self.place=place
		self.tool=tool
tiles={
'tree':Tile(30,'axe',{'x':0,'y':-64}),
'grass':Tile(10,'shovel',{'x':0,'y':0})}
class Source():
	locate='main'
pl=Source()
anim=images['white0.png']
plus=[10,0]
count=0
# Хранение дизайна :3
def main():
	global count,plus
	locs={'main':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],[500,100,images['white0.png']]],'main-exit':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],	[root.get_width()//2-250,0,p.transform.scale(images['black-screen'],(500,root.get_height()))],[root.get_width()//2-200,100,p.font.SysFont('DejaVuSans',50).render('Вы точно хотите выйти?',1,(20,255,255))],[root.get_width()//2-200,root.get_height()//2,p.font.SysFont('DejavuSans',50).render('Да',1,(255,0,0))],[root.get_width()//2+50,root.get_height()//2,p.font.SysFont('DejavuSans',50).render('Нет',1,(0,255,0))]],'main-player':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],[root.get_width()//2-250,0,p.transform.scale(images["black-screen"],(500,root.get_height()))],[root.get_width()//2-p.font.SysFont('dejavusans',50).size('Чаи - персонажи')[0]//2,50,p.font.SysFont('dejavusans',50).render('Чайные миры',1,(25,255,255))],[root.get_width()//2-250,75,p.font.SysFont('dejavusans',25).render('Закрыть',1,(0,255,0))],[root.get_width()//2-p.font.SysFont('dejavusans',50).size('Создать новый мир')[0]//2,root.get_height()-100,p.font.SysFont('dejavusans',50).render('Создать новый мир',1,(25,255,255))]],"main-create-world":[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],[root.get_width()//2-256,0,p.transform.scale(images["black-screen"],(512,root.get_height()))]]}
	game=0
	#Кнопки
	buttons=[Button([0,root.get_height()-70],[p.font.SysFont("DejaVuSans", 70).size('Выход')[0],root.get_height()],'main','pl.locate="main-exit"'),Button((root.get_width()//2-200,root.get_height()//2),(root.get_width()//2-100,root.get_height()+50),'main-exit','quit()'),Button((root.get_width()//2+50,root.get_height()//2),(root.get_width()//2+200,root.get_height()//2+50),'main-exit','pl.locate="main"'),Button((root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200),(root.get_width()//2+p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+275),'main','pl.locate="main-player"'),Button([root.get_width()//2-250,50],[root.get_width()//2-250+p.font.SysFont('dejavusans',50).size("Закрыть")[0],100],'main-player','pl.locate="main"'),Button([root.get_width()//2-p.font.SysFont('dejavusans',50).size("Создать новый мир")[0]//2,root.get_height()-120],[root.get_width()//2+p.font.SysFont('dejavusans',50).size("Создать новый мир")[0]//2,root.get_height()-70],'main-player','pl.locate="main-create-world"')]
	print(buttons[-1].rect)
	while 1:
		if pl.locate.startswith('main'):
			if plus[0]<0:
				plus
				locs[locate][-1][2]=images[f'white{count}.png']	
			else:
				locs[locate][-1][2]=p.transform.flip(images[f'white{count}.png'],1,0)
			if locs[locate][-1][1]+plus[1]>root.get_height():
				plus=[-random.randint(10,15),random.randint(10,15)]
				
				plus[1]=-plus[1]
			if locs[locate][-1][0]+plus[0]>root.get_width():
				plus=[random.randint(10,15),random.randint(10,15)]
				plus[0]=-plus[0]
				locs[locate][-1][2]=p.image.load(f'Images/white{count}.png')
			if locs[locate][-1][0]+plus[0]<0:
				plus=[random.randint(10,15),random.randint(10,15)]
				locs[locate][-1][2]=p.transform.flip(p.image.load(f'Images/white{count}.png'),1,0)
			if locs[locate][-1][1]+plus[1]<0:
				plus=[-plus[0],random.randint(10,15)]
				
			locs[locate][-1][0]=locs[locate][-1][0]+plus[0]
			locs[locate][-1][1]=locs[locate][-1][1]+plus[1]
			if count:
				count=0
			else:
				count=1
		for ev in p.event.get():
				if ev.type==locals.QUIT:
					p.quit()
					quit()
				if ev.type==locals.MOUSEBUTTONDOWN:
					for button in [i for i in buttons if i.loc==pl.locate]:
						if button.collide(ev.pos):
							button.result()
		[root.blit(locs[pl.locate][i][2],locs[pl.locate][i][:2]) for i in range(0,len(locs[pl.locate]))]
		p.display.flip()
def main2():
	global root
	try:
		main()
	except Exception as e:
		print(e)
		root=p.display.set_mode(((2000,700)))
		main2()
main2()