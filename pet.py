"""Small local desktop player for the supplied atlas. No network access."""
import json, sys, tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

ROOT=Path(__file__).resolve().parent
def main():
    meta=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    atlas=Image.open(ROOT/meta['image']).convert('RGBA')
    root=tk.Tk(); root.title('Caleb Pet'); root.overrideredirect(True)
    root.attributes('-topmost',True); root.geometry('384x416+100+100')
    key='#ff00ff'; root.configure(bg=key)
    if sys.platform=='win32':root.attributes('-transparentcolor',key)
    label=tk.Label(root,bg=key,bd=0);label.pack()
    frames={}
    for state,spec in meta['states'].items():
        frames[state]=[ImageTk.PhotoImage(atlas.crop((i*192,spec['row']*208,(i+1)*192,(spec['row']+1)*208)).resize((384,416),Image.Resampling.LANCZOS)) for i in range(spec['frames'])]
    current=['idle',0]; offset=[0,0];menu=tk.Menu(root,tearoff=False)
    def select(name):current[:]=[name,0]
    for name in frames:menu.add_command(label=name,command=lambda n=name:select(n))
    menu.add_separator();menu.add_command(label='退出 / Quit',command=root.destroy)
    def begin(e):offset[:]=[e.x,e.y]
    def move(e):root.geometry(f'+{max(0,e.x_root-offset[0])}+{max(0,e.y_root-offset[1])}')
    label.bind('<Button-1>',begin);label.bind('<B1-Motion>',move)
    label.bind('<Button-3>',lambda e:menu.tk_popup(e.x_root,e.y_root));root.bind('<Escape>',lambda e:root.destroy())
    def tick():
        state,index=current;label.configure(image=frames[state][index]);delay=meta['states'][state]['durations'][index]
        current[1]=(index+1)%len(frames[state]);root.after(delay,tick)
    tick();root.mainloop()
if __name__=='__main__':main()
