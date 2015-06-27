(function($) {

    $(function() {
        // Bootstrap tooltips
        $('[data-toggle="tooltip"]').tooltip();

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

        // Mixpanel tracker
        if (window.mixpanel !== undefined) {
            // Click event
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

            // Page loaded
            var loadedDiv = $("div[data-mixpanel-action=loaded]");

            if (loadedDiv) {
                var page = loadedDiv.data('mixpanelPage'),
                    action = loadedDiv.data('mixpanelAction');

                mixpanel.track('Page', {
                    "page"  : page,
                    "action": action,
                    "link"  : window.location.href,
                    "text"  : document.title
                });
            }
        }
    });

})(jQuery);
