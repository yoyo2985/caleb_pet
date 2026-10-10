"""Check atlas integrity and optionally export its populated cells."""
from pathlib import Path
import argparse, hashlib, json
from PIL import Image
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--export',type=Path);args=p.parse_args()
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));path=root/m['image']
assert hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256'],'Atlas hash mismatch'
image=Image.open(path);assert image.mode=='RGBA';assert image.size==(1536,2288)
used=set();count=0
for state,s in m['states'].items():
 assert len(s['durations'])==s['frames'] and all(t>0 for t in s['durations'])
 assert 0<=s['row']<9 and 1<=s['frames']<=8
 for col in range(s['frames']):used.add((s['row'],col))
for row in [9,10]:
 for col in range(8):used.add((row,col))
for row in range(11):
 for col in range(8):
  cell=image.crop((col*192,row*208,(col+1)*192,(row+1)*208))
  if (row,col) in used:
   assert cell.getchannel('A').getbbox(),f'Empty frame {row},{col}';count+=1
   if args.export:
    args.export.mkdir(parents=True,exist_ok=True);cell.save(args.export/f'row-{row:02}-frame-{col:02}.png')
  else:assert cell.getchannel('A').getbbox() is None,f'Unused cell occupied {row},{col}'
assert count==73
print('PASS: RGBA atlas, matching SHA-256, 73 frames, 15 transparent unused cells.')
