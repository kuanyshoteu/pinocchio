$('.notice').click(function() {
    $('.notice-bar').css('display', 'block');
    $('.notice').css('color', '#fff');
});
$(document).click(function(e){
    var div = $('.notice');
    if(!div.is(e.target) && div.has(e.target).length === 0) {
        $('.notice-bar').css('display', 'none');
        div.css('color', '#2D437C');
    }
});