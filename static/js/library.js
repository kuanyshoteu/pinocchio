$(document).ready(function(){ 
    $('.estimate_lesson').click(function () {
        lesson_id = $('.lesson_id').attr('id')
        var onStar = parseInt($(this).data('value'), 10); // The star currently selected
        var stars = $(this).parent().children('li.star');
        
        for (i = 0; i < stars.length; i++) {
          $(stars[i]).removeClass('selected');
        }
        
        for (i = 0; i < onStar; i++) {
          $(stars[i]).addClass('selected');
        }        
        var ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
        $.ajax({
            url: $('.estimate_url').attr('url'),
            data: {
                'new_rating':ratingValue,
                'lesson_id':lesson_id,
            },
            dataType: 'json',
            success: function (data) {
                $('.thanks').show('fast')
            }
        });            
    }) 
    $('.pay_for_course').click(function () {
        var course_id = $(this).attr('course_id')
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'course_id':course_id,
            },
            dataType: 'json',
            success: function (data) {
                if (data.ok){
                    $('.bought_course').modal('show')
                }
                else{
                    $('.not_enough_dils').show('fast')
                }
            }
        });
    })
    $(".show_edit").click(function () {
        for (var i = document.getElementsByClassName('edit').length - 1; i >= 0; i--) {
            oldclass=document.getElementsByClassName('edit')[i].getAttribute('class')
            document.getElementsByClassName('edit')[i].setAttribute('class', oldclass + ' edit_visible');
        }
    })
    $(".new_comment").click(function () {
        var parent_id = $(this).attr('parent_id')
        var content = document.getElementById('comment_content' + parent_id).value
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'parent_id':parent_id,
                'lesson_id':$('.lesson_id').attr('id'),
                'content':content,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })

    $(".like_comment").click(function () {
        this_= $(this)
        var id = $(this).attr('id')
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                if(data.like){
                    console.log(this_.attr('style'))
                    $("#likeup"+id).attr('style', "color:#6c9b45 !important;");
                }
                else{
                    $("#dislikedown"+id).attr("style", "color:#99b1c6 !important;")
                }
                document.getElementById('likes_number' + id).innerHTML = data.like_num
            }
        });
    })
    $(".dislike_comment").click(function () {
        var id = $(this).attr('id')
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                if(data.dislike){
                    $("#dislikedown"+id).attr('style','color:red !important;');
                }
                else{
                    $("#likeup"+id).attr("style", "color:#99b1c6 !important;")
                }
                document.getElementById('likes_number' + id).innerHTML = data.like_num
            }
        });
    })
    $(".like_lesson").click(function () {
        this_= $(this)
        var id = $(this).attr('id')
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                if(data.like){
                    console.log(this_.attr('style'))
                    $("#likeup_lesson"+id).attr('style', "color:#6c9b45 !important;");
                }
                else{
                    $("#dislikedown_lesson"+id).attr("style", "color:#99b1c6 !important;")
                }
                document.getElementById('likes_number_lesson' + id).innerHTML = data.like_num
            }
        });
    })
    $(".dislike_lesson").click(function () {
        var id = $(this).attr('id')
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                if(data.dislike){
                    $("#dislikedown_lesson"+id).attr('style','color:red !important;');
                }
                else{
                    $("#likeup_lesson"+id).attr("style", "color:#99b1c6 !important;")
                }
                document.getElementById('likes_number_lesson' + id).innerHTML = data.like_num
            }
        });
    })
    $(".open_rename_paper").click(function () {      
        var id = $(this).attr('id')
        $('.paper_title_' + id).hide()
        $('.paper_rename_div_' + id).attr('style', 'display:inline-block')
    })
    $(".rename_paper").click(function () {
        var id = $(this).attr('id')
        var new_title = document.getElementsByClassName('paper_new_title_' + id)[0].value
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':$(this).attr('paper_id'),
                'new_title':new_title,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })
    $(".delete_paper").click(function () {
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':$(this).attr('id'),
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })
    $(".open_rename_subtheme").click(function () {
        var id = $(this).attr('id')
        $('.subtheme_title_' + id).hide()
        $('.subtheme_rename_div_' + id).attr('style', 'display:inline-block')
    })
    $(".rename_subtheme").click(function () {
        var id = $(this).attr('id')
        var new_title = document.getElementsByClassName('subtheme_new_title_' + id)[0].value
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':$(this).attr('subtheme_id'),
                'new_title':new_title,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })
    $(".open_rewrite_subtheme").click(function () {
        var id = $(this).attr('id')
        $('.subtheme_content_' + id).hide()
        $('.subtheme_rewrite_div_' + id).show()
    })
    $(".rewrite_subtheme").click(function () {
        var id = $(this).attr('id')
        var new_content = document.getElementsByClassName('subtheme_new_content_' + id)[0].value
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':$(this).attr('subtheme_id'),
                'new_content':new_content,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })

    $(".delete_subtheme").click(function () {
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'id':$(this).attr('id'),
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })
    $(document).on("click", '.pastee', function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        var new_parent = this_.attr("new_parent")
        $.ajax({
            url: pageUrl,
            data: {
              'school_id':this_.attr("school"),
              'new_parent':new_parent,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });  
    });
    $(".create_docfolder").click(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        console.log('d')
        $.ajax({
            url: pageUrl,
            data: {
                "school_id":this_.attr("school"),
                'parent_id':this_.attr("parent_id")
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });  
    });
    $(".delete_doc").click(function (event) {
        event.preventDefault();
        var this_ = $(this);
        var pageUrl = this_.attr("data-href")
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                },
                dataType: 'json',
                success: function (data) {
                    $('#all_doc' + this_.attr('id')).hide('fast');
                }
            });  
        }
    })
})

