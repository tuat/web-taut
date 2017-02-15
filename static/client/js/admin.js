var renderTemplate = function(selector, context) {
    return Handlebars.compile($(selector).html())(context);
};

var fetchMedias = function(url) {
    var $trashAll = $(".trash-all"),
        oldValue = $trashAll.text();

    $trashAll.text("Loading...");

    $.getJSON(url, {
        status: $(".medias").data('status')
    },function(data) {
        $trashAll.text(oldValue);

        $(".medias").html(renderTemplate("#medias-template", data));
        $(".pager-list-media").html(renderTemplate("#pager-template", data));
        $("html, body").animate({
            scrollTop: 0
        }, "fast");

        $(".load-image-container").each(function() {
            var self     = this;
            var imageUrl = $(this).data("imageUrl");

            var loadingImage = loadImage(imageUrl, function(img) {
                $(self).append($(img).addClass('img-responsive'));
            }, {
                maxWidth: 250,
                maxHeight: 200,
                canvas: false
            });
        });
    });
};

(function($) {

    // Bind pager event in list-media
    $(document).on('click', ".pager-list-media > .previous a, .pager-list-media > .next a", function(event) {
        event.preventDefault();

        fetchMedias($(this).prop('href'));
    });

    // Bind status control event in list-media
    $(document).on('click', 'a.status-control', function(event) {
        event.preventDefault();

        var id     = $(this).data('id');
        var status = $(this).data('status');
        var self   = this;

        $.getJSON($(".medias").data("statusControlHref"), {
            id    : id,
            status: status,
        }, function(data) {
            if (data.status == "success") {
                $(self).closest('div.box').parent().remove()
            }else{
                alert(data.message);
            }
        })
    });

    $(document).on('click', 'a.trash-all', function(event) {
        event.preventDefault();

        $(this).addClass('btn-warning');

        var ids = [];
        $("a.status-control[data-id]").each(function() {
            ids.push($(this).data('id'));
        });

        var self = this;
        $.post($(".medias").data('trashAllHref'), {
            ids: ids
        }, function(data) {
            if (data.status == "success") {
                fetchMedias($(".medias").data('mediasHref'));
                $(self).removeClass('btn-warning');
            }else{
                alert(data.message);
            }
        }, "json");
    });

    $(document).on('click', 'a.page-control', function(event) {
        event.preventDefault();

        window.open('/media/detail/' + $(this).data('id'));
    });

    $(function() {
        fetchMedias($(".medias").data('mediasHref'));

        var loadContainer = $(".load-image-container");
        var imageUrl      = loadImageContainer.data("imageUrl");
        var loadingImage  = loadImage(imageUrl, function(img) {
            loadContainer.append($(img).addClass('img-responsive'));
        }, {
            maxWidth: 250,
            maxHeight: 200,
            canvas: false
        });
    });

})(jQuery);
