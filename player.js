'use strict';
const m=window.PET_MANIFEST, canvas=document.getElementById('pet'), ctx=canvas.getContext('2d');
const selector=document.getElementById('state'), gazeButton=document.getElementById('gaze');
const labels=['待机','向右跑','向左跑','挥手','敬礼','失败','等待','思考','检查'];
Object.keys(m.states).forEach((key,i)=>{const option=document.createElement('option');option.value=key;option.textContent=labels[i];selector.append(option);});
let frame=0,elapsed=0,last=0,gaze=false,direction=0,drag=null,hoverSalute=false;
const image=new Image();image.src=m.image;
image.onerror=()=>document.getElementById('status').textContent='素材加载失败，请保持 assets 文件夹和 index.html 在同一项目内。';
selector.onchange=()=>{frame=0;elapsed=0;hoverSalute=false;};
canvas.onpointerenter=()=>{if(!drag){selector.value='jumping';frame=0;elapsed=0;hoverSalute=true;}};
gazeButton.onclick=()=>{gaze=!gaze;gazeButton.textContent=gaze?'关闭视线跟随':'开启视线跟随';gazeButton.setAttribute('aria-pressed',String(gaze));};
canvas.onpointerdown=e=>{const box=canvas.getBoundingClientRect();drag={x:e.clientX-box.left,y:e.clientY-box.top};canvas.setPointerCapture(e.pointerId);};
canvas.onpointerup=()=>{drag=null;};canvas.onpointercancel=()=>{drag=null;};
window.addEventListener('pointermove',e=>{const box=canvas.getBoundingClientRect();direction=(Math.round(Math.atan2(e.clientX-(box.left+box.width/2),-(e.clientY-(box.top+box.height/2)))*8/Math.PI)+16)%16;if(drag){const stage=document.getElementById('stage').getBoundingClientRect();canvas.style.left=Math.max(-box.width/2,Math.min(stage.width-box.width/2,e.clientX-stage.left-drag.x))+'px';canvas.style.top=Math.max(-box.height/2,Math.min(stage.height-box.height/2,e.clientY-stage.top-drag.y))+'px';}});
function tick(now){let state=m.states[selector.value];elapsed+=Math.min(now-last,100);last=now;while(elapsed>=state.durations[frame]){elapsed-=state.durations[frame];frame=(frame+1)%state.frames;if(frame===0&&hoverSalute){hoverSalute=false;selector.value='idle';state=m.states.idle;elapsed=0;break;}}const looking=gaze&&!hoverSalute;const row=looking?9+Math.floor(direction/8):state.row,col=looking?direction%8:frame;ctx.clearRect(0,0,192,208);ctx.drawImage(image,col*192,row*208,192,208,0,0,192,208);requestAnimationFrame(tick);}
image.onload=()=>{document.getElementById('status').textContent='素材已加载 · 9 种动作 / 16 个视线方向';requestAnimationFrame(tick);};
