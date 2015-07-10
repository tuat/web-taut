(function($) {

    $(function() {
        // Turbolinks
        $(document).on('page:fetch',   function() { NProgress.start(); });
        $(document).on('page:change',  function() { NProgress.done(); });
        $(document).on('page:restore', function() { NProgress.remove(); });

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
            var size = $(this).data('errorSize');

            $(this).prop('src', "http://placehold.it/" + size + "/FFF/000?text=Error");
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
                    "link"  : window.location.pathname,
                    "text"  : document.title
                });
            }
        }
    });

})(jQuery);
