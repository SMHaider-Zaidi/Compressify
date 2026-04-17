// Get compression duration 
const result_div = document.querySelector('.loading_div');

const duration = (result_div.dataset.duration)* 1000;

const waitTime = duration + 1000;

setTimeout(()=>{
    window.location.href='/result';
}, waitTime);

