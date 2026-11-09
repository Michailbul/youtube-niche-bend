
import json, math, sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1920,1080,30
BG=(10,8,5); CARD=(25,25,25); GR=(43,39,35); CO=(242,97,87); TE=(121,183,145); LI=(255,244,234); AM=(232,168,56); MU=(141,133,122); DK=(19,16,13)
HN='/System/Library/Fonts/HelveticaNeue.ttc'; MN='/System/Library/Fonts/Menlo.ttc'
_fc={}
def F(sz,w='b'):
    k=(sz,w)
    if k not in _fc:
        idx={'b':1,'r':0,'x':9}[w] if w!='m' else 0
        try: _fc[k]=ImageFont.truetype(MN if w=='m' else HN, sz, index=idx)
        except Exception: _fc[k]=ImageFont.truetype(HN, sz, index=1)
    return _fc[k]
TH='/tmp/nbv/th/'
_ic={}
def thumb(id,w,h=None):
    h=h or int(w*9/16); k=(id,w,h)
    if k not in _ic:
        im=Image.open(TH+id+'.jpg').convert('RGB'); iw,ih=im.size
        # crop 4:3 letterbox to 16:9
        tgt=w/h; ch=int(iw/tgt); y0=(ih-ch)//2
        im=im.crop((0,y0,iw,y0+ch)).resize((w,h),Image.LANCZOS)
        m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),14,fill=255)
        _ic[k]=(im,m)
    return _ic[k]
TG=json.load(open('/tmp/nbv/targets.json'))
def cl(x): return max(0.0,min(1.0,x))
def ease(x): x=cl(x); return 1-(1-x)**3
def P(t,a,d=0.5): return ease((t-a)/d)
def mix(c,a,bg=BG): return tuple(int(b+(x-b)*a) for x,b in zip(c,bg))
def fmt(n):
    if n is None: return '-'
    return (('%.2f'%(n/1e6)).rstrip('0').rstrip('.')+'M') if n>=1e6 else (str(round(n/1e3))+'K' if n>=1e3 else str(int(n)))

class Ctx:
    def __init__(s,img): s.img=img; s.d=ImageDraw.Draw(img)
    def text(s,xy,txt,sz,col=LI,a=1,w='b',anchor='la',dy=0):
        s.d.text((xy[0],xy[1]+(1-a)*dy),txt,font=F(sz,w),fill=mix(col,a),anchor=anchor)
    def box(s,xy,col=CARD,a=1,r=16,outline=None,ow=2):
        s.d.rounded_rectangle(xy,r,fill=mix(col,a) if col else None,outline=mix(outline,a) if outline else None,width=ow)
    def pic(s,id,x,y,w,h=None,a=1):
        im,m=thumb(id,w,h)
        if a<1: m=m.point(lambda v:int(v*a))
        s.img.paste(im,(int(x),int(y)),m)
    def wrap(s,txt,sz,maxw,w='b'):
        words=txt.split(); lines=[]; cur=''
        for wd in words:
            t=(cur+' '+wd).strip()
            if s.d.textlength(t,font=F(sz,w))<=maxw: cur=t
            else: lines.append(cur); cur=wd
        if cur: lines.append(cur)
        return lines
    def para(s,xy,txt,sz,maxw,col=LI,a=1,w='b',lh=1.18,dy=0):
        y=xy[1]
        for ln in s.wrap(txt,sz,maxw,w): s.text((xy[0],y),ln,sz,col,a,w,dy=dy); y+=int(sz*lh)
        return y
    def card(s,id,x,y,w,title,meta,a=1,border=GR,tsz=26):
        h=int(w*9/16); lines=s.wrap(title,tsz,w-36)[:2]; ch=h+30+len(lines)*int(tsz*1.2)+36
        s.box((x,y,x+w,y+ch),CARD,a,16,outline=border)
        s.pic(id,x,y,w,h,a)
        yy=y+h+18
        for ln in lines: s.text((x+18,yy),ln,tsz,LI,a); yy+=int(tsz*1.2)
        s.text((x+18,yy+6),meta,18,MU,a,'m')
        return ch
    def pill(s,x,y,txt,col,a=1,sz=26,fill=None):
        tw=s.d.textlength(txt,font=F(sz)); s.box((x,y,x+tw+44,y+sz+30),fill or DK,a,40,outline=col,ow=2)
        s.text((x+22,y+14),txt,sz,col,a); return tw+44
    def mark(s,x,y,ok,a=1,sz=50):
        col=TE if ok else CO; w=max(5,sz//8)
        if ok: s.d.line((x,y+sz*0.55,x+sz*0.38,y+sz*0.9,x+sz,y+sz*0.15),fill=mix(col,a),width=w,joint='curve')
        else:
            s.d.line((x,y,x+sz*0.85,y+sz*0.85),fill=mix(col,a),width=w); s.d.line((x+sz*0.85,y,x,y+sz*0.85),fill=mix(col,a),width=w)
    def arrow(s,x1,y1,x2,y2,col=CO,a=1,wd=6):
        s.d.line((x1,y1,x2,y2),fill=mix(col,a),width=wd)
        ang=math.atan2(y2-y1,x2-x1); L=22
        pts=[(x2,y2),(x2-L*math.cos(ang-0.45),y2-L*math.sin(ang-0.45)),(x2-L*math.cos(ang+0.45),y2-L*math.sin(ang+0.45))]
        s.d.polygon(pts,fill=mix(col,a))
    def headline(s,t,txt,hi=None,y=200):
        a=P(t,0.05,0.5); x=140
        parts=txt.split('|')
        for i,pt in enumerate(parts):
            col=CO if i%2 else LI
            s.text((x,y),pt.upper(),84,col,a,dy=30); x+=s.d.textlength(pt.upper(),font=F(84))

# ---------------- scenes
def s_intro(c,t,D):
    c.text((140,330),'NICHE',230,LI,P(t,.1,.6),dy=60); c.text((140,560),'BEND',230,CO,P(t,.3,.6),dy=60)
    c.text((150,840),'How Michael decides what YouTube video to make',40,MU,P(t,1.0),'r')
    c.text((150,905),'20 scenes  ·  note the scene number for feedback',22,MU,P(t,1.8),'m')
def s_method(c,t,D):
    c.headline(t,'We never |invent| a format')
    c.card('mFiZG43v_4A',140,360,620,'Everyone Called Him an Idiot. He Got Richer Every Time. | Timothy Dexter','986K VIEWS  ·  3.9K SUBS  ·  HISTORY',P(t,.4))
    a=P(t,1.4); c.arrow(810,560,1080,560,CO,a); c.text((945,500),'KEEP THE FORMAT',22,LI,a,'m',anchor='ma'); c.text((945,600),'SWAP ONE THING',22,CO,P(t,1.8),'m',anchor='ma')
    a=P(t,2.4); x,y=1140,360
    c.box((x,y,x+620,y+349),(42,23,20),a,16,outline=CO)
    c.text((x+310,y+130),'EVERYONE CALLED',52,LI,a,anchor='ma'); c.text((x+310,y+195),'THE BEETLE UGLY',52,CO,a,anchor='ma')
    c.box((x,y+349,x+620,y+470),CARD,a,16,outline=CO); c.text((x+18,y+372),'The Beetle film · same formula, our subject',26,LI,a); c.text((x+18,y+420),'CARS  ·  KEPT 4 OCT',18,MU,a,'m')
def s_pack(c,t,D):
    c.headline(t,'Title + |thumbnail| first')
    a=P(t,.4); c.card('J6r0-AjVU5A',140,340,880,'The Most FEARED Car In F1 History','373K VIEWS · 3.1K SUBS',a,CO,34)
    c.text((1100,420),'1',150,CO,P(t,1.0)); c.text((1210,460),'PACKAGING',56,LI,P(t,1.0))
    c.text((1100,640),'2',150,MU,P(t,1.8)); c.text((1210,680),'VIDEO',56,MU,P(t,1.8))
    c.para((1100,860),'Start from what is winning now. Readapt it.',30,700,MU,P(t,2.6),'r')
def s_niches(c,t,D):
    c.headline(t,'Packaging from |other niches|')
    cx,cy=1000,640
    nodes=[('HISTORY',430,420),('WEAPONS',380,700),('BUSINESS',640,900),('NATURE',1360,900),('SCIENCE',1600,700),('MACHINES',1560,420)]
    for i,(n,x,y) in enumerate(nodes):
        a=P(t,.5+i*.25); c.arrow(x+(cx-x)*0.25,y+(cy-y)*0.25,x+(cx-x)*0.72,y+(cy-y)*0.72,TE,P(t,1.2+i*.2),5)
        c.pill(x-90,y-30,n,TE,a)
    a=P(t,.3); c.d.ellipse((cx-150,cy-150,cx+150,cy+150),fill=mix((42,23,20),a),outline=mix(CO,a),width=4)
    c.text((cx,cy-30),'OUR',40,LI,a,anchor='ma'); c.text((cx,cy+15),'NICHE',40,CO,a,anchor='ma')
    a=P(t,3.0); c.pill(1250,990,'CAR CHANNELS · ALREADY SERVED',MU,a,22)
    c.d.line((1250,1026,1700,1026),fill=mix(CO,a),width=4)
def s_filter(c,t,D):
    c.headline(t,'The |filter|',y=120)
    rows=[('THIS MONTH · BY VIEWS','search + title formulas'),('MEDIAN ≥ 50K','never one viral hit'),('MORE THAN ONE HIT','repeatable'),('CHANNEL < 6 MONTHS','fresh'),('< 100K SUBSCRIBERS','small = proof of format'),('FACELESS','read the frames'),('< 3 COMPETITORS','crossing open'),('MAKEABLE','animated stills, 3D')]
    for i,(a1,b1) in enumerate(rows):
        a=P(t,.4+i*.45); w=1500-i*110; x=(W-w)//2; y=260+i*84
        c.box((x,y,x+w,y+70),(30,24,20),a,12,outline=GR); c.text((x+30,y+20),a1,32,LI,a); c.text((x+w-30,y+26),b1.upper(),18,MU,a,'m',anchor='ra')
    a=P(t,4.4); x=560
    for txt,col in [('PROVEN',TE),('FORMAT ONLY',AM),('PASS',CO)]: x+=c.pill(x,960,txt,col,a)+24
def s_matrix(c,t,D):
    c.headline(t,'Has views. |Not occupied.|',y=120)
    x0,y0,s=600,250,320
    lab=[('TAKEN',1,0,MU),('GO',1,1,TE),('NOTHING',0,0,MU),('NO AUDIENCE',0,1,MU)]
    for i,(n,r,col_,col) in enumerate(lab):
        a=P(t,.4+i*.3); x=x0+col_*(s+16); y=y0+(1-r)*(s+16)
        go=n=='GO'
        c.box((x,y,x+s,y+s),(18,40,26) if go else CARD,a,18,outline=TE if go else GR,ow=4 if go else 2)
        c.text((x+s/2,y+s/2-30),n,64 if go else 40,col if go else MU,a,anchor='ma')
    a=P(t,1.6); c.text((x0-40,y0+s+8),'DEMAND',26,LI,a,'m',anchor='ra'); c.text((x0-40,y0+s+44),'people watch it',22,MU,a,'r',anchor='ra')
    c.text((x0+s+8,y0+2*s+40),'CROSSING EMPTY',26,LI,a,'m',anchor='ma'); c.text((x0+s+8,y0+2*s+76),'nobody serves it our way yet',22,MU,a,'r',anchor='ma')
    c.para((1400,420),'Many uploads with no views = the packaging failed, not a full niche.',30,420,AM,P(t,2.6),'b')
def s_test(c,t,D):
    c.headline(t,'Test every |bend|',y=120)
    q='Every Engine With A Strange Mechanism Explained'; n=int(len(q)*cl((t-0.4)/1.6))
    c.box((200,280,1720,380),CARD,1,50,outline=GR); c.text((260,312),q[:n]+('|' if int(t*3)%2 else ''),38,LI,1,'r')
    a=P(t,2.0); x=200
    for ch in ['THIS MONTH','SORTED BY VIEWS']: x+=c.pill(x,410,ch,MU,a,20)+16
    rows=[('The Car That Ruined Its Inventor',87),('Everyone Called Him an Idiot | car founder',324),('Every Engine With A Strange Mechanism Explained',172538)]
    for i,(ti,v) in enumerate(rows):
        a=P(t,2.6+i*.6); y=530+i*130
        c.box((200,y,1720,y+110),(28,16,14),a,14,outline=(90,42,37))
        c.text((240,y+36),ti,34,LI,a); vv=int(v*cl((t-2.6-i*.6)/1.0))
        c.text((1680,y+22),fmt(vv)+' views',52,CO,a,anchor='ra')
    c.text((W//2,960),'NO VIEWS → DROP IT, WRITE IT IN NO-GO',30,CO,P(t,4.6),'m',anchor='ma')
def s_subject(c,t,D):
    c.headline(t,'Biggest |subject| first',y=160)
    a=P(t,.4); g=ease((t-.6)/1.6)
    c.text((200,420),'FORMULA 1',48,LI,a); c.box((520,410,520+int(1150*g),490),TE,a,10)
    c.text((200,560),'RALLY',48,MU,a); c.box((520,550,520+int(165*g),630),MU,a,10)
    c.text((1700,700),'≈ 7×',150,TE,P(t,2.2),anchor='ra')
    c.para((200,800),'Fill a proven format with the biggest subject its facts allow.',32,1000,MU,P(t,2.8),'r')
def s_tension(c,t,D):
    c.headline(t,'Titles need |tension|',y=110)
    def tc(x,y,ok,parts,note,a):
        col=TE if ok else CO; c.box((x,y,x+780,y+330),(16,26,19) if ok else (28,16,14),a,18,outline=(47,90,60) if ok else (90,42,37))
        c.mark(x+40,y+40,ok,a,56)
        xx=x+40; yy=y+130
        for i,p in enumerate(parts):
            pc=col if i%2 else LI; tw=c.d.textlength(p,font=F(46))
            if xx+tw>x+760: xx=x+40; yy+=60
            c.text((xx,yy),p,46,pc,a); xx+=tw
        c.text((x+40,y+270),note,24,MU,a,'r')
    tc(140,250,True,['THE ','WORLD CHAMPION ','','FORMULA 1 ','REJECTED'],'A champion, yet rejected. Both sides matter.',P(t,.4))
    tc(1000,250,False,['THE ','MECHANIC ','','TOYOTA ','REJECTED'],'A mechanic can be anyone.',P(t,1.4))
    tc(140,640,True,['HOW A ','FEARLESS ','ENGINEER…'],'The word names a human quality.',P(t,2.6))
    tc(1000,640,False,['…A ','LOOM MAKER\'S SON'],'A description triggers nothing.',P(t,3.4))
def s_shape(c,t,D):
    c.headline(t,'Keep the source\'s |shape|',y=140)
    src=['Every','Gun','With','A','Strange','Mechanism','Explained']; our=['Every','Engine','With','A','Strange','Mechanism','Explained']
    c.text((200,330),'SOURCE  ·  1.74M VIEWS',22,MU,P(t,.3),'m'); c.text((200,600),'OURS',22,CO,P(t,1.6),'m')
    x=200
    for i,(a1,b1) in enumerate(zip(src,our)):
        w=max(c.d.textlength(a1+' ',font=F(64)),c.d.textlength(b1+' ',font=F(64)))
        c.text((x,380),a1,64,LI,P(t,.4+i*.12),dy=20)
        sw=a1!=b1; c.text((x,650),b1,64,CO if sw else LI,P(t,1.7+i*.12),dy=20)
        if sw: c.box((x-10,640,x+w-10,730),None,P(t,2.6),10,outline=CO,ow=3)
        x+=w
    c.text((200,840),'SAME WORD ORDER · LENGTH · CAPITALS · PUNCTUATION',26,MU,P(t,3.0),'m')
    c.text((200,890),'UNCHECKED FACTS GO IN [BRACKETS]',26,MU,P(t,3.4),'m')
def s_fresh(c,t,D):
    c.headline(t,'Fresh |evidence|',y=160)
    y=560; c.d.line((200,y,1720,y),fill=mix(GR,1),width=4)
    c.text((1720,y+30),'TODAY',24,LI,P(t,.3),'m',anchor='ra')
    a=P(t,.6); c.box((1470,y-90,1720,y-10),CO,a,10); c.text((1595,y-70),'≤ 1 MONTH',30,BG,a,anchor='ma')
    c.para((1470,y+80),'titles, angles, thumbnails',26,260,LI,a,'r')
    a=P(t,1.4); c.box((720,y-90,1460,y-10),TE,a,10); c.text((1090,y-70),'≤ 6 MONTHS',30,BG,a,anchor='ma')
    c.para((1000,y+80),'reference channels',26,400,LI,a,'r')
    a=P(t,2.2); c.box((200,y-90,710,y-10),CARD,a,10,outline=GR); c.text((455,y-70),'OLDER',30,MU,a,anchor='ma')
    c.para((200,y+80),'legacy style name only',26,500,MU,a,'r')
    c.text((W//2,860),'EVERY NUMBER RE-CHECKED ON THE DAY',32,AM,P(t,3.0),'m',anchor='ma')
def s_check(c,t,D):
    c.headline(t,'Independent |check|',y=140)
    for i in range(3):
        a=P(t,.4+i*.3); x,y=300,330+i*190
        c.d.ellipse((x,y,x+140,y+140),fill=mix(CARD,a),outline=mix(TE,a),width=3); c.text((x+70,y+52),'SCOUT %d'%(i+1),22,TE,a,'m',anchor='ma')
        c.arrow(x+150,y+70,880,620,TE,P(t,1.3+i*.15),4)
    a=P(t,1.9); c.d.ellipse((880,520,1080,720),fill=mix((42,23,20),a),outline=mix(CO,a),width=4); c.text((980,600),'CRITIC',30,CO,a,'m',anchor='ma')
    a=P(t,2.5); c.arrow(1090,620,1300,620,CO,a); c.pill(1320,590,'VERDICT',LI,a)
    a=P(t,3.2); c.text((1320,360),'PROPOSER',34,MU,a); c.text((1320,410),'never approves its own idea',26,MU,a,'r'); c.d.line((1310,375,1560,375),fill=mix(CO,a),width=4)
    a=P(t,3.8); x=300
    for txt,col in [('OBSERVED',TE),('INFERRED',AM),('UNKNOWN',MU)]: x+=c.pill(x,920,txt,col,a,22)+20
def s_cars(c,t,D):
    c.headline(t,'Not only |cars|',y=180)
    chips=[('CARS',MU),('HISTORY',TE),('WARHAMMER',TE),('MIDDLE-EARTH',TE),('STAR WARS',TE),('BUSINESS',TE),('NATURE',TE),('SCIENCE',TE),('WWII',TE),('ANY NICHE WITH DEMAND',CO)]
    x,y=200,400
    for i,(n,col) in enumerate(chips):
        w=c.d.textlength(n,font=F(40))+60
        if x+w>1720: x=200; y+=120
        c.pill(x,y,n,col,P(t,.4+i*.22),40); x+=w+26
def s_card(c,t,D):
    c.headline(t,'The format |card|',y=100)
    a=P(t,.3); c.text((140,230),'A',40,CO,a); c.card('2ZS01obvQR0',200,230,560,'Every Gun With A Strange Mechanism Explained','1.74M VIEWS · 31K SUBS',a)
    a=P(t,1.0); c.text((140,640),'B',40,CO,a); c.pill(200,630,'WEAPONS',LI,a,30)
    a=P(t,1.5); c.text((140,760),'C',40,CO,a); c.para((200,760),'12 objects, one odd trait, about a minute each. Photo grid on the thumbnail.',30,560,LI,a,'r')
    c.text((900,230),'D · OTHER NICHES, TESTED',22,CO,P(t,2.0),'m')
    for i,g in enumerate(TG):
        a=P(t,2.3+i*.5); y=280+i*240; ok=g['verdict'].lower()=='open'; col=TE if ok else (AM if g['verdict'].lower()=='weak' else CO)
        c.box((900,y,1780,y+210),CARD,a,14,outline=col)
        if g['id']: c.pic(g['id'],915,y+15,320,180,a)
        c.para((1260,y+30),g['title'],28,500,LI,a)
        c.text((1260,y+150),g['verdict'].upper()+'  ·  TOP '+fmt(g['top']),22,col,a,'m')
def s_show(c,t,D):
    c.headline(t,'Show, don\'t |tell|',y=120)
    a=P(t,.3); c.card('mFiZG43v_4A',200,260,620,'Everyone Called Him an Idiot. He Got Richer Every Time.','986K VIEWS',a)
    c.text((900,270),'FRAMES FROM INSIDE THE VIDEO',22,TE,P(t,1.0),'m')
    for i in range(3):
        a=P(t,1.2+i*.3); c.pic('mFiZG43v_4A_f%d'%(i+1),900+i*300,320,280,158,a)
    c.text((900,540),'THUMBNAIL · TITLE · VIEWS · DATE',26,LI,P(t,2.2),'m')
    a=P(t,3.0); c.box((900,640,1740,760),(28,16,14),a,14,outline=(90,42,37)); c.mark(935,680,False,a,40); c.text((1000,672),'Text piles and raw reports',38,CO,a)
def s_run(c,t,D):
    c.headline(t,'The |run|',y=140)
    st=['KEEPS + NO-GO','FIND','VALIDATE','BEND + TEST','PACKAGE','SHOW']
    for i,s in enumerate(st):
        a=P(t,.3+i*.35); x=120+i*240; c.box((x,420,x+220,600),CARD,a,14,outline=GR)
        c.text((x+20,440),'0%d'%(i+1),22,MU,a,'m'); c.para((x+20,500),s,28,190,LI,a)
    a=P(t,2.6); c.box((1580,380,1820,640),CO,a,16); c.text((1700,440),'GATE',40,BG,a,'m',anchor='ma'); c.text((1700,550),'MICHAEL',30,BG,a,anchor='ma'); c.text((1700,590),'KEEPS',30,BG,a,anchor='ma')
    a=P(t,3.4); c.text((120,720),'AFTER A KEEP  ›  thumbnail + title in a YouTube feed mock  ›  style options  ›  film',30,MU,a,'r')
    c.text((120,800),'NEVER SHOW A KEEP TWICE',28,AM,P(t,4.0),'m')
def s_kills(c,t,D):
    c.headline(t,'What |kills| an idea',y=140)
    k=['Presenter on screen','Channel over 100K subs','One viral hit','No views this month','Dead crossing','Job title, no famous name','No tension','Shorts-only source','Celebrity footage']
    for i,n in enumerate(k):
        a=P(t,.3+i*.25); col_=i%3; row=i//3; x=140+col_*560; y=320+row*180
        c.box((x,y,x+530,y+140),(28,16,14),a,16,outline=(90,42,37)); c.mark(x+32,y+48,False,a,40); c.para((x+100,y+46),n,32,400,LI,a)
def s_wants(c,t,D):
    c.headline(t,'Formats he |wants|',y=140)
    k=['The Entire Map of … Explained','Your Life as …','What if X were in Y?','Every [variant] Explained','Timeline Explained','3D true-scale reveal','3D timelapse of a place']
    for i,n in enumerate(k):
        a=P(t,.3+i*.3); col_=i%2; row=i//2; x=140+col_*840; y=310+row*150
        c.box((x,y,x+800,y+120),(16,26,19),a,16,outline=(47,90,60)); c.mark(x+30,y+36,True,a,46); c.text((x+100,y+40),n,38,LI,a)
def s_loop(c,t,D):
    c.headline(t,'Feedback becomes a |rule|',y=160)
    cx,cy,R=W//2,620,230
    nodes=[('YOUR FEEDBACK',-90),('RULE IN THE SKILL',30),('NEXT ROUND',150)]
    for i,(n,ang) in enumerate(nodes):
        a=P(t,.4+i*.5); x=cx+R*math.cos(math.radians(ang)); y=cy+R*math.sin(math.radians(ang))
        c.pill(x-160,y-34,n,CO if i==0 else TE,a,28)
    a=P(t,2.0); c.d.arc((cx-R+40,cy-R+40,cx+R-40,cy+R-40),0,int(360*ease((t-2)/1.5)),fill=mix(MU,a),width=4)
    c.text((cx,cy-10),'no-go · michael-said · decisions',22,MU,P(t,2.4),'m',anchor='ma')
def s_outro(c,t,D):
    c.text((140,300),'YOUR',150,LI,P(t,.2),dy=40); c.text((140,460),'TURN',150,CO,P(t,.4),dy=40)
    c.text((150,700),'Reply with the scene number:',40,MU,P(t,1.0),'r')
    c.text((150,770),'"S07 wrong, because …"   or   "all good"',44,LI,P(t,1.5),'m')

SC=[('Niche bend',4,s_intro),('The method',7,s_method),('Packaging first',6,s_pack),('Other niches',7,s_niches),('The filter',7,s_filter),('Demand × saturation',6.5,s_matrix),('Test every bend',7,s_test),('Biggest subject',5.5,s_subject),('Tension',7,s_tension),("Source's shape",6,s_shape),('Freshness',5.5,s_fresh),('Independent check',6,s_check),('Not only cars',5.5,s_cars),('Format card',7,s_card),("Show, don't tell",5.5,s_show),('The run',6.5,s_run),('Kills an idea',5.5,s_kills),('Formats he wants',5.5,s_wants),('Feedback to rule',5,s_loop),('Your turn',5,s_outro)]
TOT=sum(s[1] for s in SC)

base=Image.new('RGB',(W,H),BG); bd=ImageDraw.Draw(base)
for x in range(0,W,80): bd.line((x,0,x,H),fill=(14,12,9))
for y in range(0,H,80): bd.line((0,y,W,y),fill=(14,12,9))

def frame(gt):
    acc=0
    for i,(name,dur,fn) in enumerate(SC):
        if gt<acc+dur or i==len(SC)-1: break
        acc+=dur
    t=gt-acc; img=base.copy(); c=Ctx(img)
    fn(c,t,dur)
    # chrome: scene id + progress
    c.box((60,40,60+150,40+56),CO,1,10); c.text((135,53),'S%02d'%(i+1),28,BG,1,'b',anchor='ma')
    c.text((230,56),name.upper(),24,MU,1,'m')
    x=60; tw=W-120
    for j,(n,d,_) in enumerate(SC):
        w=tw*d/TOT; col=CO if j<i else (LI if j==i else GR)
        c.d.rectangle((x+2,H-30,x+w-2,H-24),fill=col); x+=w
    # fade at scene edges
    fa=min(cl(t/0.25),cl((dur-t)/0.25)) if i>0 else cl((dur-t)/0.25)
    if fa<1: img=Image.blend(Image.new('RGB',(W,H),BG),img,fa)
    return img

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='sheet':
        acc=0; tiles=[]
        for i,(n,d,_) in enumerate(SC):
            tiles.append(frame(acc+d*0.85).resize((480,270))); acc+=d
        sh=Image.new('RGB',(480*4,270*5),BG)
        for k,tl in enumerate(tiles): sh.paste(tl,((k%4)*480,(k//4)*270))
        sh.save('/tmp/nbv/sheet.png'); print('sheet', TOT)
    else:
        out=sys.argv[2]; n=int(TOT*FPS)
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','%dx%d'%(W,H),'-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
        for k in range(n):
            p.stdin.write(frame(k/FPS).tobytes())
            if k%150==0: open('/tmp/nbv/progress','w').write('%d/%d'%(k,n))
        p.stdin.close(); p.wait(); open('/tmp/nbv/progress','w').write('DONE %d %s'%(n,out))
