import pygame as p
import pygame.locals as locals
import random,time,datetime
import pygame.gfxdraw
import sys
from random import *
from math import *
sys.setrecursionlimit(5000)
root=p.display.set_mode((2000,700))
p.init()
from PIL import Image
import gen_world
#Изображения
images={
'stone-axe':p.image.load('Images/tool_0000.png'),
'stone-pick':p.image.load('Images/tool_0001.png'),
'grass':p.transform.scale(p.image.load('Images/grass.png'),(128,128)),
'black-screen':p.image.load('Images/black.png'),
'white0.png':p.image.load('Images/white0.png'),
'white1.png':p.image.load('Images/white1.png'),
'tree':p.image.load('Images/tree1.png'),
'water':p.image.load('Images/water.png'),
'settings':p.image.load('Images/settings.png'),
'pause':p.image.load('Images/pause.png'),
'arrowleft':p.transform.scale(p.image.load('Images/goleft.png'),(128,128)),
'arrowright':p.transform.scale(p.image.load('Images/goright.png'),(128,128)),
'arrowup':p.transform.scale(p.image.load('Images/goup.png'),(128,128)),
'arrowdown':p.transform.scale(p.image.load('Images/godown.png'),(128,128))}
locate='main'
__version__='0.0.2'
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
	def __init__(self,hp,maxhp,attack,critchance,x,y,inventory=[],name='tea'):
		self.hp=hp
		self.maxhp=maxhp
		self.attack=attack
		self.inventory=inventory
		self.x,self.y=x,y
		self.spawn=[256,256]
		self.name=name
		self.anim=images["white0.png"]
	def regen(self,count):
		if not count+self.hp>self.maxhp:
			return exec('self.hp+=count')
		self.hp=self.maxhp
class Tile():
	def __init__(self,breaktime,tool,place,name):
		self.breaktime=breaktime
		self.place=place
		self.tool=tool
		self.name=name
tiles={
'tree':Tile(30,'axe',{'x':0,'y':-256},'tree'),
'grass':Tile(10,'shovel',{'x':0,'y':0},'grass'),
'water':Tile(-1,'bucket',{'x':0,'y':0},"water")}
class World():
	def gen_plants(self):
		for i in range(len(self.map)):
			for j in range(len(self.map[i])):
				if self.map[i][j]==tiles['grass']:
					if randint(0,10)==10:
						self.builds.append([i*128,j*128,tiles['tree']])
	def __init__(self,name,map=[],players={},builds=[]):
		self.name=name
		self.map=[[tiles[i]  for i in j] for j in map]
		self.builds=[]
		self.players=players
		self.gen_plants()
	
worlds=[]

class Source():
	locate='main'
	world=0
	name='alpha'
pl=Source()
anim=images['white0.png']
plus=[10,0]
count=0
inp=[0,'']
# Хранение дизайна :3
def main():
	global count,plus,inp,game,world
	def new_world():
		global locs
		seed=locs['main-create-world'][-1][3]
	game=0
	locs={'main':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],[500,100,images['white0.png']]],
	'main-exit':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],	[root.get_width()//2-250,0,p.transform.scale(images['black-screen'],(500,root.get_height()))],[root.get_width()//2-200,100,p.font.SysFont('DejaVuSans',50).render('Вы точно хотите выйти?',1,(20,255,255))],[root.get_width()//2-200,root.get_height()//2,p.font.SysFont('DejavuSans',50).render('Да',1,(255,0,0))],[root.get_width()//2+50,root.get_height()//2,p.font.SysFont('DejavuSans',50).render('Нет',1,(0,255,0))]],
	'main-player':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],[root.get_width()//2-250,0,p.transform.scale(images["black-screen"],(500,root.get_height()))],[root.get_width()//2-p.font.SysFont('dejavusans',50).size('Чайные миры')[0]//2,50,p.font.SysFont('dejavusans',50).render('Чайные миры',1,(25,255,255))],[root.get_width()//2-250,75,p.font.SysFont('dejavusans',25).render('Закрыть',1,(0,255,0))],[root.get_width()//2-p.font.SysFont('dejavusans',50).size('Создать новый мир')[0]//2,root.get_height()-100,p.font.SysFont('dejavusans',50).render('Создать новый мир',1,(25,255,255))]]+[[root.get_width()//2-256,(i+1)*128,p.font.SysFont('dejavusans',128).render(worlds[i].name,1,(25,255,255))] for i in range(len(worlds))],
	"main-create-world":[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.font.SysFont("DejaVuSans", 100).render('Tea Survival',1,(20,255,255))],[root.get_width()//2+(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(p.font.SysFont("DejaVuSans", 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Сервера')[0]//2,root.get_height()//5+100,p.font.SysFont('dejavusans',75).render('Сервера',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200,p.font.SysFont('dejavusans',75).render('Локал',1,(25,255,255))],[0,root.get_height()-70,p.font.SysFont("DejaVuSans", 70).render('Выход',1,(20,255,255))],[root.get_width()//2-256,0,p.transform.scale(images["black-screen"],(512,root.get_height()))],[root.get_width()//2-256,100,p.font.SysFont('dejavusans',50).render('Название:',1,(25,255,255))],[root.get_width()//2-p.font.SysFont('dejavusans',75).size("Создание мира")[0]//2,20,p.font.SysFont('dejavusans',50).render('Создание мира',1,(25,255,255))],[root.get_width()//2-256,root.get_height()-100,p.font.SysFont('dejavusans',75).render('Создать',1,(0,255,0))],[root.get_width()//2-256+p.font.SysFont('dejavusans',50).size('Название:')[0]+20,110,p.font.SysFont('dejavusans',30).render(str(randint(10000,100000)),1,(25,255,255)),'']],'game':[(0,0,p.transform.scale(images['pause'],(128,128))),[0,root.get_height()-256,images['arrowleft']],[128*2,root.get_height()-256,images['arrowright']],[128,root.get_height()-128,images['arrowdown']],[128,root.get_height()-128*3,images['arrowup']]]}

	buttons=[Button([0,root.get_height()-70],[p.font.SysFont("DejaVuSans", 70).size('Выход')[0],root.get_height()],'main','pl.locate="main-exit"'),Button((root.get_width()//2-200,root.get_height()//2),(root.get_width()//2-100,root.get_height()+50),'main-exit','quit()'),Button((root.get_width()//2+50,root.get_height()//2),(root.get_width()//2+200,root.get_height()//2+50),'main-exit','pl.locate="main"'),Button((root.get_width()//2-p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+200),(root.get_width()//2+p.font.SysFont('dejavusans',75).size('Локал')[0]//2,root.get_height()//5+275),'main','pl.locate="main-player"'),Button([root.get_width()//2-250,50],[root.get_width()//2-250+p.font.SysFont('dejavusans',50).size("Закрыть")[0],100],'main-player','pl.locate="main"'),Button([root.get_width()//2-p.font.SysFont('dejavusans',50).size("Создать новый мир")[0]//2,root.get_height()-120],[root.get_width()//2+p.font.SysFont('dejavusans',50).size("Создать новый мир")[0]//2,root.get_height()-70],'main-player','pl.locate="main-create-world"'),Button([root.get_width()//2-256+p.font.SysFont('dejavusans',50).size('Название:')[0]+10,100],[root.get_width()//2-256+p.font.SysFont('dejavusans',50).size('Название:')[0]+200,150],'main-create-world','p.key.start_text_input();inp[0]=1'),Button([root.get_width()//2-256,root.get_height()-100],[root.get_width()//2-256+p.font.SysFont('dejavusans',75).size('Создать')[0],root.get_height()],'main-create-world','worlds.append(World(inp[1],map=gen_world.new_world(inp,il=[256]),players={pl.name:Player(50,50,0,2,128*128,128*128,name=pl.name)}));pl.locate="main-player";main2();inp[1]=""'),Button([0,0],[128,128],'game','0'),Button([0,root.get_height()-256],[128,root.get_height()-128],'game','pl.world.players[pl.name].x-=16'),Button([128*2,root.get_height()-256],[128*3,root.get_height()-128],'game','pl.world.players[pl.name].x+=16'),Button([128,root.get_height()-128],[256,root.get_height()],'game','pl.world.players[pl.name].y+=16'),Button([128,root.get_height()-128*3],[256,root.get_height()-256],'game','pl.world.players[pl.name].y-=16')]+[Button([root.get_width()//2-256,(i+1)*128],[root.get_width()//2+256,(i+2)*128],'main-player',f'''
pl.world=worlds[{i}]
pl.locate="game"''') for i in range(len(worlds))]

	while 1:
		if pl.world==0:
			if pl.locate.startswith('main'):
				if plus[0]<0:
					plus
					locs[locate][-1][2]=images[f'white{count}.png']	
				else:
					locs[locate][-1][2]=p.transform.flip(images[f'white{count}.png'],1,0)
				if locs[locate][-1][1]+plus[1]>root.get_height():
					plus=[-randint(10,15),randint(10,15)]
					plus[1]=-plus[1]
				if locs[locate][-1][0]+plus[0]>root.get_width():
					plus=[randint(10,15),randint(10,15)]
					plus[0]=-plus[0]
					locs[locate][-1][2]=p.image.load(f'Images/white{count}.png')
				if locs[locate][-1][0]+plus[0]<0:
					plus=[randint(10,15),randint(10,15)]
					locs[locate][-1][2]=p.transform.flip(p.image.load(f'Images/white{count}.png'),1,0)
				if locs[locate][-1][1]+plus[1]<0:
					plus=[-plus[0],randint(10,15)]
					
				locs[locate][-1][0]=locs[locate][-1][0]+plus[0]
				locs[locate][-1][1]=locs[locate][-1][1]+plus[1]
				if count:
					count=0
				else:
					count=1
			for ev in p.event.get():
					#print(ev)
				
					if ev.type==locals.QUIT:
						p.quit()
						quit()
					if ev.type==locals.KEYUP and inp[0]:
						if ev.key==8:
							locs['main-create-world'][-1][2]=p.font.SysFont('dejavusans',30).render(locs['main-create-world'][-1][3][:-1],1,(25,255,255))
							locs['main-create-world'][-1][3]=locs['main-create-world'][-1][3][:-1]
							inp[1]=locs['main-create-world'][-1][3][:-1]
					if ev.type==locals.TEXTINPUT and inp[0]:
						locs['main-create-world'][-1][3]+=ev.text
						if not game:
							locs['main-create-world'][-1][2]=p.font.SysFont('dejavusans',30).render(locs["main-create-world"][-1][3],1,(25,255,255))
							inp[1]=locs["main-create-world"][-1][3]
					if ev.type==locals.MOUSEBUTTONDOWN:
						for button in [i for i in buttons if i.loc==pl.locate]:
							if button.collide(ev.pos):
								button.result()
		else:
			
			for button in [i for i in buttons if i.loc==pl.locate]:
				if button.collide(p.mouse.get_pos()):
					button.result()
		#	try:
		#	if 1:
		#		pl.world.players[pl.name].x+=10
			
			
		#	try:
				
			[root.blit(images[pl.world.map[i][j].name],(i*128-(pl.world.players[pl.name].x), j*128-pl.world.players[pl.name].y))
			 for i in range(pl.world.players[pl.name].x//128-root.get_width()//128-2,pl.world.players[pl.name].x//128+root.get_width()//128+2) 
			 for j in range(len(pl.world.map[0]))]
		#	except:
		#		print([(i*128-pl.world.players[pl.name].x, j*128-pl.world.players[pl.name].y) for i in range(pl.world.players[pl.name].x//128-root.get_width()//2,pl.world.players[pl.name].x//128+root.get_width()//2) for j in range(pl.world.players[pl.name].y//128-root.get_height()//2,pl.world.players[pl.name].y//128+root.get_height()//2)])
		#		sys.exit()
		#		quit()
		#		p.quit()
			[root.blit(images[pl.world.builds[i][2].name],(pl.world.builds[i][0]+pl.world.builds[i][2].place['x']-pl.world.players[pl.name].x,pl.world.builds[i][1]+-pl.world.players[pl.name].y)) for i in range(len(pl.world.builds))]
			[root.blit(pl.world.players[pl.name].anim,(root.get_width()//2-32,root.get_height()//2)) for i in pl.world.players ]
			[root.blit(p.font.SysFont('dejavusans',25).render(pl.world.players[i].name,1,(25,255,255)),(root.get_width()//2,root.get_height()//2-30)) for i in pl.world.players]
		
		#	except:
		#		print([i for i in pl.world.players if i.name==pl.name],pl.name,[i.name for i in pl.world.players])
		#		quit()
		#	p.display.flip()
		[root.blit(locs[pl.locate][i][2],locs[pl.locate][i][:2]) for i in range(0,len(locs[pl.locate]))]
		
		p.display.flip()
def main2():
	global root
	try:
		main()
	except Exception as e:
		print(e.with_traceback(e.__traceback__))
		root=p.display.set_mode(((2000,700)))
		main2()
main2()