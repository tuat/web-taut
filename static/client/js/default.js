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

        // Remove broken image in index page
        $("img[src*=twimg]").one('error', function() {
            $(this).closest('.panel').parent().fadeOut('fast', function() {
                $(this).remove();
            });
        });

        //
        if (window.mixpanel !== undefined) {
            $("a").on('click', function(event) {
                var page   = $(this).data('mixpanelPage'),
                    action = $(this).data('mixpanelAction')
                    link   = $(this).prop('href');

                switch(page) {
                    case 'home':
                        mixpanel.track('Home', {
                            "page"  : page,
                            "action": action,
                            "link"  : $(this).prop('href'),
                            "text"  : $(this).find('img').prop('alt')
                        });
                        break;
                    case 'media':
                        mixpanel.track('Media', {
                            "page"  : page,
                            "action": action,
                            "link"  : $(this).prop('href'),
                            "text"  : $(this).find('img').prop('alt')
                        });
                        break;
                }
            });
        }
    });

})(jQuery);
