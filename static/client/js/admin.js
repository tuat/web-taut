var renderTemplate = function(selector, context) {
    return Handlebars.compile($(selector).html())(context);
};

var fetchMedias = function(url) {
    $.getJSON(url, {
        status: $(".medias").data('status')
    },function(data) {
        $(".medias").html(renderTemplate("#medias-template", data));
        $(".pager").html(renderTemplate("#pager-template", data));
        $("html, body").animate({
            scrollTop: 0
        }, "fast");
    });
};

(function($) {

    // Bind pager event in list-media
    $(document).on('click', ".pager > .previous a, .next a", function(event) {
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

        var ids = [];
        $("a.status-control[data-id]").each(function() {
            ids.push($(this).data('id'));
        });

        $.post($(".medias").data('trashAllHref'), {
            ids: ids
        }, function(data) {
            if (data.status == "success") {
                fetchMedias($(".medias").data('mediasHref'));
            }else{
                alert(data.message);
            }
        }, "json");
    });

    $(function() {
        fetchMedias($(".medias").data('mediasHref'));
    });

})(jQuery);
