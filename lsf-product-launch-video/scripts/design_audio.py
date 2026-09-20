"""Original event-led sound design: no borrowed reference audio, no looping arpeggio."""
import json, wave, argparse
from validate_plan import validate
from pathlib import Path
import numpy as np
parser=argparse.ArgumentParser(description='Original event-led sound design')
parser.add_argument('plan',type=Path)
parser.add_argument('output',type=Path)
parser.add_argument('--motion',type=Path)
args=parser.parse_args()
plan=json.loads(args.plan.read_text(encoding='utf-8-sig'))
errors=validate(plan)
if errors: raise SystemExit('; '.join(errors))
motion=json.loads(args.motion.read_text(encoding='utf-8')) if args.motion else None
if motion is not None and (len(motion)!=plan['durationFrames'] or not all(isinstance(x.get('pos'),(int,float)) and 0<=x['pos']<=100 for x in motion)):
    raise SystemExit('motion must have one bounded numeric pos per frame')
args.output.parent.mkdir(parents=True,exist_ok=True)
sr=48000
mix=np.zeros((round(plan['durationFrames']/plan['fps']*sr),2))
rng=np.random.default_rng(20260919)
def smooth(noise,width):
    return np.convolve(noise,np.ones(width)/width,mode='same')
def sound(kind,duration,index):
    kind={'click':'tap','swish':'sweep','thump':'soft','chime':'resolve'}.get(kind,kind)
    t=np.arange(round(duration*sr))/sr;u=t/duration
    noise=rng.normal(0,1,len(t));tail=np.exp(-t*9/max(.5,duration))
    if kind=='tap':
        # Small wooden contact + high air transient; every contact has a different pitch.
        hz=660+index*37
        x=.6*np.sin(2*np.pi*hz*t)*np.exp(-t*85)+.36*noise*np.exp(-t*170)
    elif kind=='connect':
        hz=740 if index%2 else 990
        x=(np.sin(2*np.pi*hz*t)+.24*np.sin(2*np.pi*hz*2.03*t))*np.exp(-t*32)
    elif kind in ('air','sweep','rise','drag'):
        band=smooth(noise,7)-smooth(noise,80)
        phase=2*np.pi*(90*t+(550 if kind=='rise' else -30)*t*t/max(duration,.1))
        envelope=np.sin(np.pi*u)**(1.6 if kind=='drag' else 2.5)
        x=band*envelope*1.2+np.sin(phase)*envelope*.09
    elif kind=='type':
        x=np.zeros(len(t))
        for j,p in enumerate([.03,.115,.23,.28,.435,.59,.64,.83,.95]):
            dt=t-p*duration;on=dt>=0
            x+=on*(np.sin(2*np.pi*(780+j*79)*dt)*.26+noise*.12)*np.exp(-np.maximum(dt,0)*180)
    elif kind in ('bloom','resolve'):
        x=np.zeros(len(t))
        for j,hz in enumerate([261.63,392,523.25] if kind=='bloom' else [392,587.33,783.99]):
            dt=np.maximum(t-j*.065,0)
            env=(t>=j*.065)*(1-np.exp(-dt*80))*np.exp(-dt*(4+j))
            x+=(np.sin(2*np.pi*hz*dt)+.16*np.sin(2*np.pi*hz*2.006*dt))*env*.38
        x+=smooth(noise,40)*np.sin(np.pi*u)**2*.2
    else:
        phase=2*np.pi*(72*t+30*(1-np.exp(-t*14))/14)
        x=np.sin(phase)*np.exp(-t*17)+smooth(noise,25)*np.exp(-t*28)*.22
    edge=np.minimum(1,t/.003)*np.minimum(1,(duration-t)/.03)
    return x*edge

cue_report=[]
for i,e in enumerate(plan['events']):
    start=e['frame']/plan['fps'];d=max(.13,e['durationFrames']/plan['fps'])
    if e['kind'] in ('resolve','bloom'):d=max(d,1.3)
    x=sound(e['kind'],d,i)*e['gain']
    pan=np.full(len(x),e['pan'])
    if e['kind'] in ('sweep','rise','air'):pan=np.linspace(-.35,.35,len(x))*(1 if e['pan']>=0 else -1)
    if e['kind']=='drag' and motion is not None:
        frames=np.arange(e['frame'],min(len(motion),e['frame']+e['durationFrames']+1))
        pos=np.array([motion[int(f)]['pos'] for f in frames])
        velocity=np.abs(np.gradient(pos)) if len(pos)>1 else np.zeros(len(pos));velocity/=max(.001,velocity.max())
        x*=np.interp(np.linspace(frames[0],frames[-1],len(x)),frames,velocity)
        pan=np.interp(np.linspace(frames[0],frames[-1],len(x)),frames,(pos-50)/90)
    stereo=x[:,None]*np.stack([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)],axis=1)
    first=round(start*sr);n=min(len(stereo),len(mix)-first);mix[first:first+n]+=stereo[:n]
    # Short, quiet room tail on tonal events, rather than a hard digital stop.
    if e['kind'] in ('connect','bloom','resolve','soft'):
        for delay,g in [(0.053,.14),(.089,.09),(.137,.055)]:
            a=first+round(delay*sr);n=min(len(stereo),len(mix)-a)
            if n>0:mix[a:a+n]+=stereo[:n,::-1]*g
    cue_report.append({'id':e['id'],'atSeconds':start,'kind':e['kind'],'durationSeconds':d})
# Quiet sustained harmonic beds only in motion passages, with a deliberate gap at comparison.
for bed in plan.get('beds',[]):
    a,b,hz=bed['start'],bed['end'],bed['frequency']
    if not 0<=a<b<=len(mix)/sr or not 30<=hz<=2000: raise SystemExit('bed bounds or frequency invalid')
    n=round((b-a)*sr);t=np.arange(n)/sr;env=np.minimum(1,t/.7)*np.minimum(1,(b-a-t)/.8)
    pad=(np.sin(2*np.pi*hz*t)+.38*np.sin(2*np.pi*hz*1.5*t)+.16*np.sin(2*np.pi*hz*2*t))*env*.022
    start=round(a*sr);mix[start:start+n]+=pad[:,None]
peak=float(np.abs(mix).max());mix*=min(1,10**(-4/20)/max(peak,1e-9))
with wave.open(str(args.output),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
args.output.with_suffix('.audio-events.json').write_text(json.dumps({'samplePeakDbFS':20*np.log10(max(np.abs(mix).max(),1e-9)),'listeningReview':False,'source':'Original deterministic synthesis','events':cue_report},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(mix)/sr:g}s stereo; {len(cue_report)} designed events')
