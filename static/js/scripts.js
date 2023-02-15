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
// 




// CAROUSEL 
let slideIndex = 0;
showSlides();
function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
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
    timer = setTimeout(showSlides, 3000);
}

function startTimer() {
    showSlides();
}

function pauseTimer() {
    clearInterval(timer);
}

const slideshow_container = document.querySelector(".slideshow-container");
slideshow_container.addEventListener("mouseover", pauseTimer);
slideshow_container.addEventListener("mouseout", startTimer);

// FIM CAROUSEL


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



////////////////////\\\\\\\\\\\\\\\\\\\\\\
//////////////// MOBILE \\\\\\\\\\\\\\\\\\
////////////////////\\\\\\\\\\\\\\\\\\\\\\



const mobile_search = document.querySelector("#mobile-search");
// SEARCH
mobile_search.addEventListener("focus", (event)=> {
    mobile_search.removeAttribute('placeholder')
    mobile_search.style.padding = "0px 20px 0px 28px"
    let button = document.querySelector(".mobile-search-form");
        button.classList.toggle("mobile-icon");
    let body = document.querySelector("body");
});

mobile_search.addEventListener("blur", (event)=> {
    mobile_search.setAttribute('placeholder', 'Procurar')
    mobile_search.style.padding = "0px 20px"
    let button = document.querySelector(".mobile-search-form");
        button.classList.toggle("mobile-icon");
});

//

// MENU
const menu_icon = document.querySelector("#mobile-menu");

menu_icon.addEventListener("click", (event)=> {
    console.log(678)
    let show_menu = document.querySelector(".menu-click");
    show_menu.classList.toggle("show-menu");
    
});

const close_menu = document.querySelector("#menu-close");
close_menu.addEventListener("click", (event)=> {
    let close_menu = document.querySelector(".menu-click");
    close_menu.classList.toggle("show-menu");
});










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