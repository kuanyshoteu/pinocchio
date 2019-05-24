$('.notice').click(function(event) {
    $('.notice-bar').fadeToggle('fast');
    $('.notice').css('color', '#fff');
    $('.search-bar').hide();
    event.stopPropagation();
});
$("body").click(function(e){
    $('.notice-bar').css('display', 'none');
    var div = $('.notice');
    div.css('color', '#2D437C');
});
