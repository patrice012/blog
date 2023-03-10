// toggle to shwo the nav link

const navLink = document.querySelector(".nav__link");
const box = document.querySelector(".box");

box.addEventListener("click", () => {
  navLink.classList.toggle("active");
  document.querySelector(".lign").classList.toggle("active");
});

// switch theme

// const ligth = document.querySelector('.light')
// const dark = document.querySelector(".dark");

// ligth.addEventListener('click', switchTheme);
// dark.addEventListener("click", switchTheme);

// const currentTheme = window.matchMedia("(prefers-color-scheme:dark)");

// console.log(currentTheme.media);
// console.log(currentTheme);

// function switchTheme(e) {
//   if (e.target.classList.contains('light')) {
//     currentTheme.matches = !currentTheme.matches;
//     console.log(currentTheme.matches);
//   }
//   // console.log(e.target)
// }

// hover link

document
  .querySelectorAll(".link")
  .forEach((link) => link.addEventListener("mouseover", overLink));

document
  .querySelectorAll(".link")
  .forEach((link) => link.addEventListener("mouseleave", overLink));

function overLink(e) {
  if (e.type === "mouseover") {
    e.target.classList.add("hover");
  } else if (e.type === "mouseleave") {
    e.target.classList.remove("hover");
  }
}

// animation

document.addEventListener("DOMContentLoaded", animateItem);

function animateItem() {
  const headerTitle = document.getElementById("header__title");
  if (headerTitle) headerTitle.classList.add("animate");
}

// observer navbar

const sectionOneOptions = {
  rootMargin: "-350px 0px 0px 0px",
};

const nav = document.querySelector("nav");
const header = document.querySelector("header");

const navObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) {
      nav.classList.add("scroll");
    } else nav.classList.remove("scroll");
  });
}, sectionOneOptions);

const body = document.getElementById("body");

console.log(body);

// navObserver.observe(header);
navObserver.observe(nav);

// lazy loading

const loadingItem = document.querySelector(".container");
const brand = document.querySelector(".brand");
const cardContainer = document.querySelector(".card__container");
const about = document.querySelector(".about_us");

if (loadingItem && brand && cardContainer && about) {
  const appearOptions = {
    threshold: 0.5,
    rootMargin: "0px 0px 200px 0px",
  };

  const lazyLoadingObserver = new IntersectionObserver(
    (entries, lazyLoadingObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("lazy-loading");
        lazyLoadingObserver.unobserve(entry.target);
      }, appearOptions);
    }
  );

  lazyLoadingObserver.observe(loadingItem);
  lazyLoadingObserver.observe(brand);
  lazyLoadingObserver.observe(cardContainer);
  lazyLoadingObserver.observe(about);
}


// search part toggle on mobil view

let searchForm = document.getElementById("search__form");
let searchToggle = document.getElementById("search__toggle");

if (searchToggle) {
  searchToggle.addEventListener('click', ()=> {
    searchForm.classList.toggle('active')
    document.getElementById("search").focus();
  })
}

