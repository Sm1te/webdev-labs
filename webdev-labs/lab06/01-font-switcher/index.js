let cur_font = 1;


const makeBigger = () => {
   cur_font += 0.3
   setFont()
};

const makeSmaller = () => {
   cur_font -= 0.3
   setFont()
};

const setFont = () =>{
   document.querySelector('.content').style.fontSize = `${cur_font}em`;
   document.querySelector('.h1').style.fontSize = `${cur_font}em`;
}

document.querySelector('#a1').addEventListener('click', makeBigger);
document.querySelector('#a2').addEventListener('click', makeSmaller);

