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
                    if (avatar=='None') {
                        avatar = '/static/images/nophoto.svg'
                    }
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

$('.school_landing').click(function(e){
    e.stopPropagation();
});
$('.rename_folder_form').click(function(e){
    e.stopPropagation();
});
$('.rename_lesson_form').click(function(e){
    e.stopPropagation();
});
$('.hint_students_group').click(function(e){
    e.stopPropagation();
});
$('.search_group_show').click(function(e){
    e.stopPropagation();
});
$('.search_students_group').click(function(e){
    e.stopPropagation();
});
$('.profile_links').click(function(e){
    e.stopPropagation();
});
$('.profile_name').click(function(e){
    e.stopPropagation();
});
$('.card_comment-textarea').click(function(e){
    e.stopPropagation();
});
$('.content').click(function(e){
    e.stopPropagation();
});
$('.filter-title').click(function(e){
    e.stopPropagation();
});
$('.filter-list').click(function(e){
    e.stopPropagation();
});
$('.show_hint_schedule').click(function(e){
    e.stopPropagation();
});
$('.show_search_groups').click(function(e){
    e.stopPropagation();
});
$('.folder_form').click(function(e){
    e.stopPropagation();
});
$("body").click(function(e){
    $('.hint_schedule').hide()
    $('.filter-list').hide()
    $('.profile_name').attr('status', '0')
    $('.notice-bar').hide();
    var div = $('.notice');
    div.css('color', '#2D437C');
    $(this).attr('status', 'hide')
    $('.school_landing').hide()
    $('.map_phone-main').show();
    $('.map_phone-other').hide();
    $('.folder_features').hide();
    $('.lesson_features').hide();
    $('.doc_features').hide();
    $('.rename_folder_form').hide();
    $('.hint_students_group').hide();
    $('.profile_links').hide()
    $('.card_comment-helper').hide()
    $('.search_hint').hide();
    $('#zaiavka_modal').hide('fast')    
    $('.darker').hide() 
    $('.show_search_groups').hide()    
    $('.show_search_subjects').hide() 
    $('.bselect').hide()
    $('.show_search_students').hide()
    $('.folder_form').hide()
    $('.change_task_modal').hide()
});
$('.reg_segment').click(function(e){
    $('.bselect').hide()
})