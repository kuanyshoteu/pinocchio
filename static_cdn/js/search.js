$(document).ready(function () { 
    $('#search-input').on('input', function(e) {
        id = $(this).attr('id')
        text = $(this).val()
        url = $(this).attr('url')
        $.ajax({
            url: url,
            data: {
                'text':text,
            },
            dataType: 'json',
            success: function (data) {
                $('.search-list').empty();
                $('.search-list-title').hide()
                if(data.res_profiles.length == 0 && data.res_subjects.length == 0 && data.res_squads.length == 0 && data.res_courses.length == 0){
                    $('.search-bar').hide()
                }
                else{
                    $('.search-bar').show()                    
                }
                if(data.res_profiles.length == 0){
                    $('.search-list-people').hide();
                    $('.search-list-title-people').hide()
                }
                else{
                    $('.search-list-title-people').show()
                    $('.search-list-people').show();
                    for(var i = 0; i < data.res_profiles.length; i++){
                        name = data.res_profiles[i][0]
                        url = data.res_profiles[i][1]
                        image_url = data.res_profiles[i][2]
                        if (image_url == ''){
                            image_url = "/static/images/nophoto.svg"
                        }
                        var element = $('<a class="search-item" href="'+url+'"><img class="search-item-img" src='+image_url+' alt="photo"><span class="search-item-name">'+name+'</span></a>').appendTo('.search-list-people');
                    }
                }
                if(data.res_subjects.length == 0){
                    $('.search-list-subjects').hide();
                    $('.search-list-title-subjects').hide()
                }
                else{
                    $('.search-list-subjects').show();
                    $('.search-list-title-subjects').show()
                    for(var i = 0; i < data.res_subjects.length; i++){
                        name = data.res_subjects[i][0]
                        url = data.res_subjects[i][1]
                        image_url = data.res_subjects[i][2]
                        if (image_url == ''){
                            image_url = "/static/images/nophoto.svg"
                        }
                        var element = $('<a class="search-item" href="'+url+'"><img class="search-item-img" src='+image_url+' alt="photo"><span class="search-item-name">'+name+'</span></a>').appendTo('.search-list-subjects');
                    }
                }
                if(data.res_squads.length == 0){
                    $('.search-list-squads').hide();
                    $('.search-list-title-squads').hide()
                }
                else{
                    $('.search-list-squads').show();
                    $('.search-list-title-squads').show()
                    for(var i = 0; i < data.res_squads.length; i++){
                        name = data.res_squads[i][0]
                        url = data.res_squads[i][1]
                        image_url = data.res_squads[i][2]
                        if (image_url == ''){
                            image_url = "/static/images/nophoto.svg"
                        }
                        var element = $('<a class="search-item" href="'+url+'"><img class="search-item-img" src='+image_url+' alt="photo"><span class="search-item-name">'+name+'</span></a>').appendTo('.search-list-classes');
                    }
                }
                if(data.res_courses.length == 0){
                    $('.search-list-courses').hide();
                    $('.search-list-title-courses').hide()
                }
                else{
                    $('.search-list-courses').show();
                    $('.search-list-title-courses').show()
                    for(var i = 0; i < data.res_courses.length; i++){
                        name = data.res_courses[i][0]
                        url = data.res_courses[i][1]
                        image_url = data.res_courses[i][2]
                        if (image_url == ''){
                            image_url = "/static/images/nophoto.svg"
                        }
                        var element = $('<a class="search-item" href="'+url+'"><img class="search-item-img" src='+image_url+' alt="photo"><span class="search-item-name">'+name+'</span></a>').appendTo('.search-list-courses');
                    }

                }
            }
        });
    }) 
})
$('#search-input').focus(function (event) {
    $('.search-bar').show();
    event.stopPropagation();
    $('.notice-bar').css('display', 'none');
    var div = $('.notice');
    div.css('color', '#2D437C');
});
$('#search-form').click(function (event){
    $('.search-bar').show();
    event.stopPropagation();
    $('.notice-bar').hide();
    $('.notice').attr('status', 'hide')
    var div = $('.notice');
    div.css('color', '#2D437C');
})
$("body").click(function(e){
    $('.search-bar').hide();
});

