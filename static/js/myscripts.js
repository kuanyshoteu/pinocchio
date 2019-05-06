$(document).ready(function () {
    $('.delete_card').click(function(e) {
        id = $(this).attr('id');
        $('.delete_card_data').attr('id', id);
        $('#delete_card_modal').modal('show');
    })
    $('.yes_delete_card').click(function(e) {
        url = $('.delete_card_data').attr('url')
        id = $('.delete_card_data').attr('id')
        $.ajax({
            url: url,
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('#delete_card_modal').modal('hide');
                $('#card' + id).hide('fast');
            }
        })        
    });
    $('.save_job_salary').click(function(e) {
        url = $('.save_job_salary_url').attr('url')
        id = $(this).attr('id')
        this_ = $(this)
        salary = $('#job_salary' + id).val();
        $.ajax({
            url: url,
            data: {
                'id':id,
                'salary':salary,
            },
            dataType: 'json',
            success: function (data) {
                location.reload();
            }
        })        
    });    
    $('.update_hints').click(function(e) {
        url = $(this).attr('url')
        console.log('de')
        $.ajax({
            url: url,
            data: {
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        })        
    });    
    $('.save_card_as_user').click(function(e) {
        id = $('.card_for_save').attr('id')
        squad_id = $(this).attr('squad_id')
        $.ajax({
            url: $('.card_for_save').attr('url'),
            data: {
                'id':id,
                'squad_id':squad_id,
            },
            dataType: 'json',
            success: function (data) {
                document.getElementById("school_schedule").style.width = "0";
                $('.backg').removeClass('darker');
                $('#saved_modal').modal('show')
            }
        })        
    });
    $('.open_card_form').click(function(e) {
        $('#card_form'+$(this).attr('id')).modal('show')
    })
    $('.add_card').click(function(e) {
        var id = $(this).attr("id")
        var name = $('.new_card_name' + id).val()
        var phone = $('.new_card_phone' + id).val()
        var mail = $('.new_card_mail' + id).val()
        var comment = $('.new_card_comment' + id).val()
        $.ajax({
            url: $('.add_card_url').attr('url'),
            data: {
                'name':name,
                'phone':phone,
                'mail':mail,
                'comment':comment,
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                card_id = data.card_id;
                                
                var element = $('<div id="card'+data.card_id+'" style="margin-bottom: 10px;" ondragstart="save_card_id('+data.card_id+')" draggable="true"> <div class="ui segment full-w" style="cursor: pointer;padding: 3px 7px;"> <div style="float: right;font-size: 11px;color: #b3b300"> '+data.card_date+' <br> </div> <i class="icon user"></i> <a class="open_card_form" id="'+card_id+'" onclick="" style="font-weight: 600">'+data.card_name+'</a> <div style="color: darkgrey;font-size: 12px;"> <i class="icon phone"></i> '+data.card_phone+' <br> <i class="icon envelope"></i> '+data.card_mail+' </div> </div> </div>');
                element.appendTo('.crmbox' + id)
                $('#new_card_form'+id).modal('hide')
            }
        })        
    });
    $('.edit_card').click(function(e) {
        var id = $(this).attr("id")
        var name = $('.card_name' + id).val()
        var phone = $('.card_phone' + id).val()
        var mail = $('.card_mail' + id).val()
        var comment = $('.card_comment' + id).val()
        $.ajax({
            url: $('.edit_card_url').attr('url'),
            data: {
                'name':name,
                'phone':phone,
                'mail':mail,
                'comment':comment,
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('#card' + id).load(document.URL +  ' #card' + id);
                $('#card_form'+id).modal('hide')
            }
        })        
    });
    $('.show_subject_cost').hover(function(e) {
        cost = $(this).attr('cost')
        $('.subject_cost').html(cost)
    })
    $('.show_subject_cost').click(function(e) {
        console.log('d')
        id = $(this).attr("squad_id")
        $(".current_squad").attr("id", id)
        $('#add_student_modal').modal('show')
    })
    $('.crm_option').on('change', function(e) {
        id = $(this).attr('id')
        this_ = document.getElementById(id);
        object_id = this_.options[this_.selectedIndex].value;
        url = $(this).attr('url')
        option = $(this).attr('option')
        $.ajax({
            url: url,
            data: {
                'object_id':object_id,
                'option':option,
            },
            dataType: 'json',
            success: function (data) {
                $( "#calendar" ).load(document.URL +  ' #calendar');
            }
        });
    }) 
    $('.change_subject_category').on('change', function(e) {
        id = $(this).attr('id')
        this_ = document.getElementById(id);
        object_id = this_.options[this_.selectedIndex].value;
        url = $(this).attr('url')
        $.ajax({
            url: url,
            data: {
                'object_id':object_id,
            },
            dataType: 'json',
            success: function (data) {
            }
        });
    }) 
    $('.change_subject_age').on('change', function(e) {
        id = $(this).attr('id')
        this_ = document.getElementById(id);
        object_id = this_.options[this_.selectedIndex].value;
        url = $(this).attr('url')
        $.ajax({
            url: url,
            data: {
                'object_id':object_id,
            },
            dataType: 'json',
            success: function (data) {
            }
        });
    }) 
    $('.choose_subject_category').on('click', function(e) {
        id = $(this).attr('id')
        url = $(".get_subject_category_url").attr('url')
        option = $(this).attr('option')
        $.ajax({
            url: url,
            data: {
                'object_id':id,
                'option':option,
            },
            dataType: 'json',
            success: function (data) {
                $( "#list" ).load(document.URL +  ' #list');
                $(".option_vertical").removeClass('option_vertical_active')
                $('#category'+id).addClass('option_vertical_active')
            }
        });
    }) 
    $('.add_student').on('click', function(e) {
        console.log('d')
        var name = $('.new_student_name').val()
        var phone = $('.new_student_phone').val()
        var mail = $('.new_student_mail').val()
        var squad_id = $('.current_squad').attr("id")
        $.ajax({
            url: $('.register_to_school_url').attr('url'),
            data: {
                'name':name,
                'phone':phone,
                'mail':mail,
                'squad_id':squad_id,
                'status':'student',
            },
            dataType: 'json',
            success: function (data) {
                $('.new_student_name').attr('class', '')
                $('.new_student_phone').attr('class', '')
                $('.new_student_mail').attr('class', '')
                password_place = document.getElementById('password_place')
                password = document.createElement('span')
                password.innerHTML = data.password
                password_place.appendChild(password)
                $('#password_place').attr('id', '')

                tr = document.createElement('tr')
                td = document.createElement('td')
                textarea = document.createElement('textarea')
                textarea.setAttribute('class', 'new_student_name')
                td.appendChild(textarea)
                tr.appendChild(td)
                // 
                td2 = document.createElement('td')
                textarea = document.createElement('textarea')
                textarea.setAttribute('class', 'new_student_phone')
                td2.appendChild(textarea)
                tr.appendChild(td2)
                // 
                td3 = document.createElement('td')
                textarea = document.createElement('textarea')
                textarea.setAttribute('class', 'new_student_mail')
                td3.appendChild(textarea)    
                tr.appendChild(td3)
                // 
                td4 = document.createElement('td')
                td4.setAttribute('id', 'password_place')
                tr.appendChild(td4)
                tbody = document.getElementById('create_student_rows')
                tbody.appendChild(tr)
            }
        });
    })
    $('.update_schedule').click(function (event){
        $.ajax({
            url: $(this).attr('url'),
            data: {
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })
    $('.delete_post').click(function (event){
        var id = $(this).attr('id')
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'post_id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('.post_details' + id).hide('fast')
            }
        });
    })    
    $('.create_new_post').on('click', function(e) {
        this_ = $(this)
        var text = $('.new_post_area').val()
        var file = document.getElementById('postfile').files[0];
        var url = this_.attr('url')

        var xhr = new XMLHttpRequest();
        var csrfToken = xhr.getResponseHeader('x-csrf-token');
        xhr.open('post', url, true);
        xhr.setRequestHeader('x-csrf-token', csrfToken); 
        xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        xhr.setRequestHeader("Accept", "application/json");
        xhr.send(file);
    });
    $('.show_post_form').click(function (event){
        $('.new_post_details').show('fast')
        event.stopPropagation();
    })
    $("body").click(function(e){
        $('.new_post_details').hide('fast');
    });
    $('.profile_name').click(function (event){
        $('.profile_links').fadeToggle('fast')
    })
    $('.tell_about_corruption').click(function (event){
        var text = $('.corruption_text').val()
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'text':text,
            },
            dataType: 'json',
            success: function (data) {
                if(data.ok){
                    $('.thanks').attr('style', 'background-color: #65C063;color: #fff;display: block;')                    
                }
            }
        });
    })
    $('.show_att_chart').click(function (event){
        $('.attendances').hide()
        $('.att_charts').show()
        $('.show_att_chart').hide()
        $('.show_attendances').show()
    })
    $('.show_attendances').click(function (event){
        $('.att_charts').hide()
        $('.attendances').show()
        $('.show_attendances').hide()
        $('.show_att_chart').show()
    })
    $('.open_point').click(function (event){
        
    })

    $(document).on("click", '.att_present', function () {    
        var id = $(this).attr('id')
        $.ajax({
            url: $('.attendance_present_url').attr('url'),
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('#grades' + id).show()
                $('#attendance'+id).hide()
            }
        });
    })
    $(".switch_att_btn").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var paper_id = this_.attr('paper_id')
        var lesson_id = this_.attr('lesson_id')
        current_class = this_.attr('class')
        for(var i = 0; i < document.getElementsByClassName('switch_att_btn' + lesson_id).length; i++){
            document.getElementsByClassName('switch_att_btn' + lesson_id)[i].setAttribute('class', 'switch_att_btn switch_att_btn' + lesson_id)    
        }
        for(var i = 0; i < document.getElementsByClassName('ppr' + lesson_id).length; i++){
            document.getElementsByClassName('ppr' + lesson_id)[i].setAttribute('class', 'paper ppr ppr' + lesson_id)
        }
        this_.attr('class', current_class + ' switch_att_btn_active switch_att_btn')
        $('#paper' + paper_id + lesson_id).attr('class', 'paper_active ppr ppr' + lesson_id)
    })
    $('.open_attendance').click(function (event){
        var id = $(this).attr('id')
        for (var i = 0; i < document.getElementsByClassName('subject_attendance').length; i++){
            document.getElementsByClassName('subject_attendance')[i].setAttribute('style', 'display:none;')
        }
        document.getElementById('subject' + id).setAttribute('style', 'display:block')
    })
    $('.login_btn').click(function (event){
        var username = document.getElementsByClassName('username')[0].value
        var password = document.getElementsByClassName('password')[0].value
        $.ajax({
            url: $(this).attr('url'),
            data: {
                'username':username,
                'password':password,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        });
    })
    $('.continue').click(function (event){
        $(this).hide()
        $(".continue_div").show()
    })
    $('.register_btn').click(function (event){
        var first_name = document.getElementsByClassName('reg_first_name')[0].value
        var second_name = document.getElementsByClassName('reg_second_name')[0].value
        var school = document.getElementsByClassName('reg_school')[0].value
        var phone = document.getElementsByClassName('reg_phone')[0].value
        var mail = document.getElementsByClassName('reg_mail')[0].value
        if(first_name != '' && second_name != '' && school != '' && phone != '' && mail != ''){
            var password1 = document.getElementsByClassName('reg_password1')[0].value
            var password2 = document.getElementsByClassName('reg_password2')[0].value
            if(password1 == password2){
                $(".match_pass_message").hide()
                if(password1.length > 6){
                    $(".short_pass_message").hide()
                    $.ajax({
                        url: $(this).attr('url'),
                        data: {
                            'first_name':first_name,
                            'second_name':second_name,
                            'school':school,
                            'phone':phone,
                            'mail':mail,  
                            'password1':password1,
                            'password2':password2,              
                        },
                        dataType: 'json',
                        success: function (data) {
                            location.reload()
                        }
                    });
                }
                else{$(".short_pass_message").show()}
            }
            else{$(".match_pass_message").show()}
        }
        else{$(".fill_message").show()}
        
    })
    $('.openchart').on('click', function(e) {
        id = $(this).attr('id')
        if ($(this).attr('status') == 'closed'){
            $('#chart' + id).show('slow')
            $(this).attr('status', 'opened')
            $('#icondown' + id).show()
            $('#iconright' + id).hide()
        }
        else{
            $('#chart' + id).hide('slow')
            $(this).attr('status', 'closed')
            $('#icondown' + id).hide()
            $('#iconright' + id).show()
        }
    });
    $('.add_variant').click(function (event){
        var id = $(this).attr('id')
        var current_variant_number = parseInt($(this).attr('current_variant_number')) + 1
        $(this).attr('current_variant_number', current_variant_number)
        ul = document.getElementsByClassName(id + 'variants')[0]
        li = document.createElement('div')
        b = document.createElement('span')
        b.innerHTML = 'Вариант ответа: '
        textarea = document.createElement('textarea')
        textarea.setAttribute('style', 'height: 33px;width: 200px;')
        textarea.setAttribute('class', 'new_problem_test_' + id)
        textarea.setAttribute('variant_number', current_variant_number)
        checkbox = document.createElement('input')
        checkbox.setAttribute('id', 'is_correct_variant_' + id + 'variant' + current_variant_number)
        checkbox.setAttribute('type', 'checkbox')
        li.appendChild(b)
        li.appendChild(textarea)
        li.appendChild(checkbox)
        ul.appendChild(li)
    })
    $('.add_answer').click(function (event){
        var id = $(this).attr('id')
        div = document.getElementsByClassName('answers_' + id)[0]
        li = document.createElement('li')
        b = document.createElement('span')
        b.innerHTML = 'Ответ: '
        br = document.createElement('br')
        textarea = document.createElement('textarea')
        textarea.setAttribute('style', 'height: 33px;width: 200px;')
        textarea.setAttribute('class', 'new_problem_ans_' + id)
        div.appendChild(b)
        div.appendChild(br)
        div.appendChild(textarea)
        div.appendChild(br)
    })
    $('.add_tag').click(function (event){
        var id = $(this).attr('id')
        div = document.getElementsByClassName('new_problem_tags_' + id)[0]
        name = document.getElementById('new_problem_tag_name_' + id).value
        a = document.createElement('a')
        a.setAttribute('class', 'ui label new_problem_tag_'  + id)
        a.setAttribute('name', name)
        a.innerHTML = name
        div.appendChild(a)
    })
    $(".problem_type").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var id = this_.attr('id')
        $('.' + id + 'not_test').fadeToggle()
        $('.' + id + 'test').fadeToggle()
        if ($('.problem_type_info').attr('info') == 'input'){
            $('.problem_type_info').attr('info', 'test')
            this_.text('Ввод ответа')
        }
        else{
            $('.problem_type_info').attr('info', 'input')
            this_.text('Тест')
        }
    })
    $(".content-markdown").each(function () {
        var content = $(this).text()
        var markedContent = marked(content)
        $(this).html(markedContent)
    });
    $(".open_form_trener").click(function (event) {
        event.preventDefault();
        $(".form_trener").fadeToggle();
    });
    $(".open_subject_form").click(function (event) {
        event.preventDefault();
        $(".subject_form" + $(this).attr('id')).fadeToggle();
    });
    $(".change_subject").click(function () {
        var this_ = $(this)
        id = this_.attr("id")
        var pageUrl = this_.attr("data-href")
        var title = $('#subject_title' + id).val();
        var text = $('#id_text' + id).val();
        var cost = $('#subject_cost' + id).val();
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                    'title':title,
                    'cost':cost,
                    'text':text,
                },
                dataType: 'json',
                success: function (data) {
                    document.getElementById(this_.attr("id")+'title').innerHTML = title 
                    document.getElementById(this_.attr("id")+'text').innerHTML = marked(text) 
                    document.getElementById(this_.attr("id")+'cost').innerHTML = cost 
                    $(".subject_form" + id).fadeToggle();
                }
            });
        }
    });
    $(".open_form").click(function (event) {
        event.preventDefault();
        $(".update_form").fadeToggle();
    })
    $(".open_comments").click(function (event) {
        event.preventDefault();
        $(".comments").fadeToggle();
    })
    $(".open_docs").click(function (event) {
        event.preventDefault();
        $(".docs").fadeToggle();
    })
    $(".open_page").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var page = this_.attr('page')
        $("#detailed_info").attr('class', 'ui tab');
        $("#all_squads").attr('class', 'ui tab');
        $("#attendance").attr('class', 'ui tab');
        $("#zaiavki").attr('class', 'ui tab');
        if (page == 'profile_info'){
            $("#detailed_info").attr('class', 'ui tab active');
        }
        if (page == 'profile_zaiavki'){
            $("#zaiavki").attr('class', 'ui tab active');
        }
        if (page == 'profile_attendance'){
            $("#attendance").attr('class', 'ui tab active');
        }
        if (page == 'profile_squads'){
            $("#all_squads").attr('class', 'ui tab active');
        }
    })
    $(".open_students_table").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var page = this_.attr('page')
        for(var i = 0; i < document.getElementsByClassName('tab').length; i++){
            document.getElementsByClassName('tab')[i].setAttribute('class', 'ui tab')
        }
        $("#" + page).attr('class', 'ui tab active');

    })

    $(".save_zaiavka").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var Url = this_.attr("data-href")
        var name = $('.zaiavka_name').val()
        var phone = $('.zaiavka_phone').val()
        if (Url) {
            $.ajax({
                url: Url,
                method: "GET",
                data: {
                    'name':name,
                    'phone':phone
                },
                success: function (data) {
                    $(".ok_zaiavka").show()
                }, error: function (error) {
                }
            })
        }
    })
    $(".open_form_status").click(function (event) {
        event.preventDefault();
        $(".update_status").fadeToggle();
    })
    $(".open_form_paper").click(function (event) {
        event.preventDefault();
        $(".create_paper").fadeToggle();
    })
    $(".open_form_task").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var form_id = '.' + this_.attr("id") + 'add_task'
        $(form_id).fadeToggle();
    })
    $(".open_add_child").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var form_id = '.' + this_.attr("id") + 'add_child'
        $(form_id).fadeToggle();
    })
    $(".open_groups").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var form_id = '.' + 'groups' + this_.attr("id")
        $(form_id).fadeToggle();
    })
    $(".open_group_details").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var table_id = '#' + this_.attr("id") + 'details';
        $(table_id).fadeToggle();
    })
    
    $(".open_group_details_hmw").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var table_id = '#' + this_.attr("id") + 'details_hmw'
        $(table_id).fadeToggle();
    })
    $(".open_group_details_cls").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var table_id = '#' + this_.attr("id") + 'details_cls'
        $(table_id).fadeToggle();
    })
    $(".open_chart").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        $('#' + this_.attr("id") + 'chart').fadeToggle();
    })
})
$(document).ready(function () {
    $(".delete_zaiavka").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var icon = '#zaiavka' + this_.attr("id")
        var name = '#zaiavka_name_' + this_.attr("id")
        var phone = '#zaiavka_phone_' + this_.attr("id")
        var time = '#zaiavka_time_' + this_.attr("id")
        var changeUrl = this_.attr("data-href")
        if (changeUrl) {
            $.ajax({
                url: changeUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    $(icon).css('display', 'none')
                    $(name).css('text-decoration', 'line-through')
                    $(name).css('color', 'grey')
                    $(phone).css('text-decoration', 'line-through')
                    $(phone).css('color', 'grey')
                    $(time).css('text-decoration', 'line-through')
                    $(time).css('color', 'grey')
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(".delete_follow").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var icon = '#follow' + this_.attr("id")
        var user = '#follow_user_' + this_.attr("id")
        var group = '#follow_group_' + this_.attr("id")
        var phone = '#follow_phone_' + this_.attr("id")
        var time = '#follow_time_' + this_.attr("id")
        var changeUrl = this_.attr("data-href")
        if (changeUrl) {
            $.ajax({
                url: changeUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    $(icon).css('display', 'none')
                    $(user).css('text-decoration', 'line-through')
                    $(user).css('color', 'grey')
                    $(group).css('text-decoration', 'line-through')
                    $(group).css('color', 'grey')
                    $(phone).css('text-decoration', 'line-through')
                    $(phone).css('color', 'grey')
                    $(time).css('text-decoration', 'line-through')
                    $(time).css('color', 'grey')
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(".change_status").click(function (e) {
        e.preventDefault()
        var Url = $(this).attr("data-href")
        status = $(".textarea_status").val()
        $.ajax({
            url: Url,
            method: "GET",
            data: {
                'status':status
            },
            success: function (data) {
                hisstatus = document.getElementsByClassName('hisstatus')[0]
                hisstatus.innerHTML = status
            }, error: function (error) {
            }

        })
    })
    $(".add_group_btn").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var squadUrl = this_.attr("data-href")
        if (squadUrl) {
            $.ajax({
                url: squadUrl,
                data: {
                    'paper_id':this_.attr("paper_id"),
                    'squad_id':this_.attr("squad_id"),
                    'isin':this_.attr("isin"),
                },
                success: function (data) {
                    if (this_.attr("isin") == 'yes') {
                        this_.css('background-color', '#F2F2F2')
                        this_.css('color', 'black')
                        this_.attr('isin', 'no')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn_urok").css('background-color', '#F2F2F2')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn_urok").css('color', 'black')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn_urok").attr('isin', 'no')

                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results').hide()
                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results_urok').hide()
                    }
                    else {
                        this_.css('background-color', '#5181b8')
                        this_.css('color', 'white')
                        this_.attr('isin', 'yes')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn_urok").css('background-color', '#5181b8')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn_urok").css('color', 'white')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn_urok").attr('isin', 'yes')
                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results').show()
                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results_urok').show()

                    }
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(document).on("click", '.save_grade', function () {
        event.preventDefault();
        var this_ = $(this)
        var pageUrl = $('.attendance_change_url').attr("url")
        var grade = this_.attr('grade')
        var id = this_.attr('id')
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                method: "GET",
                data: {
                    'id':id,
                    'grade':grade,                        
                },
                success: function (data) {
                    this_.attr('class','ui button mini green save_grade')
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(".present").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                method: "GET",
                data: {
                    'id':this_.attr("id2"),
                    'attendance':'present',                        
                },
                success: function (data) {
                    var attendance = '#' + 'att' + this_.attr("id2")
                    var absent = '#' + 'absent' + this_.attr("id2")
                    var late = '#' + 'late' + this_.attr("id2")
                    $(attendance).attr('value', 'present');
                    this_.css('background-color', '#21BA45');
                    this_.css('color', 'white');
                    $(absent).css('background-color', '#e5ebf1');
                    $(absent).css('color', 'rgba(0, 0, 0, 0.9)');
                    $(late).css('background-color', '#e5ebf1');
                    $(late).css('color', 'rgba(0, 0, 0, 0.9)');
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(".absent").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                method: "GET",
                data: {
                    'id':this_.attr("id2"),
                    'attendance':'absent',                        
                },
                success: function (data) {
                    var attendance = '#' + 'att' + this_.attr("id2");
                    var present = '#' + 'present' + this_.attr("id2");
                    var late = '#' + 'late' + this_.attr("id2");
                    $(attendance).attr('value', 'absent');
                    this_.css('background-color', '#DB2828');
                    this_.css('color', 'white');
                    $(present).css('background-color', '#e5ebf1');
                    $(present).css('color', 'rgba(0, 0, 0, 0.9)');
                    $(late).css('background-color', '#e5ebf1');
                    $(late).css('color', 'rgba(0, 0, 0, 0.9)');
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(".late").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        var attendance = '#' + 'att' + this_.attr("id2")
                    
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id2"),
                    'attendance':'late',
                },
                success: function (data) {
                    var absent = '#' + 'absent' + this_.attr("id2")
                    var present = '#' + 'present' + this_.attr("id2")
                    $(attendance).attr('value', 'late');
                    this_.css('background-color', '#FBBD08')
                    this_.css('color', 'white')
                    $(absent).css('background-color', '#e5ebf1')
                    $(absent).css('color', 'rgba(0, 0, 0, 0.9)')
                    $(present).css('background-color', '#e5ebf1')
                    $(present).css('color', 'rgba(0, 0, 0, 0.9)')
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
    $(".grade").change(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        var grade = $(this).val();
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("name"),
                    'grade':grade
                },
                dataType: 'json',
                success: function (data) {
                }
            });
        }
    });
    $(".zhurnal_grade").click(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        var grade = $('#grade' + this_.attr("name")).val();
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("name"),
                    'grade':grade
                },
                dataType: 'json',
                success: function (data) {
                }
            });
        }
    });
})
$(document).ready(function () {
    $(".check_task_answer").click(function () {
        var this_ = $(this)
        var id = this_.attr("id")
        var pageUrl = this_.attr("data-href")
        var paper_id = this_.attr("paper_id")
        var answer = ""
        var tags = ''
        for(var i = 0; i < document.getElementsByClassName('problem_tag_' + paper_id).length; i++){
            tags = tags + document.getElementsByClassName('problem_tag_' + paper_id)[i].getAttribute('tag_id') + '&'
        }        
        if( $(".task_type_" + paper_id).attr("type") == "input" ){
            for(var i = 0; i < document.getElementsByClassName('check_task_answer_' + paper_id).length; i++){
                answer = answer + document.getElementsByClassName('check_task_answer_' + paper_id)[i].value + "&"
            }
        }
        if( $(".task_type_" + paper_id).attr("type") == "test" ){
            for(var i = 0; i < document.getElementsByClassName("option_" + paper_id).length; i++){
                if(document.getElementsByClassName("option_" + paper_id)[i].checked){
                    answer = answer + document.getElementsByClassName("option_" + paper_id)[i].getAttribute("value") + "&"
                }
            }
        }
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                    'answer':answer,
                    'tags':tags,
                    'parent_id':this_.attr("parent_id"),
                },
                dataType: 'json',
                success: function (data) {
                    if(document.getElementById('hiscoins') != undefined){
                        document.getElementById('hiscoins').innerHTML = data.hiscoins;
                    }
                    if (data.solved == true){
                        document.getElementsByClassName('wrong_answer_alert_' + paper_id)[0].setAttribute('style', 'display:none')
                        document.getElementsByClassName(paper_id + 'solved')[0].setAttribute('style', 'margin-right: 10px; font-size: 16px; font-weight: 600; color: green;');
                        document.getElementsByClassName(paper_id + 'solved_tick')[0].setAttribute('style', 'color: green;font-size: 16px; font-weight: 600;')
                        if(data.action == 'plus'){
                            $('#coins_' + paper_id).toggleClass('bubble');
                            $('.check_task_answer_' + paper_id).attr('style', 'border: 1.5px solid #008100 !important');                            
                        }
                    }
                    else{
                        document.getElementsByClassName('wrong_answer_alert_' + paper_id)[0].setAttribute('style', 'display:block')
                        $('.check_task_answer_' + paper_id).attr('style', '')
                        document.getElementsByClassName(paper_id + 'solved')[0].setAttribute('style', 'margin-right: 10px; font-size: 16px; font-weight: 600; color: black;');
                        document.getElementsByClassName(paper_id + 'solved_tick')[0].setAttribute('style', 'display:none')
                    }
                }
            });
        }
    });
    $(".open_group_details_urok").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        var table_id = '#' + this_.attr("id") + 'details_urok'
        $(table_id).fadeToggle();
    })
    $(".add_group_btn_urok").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var squadUrl = this_.attr("data-href")
        if (squadUrl) {
            $.ajax({
                url: squadUrl,
                data: {
                    'paper_id':this_.attr("paper_id"),
                    'squad_id':this_.attr("squad_id"),
                    'isin':this_.attr("isin"),
                },
                success: function (data) {
                    if (this_.attr("isin") == 'yes') {
                        this_.css('background-color', '#F2F2F2')
                        this_.css('color', 'black')
                        this_.attr('isin', 'no')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn").css('background-color', '#F2F2F2')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn").css('color', 'black')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn").attr('isin', 'no')

                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results_urok').hide()
                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results').hide()
                    }
                    else {
                        this_.css('background-color', '#5181b8')
                        this_.css('color', 'white')
                        this_.attr('isin', 'yes')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn").css('background-color', '#5181b8')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn").css('color', 'white')
                        $('#' + this_.attr("paper_id") + this_.attr("squad_id") + "add_group_btn").attr('isin', 'yes')

                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results_urok').show()
                        $('.' + this_.attr("paper_id") + this_.attr("squad_id") + 'squad_results').show()
                    }
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    })
})
$(document).ready(function () {
    $(".task_answer").change(function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        var answer = $(this).val();
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                    'answer':answer
                },
                dataType: 'json',
                success: function (data) {
                    this_.attr('placeholder', answer);
                }
            });
        }
    });
    $(document).on("click", '.delete_task', function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':this_.attr("id"),
                },
                dataType: 'json',
                success: function (data) {
                    location.reload()
                }
            });
        }
    });
    $(document).on("click", '.delete_subject_lesson', function () {
        console.log('bb')
        url = $('.delete_lesson_data').attr('url')
        id = $(this).attr('id')
        $.ajax({
            url: url,
            data: {
                'lecture_id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('#subject_lesson' + id).hide('fast');
            }
        })        
    });    
    $(document).on("click", '.change_task_text', function () {
        var this_ = $(this)
        var pageUrl = this_.attr("data-href")
        id = this_.attr("id")
        paper_id = this_.attr("paper_id")
        var text = document.getElementsByClassName('change_task_text' + paper_id)[0].value
        var cost = document.getElementsByClassName('change_task_cost' + paper_id)[0].value

        var answer = ""
        var variant = ""
        if( $(".task_type_" + paper_id).attr("type") == "input" ){
            answer = answer + document.getElementsByClassName('change_task_answer_' + paper_id)[0].value + "&"
        }
        if( $(".task_type_" + paper_id).attr("type") == "test" ){
            for(var i = 0; i < document.getElementsByClassName("option_" + paper_id).length; i++){
                var old_variant = document.getElementsByClassName("option_" + paper_id)[i].getAttribute("value")
                variant = variant + document.getElementsByClassName("variant_value_"+paper_id +'v'+ old_variant)[0].value+"&"
                if(document.getElementsByClassName("option_" + paper_id)[i].checked){
                    answer = answer + document.getElementsByClassName("variant_value_"+paper_id +'v'+ old_variant)[0].value+"&"
                }
            }
        }

        if (pageUrl) {
            $.ajax({
                url: pageUrl,
                data: {
                    'id':id,
                    'text':text,
                    'cost':cost,
                    'answer':answer,
                    'variant':variant,
                },
                dataType: 'json',
                success: function (data) {
                    location.reload()
                }
            });
        }
    });

})
// vmenu2

// $('#toggle').on('ready', function(e) {
//     $('#vmenu2').toggleClass('menu_active')
//     console.log(e)
// })
// $('.image').on("click", function(e) {
//     console.log(e)
// })

// $('.menu-btn').on('click', function(e) {
//   e.preventDefault();
//   this_ = $('.vmenu')
//   if ( this_.attr('stage') == 'passive' ){
//       this_.attr('stage', 'active');
//       this_.toggleClass('menu_active');
//       $('.contenttt').toggleClass('content_active');
//   }
//   else{
//       this_.attr('stage', 'passive');
//       document.getElementById("contenttt").classList.remove('content_active');
//       document.getElementById("vmenu2").classList.remove('menu_active');
//   }
// })
// $('.menu_back').on('click', function(e) {
//   e.preventDefault();
//   this_ = $('.vmenu')
//   if ( this_.attr('stage') == 'active' ){
//       this_.attr('stage', 'passive');
//       document.getElementById("contenttt").classList.remove('content_active');
//       document.getElementById("vmenu2").classList.remove('menu_active');
//   }
// })

