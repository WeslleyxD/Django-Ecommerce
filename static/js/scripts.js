// function teste_onfocus() {
//     let funfapls = document.querySelector('.search-form');
//     if (funfapls.classList.contains('search-form')) {
//         funfapls.removeAttribute('placeholder', '');
//         funfapls.setAttribute('class', 'icon')

//         // funfapls.style.backgroundColor = 'red';
//         console.log(1)
//     } else {
//         console.log(2)
//     }
//     console.dir(funfapls)
//     console.log('ok')
// }


// let button = document.querySelector(".search-form");
// this.addEventListener("focus", (e) => {
//     button.setAttribute('class', 'icon')
//     let search = document.querySelector("#search");
//     search.removeAttribute('placeholder')
// })


const search = document.querySelector("#search");

// SEARCH INPUT //

search.addEventListener("focus", (event)=> {
    search.removeAttribute('placeholder')
    console.log(event)
    search.style.padding = "0px 20px 0px 50px"
    let button = document.querySelector(".search-form");
        button.classList.toggle("icon");
});

search.addEventListener("blur", (event)=> {
    search.setAttribute('placeholder', 'Procurar')
    search.style.padding = "0px 20px"
    let button = document.querySelector(".search-form");
        button.classList.toggle("icon");
});

// ---







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