/*
    Hints: 
    1. Attach click event handlers to all four of the 
       buttons (#default, #ocean, #desert, and #high-contrast).
    2. Modify the className property of the body tag 
       based on the button that was clicked.
*/
let changeColor = (color) => {
   document.querySelector('body').className = color
}

document.getElementById('default').addEventListener('click', changeColor);

document.getElementById('desert').addEventListener('click', function(){
   changeColor('desert')}
   );

document.getElementById('ocean').addEventListener('click', function(){
   changeColor('ocean')}
   );

document.getElementById('high-contrast').addEventListener('click', function(){
   changeColor('high-contrast')}
   );