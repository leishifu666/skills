// Original parameterised recipes. They do not reconstruct proprietary source curves.
export const restToRest = p => p*p*p*(p*(p*6-15)+10);
export function focusReadRelease(gsap,camera,{focus,scale=1.6,travel=1.1,hold=2,screen={x:960,y:540},rest={s:1,x:0,y:0}}){
 const tl=gsap.timeline();tl.addLabel('focus',0).to(camera,{s:scale,x:screen.x-focus.x*scale,y:screen.y-focus.y*scale,duration:travel,ease:restToRest},0).addLabel('read',travel).to(camera,{...rest,duration:travel,ease:restToRest},travel+hold).addLabel('released');return tl;
}
export function sameObjectHandoff(gsap,carrier,{from,to,duration=.85}){
 // The caller must retain image identity, crop and object-fit while moving this carrier.
 const tl=gsap.timeline();tl.set(carrier,{...from},0).to(carrier,{...to,duration,ease:restToRest},0);return tl;
}
export function directionalLayerPass(gsap,objects,{distance=600,duration=.9,stagger=.12,direction=-1}){
 const tl=gsap.timeline();objects.forEach((item,i)=>tl.fromTo(item,{x:item.x-direction*distance,opacity:0},{x:item.x,opacity:1,duration,ease:'power2.inOut'},i*stagger));return tl;
}
