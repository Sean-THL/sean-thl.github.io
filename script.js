'use strict';
const toggle=document.querySelector('#theme-toggle');
function setTheme(theme){document.documentElement.dataset.theme=theme;if(toggle){toggle.setAttribute('aria-pressed',String(theme==='dark'));toggle.textContent=theme==='dark'?'Light mode':'Dark mode';}}
let saved;try{saved=localStorage.getItem('portfolio-theme')}catch{}
setTheme(saved||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));
if(toggle)toggle.addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';setTheme(theme);try{localStorage.setItem('portfolio-theme',theme)}catch{}});
