from pathlib import Path
import json, base64, urllib.request
import numpy as np
import trimesh

OUT=Path(__file__).parent
scene=trimesh.Scene()
parts=[]
colors={'wall':'#efe6d2','roof':'#ad533c','trim':'#faf3e4','glass':'#54848e','wood':'#71503b','ground':'#91a17a','path':'#d1c6b2','plant':'#54734a','dark':'#394a3e'}
def add(name, mesh, color):
    rgb=bytes.fromhex(color.lstrip('#'))
    mesh.visual=trimesh.visual.ColorVisuals(mesh=mesh,face_colors=list(rgb)+[255])
    scene.add_geometry(mesh,node_name=name,geom_name=name)
    parts.append({'name':name,'v':mesh.vertices.tolist(),'f':mesh.faces.tolist(),'color':color})
def box(name,pos,size,color):
    mesh=trimesh.creation.box(extents=size)
    mesh.apply_translation(pos)
    add(name,mesh,colors.get(color,color))
def roof(name,cx,cz,width,depth,base,peak):
    x=width/2; z=depth/2
    v=np.array([[-x,base,-z],[x,base,-z],[0,peak,-z],[-x,base,z],[x,base,z],[0,peak,z]])+[cx,0,cz]
    f=[[0,2,1],[3,4,5],[0,1,4],[0,4,3],[0,3,5],[0,5,2],[1,2,5],[1,5,4]]
    m=trimesh.Trimesh(vertices=v,faces=f); m.fix_normals(); add(name,m,colors['roof'])
box('Garden base',[0,-.22,0],[13,.4,12],'ground')
box('Foundation',[0,.13,0],[8.4,.3,6.4],'path')
box('Cream walls',[0,1.85,0],[8,3.4,6],'wall')
box('Front fascia',[0,3.5,3.12],[8.55,.2,.2],'trim')
box('Back fascia',[0,3.5,-3.12],[8.55,.2,.2],'trim')
roof('Main terracotta roof',0,0,8.8,6.8,3.58,5.35)
box('Front door',[0,1.34,3.05],[1.18,2.34,.12],'wood')
box('Door glass',[0,1.7,3.12],[.72,.85,.025],'glass')
box('Door handle',[.43,1.17,3.15],[.055,.2,.07],'trim')
def window(name,x,z,side=False):
    w=1.6; h=1.35; y=2.05
    def b(s,dx,dy,dz,sx,sy,sz,c):
        if side: box(name+s,[x+dz,y+dy,z+dx],[sz,sy,sx],c)
        else: box(name+s,[x+dx,y+dy,z+dz],[sx,sy,sz],c)
    b(' surround',0,0,0,w+.2,h+.2,.12,'trim')
    b(' glass',0,0,.075,w,h,.04,'glass')
    b(' vertical mullion',0,0,.11,.065,h,.045,'trim')
    b(' horizontal mullion',0,0,.11,w,.065,.045,'trim')
    b(' sill',0,-h/2-.1,.08,w+.35,.12,.3,'trim')
for x in [-2.45,2.45]: window('Front window '+str(x),x,3.06)
for z in [-1.5,1.4]: window('East window '+str(z),4.06,z,True)
# Back and west windows face outward via mirrored complete meshes.
start=len(parts)
for x in [-2.45,2.45]: window('Back window '+str(x),x,3.06)
for part in parts[start:]:
    m=scene.geometry[part['name']]; m.vertices[:,2]*=-1; m.invert(); part['v']=m.vertices.tolist(); part['f']=m.faces.tolist()
box('Porch platform',[0,.22,4.05],[3.65,.4,2.0],'path')
box('Porch step',[0,.08,5.22],[2.25,.16,.5],'path')
box('Walkway',[0,.003,5.72],[1.65,.045,.55],'path')
for x in [-1.55,1.55]:
    box('Porch post '+str(x),[x,1.67,4.65],[.16,2.9,.16],'trim')
    box('Post foot '+str(x),[x,.56,4.65],[.27,.28,.27],'trim')
roof('Porch roof',0,3.98,3.85,2.3,3.05,3.85)
box('Porch fascia',[0,3.03,5.15],[3.86,.16,.16],'trim')
box('Chimney',[-2.35,4.55,-1.5],[.68,1.9,.7],'wall')
box('Chimney cap',[-2.35,5.53,-1.5],[.84,.16,.86],'dark')
for i,(x,z) in enumerate([(-3,3.7),(3,3.7),(-4.8,-2),(4.9,-2.8)]):
    m=trimesh.creation.icosphere(subdivisions=1,radius=.66); m.apply_scale([1,.8,1]); m.apply_translation([x,.48,z]); add('Garden shrub '+str(i),m,colors['plant'])
box('Tree trunk',[-5,.8,1],[.22,1.6,.22],'wood')
for i,(y,r) in enumerate([(1.65,1.0),(2.25,.8),(2.85,.6)]):
    m=trimesh.creation.icosphere(subdivisions=1,radius=r); m.apply_translation([-5,y,1]); add('Tree foliage '+str(i),m,colors['plant'])
scene.metadata={'description':'Simple single-storey house exterior concept. Y up; dimensions in metres. Not construction drawings.'}
glb=scene.export(file_type='glb'); (OUT/'Simple House.glb').write_bytes(glb)
assert all(m.is_watertight for m in scene.geometry.values())
reloaded=trimesh.load(OUT/'Simple House.glb',force='scene')
assert len(reloaded.geometry)==len(parts)
three=urllib.request.urlopen('https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js',timeout=60).read().decode()
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Simple House · 3D model</title>
<style>
*{box-sizing:border-box} .house-app{width:min(100%,1000px);color:var(--foreground,#27372e)} header{padding:18px 18px 10px;display:flex;justify-content:space-between;align-items:center;gap:16px}h1{font-size:21px;font-weight:600;margin:0 0 4px}p{font-size:13px;color:var(--muted-foreground,#627066);margin:0}#view{position:relative;width:100%;height:470px;border-radius:12px;overflow:hidden;background:#e9ede5;touch-action:none}canvas{display:block;width:100%;height:100%;cursor:grab}canvas:active{cursor:grabbing}.controls{display:flex;gap:8px;flex-wrap:wrap;padding:12px 18px}button,a{font:inherit;font-size:13px;min-height:44px;padding:10px 15px;border:1px solid var(--border,#c8d0c5);background:var(--card,#f7f8f4);color:inherit;border-radius:7px;cursor:pointer;text-decoration:none}button:hover,a:hover{border-color:#718976}button:focus-visible,a:focus-visible{outline:2px solid #4c7861;outline-offset:2px}#hint{position:absolute;bottom:14px;left:18px;color:#4d6050;font:12px sans-serif;pointer-events:none}footer{padding:0 18px 14px;color:var(--muted-foreground,#647065);font-size:12px}@media(max-width:540px){header{align-items:flex-start}#view{height:380px}h1{font-size:19px}}
</style><div class="house-app"><header><div><h1>Simple House</h1><p>Single-storey cottage · exterior model</p></div><a id="download" download="Simple House.glb">Download 3D model</a></header><div id="view"><div id="hint">Drag to rotate · Scroll or pinch to zoom</div></div><div class="controls"><button id="reset">Reset view</button><button id="front">Front view</button><button id="spin" aria-pressed="false">Auto-rotate: off</button></div><footer>Concept model only — not a construction plan. GLB opens in Blender and other 3D tools.</footer></div>
<script>THREE_SOURCE</script><script>
const parts=MODEL_DATA;
const glb='GLB_DATA';
const bytes=Uint8Array.from(atob(glb),c=>c.charCodeAt(0));document.querySelector('#download').href=URL.createObjectURL(new Blob([bytes],{type:'model/gltf-binary'}));
const host=document.querySelector('#view'),scene=new THREE.Scene();
const camera=new THREE.OrthographicCamera(-10,10,8,-8,.1,150);
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputEncoding=THREE.sRGBEncoding;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;host.prepend(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xffffff,0x747b65,.85));const sun=new THREE.DirectionalLight(0xfff2d8,.9);sun.position.set(-6,13,7);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-12,right:12,top:12,bottom:-12,near:.5,far:40});sun.shadow.normalBias=.025;scene.add(sun);
for(const p of parts){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p.v.flat(),3));g.setIndex(p.f.flat());g.computeVertexNormals();const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:p.color,roughness:.86,flatShading:true}));m.name=p.name;m.castShadow=true;m.receiveShadow=true;scene.add(m);}
let theta=.72,phi=1.08,scale=10,spin=false;const target=new THREE.Vector3(0,1.5,0);
function resize(){const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);const aspect=w/h;camera.left=-scale*aspect;camera.right=scale*aspect;camera.top=scale;camera.bottom=-scale;camera.updateProjectionMatrix()}
function position(){camera.position.set(25*Math.sin(phi)*Math.sin(theta),25*Math.cos(phi)+1.5,25*Math.sin(phi)*Math.cos(theta));camera.lookAt(target)}
function reset(){theta=.72;phi=1.08;scale=host.clientWidth<550?10.5:7.8;resize();position()}
const pointers=new Map();let pinch=0;
host.addEventListener('pointerdown',e=>{host.setPointerCapture(e.pointerId);pointers.set(e.pointerId,[e.clientX,e.clientY]);if(pointers.size===2){const [a,b]=[...pointers.values()];pinch=Math.hypot(a[0]-b[0],a[1]-b[1]);}});
host.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;const old=pointers.get(e.pointerId);pointers.set(e.pointerId,[e.clientX,e.clientY]);if(pointers.size===1){theta-=(e.clientX-old[0])*.009;phi=Math.max(.18,Math.min(1.48,phi+(e.clientY-old[1])*.007));}else{const[a,b]=[...pointers.values()],d=Math.hypot(a[0]-b[0],a[1]-b[1]);if(pinch&&d){scale=Math.max(4,Math.min(17,scale*pinch/d));resize();}pinch=d;}position()});
for(const event of ['pointerup','pointercancel','lostpointercapture'])host.addEventListener(event,e=>pointers.delete(e.pointerId));
host.addEventListener('wheel',e=>{e.preventDefault();scale=Math.max(4,Math.min(17,scale*Math.exp(e.deltaY*.001)));resize()},{passive:false});
document.querySelector('#reset').onclick=reset;document.querySelector('#front').onclick=()=>{theta=0;phi=Math.PI/2;position()};document.querySelector('#spin').onclick=e=>{spin=!spin;e.target.textContent='Auto-rotate: '+(spin?'on':'off');e.target.setAttribute('aria-pressed',String(spin))};
new ResizeObserver(resize).observe(host);reset();let last=0;
function frame(t){requestAnimationFrame(frame);if(spin){theta+=Math.min((t-last)/1000,.05)*.24;position()}last=t;renderer.render(scene,camera)}requestAnimationFrame(frame);
window.houseTest={parts:parts.length,renderer,scene,camera,getState:()=>({theta,phi,scale,spin})};
</script></html>'''
html=html.replace('THREE_SOURCE',three).replace('MODEL_DATA',json.dumps(parts,separators=(',',':'))).replace('GLB_DATA',base64.b64encode(glb).decode())
(OUT/'Simple House.html').write_text(html,encoding='utf-8')
print(json.dumps({'parts':len(parts),'glb_bytes':len(glb),'bounds':scene.bounds.tolist(),'all_parts_watertight':True,'glb_reload':'passed','html':str(OUT/'Simple House.html')}))
