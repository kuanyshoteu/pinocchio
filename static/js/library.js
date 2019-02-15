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
        
        // JUST RESPONSE (Not needed)
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
        console.log(new_parent, 'de', pageUrl)
        $.ajax({
            url: pageUrl,
            data: {
              'new_parent':new_parent,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });  
    });
    $(document).on("click", '.file_action', function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        var object_type = this_.attr("object_type")
        var action = this_.attr("action")
        var id = this_.attr("id")
        var parent = this_.attr("parent")
        console.log('ee', pageUrl)
        $.ajax({
            url: pageUrl,
            data: {
              'object_type':object_type,
              'action':action,
              'object_id':id,
              'parent':parent,
            },
            dataType: 'json',
            success: function (data) {
                if (action == 'cut'){
                    img = document.getElementById(this_.attr("object_type") + '_image' + this_.attr('id'));
                    img.setAttribute('style', 'height: 50px; -webkit-filter: opacity(.5); filter: opacity(.5);')
                } 
                if (action == 'copy'){
                    img = document.getElementById(this_.attr("object_type") + '_image' + this_.attr('id'));
                    img.setAttribute('style', 'height: 50px; -webkit-filter: opacity(1); filter: opacity(1);')
                } 
                features = document.getElementsByClassName(this_.attr("object_type") + '_features' + this_.attr('id'))[0]
                
                features.setAttribute('style', 'position: absolute; z-index: 3000; display: none; margin: 30px 0 0 30px;')
                console.log('www')
            }
        });  
    });
})



$(document).ready(function(){
    $(".create_folder").click(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        console.log('d')
        $.ajax({
            url: pageUrl,
            data: {
                'parent_id':this_.attr("parent_id")
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
                'parent_id':this_.attr("parent_id")
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });  
    });
    $(document).on("click", '#new', function () {
        var this_ = $(this);
        console.log('f', this_.attr("data-href"));
        var pageUrl = this_.attr("data-href");
        var name = $('#change_folder_name' + this_.attr('id')).val();
        console.log('f')
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                    'name':name,
                },
                dataType: 'json',
                success: function (data) {
                    $('.rename_form' + this_.attr('id')).hide()
                    span = document.getElementById('folder_title' + this_.attr('id'));
                    span.innerHTML = name
                    $('#folder_title' + this_.attr('id')).show()
                }
            });  
        }
    });
    $(".change_folder_name").click(function () {
        var this_ = $(this);
        console.log('f');
        var pageUrl = this_.attr("data-href");
        var name = $('#change_folder_name' + this_.attr('id')).val();
        console.log('f')
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                    'name':name,
                },
                dataType: 'json',
                success: function (data) {
                    $('.rename_form' + this_.attr('id')).hide()
                    span = document.getElementById('folder_title' + this_.attr('id'));
                    span.innerHTML = name
                    $('#folder_title' + this_.attr('id')).show()
                }
            });  
        }
    });
    $(".open_folder_features").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        $('.folder_features' + this_.attr("id")).fadeToggle();
    })
    $(".rename_folder").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        $('.folder_features' + this_.attr('id')).hide() 
        $('.rename_form' + this_.attr("id")).show();
        $('#folder_title' + this_.attr('id')).hide()            
    })
    $(".delete_folder").click(function (event) {
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
                    $('#all_folder' + this_.attr('id')).hide();
                }
            });  
        }
    })
})



$(document).ready(function(){
    $(".create_lesson").click(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        $.ajax({
            url: pageUrl,
            data: {
              'parent_id':this_.attr("parent_id")
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });  
    });

    $(document).on("click", '.change_lesson_name', function () {
        var this_ = $(this);
        var pageUrl = this_.attr("data-href");
        var name = $('#change_lesson_name' + this_.attr('id')).val();
        console.log('feee', pageUrl, name);
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                    'name':name,
                },
                dataType: 'json',
                success: function (data) {
                    $('.rename_lesson' + this_.attr('id')).hide()
                    span = document.getElementById('lesson_title' + this_.attr('id'));
                    span.innerHTML = name
                    $('#lesson_title' + this_.attr('id')).show()
                }
            });  
        }
    });
    $(".new_paper").click(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        id = this_.attr("id")
        paper_id = this_.attr("paper_id")
        var title = document.getElementsByClassName('new_paper_title_' + paper_id)[0].value
        $.ajax({
            url: pageUrl,
            data: {
                'id':id,
                'title':title,
            },
            dataType: 'json',
            success: function (data) {
                location.reload();
            }
        });
    });
    $(".new_subtheme").click(function () {
        console.log('xxx')
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        id = this_.attr("id")
        paper_id = this_.attr("paper_id")
        var title = document.getElementsByClassName('new_subtheme_title_' + paper_id)[0].value
        var content = document.getElementById('new_subtheme_content' + paper_id).value
        var videolink = document.getElementsByClassName('new_subtheme_videolink_' + paper_id)[0].value
        
        var files = document.getElementById("video_" + paper_id).files
        for (var i = 0; i < files.length; i++) {
            var file = files[i],
                name = file.name || file.fileName,
                reader = new FileReader();

            reader.readAsText(file);
        }
        $.ajax({
            url: pageUrl,
            data: {
                'id':id,
                'title':title,
                'content':content,
                'videolink':videolink,
                'video':reader
            },
            dataType: 'json',
            success: function (data) {
                location.reload();
            }
        });
    });
    $(".new_problem").click(function () {
        var this_ = $(this) 
        var pageUrl = this_.attr("data-href")
        subtheme_id = this_.attr("subtheme_id");
        id = this_.attr("id");
        text = $('#new_problem_text' + id).val()
        cost = $('#new_problem_cost' + id).val()
        var variants = ''
        var ans = ''
        var tags = ''
        var variant_ans = ''
        for(var i = 0; i < document.getElementsByClassName('new_problem_tag_' + id).length; i++){
            tags = tags + document.getElementsByClassName('new_problem_tag_' + id)[i].getAttribute('name') + '&'
        }
        for(var i = 0; i < document.getElementsByClassName('new_problem_ans_' + id).length; i++){
            ans = ans + document.getElementsByClassName('new_problem_ans_' + id)[i].value + '&'
        }
        for(var i = 0; i < document.getElementsByClassName('new_problem_test_' + id).length; i++){
            textarea = document.getElementsByClassName('new_problem_test_' + id)[i]
            variants = variants + textarea.value + '&';
            checkbox = document.getElementById('is_correct_variant_' + id + 'variant' + textarea.getAttribute('variant_number'))
            if (checkbox.checked){
                variant_ans = variant_ans + textarea.value + '&';
            }
        }

        $.ajax({
            url: pageUrl,
            data: {
                'text':text,
                'ans':ans,
                'tags':tags,
                'variant_ans':variant_ans,
                'cost':cost,
                'subtheme_id':subtheme_id,
                'variants':variants,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });  
    });
    $(".add_problem").click(function () {
        var this_ = $(this) 
        var Url = this_.attr("url")
        subtheme_id = this_.attr("subtheme_id");
        task_id = this_.attr("task_id");
        id = this_.attr("id");
        $.ajax({
            url: Url,
            data: {
                'subtheme_id':subtheme_id,
                'task_id':task_id,
            },
            dataType: 'json',
            success: function (data) {
                if(data.action == 'add'){
                    this_.text("Убрать");                    
                }
                else{
                    this_.text("Добавить");
                }
            }
        });  
    });
    $(".open_lesson_features").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        $('.lesson_features' + this_.attr("id")).fadeToggle();
    })
    $(".open_doc_features").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        $('.doc_features' + this_.attr("id")).fadeToggle();
    })
    $(".rename_lesson").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        $('.paper_features' + this_.attr('id')).hide() 
        $('.rename_lesson' + this_.attr("id")).show();
        $('#paper_title' + this_.attr('id')).hide()            
    })
    $(".delete_lesson").click(function (event) {
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
                    $('#all_lesson' + this_.attr('id')).hide();
                }
            });  
        }
    })
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
                    $('#all_doc' + this_.attr('id')).hide();
                }
            });  
        }
    })
})

