$('#search-input').focus(function (event) {
    $('.search-bar').show();
    console.log('input focus')
    event.stopPropagation();
    $('.notice-bar').css('display', 'none');
    var div = $('.notice');
    div.css('color', '#2D437C');
});
$('#search-form').click(function (event){
    $('.search-bar').show();
    console.log('bar')
    event.stopPropagation();
    $('.notice-bar').css('display', 'none');
    var div = $('.notice');
    div.css('color', '#2D437C');
})
$("body").click(function(e){
    console.log('body')
    $('.search-bar').hide();
});

