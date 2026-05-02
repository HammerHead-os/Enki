(function(){
'use strict';
var drip=document.createElement('div');
drip.style.cssText='position:fixed;top:0;left:0;width:100%;height:80px;z-index:9990;pointer-events:none;background:url(assets/blood_drip.gif) top center/100% auto no-repeat;opacity:.6';
document.body.appendChild(drip);
var glitch=document.createElement('div');
glitch.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;z-index:9995;pointer-events:none;opacity:0;transition:opacity .05s;background:url(assets/glitch_overlay.gif) center/cover;mix-blend-mode:screen';
document.body.appendChild(glitch);
function triggerGlitch(){glitch.style.opacity='0.25';setTimeout(function(){glitch.style.opacity='0';},80+Math.random()*120);setTimeout(triggerGlitch,4000+Math.random()*8000);}
setTimeout(triggerGlitch,5000);
var jumpDone=false;
window.addEventListener('scroll',function(){if(jumpDone)return;if(window.scrollY/window.innerHeight>0.8){jumpDone=true;var f=document.createElement('div');f.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;z-index:99999;background:rgba(230,57,70,.7);display:flex;align-items:center;justify-content:center;pointer-events:none';var e=document.createElement('img');e.src='assets/blinking_eyes.gif';e.style.cssText='width:60vw;max-width:500px;filter:drop-shadow(0 0 60px rgba(255,0,0,.8))';f.appendChild(e);document.body.appendChild(f);setTimeout(function(){f.style.transition='opacity .3s';f.style.opacity='0';},250);setTimeout(function(){f.remove();},600);}},{passive:true});
var lastTrail=0;
document.addEventListener('mousemove',function(e){if(Date.now()-lastTrail<60)return;lastTrail=Date.now();var d=document.createElement('div');var s=4+Math.random()*6;d.style.cssText='position:fixed;left:'+(e.clientX-s/2)+'px;top:'+(e.clientY-s/2)+'px;width:'+s+'px;height:'+s+'px;border-radius:50%;background:#8b0000;pointer-events:none;z-index:9989;opacity:.6;transition:opacity 1.5s,transform 1.5s';document.body.appendChild(d);requestAnimationFrame(function(){d.style.opacity='0';d.style.transform='translateY(20px) scale(0.3)';});setTimeout(function(){d.remove();},1600);});
var shaken=false;var killStat=document.querySelector('[data-view="group-outcome"]');
if(killStat){new IntersectionObserver(function(entries){if(entries[0].isIntersecting&&!shaken){shaken=true;document.body.style.animation='horrorShake .4s ease';setTimeout(function(){document.body.style.animation='';},500);}},{threshold:0.5}).observe(killStat);}
var eyeSpots=[{top:'15%',left:'2%'},{top:'50%',right:'1%'},{bottom:'20%',left:'3%'},{top:'75%',right:'2%'}];
eyeSpots.forEach(function(pos){var el=document.createElement('img');el.src='assets/blinking_eyes_small.gif';el.style.cssText='position:fixed;width:80px;opacity:0;pointer-events:none;z-index:9988;transition:opacity 2s;background:transparent;border:none;outline:none;mix-blend-mode:lighten';if(pos.top)el.style.top=pos.top;if(pos.bottom)el.style.bottom=pos.bottom;if(pos.left)el.style.left=pos.left;if(pos.right)el.style.right=pos.right;document.body.appendChild(el);(function blink(eye){setTimeout(function(){eye.style.opacity='0.5';setTimeout(function(){eye.style.opacity='0';blink(eye);},2000+Math.random()*3000);},3000+Math.random()*10000);})(el);});
var whispers=['they know what you clicked','your data is being sold right now','the algorithm is watching','you are the product','there is no privacy','they killed the bills that protected you','73% of your rights... gone','big brother is watching','you cannot opt out','your face has been logged'];
function showWhisper(){var el=document.createElement('div');el.textContent=whispers[Math.floor(Math.random()*whispers.length)];el.style.cssText='position:fixed;z-index:9987;pointer-events:none;font-family:Creepster,cursive;color:rgba(230,57,70,.18);font-size:2.5rem;white-space:nowrap;transition:opacity 3s;opacity:0;top:'+(10+Math.random()*80)+'%;left:'+(5+Math.random()*70)+'%;transform:rotate('+(Math.random()*10-5)+'deg)';document.body.appendChild(el);requestAnimationFrame(function(){el.style.opacity='1';});setTimeout(function(){el.style.opacity='0';},3000);setTimeout(function(){el.remove();},6000);setTimeout(showWhisper,6000+Math.random()*10000);}
setTimeout(showWhisper,8000);
var scratches=document.createElement('div');
scratches.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9984;opacity:.06;background:url(assets/scratches.png) center/cover';
document.body.appendChild(scratches);
window.addEventListener('scroll',function(){var pct=window.scrollY/(document.body.scrollHeight-window.innerHeight);var r=Math.round(12+pct*16),g=Math.round(12-pct*8),b=Math.round(16-pct*10);document.body.style.backgroundColor='rgb('+r+','+g+','+b+')';},{passive:true});
var echoSec=document.getElementById('echoSection');var nShown=false;
var notifMsgs=['Your data was shared with 47 advertisers','Your location was accessed 12 times today','Face detected. Profile updated.','Emotional state: CONCERNED','Screen time today: 4h 32m'];
if(echoSec){new IntersectionObserver(function(e){if(e[0].isIntersecting&&!nShown){nShown=true;notifMsgs.forEach(function(msg,i){setTimeout(function(){var n=document.createElement('div');n.textContent=msg;n.style.cssText='position:fixed;right:-500px;top:'+(80+i*80)+'px;z-index:9991;background:#14141e;border:1px solid #e63946;border-radius:12px;padding:16px 22px;max-width:400px;font-family:Share Tech Mono,monospace;font-size:1.3rem;color:#b0b0c0;transition:right .6s cubic-bezier(.22,1,.36,1);box-shadow:0 4px 30px rgba(230,57,70,.25)';document.body.appendChild(n);requestAnimationFrame(function(){n.style.right='20px';});setTimeout(function(){n.style.right='-500px';},4000);setTimeout(function(){n.remove();},5000);},1500+i*2500);});}},{threshold:.2}).observe(echoSec);}
var style=document.createElement('style');
style.textContent='@keyframes horrorShake{0%,100%{transform:translate(0)}10%{transform:translate(-8px,4px)}20%{transform:translate(6px,-6px)}30%{transform:translate(-4px,8px)}40%{transform:translate(8px,-4px)}50%{transform:translate(-6px,6px)}60%{transform:translate(4px,-8px)}70%{transform:translate(-8px,4px)}80%{transform:translate(6px,-6px)}90%{transform:translate(-4px,8px)}}';
document.head.appendChild(style);
})();
