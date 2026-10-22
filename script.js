'use strict';
const toggle=document.querySelector('#theme-toggle');
function setTheme(theme){document.documentElement.dataset.theme=theme;if(toggle){toggle.setAttribute('aria-pressed',String(theme==='dark'));toggle.textContent=theme==='dark'?'Light mode':'Dark mode';}}
let saved;try{saved=localStorage.getItem('portfolio-theme')}catch{}
setTheme(saved||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));
if(toggle)toggle.addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';setTheme(theme);try{localStorage.setItem('portfolio-theme',theme)}catch{}});
const filters=document.querySelectorAll('[data-filter]');const rows=document.querySelectorAll('.project-row');
filters.forEach(b=>b.addEventListener('click',()=>{let count=0;filters.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));rows.forEach(row=>{row.hidden=b.dataset.filter!=='all'&&row.dataset.category!==b.dataset.filter;if(!row.hidden)count++});document.querySelector('#project-count').textContent=`${count} projects`;}));
