$(function (){

/*    $('.search-block').on('click',function () {
        $(this).css('width','380');
        $(this).on('mouseleave',function () {
            $(this).css('width','209px');
        });
        $(this).on('mouseenter',function () {
            $(this).css('width','380');
        });
    })*/

    $('.ui.dropdown')
        .dropdown()
    ;

    $('.menu .item')
        .tab()
    ;



  /*  $('.category-card').hover(function () {
        $('.go-about').css('display','block').css('background-color','#333');
    },function () {
        $('.go-about').css('display','none').css('background-color','#333');
    })
*/


    //comments
/*
    $('.hide-me').hide();

    $('.reply-me').on('click', function () {
        $('.hide-me').show();
        return false;
    })
*/




});



$(document).ready(function(){
    $(".content-markdown").each(function(){
        var content = $(this).text()
        var markedContent = marked(content)
        $(this).html(markedContent)
    })
    $(".post-detail-item img").each(function(){
        $(this).addClass("img-responsive");
    })
    var contentInput = $("#id_content");
    function setContent(value){
        $("#preview-content").html(marked(value))
        $("#preview-content img").each(function(){
            $(this).addClass("img-responsive")
        })
    }
    setContent(contentInput.val())
    contentInput.keyup(function(){
        var newContent = $(this).val()
        setContent(newContent)
    })
    var titleInput = $("#id_title");
    function setTitle(value) {
        $("#preview-title").text(value)
    }
    setTitle(titleInput.val())
    titleInput.keyup(function(){
        var newContent = $(this).val()
        setTitle(newContent)
    })
    $(".comment-reply-btn").click(function(event){
        event.preventDefault();
        $(this).parent().next(".comment-reply").fadeToggle();
    })
    $(".comment-children-reply-btn").click(function(event){
        event.preventDefault();
        $(this).parent().next(".comment-reply").fadeToggle();
    })
})

$('.ui .item').on('click', function() {
    $('.ui .item').removeClass('active');
    $(this).addClass('active');
});

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = 'https://connect.facebook.net/ru_RU/sdk.js#xfbml=1&version=v2.12';
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));