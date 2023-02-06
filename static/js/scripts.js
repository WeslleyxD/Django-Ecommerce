function teste_onfocus() {
    let funfapls = document.querySelector('.search-form');
    if (funfapls.classList.contains('search-form')) {
        funfapls.removeAttribute('placeholder', '');
        funfapls.setAttribute('class', 'icon')

        // funfapls.style.backgroundColor = 'red';
        console.log(1)
    } else {
        console.log(2)
    }
    console.dir(funfapls)
    console.log('ok')
}

// function mascara_cpf(){
//     var cpf = document.getElementById('id_cep')
//     if (cpf.value.length == 3 || cpf.value.length == 7) {
//         cpf.value += "."
//     } else if (cpf.value.length == 11) {
//         cpf.value += "."
//     }
// }

// function mascara_cep() {
//     var cep = document.getElementById('id_cep')
//     if (cep.value.length == 5) {
//         cep.value += "-"
//     }
// }





// const images = document.querySelectorAll(".carousel img");
// let current = 0;

// console.log(images)

// setInterval(() => {
//   images[current].classList.remove("active");
//   current = (current + 1) % images.length;
//   images[current].classList.add("active");
// }, 3000);



// const input = document.querySelector("input");
// const placeholder = document.querySelector(".placeholder");

// input.addEventListener("focus", function () {
//   placeholder.classList.add("focus");
// });

// input.addEventListener("blur", function () {
//   placeholder.classList.remove("focus");
// });