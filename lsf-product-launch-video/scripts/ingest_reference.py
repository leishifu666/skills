"""Probe a user-provided local reference and extract evidence; does not claim visual review."""
import argparse, hashlib, json, subprocess
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('input',type=Path)
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--source',default='user-supplied local video')
parser.add_argument('--start',type=float,default=0)
parser.add_argument('--end',type=float)
parser.add_argument('--fps',type=float,default=2)
args=parser.parse_args()
if not args.input.is_file():parser.error('Input file not found')
if args.out.exists() and any(args.out.iterdir()):parser.error('Use a new or empty evidence directory; existing evidence is not overwritten')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(args.input)],text=True,encoding='utf-8'))
duration=float(probe['format']['duration']);end=min(duration,args.end if args.end is not None else duration)
if not (0<=args.start<end and 0<args.fps<=120):parser.error('Invalid range or sampling rate')
if (end-args.start)*args.fps>3000:parser.error('More than 3000 frames; choose an overview rate or a shorter selected segment')
args.out.mkdir(parents=True,exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-i',str(args.input),'-vf',f'trim=start={args.start}:end={end},setpts=PTS-STARTPTS,fps={args.fps},scale=960:-2','-q:v','3',str(args.out/'frame-%05d.jpg')],check=True)
digest=hashlib.file_digest(args.input.open('rb'),'sha256').hexdigest()
metadata={'input':str(args.input.resolve()),'source':args.source,'sha256':digest,'probe':probe,'extractedRange':[args.start,end],'sampleFps':args.fps,'frameCount':len(list(args.out.glob('frame-*.jpg'))),'reviewStatus':'unreviewed','observations':[],'curveStatus':'unknown; measured or author-supplied evidence required','mediaUse':'local reference only; no publication or redistribution implied'}
(args.out/'evidence.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'directory':str(args.out.resolve()),'frames':metadata['frameCount'],'reviewStatus':'unreviewed'},ensure_ascii=False))
