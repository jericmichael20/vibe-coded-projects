from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import numpy as np
out=Path('C:/Users/Administrator/Desktop/Hermes Files')
im=Image.open('C:/Users/Administrator/Desktop/0d422178-792c-4c78-89de-87bdd6f612fb.jpg').convert('RGB')
w,h=im.size
scale=w/768
mask=Image.new('L',im.size)
d=ImageDraw.Draw(mask)
polys=[[(389,302),(408,294),(416,306),(430,285),(443,283),(451,302),(461,286),(473,285),(479,298),(495,280),(507,281),(507,302),(531,295),(550,272),(560,269),(558,304),(569,305),(578,272),(591,269),(600,272),(598,304),(619,296),(623,269),(641,263),(649,265),(652,279),(661,274),(675,258),(692,257),(697,313),(687,425),(680,567),(672,624),(647,620),(567,613),(552,625),(551,607),(539,592),(379,583),(386,483)],[(106,255),(123,258),(132,275),(141,273),(153,277),(157,294),(168,289),(180,293),(182,312),(197,306),(208,311),(208,323),(219,324),(223,399),(221,449),(207,468),(166,475),(116,472),(112,447)],[(0,201),(23,213),(30,296),(22,380),(18,490),(28,540),(3,556),(0,545)]]
for poly in polys:d.polygon([(int(x*scale),int(y*scale)) for x,y in poly],fill=255)
# Preserve the pink clip on the curtain edge.
d.rectangle((374*scale,497*scale,394*scale,528*scale),fill=0)
mask=mask.filter(ImageFilter.GaussianBlur(1.2))
a=np.asarray(im).astype(float)
alpha=np.asarray(mask).astype(float)/255
# Catch narrow blue fabric edges while leaving neutral hardware alone.
expanded=np.asarray(mask.filter(ImageFilter.MaxFilter(41))).astype(float)/255
blue=(a[:,:,2]>a[:,:,0]*1.12)&(a[:,:,2]>a[:,:,1]*1.035)
alpha=np.maximum(alpha,expanded*blue)
# Warm neutral recoloring retains real folds, shadows and fabric pattern.
lum=.2126*a[:,:,0]+.7152*a[:,:,1]+.0722*a[:,:,2]
value=np.clip(65+.66*a[:,:,2]+.21*lum,0,246)
cream=np.stack([value,value*.961,value*.872],axis=-1)
arr=a*(1-alpha[:,:,None])+cream*alpha[:,:,None]
# Cool light-gray treatment for the exposed sheet, without erasing objects.
bm=Image.new('L',im.size);bd=ImageDraw.Draw(bm)
bed=[(319,674),(357,684),(391,689),(425,692),(442,660),(459,651),(489,659),(517,666),(550,678),(571,709),(594,719),(606,751),(627,770),(649,788),(685,801),(729,816),(767,819),(767,935),(672,915),(597,893),(504,868),(430,838),(344,813),(317,793),(331,744),(316,728)]
bd.polygon([(x*scale,y*scale) for x,y in bed],fill=255)
beta=np.asarray(bm.filter(ImageFilter.GaussianBlur(2))).astype(float)/255*.7
gray=np.stack([lum*.99,lum*1.015,lum*1.018],axis=-1)
arr=arr*(1-beta[:,:,None])+gray*beta[:,:,None]
edited=Image.fromarray(np.uint8(np.clip(arr,0,255)))
edited.save(out/'room-photo-color-mockup.jpg',quality=95)
# Annotated board uses the real photo, not invented dimensions or hidden walls.
photo=edited.resize((900,1200),Image.Resampling.LANCZOS)
board=Image.new('RGB',(1500,1340),'#f6f3ec'); board.paste(photo,(30,110))
draw=ImageDraw.Draw(board)
fontdir=Path('C:/Windows/Fonts')
def font(n,b=False):return ImageFont.truetype(str(fontdir/('segoeuib.ttf' if b else 'segoeui.ttf')),n)
def text(x,y,t,n=23,c='#30434b',b=False):draw.text((x,y),t,font=font(n,b),fill=c)
text(30,20,'YOUR ROOM / PHOTO-BASED COLOR MOCKUP',31,b=True)
text(30,64,'Original layout retained. Cream curtain preview + cooler gray bedding.',22,c='#67747a')
# numbered markers on the photo with high-contrast outlines
points=[(1,590,442),(2,533,779),(3,275,381),(4,235,740),(5,480,941)]
for n,x,y in points:
 X=30+x/768*900;Y=110+y/1024*1200
 draw.ellipse((X-20,Y-20,X+20,Y+20),fill='#304d58',outline='white',width=3)
 bb=draw.textbbox((0,0),str(n),font=font(22,True))
 draw.text((X-(bb[2]-bb[0])/2,Y-16),str(n),font=font(22,True),fill='white')
text(970,125,'WHAT I WOULD CHANGE',22,b=True)
notes=[('01  LIGHTEN THE CURTAINS',['Choose plain cream curtains.','This edit keeps the original fabric','pattern and folds as a color preview.']),('02  SIMPLIFY THE BED',['Use matching light-gray bedding','with one muted-blue accent.','Put clothes and spare pillows away.']),('03  EDIT THE DISPLAY',['Store the product packaging.','Keep a few favorite collectibles','and leave space between them.']),('04  RECLAIM THE WALKWAY',['Tuck the chair under the desk.','Check the armrest clearance before','buying a smaller replacement.']),('05  TIDY THE CABLES',['Route cables along the desk or wall.','Secure the power strip away from','bedding and keep it accessible.'])]
y=190
for title,lines in notes:
 text(970,y,title,24,b=True)
 for i,t in enumerate(lines):text(970,y+44+i*32,t,21,c='#58686e')
 y+=181
text(970,1130,'BEFORE BUYING ANYTHING',21,b=True)
for i,t in enumerate(['Clear the bed and shelf boxes first.','Keep AC vents unobstructed.','Furniture removal and rearrangement','are suggestions, not shown edits.']):text(970,1174+i*29,t,20,c='#58686e')
board.save(out/'room-photo-suggestions.jpg',quality=95)
print({'edited_photo':str(out/'room-photo-color-mockup.jpg'),'suggestion_board':str(out/'room-photo-suggestions.jpg'),'board_size':board.size})
