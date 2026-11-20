'use strict';
const toggle=document.querySelector('#theme-toggle');
function setTheme(theme){document.documentElement.dataset.theme=theme;if(toggle){toggle.setAttribute('aria-pressed',String(theme==='dark'));toggle.textContent=theme==='dark'?'Light mode':'Dark mode';}}
let saved;try{saved=localStorage.getItem('portfolio-theme')}catch{}
setTheme(saved||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));
if(toggle)toggle.addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';setTheme(theme);try{localStorage.setItem('portfolio-theme',theme)}catch{}});
const filters=document.querySelectorAll('[data-filter]');const rows=document.querySelectorAll('.project-row');const projectCount=document.querySelector('#project-count');
filters.forEach(b=>b.addEventListener('click',()=>{let count=0;filters.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));rows.forEach(row=>{const categories=(row.dataset.categories||'').split(/\s+/);row.hidden=b.dataset.filter!=='all'&&!categories.includes(b.dataset.filter);if(!row.hidden)count++});if(projectCount)projectCount.textContent=`${count} ${count===1?'project':'projects'}`;}));

const placesSection=document.querySelector('.places-lived');
if(placesSection){
  const pins=[...placesSection.querySelectorAll('[data-place]')];
  const placeButtons=[...placesSection.querySelectorAll('[data-place-select]')];
  const popup=placesSection.querySelector('.map-popup');
  const animationToggle=placesSection.querySelector('.map-animation-toggle');
  const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
  let current=0,timer=null,visible=false,paused=reducedMotion.matches;
  function showPlace(index){
    current=index;
    pins.forEach((pin,i)=>{pin.classList.toggle('is-active',i===index);pin.setAttribute('aria-pressed',String(i===index));});
    placeButtons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
    const pin=pins[index];
    popup.hidden=false;
    popup.style.left=`${Math.max(18,Math.min(82,Number(pin.dataset.x)))}%`;
    popup.style.top=`${pin.dataset.y}%`;
    popup.querySelector('strong').textContent=pin.dataset.city;
    popup.querySelector('span').textContent=pin.dataset.country;
  }
  function updateTimer(){
    clearInterval(timer);timer=null;
    animationToggle.textContent=paused?'Play map animation':'Pause map animation';
    if(visible&&!paused)timer=setInterval(()=>showPlace((current+1)%pins.length),2600);
  }
  function selectPlace(index){paused=true;showPlace(index);updateTimer();}
  pins.forEach((pin,i)=>{
    pin.addEventListener('click',()=>selectPlace(i));
    pin.addEventListener('pointerenter',()=>selectPlace(i));
    pin.addEventListener('focus',()=>selectPlace(i));
    pin.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();selectPlace(i);}});
  });
  placeButtons.forEach((button,i)=>button.addEventListener('click',()=>selectPlace(i)));
  animationToggle.hidden=false;
  animationToggle.addEventListener('click',()=>{paused=!paused;updateTimer();});
  reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches)paused=true;updateTimer();});
  showPlace(0);
  if('IntersectionObserver' in window){
    new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)placesSection.classList.add('map-started');updateTimer();},{threshold:.15}).observe(placesSection);
  }else{visible=true;placesSection.classList.add('map-started');updateTimer();}
  document.addEventListener('visibilitychange',()=>{if(document.hidden){clearInterval(timer);timer=null;}else updateTimer();});
}
