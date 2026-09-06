from pathlib import Path
from html import escape
from playwright.sync_api import sync_playwright
out=Path('C:/Users/Administrator/Desktop/Hermes Files')
out.mkdir(parents=True,exist_ok=True)
s=[]
def add(x): s.append(x)
def p(u,v,z=0): return (700+(u-v)*1.12,480+(u+v)*.54-z)
def poly(coords,fill,stroke='none',sw=1):
 add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in coords)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
def plane(coords,fill,stroke='none',sw=1): poly([p(*q) for q in coords],fill,stroke,sw)
def line(a,b,color,width=2):
 x,y=p(*a); X,Y=p(*b); add(f'<path d="M{x},{y} L{X},{Y}" stroke="{color}" stroke-width="{width}" fill="none"/>')
def box(u,v,w,d,z,h,top,front,side):
 plane([(u,v+d,z),(u+w,v+d,z),(u+w,v+d,z+h),(u,v+d,z+h)],front)
 plane([(u+w,v,z),(u+w,v+d,z),(u+w,v+d,z+h),(u+w,v,z+h)],side)
 plane([(u,v,z+h),(u+w,v,z+h),(u+w,v+d,z+h),(u,v+d,z+h)],top)
def text(x,y,t,size=20,color='#324047',weight=400): add(f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(t)}</text>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1280" viewBox="0 0 1400 1280"><rect width="1400" height="1280" fill="#f7f5ef"/>')
text(65,66,'YOUR ROOM, WITH MORE BREATHING SPACE',17,'#68767a',600)
text(65,117,'Lighter. Calmer. Still yours.',43,'#283b42',600)
text(65,154,'Illustrated concept based on your photo · approximate layout, not measured',18,'#68767a')
# Room shell
plane([(0,0,0),(500,0,0),(500,500,0),(0,500,0)],'#d9d0c0')
plane([(0,0,0),(0,500,0),(0,500,310),(0,0,310)],'#e4e1d8')
plane([(0,0,0),(500,0,0),(500,0,310),(0,0,310)],'#f0ede4')
for q in range(100,500,100):
 line((q,0,0),(q,500,0),'#c7bfae',1)
 line((0,q,0),(500,q,0),'#c7bfae',1)
line((0,500,5),(0,0,5),'#faf8f0',8);line((0,0,5),(500,0,5),'#fffdf6',8)
# Cream curtains on back/right wall
plane([(160,2,80),(450,2,80),(450,2,272),(160,2,272)],'#bdb6a5')
for u in range(160,450,14):
 plane([(u,4,80),(u+14,4,80),(u+14,4,272),(u,4,272)],['#dfd7c4','#f0e8d7','#e9e1ce'][(u-160)//14%3])
 line((u+3,5,86),(u+3,5,266),'#d5cbb5',1)
line((149,8,280),(461,8,280),'#8f887b',5)
# Left short curtain, AC kept clear
plane([(2,300,185),(2,460,185),(2,460,275),(2,300,275)],'#ebe3d0')
for v in range(300,460,12): line((4,v,186),(4,v,274),'#cfc5b0',4)
line((6,292,282),(6,468,282),'#8f887b',5)
box(1,325,21,120,99,73,'#edece6','#c8c6bd','#dedcd2')
for z in range(111,160,7):line((23,334,z),(23,435,z),'#92978e',3)
# Sparse display shelves by corner on left wall
for z in [158,226]:
 box(0,45,38,146,z,7,'#bd9b72','#917151','#a98965')
# display objects, no packaging
box(5,65,19,27,233,28,'#536d79','#405a67','#657e86')
box(5,130,18,25,233,19,'#e5b888','#b08051','#cea06e')
box(5,85,20,32,165,20,'#e8e3d8','#bdbbae','#d5d1c5')
box(7,143,20,20,165,30,'#6e8b73','#486c56','#5b7d63')
# Bed: low base with front storage
box(295,35,180,360,5,41,'#ab9072','#92795e','#aa9072')
box(295,35,180,360,46,21,'#d4d6d3','#b7bfbd','#c2c8c5')
box(292,33,185,364,67,7,'#dce0dd','#bfc8c6','#cbd2cf')
# a soft blue throw across foot
plane([(292,300,75),(477,300,75),(477,372,75),(292,372,75)],'#7898a7')
plane([(477,300,75),(477,372,75),(477,372,40),(477,300,40)],'#5c7b8b')
for u in range(300,475,14):line((u,304,76),(u,369,76),'#88a7b4',1)
# two matching pillows
box(310,57,68,56,75,13,'#f3efe5','#d5d4ca','#e6e2d7')
box(389,57,68,56,75,13,'#b1c4c9','#8fa8b1','#9bb4bb')
for v in [100,224]:
 plane([(476,v,11),(476,v+103,11),(476,v+103,39),(476,v,39)],'#c1af94','#a48e71',1)
 line((478,v+39,30),(478,v+62,30),'#776c5b',3)
# slim workstation along left wall
for u,v in [(18,275),(91,275),(18,467),(91,467)]:box(u,v,6,6,0,116,'#d7d9d3','#a7b1ae','#bbc2be')
box(12,266,94,218,116,10,'#faf9f3','#ced3cc','#e2e5dd')
# monitor parallel to left wall
box(28,300,5,100,145,69,'#26383c','#253b40','#35484e')
plane([(34,306,152),(34,395,152),(34,395,208),(34,306,208)],'#7395a1')
line((35,330,139),(35,330,146),'#435459',5)
box(24,318,24,50,127,3,'#5d6b6b','#465858','#5c6a6a')
box(64,312,27,85,127,3,'#d3d9d5','#a5b3b0','#bdc9c4')
for v in range(316,391,8):line((68,v,131),(87,v,131),'#929f9c',1)
# small compact chair tucked toward desk
for u,v in [(115,337),(155,337),(115,389),(155,389)]:box(u,v,4,4,0,64,'#576768','#384e53','#435b60')
box(110,332,54,67,64,10,'#5c7279','#3e5861','#4b666e')
box(158,332,7,67,76,68,'#617980','#435d66','#526e76')
# ceiling light shown as small detached fixture above room
add('<ellipse cx="700" cy="219" rx="58" ry="19" fill="#d7d4c9"/><ellipse cx="700" cy="215" rx="58" ry="19" fill="#fffdf2" stroke="#e0ddd2" stroke-width="2"/>')
# uncluttered floor note
text(487,944,'OPEN WALKWAY',16,'#776f60',600)
# bottom rule and palette
add('<path d="M65 1084H1335" stroke="#d4d5cb"/>')
text(65,1126,'THE LOOK',14,'#68767a',600)
colors=[('#efeadc','Cream curtains'),('#d8deda','Light-gray bedding'),('#7898a7','Muted blue accents'),('#b69a77','Warm wood')]
for i,(c,label) in enumerate(colors):
 x=65+i*325
 add(f'<rect x="{x}" y="1150" width="28" height="28" rx="14" fill="{c}" stroke="#c8c9bf"/>')
 text(x+40,1171,label,18)
text(65,1226,'Keep the bed + desk • Display fewer items • Hide spare bedding • Keep AC airflow clear',19,'#536368')
add('</svg>')
svg=''.join(s)
(out/'room-concept.svg').write_text(svg,encoding='utf-8')
html='<html><body style="margin:0">'+svg+'</body></html>'
(out/'room-concept.html').write_text(html,encoding='utf-8')
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True)
 page=browser.new_page(viewport={'width':1400,'height':1280},device_scale_factor=1.5)
 page.goto((out/'room-concept.html').as_uri())
 page.screenshot(path=str(out/'room-concept.png'),full_page=True)
 browser.close()
from PIL import Image
im=Image.open(out/'room-concept.png')
print({'image':str(out/'room-concept.png'),'size':im.size,'bytes':(out/'room-concept.png').stat().st_size})
