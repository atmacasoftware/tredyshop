"use strict";

/*Message page JS code [START]*/

new Swiper('div#recommendations-slider', {
    slidesPerView: 5.5,
    speed: 1000,
    spaceBetween: 10,
    loop: false,
    navigation: {
        nextEl: 'div#recommendations-slider button.slider-btn.next',
        prevEl: 'div#recommendations-slider button.slider-btn.prev'
    },
    breakpoints:{
        320: {
            slidesPerView: 2.2,
            spaceBetween: 10
        },
        480: {
            slidesPerView: 2.5,
            spaceBetween: 10
        },
        640: {
            slidesPerView: 3.5,
            spaceBetween: 10
        },
        768: {
            slidesPerView: 3.5,
            spaceBetween: 10
        },
        1024: {
            slidesPerView: 4.5,
            spaceBetween: 10
        },
        1200: {
            slidesPerView: 5.5,
            spaceBetween: 10
        },
        1400: {
            slidesPerView: 6,
            spaceBetween: 10
        }
    }
});

new Swiper('div#recently-viewed-slider', {
    slidesPerView: 5.5,
    speed: 1000,
    spaceBetween: 10,
    loop: false,
    navigation: {
        nextEl: 'div#recently-viewed-slider button.slider-btn.next',
        prevEl: 'div#recently-viewed-slider button.slider-btn.prev'
    },
    breakpoints:{
        320: {
            slidesPerView: 2.2,
            spaceBetween: 10
        },
        480: {
            slidesPerView: 2.5,
            spaceBetween: 10
        },
        640: {
            slidesPerView: 3.5,
            spaceBetween: 10
        },
        768: {
            slidesPerView: 3.5,
            spaceBetween: 10
        },
        1024: {
            slidesPerView: 4.5,
            spaceBetween: 10
        },
        1200: {
            slidesPerView: 5.5,
            spaceBetween: 10
        },
        1400: {
            slidesPerView: 6,
            spaceBetween: 10
        }
    }
});

/*Message page JS code [END]*/

