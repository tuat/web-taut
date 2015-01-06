(function($) {

    $(function() {
        // Preview
        $("a[data-photo-swipe]").on('click', function(event) {
            event.preventDefault();

            var items = [];
            var src   = $(this).prop('href');
            var size  = $(this).data('size').split('x');

            items.push({
                src: src,
                w  : size[0],
                h  : size[1]
            });

            new PhotoSwipe(document.querySelectorAll('.pswp')[0], PhotoSwipeUI_Default, items, {
                index: 0
            }).init();
        });

        // AJAX on admin list medai page for set it status
        $("a.admin-list-media").on('click', function(event) {
            event.preventDefault();

            var href = $(this).prop('href');
            var self = this;

            $.get(href).done(function(data) {
                $(self).closest('div.box').parent().fadeOut(function() {
                    $(this).remove();
                });
            }).fail(function(data) {
                alert('Moving data failed');
            });
        });

        // AJAX on admin list medai page for set all to trash
        $("a.admin-list-media-trash-all").on('click', function(event) {
            $(".content .row > div a.admin-list-media:odd").each(function() {
                $(this).trigger('click');
            });

            // Trigger next page monitor
            var deferred = new jQuery.Deferred();
            var promise  = deferred.promise();
            var timer    = setInterval(function () {
                len = $(".content .row > div a.admin-list-media").length;

                if (len <= 0) {
                    deferred.resolve();
                }
            }, 1000);

            promise.done(function () {
                clearInterval(timer);

                $(".next a")[0].click();
            });
        });

        // Remove broken image in index page
        $("img[src*=twimg]").on('error', function() {
            $(this).closest('.panel').parent().fadeOut('fast', function() {
                $(this).remove();
            });
        });
    });

})(jQuery);
