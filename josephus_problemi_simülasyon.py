import math
import pygame

pygame.init()
pen=pygame.display.set_mode((660,660))

def açı_bul(knm1, knm2):
	return pygame.Vector2(0, 0).angle_to(knm2 - knm1)
def hareket_ettir(knm1, knm2, adm):
	if knm1.distance_to(knm2) < adm:
		return pygame.Vector2(knm2)
	return knm1 + adm * pygame.Vector2(math.cos(math.radians(açı_bul(knm1, knm2))), math.sin(math.radians(açı_bul(knm1, knm2))))
class eleman:
	def __init__(self,i,hayat,açı,konum,mevcutaçı,mevcutkonum):
		self.i=i
		self.hayat=hayat
		self.açı=açı
		self.konum=konum
		self.mevcutaçı=mevcutaçı
		self.mevcutkonum=mevcutkonum
	

n=13
çap=300
lst=[]

xy=pygame.Vector2(430,330)
for i in range(1,n+1):
	konum=pygame.Vector2(math.cos(math.radians(360/n*(i-1)))*çap,math.sin(math.radians(360/n*(i-1)))*çap)
	lst.append(eleman(i,True,360/n*(i-1)+180,xy+konum,360/n*(i-1)+180,xy+konum))



def öldürme():
	syc=0
	çık=0
	hayatta=[]
	for i in lst:
		if i[1]:
			hayatta.append(i[0])
	print(hayatta)
	
	kesilen=(syc+1)%len(lst)
	while not lst[kesilen][1]:
		kesilen=(kesilen+1)%len(lst)
	print("kesen",lst[(syc)%len(lst)][0],"kesilen",lst[(kesilen)%len(lst)][0])
	lst[(kesilen)%len(lst)][1]=False
	
	kesilen=(kesilen+1)%len(lst)
	while not lst[kesilen][1]:
		kesilen=(kesilen+1)%len(lst)
	syc=(kesilen)%(len(lst))
	
	hayatta=[]
	for i in lst:
		if i[1]:
			hayatta.append(i[0])
	
	print(hayatta)
	print("hayatta kalan",hayatta[0])
def kesme_başla():
	global kesilen
	kesilen=(syc+1)%len(lst)
	while not lst[kesilen].hayat:
		kesilen=(kesilen+1)%len(lst)
def kes():
	global lst
	lst[(kesilen)%len(lst)].hayat=False
def sonrakine_geç():
	global syc,kesilen,hayatta
	kesilen=(kesilen+1)%len(lst)
	while not lst[kesilen].hayat:
		kesilen=(kesilen+1)%len(lst)
	syc=(kesilen)%(len(lst))
	
	hayatta=[]
	for i in lst:
		if i.hayat:
			hayatta.append(i.i)
syc=0
kesilen=0
hayatta=[]
for i in lst:
	if i.hayat:
		hayatta.append(i.i)

#lst[kesilen].hayat=False
def çizme(pen,lst):
	syc31=0
	for i in lst:
		if syc31!=syc:
			if i.hayat:
				pygame.draw.circle(pen,(0,0,255),i.mevcutkonum,20,0)
			else:
				pygame.draw.circle(pen,(170,170,170),i.mevcutkonum,20,0)
			açır=math.radians(i.mevcutaçı)
			if i.hayat:
				pygame.draw.line(pen,(200,200,200),i.mevcutkonum+pygame.Vector2(math.cos(açır),math.sin(açır))*25,i.mevcutkonum+pygame.Vector2(math.cos(açır),math.sin(açır))*70,2)
			rnd_i=fnt2.render(str(i.i),True,(255,0,0))
			pen.blit(rnd_i,i.mevcutkonum-pygame.Vector2(rnd_i.get_size())/2)
		syc31+=1
	if lst[syc].hayat:
		pygame.draw.circle(pen,(0,0,255),lst[syc].mevcutkonum,20,0)
	else:
		pygame.draw.circle(pen,(170,170,170),lst[syc].mevcutkonum,20,0)
	açır=math.radians(lst[syc].mevcutaçı)
	if lst[syc].hayat:
		pygame.draw.line(pen,(200,200,200),lst[syc].mevcutkonum+pygame.Vector2(math.cos(açır),math.sin(açır))*25,lst[syc].mevcutkonum+pygame.Vector2(math.cos(açır),math.sin(açır))*70,2)
	rnd_i=fnt2.render(str(lst[syc].i),True,(255,0,0))
	pen.blit(rnd_i,lst[syc].mevcutkonum-pygame.Vector2(rnd_i.get_size())/2)
fnt=pygame.font.Font(None, 55)	
fnt2=pygame.font.Font(None, 35)	
rnd=pygame.Surface((0,0))


zmn=pygame.time.get_ticks()
drm=True
mod=0
artış_açı_işaret=0
artış_açı=1
while drm:
	for o in pygame.event.get():
		if o.type==pygame.QUIT:
			drm=False
			
			
	if pygame.time.get_ticks()-zmn>=5:
		if mod==0:
			kesme_başla()
			
			#kesilen=15
			açısı=açı_bul(lst[syc].mevcutkonum,lst[kesilen].mevcutkonum)
			açısır=math.radians(açısı)
			hedef_açısı=açısı
			hedef_konum=lst[kesilen].mevcutkonum-pygame.Vector2(math.cos(açısır),math.sin(açısır))*(20+25)
			mod=1
			if (hedef_açısı-lst[syc].mevcutaçı)%360<180:
				artış_açı_işaret=1
			else:
				artış_açı_işaret=-1
		elif mod==1:
			lst[syc].mevcutaçı+=artış_açı*artış_açı_işaret
			if abs(lst[syc].mevcutaçı-hedef_açısı)%360<=artış_açı:
				print("zooort")
				lst[syc].mevcutaçı=hedef_açısı
				mod=2
		elif mod==2:
			lst[syc].mevcutkonum=hareket_ettir(lst[syc].mevcutkonum,hedef_konum,1)
			if lst[syc].mevcutkonum==hedef_konum:
				mod=3
				kes()
				print("bitti")
		elif mod==3:
			lst[syc].mevcutkonum=hareket_ettir(lst[syc].mevcutkonum,lst[syc].konum,1)
			if lst[syc].mevcutkonum==lst[syc].konum:
				mod=4
				kes()
				print("bitti")
				artış_açı_işaret=-artış_açı_işaret
		elif mod==4:
			lst[syc].mevcutaçı+=artış_açı*artış_açı_işaret
			if abs(lst[syc].mevcutaçı-lst[syc].açı)%360<=artış_açı:
				print("zooort")
				lst[syc].mevcutaçı=lst[syc].açı
				mod=5
		elif mod==5:
			sonrakine_geç()
			mod=0
			if len(hayatta)==1:
				mod=-1
				rnd=fnt.render("Hayatta kalan "+str(hayatta[0]),True,(255,255,255))
			
		zmn=pygame.time.get_ticks()
	
	pen.fill((120,155,100))
	çizme(pen,lst)
	
	if mod==-1:
		#print("hayatta kalan",hayatta[0])
		pen.blit(rnd,(100,200))
	pygame.display.flip()