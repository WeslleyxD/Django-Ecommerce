// CAROUSEL MANUAL

const productContainers = [...document.querySelectorAll('.product-container')];
const nxtBtn = [...document.querySelectorAll('.nxt-btn')];
const preBtn = [...document.querySelectorAll('.pre-btn')];

productContainers.forEach((item, i) => {
    let containerDimensions = item.getBoundingClientRect();
    let containerWidth = containerDimensions.width;

    nxtBtn[i].addEventListener('click', () => {
        item.scrollLeft += containerWidth;
    })

    preBtn[i].addEventListener('click', () => {
        item.scrollLeft -= containerWidth;
    })
})
// FIM DO CAROUSEL MANUAL



// CAROUSEL AUTOMÁTICO
let mouseEmCima = false;
const slideshowContainer = document.querySelector(".slideshow-container");

if (slideshowContainer) {
    slideshowContainer.addEventListener("mouseover", () => {mouseEmCima = true});
    slideshowContainer.addEventListener("mouseout", () => {mouseEmCima = false});

    slideIndex = 0
    setInterval(() => {
        if(!mouseEmCima) {
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");

        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
            console.log (11)
        }
        slideIndex++;
        if (slideIndex > slides.length) {
            slideIndex = 1
        }
        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace("active", "");
        }
        slides[slideIndex-1].style.display = "block";  
        dots[slideIndex-1].className += " active";
        }
    }, 1000);
}

// FIM DO CAROUSEL AUTOMATICO


// SEARCH INPUT //

const search = document.querySelector("#search");

search.addEventListener("focus", (event)=> {
    search.removeAttribute('placeholder')
    search.style.padding = "0px 20px 0px 50px"
    let button = document.querySelector(".search-form");
        button.classList.toggle("icon");
    let body = document.querySelector("body");
});

search.addEventListener("blur", (event)=> {
    search.setAttribute('placeholder', 'Procurar')
    search.style.padding = "0px 20px"
    let button = document.querySelector(".search-form");
        button.classList.toggle("icon");
});

/// FIM SEARCH INPUT


////////////////////\\\\\\\\\\\\\\\\\\\\\\
//////////////// MOBILE \\\\\\\\\\\\\\\\\\
////////////////////\\\\\\\\\\\\\\\\\\\\\\


// SEARCH INPUT

const mobileSearch = document.querySelector("#mobile-search");

mobileSearch.addEventListener("focus", (event)=> {
    mobileSearch.removeAttribute('placeholder')
    mobileSearch.style.padding = "0px 20px 0px 28px"
    let button = document.querySelector(".mobile-search-form");
        button.classList.toggle("mobile-icon");
    let body = document.querySelector("body");
});

mobileSearch.addEventListener("blur", (event)=> {
    mobileSearch.setAttribute('placeholder', 'Procurar')
    mobileSearch.style.padding = "0px 20px"
    let button = document.querySelector(".mobile-search-form");
        button.classList.toggle("mobile-icon");
});

// SEARCH INPUT

// MENU

const menuIcon = document.querySelector("#mobile-menu");

menuIcon.addEventListener("click", (event)=> {
    console.log(678)
    let show_menu = document.querySelector(".menu-click");
    show_menu.classList.toggle("show-menu");
    
});

const closeMenu = document.querySelector("#menu-close");
closeMenu.addEventListener("click", (event)=> {
    let closeMenu = document.querySelector(".menu-click");
    closeMenu.classList.toggle("show-menu");
});

// FIM MENU







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