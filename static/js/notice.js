$('.notice').click(function(event) {
    $('.notice-bar').fadeToggle('fast');
    $('.search-bar').hide();
    event.stopPropagation();
    if($(this).attr('status') == 'hide'){
        $(this).attr('status', 'show')
        $('.bell').attr('style', 'color:#2D437C;')
        $('.notice').css('color', '#fff');
        $('.notification_exists').hide()
        url = $(this).attr('url')
        $.ajax({
            url: url,
            data: {
            },
            dataType: 'json',
            success: function (data) {
                $('.notice-list').empty()
                for (var i = 0; i < data.res.length; i++){
                    author = data.res[i][0]
                    avatar = data.res[i][1]
                    type = data.res[i][2]
                    url = data.res[i][3]
                    text = data.res[i][4]
                    time = data.res[i][5]
                    $('<li class="notice-item"> <a class="notice-item-link"> <img class="notice_item_img" src='+avatar+' alt="photo"> </a> <div style="display: inline-block;"> <a class="notice-item-link"> '+author+' </a> <span class="notice-item-name"> опубликовал новость </span> <a href="'+url+'">"'+text+'"</a> <br> <div class="notice_time">'+time+'</div> </div> </li> <div class="ui divider" style="margin: 10px 0;"></div>').appendTo('.notice-list');
                }
            }
        })            
    }
    else{
        $(this).attr('status', 'hide')
        $('.bell').attr('style', 'color:#2D437C;')
    }
});
$("body").click(function(e){
    $('.notice-bar').css('display', 'none');
    var div = $('.notice');
    div.css('color', '#2D437C');
    $(this).attr('status', 'hide')
});
