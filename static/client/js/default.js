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
    });

})(jQuery);
