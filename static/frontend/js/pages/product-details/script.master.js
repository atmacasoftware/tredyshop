"use strict";

/*Product details JS code [START]*/

jQuery(document).ready(function($) {
    var _prod_bot_gallery_ = new Swiper('div#prod-bot-gallery', {
        slidesPerView: 6,
        speed: 300,
        loop: true,
        spaceBetween: 10,
        freeMode: true,
        watchSlidesProgress: true,
        breakpoints:{
            320: {
                slidesPerView: 4,
                spaceBetween: 10
            },
            480: {
                slidesPerView: 4,
                spaceBetween: 10
            },
            640: {
                slidesPerView: 4,
                spaceBetween: 10
            },
            768: {
                slidesPerView: 4,
                spaceBetween: 10
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 10
            }
        }
    });

    new Swiper('div#prod-top-gallery', {
        slidesPerView: 1,
        speed: 300,
        loop: true,
        spaceBetween: 0,
        thumbs: {
            swiper: _prod_bot_gallery_
        }
    });

    var clipboard = new ClipboardJS('.clip-board-copy');

    clipboard.on('success', function(event) {
        var _copybtn_ = $("div#share-item-modal").find("button.clip-board-copy");

        _copybtn_.attr("disabled", "true").find("span.clip-board-success").text("Link copied");

        setTimeout(function() {
            $("div#share-item-modal").modal("hide");

            _copybtn_.removeAttr("disabled").find("span.clip-board-success").text("Copy link");
        }, 1000);
    });
});

/*Product details JS code [END]*/