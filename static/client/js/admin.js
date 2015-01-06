(function($) {

    $(function() {
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
    });

})(jQuery);
