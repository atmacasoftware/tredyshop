"use strict";

/*Blog post (Post body) [START]*/

jQuery(document).ready(function($) {
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

/*Blog post (Post body) [END]*/