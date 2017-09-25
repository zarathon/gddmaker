$(document).on('click', '.confirm-remove', function () {
    return confirm('Você tem certeza dessa exclusão?');
});

$(document).ready(function () {
    $("a").each(function () {
        var link = this.href;
        var extension = link.substr(link.length - 3);
        if (extension == "png" ||
            extension == "gif" ||
            extension == "jpg") {
            $(this).attr("data-lightbox", "gddMaker");
        }
    });
});



