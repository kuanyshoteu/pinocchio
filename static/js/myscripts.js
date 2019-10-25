    $('.subject_period').click(function(e) {
        $('.subject_period').removeClass('green')
        $(this).addClass('green')
        newstatus = $(this).attr('status')
        $('.get_subject_period').attr('value', newstatus)
    })
    $('.download_report').click(function(e) {
        url = $(this).attr('url');
        first_report = $('.first_report').val();
        second_report = $('.second_report').val();
        $.ajax({
            url: url,
            data: {
                'first_report':first_report,
                'second_report':second_report,
            },
            dataType: 'json',
            success: function (data) {
            }
        })
    })
    $('.get_manager_actions').click(function(e) {
        url = $(this).attr('url')
        id = $(this).attr('id')
        $('#manager_actions'+id).modal('show')
        $.ajax({
            url: url,
            data: {
                "id":id,
            },
            dataType: 'json',
            success: function (data) {
                prof = 'Менеджер'
                if (data.student) {
                    prof = 'Студент'
                }
                $('.set_manager_actions'+id).empty()
                res = data.res
                table = ''
                for (var i = res.length-1; i >=0 ; i--) {
                    crnt = '<td class="border">'+res[i][0]+'</td>'
                    crnt += '<td class="border">'+res[i][1]+'</td>'
                    crnt += '<td class="border">'+res[i][2]+'</td>'
                    table += '<tr style="color: #222;"> '+crnt+' </tr>'
                }
                $('<table id="keywords" cellspacing="0" cellpadding="0" style="color: #222;">'+
                    ' <thead> <tr style="color: #222;"> <th>'+prof+'</th> <th>Время</th> <th>Действие</th> </tr>'+
                    ' </thead> <tbody> '+table+
                    ' </tbody> </table>').appendTo('.set_manager_actions'+id)
            }
        })
    })
    $('.make_zaiavka_new').click(function(e) {
        url = '/api/make_zaiavka/'
        id = $(this).attr('id')
        name = $('.zaiavka_name').val()
        phone = $('.zaiavka_phone').val()
        course = $(this).attr('course')
        $.ajax({
            url: url,
            data: {
                "id":id,
                "name":name,
                "phone":phone,
                "course":course,
            },
            dataType: 'json',
            success: function (data) {
                if (data.ok) {
                    console.log('ok')
                    $('.make_zaiavka').hide()
                    $('.ok_zaiavka').show()
                    $('.ok_zaiavka_new').show()
                }
            }
        })
    })
    $('.make_zaiavka').click(function(e) {
        course = $(this).attr('course')
        if ($(this).attr('status') == 'auth') {
            url = '/api/make_zaiavka/'
            id = $(this).attr('id')
            $.ajax({
                url: url,
                data: {
                    "id":id,
                    "course":course,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.ok) {
                        $('.ok_zaiavka-1').show()
                        $('.make_zaiavka-1').hide()
                        $('.ok_zaiavka' + course).show()
                        $('.make_zaiavka'+course).hide()
                    }
                }
            })
        }
        else{
            $('#zaiavka_modal').modal('show')    
            $('.make_zaiavka_new').attr('course', course)        
        }
    })
    $('.create_school').click(function(e) {
        url = $(this).attr('url');
        $('.not_success_created').hide()
        $('.success_created').hide()
        title = $('.new_school_title').val();
        slogan = $('.new_school_slogan').val();
        name = $('.new_school_name').val();
        phone = $('.new_school_phone').val();
        version = $('.new_school_version').val();
        if (title == '' || slogan == '' || name == "" || phone == "" || version == "") {
            $('.not_success_created').show()
        }
        else{
            $.ajax({
                url: url,
                data: {
                    'title':title,
                    'slogan':slogan,
                    'name':name,
                    'phone':phone,
                    'version':version,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.ok) {
                        $('.success_created').show()
                        title = $('.new_school_title').val('');
                        slogan = $('.new_school_slogan').val('');
                        name = $('.new_school_name').val('');
                        phone = $('.new_school_phone').val('');
                        $('.director_password').text(data.password)
                    }
                }
            })
        }
    })
    $('.create_worker').click(function(e) {
        url = $(this).attr('url');
        $('.not_success_created_worker').hide()
        $('.success_created_worker').hide()
        this_ = document.getElementById('new_worker_prof');
        prof_id = this_.options[this_.selectedIndex].value;
        school = $('.new_worker_school').val();
        name = $('.new_worker_name').val();
        phone = $('.new_worker_phone').val();
        mail = $('.new_worker_mail').val();
        if (school == '' || name == '' || phone == '') {
            $('.not_success_created_worker').show()
        }
        else{
            $.ajax({
                url: url,
                data: {
                    'school':school,
                    'name':name,
                    'phone':phone,
                    'mail':mail,
                    'prof_id':prof_id,
                    'mail':mail,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.ok) {
                        $('.success_created_worker').show()
                        $('.worker_password').text(data.password);
                        $('.create_worker').addClass('disabled')
                    }
                    else{
                        $('.not_success_created_worker').show()
                    }
                }
            })
        }
    })
    $('.worker_saved_password').click(function(e) {
        $('.create_worker').removeClass('disabled');
        $('.new_worker_school').val();
        $('.new_worker_name').val('');
        $('.new_worker_phone').val('');
        $('.new_worker_mail').val('');
    })
    $('.show_money_history').click(function(e) {
        url = $(this).attr('url')
        $('.money_history').modal('show')
        $.ajax({
            url: url,
            data: {
            },
            dataType: 'json',
            success: function (data) {
                for (var i = 0; i < data.res.length; i++) {
                    $('<tr style="color: #222;"><td>'+data.res[i][0]+'</td><td>'+data.res[i][1]+'</td><td>'+data.res[i][2]+'</td>').appendTo('.history_cont')
                }
            }
        })
    })
    $('.new_money_object').click(function(e) {
        url = $(this).attr('url')
        title = $('.new_money_title').val()
        amount = $('.new_money_amount').val()
        $('.success_new_money').hide()
        $.ajax({
            url: url,
            data: {
                'title':title,
                'amount':amount,
            },
            dataType: 'json',
            success: function (data) {
                $('.new_money_title').val('')
                $('.new_money_amount').val('')
                $('.success_new_money').show()
            }
        })
    })
    $('.delete_school_banner').click(function(e) {
        url = $(this).attr('url')
        id = $(this).attr('id')
        $.ajax({
            url: url,
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('#banner'+id).hide('fast')
            }
        })
    })
    $('.save_review').click(function(e) {
        number = $('.result_rating').attr('number')
        url = $(this).attr('url')
        text = $('.review_text').val()
        $.ajax({
            url: url,
            data: {
                'text':text,
                'number':number,
            },
            dataType: 'json',
            success: function (data) {
                if (data.nouser) {
                    $('.review_error').show()
                }
                else{
                    $('.review_error').hide()
                    number = parseInt(number)
                    stars = ''
                    notstars = ''
                    for (var i = 1; i <= number; i++) {
                        stars += '<i class="icon star"></i>'
                    }
                    for (var i = number+1; i <= 5; i++) {
                        notstars += '<i class="icon star"></i>'
                    }
                    rev='<div class="schoolLanding__content-review-comment__rating"> <span class="organization__info-rating-icon active">'+
                    stars+'</span> <span class="organization__info-rating-icon"> '+notstars+
                    ' </span> </div> <div class="schoolLanding__content-review-comment__text"> '+text+
                    ' </div> <div class="schoolLanding__content-review-comment__about"> <span class="schoolLanding__content-review-comment__about-left"> <span class="schoolLanding__content-review-comment__about-name">'+data.name+'</span> <span class="schoolLanding__content-review-comment__about-date">'+data.timestamp+'</span> </span> </div>'
                    $(rev).appendTo('.schoolLanding__content-review-comment')
                    $('.review_text').val('')
                    $('.wright_review').hide()
                    $('.thanks_review').show()
                }
            }
        })
    })
    $('.make_review').click(function(e) {
        number = parseInt($(this).attr('number'))
        $('.result_rating').attr('number', number)
        for (var i = 0; i <= number; i++) {
            $('#star'+i).attr('style', 'color: #D4C14A;')
        }
        for (var i = number+1; i <= 5; i++) {
            $('#star'+i).attr('style', '')
        }
        $('.wright_review').show()
    })
    $('.save_office_cabinet').click(function(e) {
        url = $(this).attr('url')
        id = $(this).attr('id')
        status = $(this).attr('status')
        title = $('.office_cabinet_create_title'+id).val()
        capacity = $('.office_cabinet_create_capacity'+id).val()
        type = ''
        if (status != '') {
            type = 'moderator'
        }
        $.ajax({
            url: url,
            data: {
                'title':title,
                'id':id,
                'capacity':capacity,
                'mod_school_id':status,
                'type':type
            },
            dataType: 'json',
            success: function (data) {
                console.log('ffff')
                $('<div class="four wide column highlight" style="margin-right: 7px;margin-bottom: 7px;">'+title+' </div>').appendTo('.office_cabinets'+id)
            }
        })        
    });
    $('.save_school_title').click(function(e) {
        url = $(this).attr('url')
        if ($('.check_moderator').attr('status')=='True') {
            url = url + '?type=moderator&mod_school_id='+$('.day_id').attr('group_id')
        }
        id = $(this).attr('id')
        status = $(this).attr('status')
        if (status == 'worktime') {
            part1 = $('.school_'+status+'_edit1').val()
            part2 =  $('.school_'+status+'_edit2').val()
            if (part1 == '' || part2 == '') {
                text = 'По предварительной записи'
            }
            else{
                text = part1+'-'+part2
            }
        }
        else{
            text = $('.school_'+status+'_edit').val()
        }
        $.ajax({
            url: url,
            data: {
                'text':text,
                'id':id,
                'status':status
            },
            dataType: 'json',
            success: function (data) {
                $('.school_'+status+'_form')
                $('.school_'+status+'_form').hide();
                $('.school_'+status).text(text);
            }
        })        
    });
    $('.login-btn').click(function(e) {
        url = '/api/login/'
        username = $('.username').val()
        password = $('.password').val()
        $('.wrong_login').hide()
        $.ajax({
            url: url,
            data: {
                'username':username,
                'password':password
            },
            dataType: 'json',
            success: function (data) {
                if (data.res == 'login') {
                    location.reload()
                }
                else if (data.res == 'error'){
                    $('.wrong_login').show()
                }
            }
        })        
    });
    $('.register-btn').click(function(e) {
        url = '/api/register/'
        name = $('.new_name').val()
        phone = $('.new_username').val()
        mail = $('.new_mail').val()
        new_password = $('.new_password').val()
        new_password2 = $('.new_password2').val()
        console.log(name, phone, mail)
        if (name.length > 0 && phone.length > 0 && mail.length > 0 && new_password.length > 0 && new_password==new_password2) {        
            $.ajax({
                url: url,
                data: {
                    'name':name,
                    'phone':phone,
                    'mail':mail,
                    'password1':new_password,
                    'password2':new_password2,
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data.res)
                    if (data.res == 'ok') {
                        $('.reg_wrong_phone').hide()
                        $('.reg_fill_all').hide()
                        $('.reg_wrong_pass').hide()
                        location.reload()
                    }
                    else if (data.res == 'second_user'){
                        $('.reg_wrong_phone').show()
                    }
                    else if (data.res == 'not_equal_password'){
                        $('.reg_wrong_pass').show()
                    }
                }
            })
        }
        else{
            $('.reg_fill_all').show()
        }
    });
    $('.login-btn2').click(function(e) {
        url = '/api/login/'
        username = $('.username2').val()
        password = $('.password2').val()
        $.ajax({
            url: url,
            data: {
                'username':username,
                'password':password
            },
            dataType: 'json',
            success: function (data) {
                if (data.res == 'login') {
                    $('.wrong_login').hide()
                    location.reload()
                }
                else if (data.res == 'error'){
                    $('.wrong_login').show()
                }
            }
        })        
    });
    $('.register-btn2').click(function(e) {
        url = '/api/register/'
        name = $('.new_name2').val()
        phone = $('.new_username2').val()
        mail = $('.new_mail2').val()
        new_password = $('.new_password22').val()
        new_password2 = $('.new_password222').val()
        console.log(name, phone, mail, new_password, new_password2)
        if (name.length > 0 && phone.length > 0 && mail.length > 0 && new_password.length > 0 && new_password==new_password2) {        
            $.ajax({
                url: url,
                data: {
                    'name':name,
                    'phone':phone,
                    'mail':mail,
                    'password1':new_password,
                    'password2':new_password2,
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data.res)
                    if (data.res == 'ok') {
                        $('.reg_wrong_phone').hide()
                        $('.reg_fill_all').hide()
                        $('.reg_wrong_pass').hide()
                        location.reload()
                    }
                    else if (data.res == 'second_user'){
                        $('.reg_wrong_phone').show()
                    }
                    else if (data.res == 'not_equal_password'){
                        $('.reg_wrong_pass').show()
                    }
                }
            })
        }
        else{
            $('.reg_fill_all').show()
        }
    });
    $('.update_pswd-btn').click(function(e) {
        url = '/api/update_pswd/'
        mail = $('.update_pswd_mail').val()
        $('.loading').show()
        $(this).addClass('disabled')
        $.ajax({
            url: url,
            data: {
                'mail':mail,
            },
            dataType: 'json',
            success: function (data) {
                if (data.ok) {
                    $('.wrong_mail_update_pswd').hide()
                    $('.ok_update_pswd').show()
                }
                else{
                    $('.wrong_mail_update_pswd').show()
                    $('.ok_update_pswd').hide()
                }
                $('.loading').hide()
            }
        })        
    });
    $('.reset_pswd').click(function(e) {
        url = '/api/reset_pswrd/'
        password1 = $('.reset_password1').val()
        password2 = $('.reset_password2').val()
        id = $(this).attr('id')
        $.ajax({
            url: url,
            data: {
                'password1':password1,
                'password2':password2,
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        })        
    });
    $('.show_free_cards').click(function(e) {
        url = $(this).attr('url')
        checked = $(this).prop('checked')
        $.ajax({
            url: url,
            data: {
                'check':checked,
            },
            dataType: 'json',
            success: function (data) {
                location.reload()
            }
        })        
    });
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
                $('#card_container' + id).hide('fast');
            }
        })        
    });
    $('.save_salary').click(function(e) {
        url = $('.salary_url').attr('url')
        id = $(this).attr('id')
        this_ = $(this)
        salary = $('#salary' + id).val();
        $.ajax({
            url: url,
            data: {
                'id':id,
                'salary':salary,
            },
            dataType: 'json',
            success: function (data) {
                $('#input' + id).hide();
                $('#salary_show' + id).show();
                $('#salary_show_value'+id).text(salary)
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
    $('.open_card_form').click(function(e) {
        $('#card_form'+$(this).attr('id')).modal('show')
    })
    $('.change_mode').click(function(e) {
        if ($('.dataconst').attr('page_mode') == 'norm') {
            $('.body').addClass('oveflowy_h')
            $('.schedule_body').removeClass('oveflowx_h')
            $('.schedule_body').addClass('oveflowx_a')
            $('#group-details').addClass('oveflowy_h')
            $('.content-container').addClass('oveflowy_h') 
            $('.dataconst').attr('page_mode', 'horz')           
        }
        else{
            $('.body').removeClass('oveflowy_h')
            $('.schedule_body').addClass('oveflowx_h')
            $('.schedule_body').removeClass('oveflowx_a')
            $('#group-details').removeClass('oveflowy_h')
            $('.content-container').removeClass('oveflowy_h') 
            $('.dataconst').attr('page_mode', 'norm')            
        }
    })
    $('.add_card').click(function(e) {
        var id = $(this).attr("id")
        var name = $('.new_card_name' + id).val()
        var phone = $('.new_card_phone' + id).val()
        var mail = $('.new_card_mail' + id).val()
        var comment = $('.new_card_comment' + id).val()
        $('.alreadyregistered').hide()
        ok = false
        if (mail != '') {
            for (var i = mail.length - 1; i >= 0; i--) {
                if (mail[i] == '@') {
                    ok = true;
                    break;
                } 
            }            
        }
        else{
            ok = true;
        }
        if (ok) {
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
                    if (data.already_registered) {
                        $('.alreadyregistered'+id).show()
                    }
                    else{
                        location.reload()                        
                    }
                    // card_id = data.card_id; 
                    // var element = $('<div style="padding: 5px 0" id="card_container'+card_id+'" is_saved="'+data.is_saved+
                    //     '"><div id="card'+card_id+'" class="ui segment full-w crm_card mine" ondragstart="save_card_id('
                    //     +"'"+card_id+"'"+", "+"'"+data.card_name+"'"+')" draggable="true" column_id="'
                    //     +id+'"> <div onclick="open_crmcard('+"'"+card_id+"'"+')" style="width: 80%;display: inline-block;">'+
                    //     '<a onclick="delete_card('+"'"+card_id+"'"+')" class="delete_card" id="'
                    //     +card_id+'"><b>×</b></a><span style="font-weight: 600;color:#285473;">'
                    //     +data.card_name+'</span><div style="color: darkgrey;font-size: 12px;">'
                    //     +data.card_phone+' </div></div><div style="width: 20%;display: inline-block;float: right;margin-top: 20px;">'+
                    //     '<a class="show_card_schedule" onclick="openNav('+"'"+card_id+"'"+', '+"'"+data.card_name+
                    //     "'"+')"><i class="icon table green"></i></a></div>'+
                    //     '<div style="width: 100%;"><a class="nouser{{card.id}}" href="'+
                    //     data.author_url+'" style="color: darkblue;font-size: 11px">'+data.author_profile+'</a> </div></div></div>');
                    // element.appendTo('.crmbox' + id)
                    // $('#new_card_form'+id).modal('hide')
                    // var form = $('<div class="ui modal large" style="margin-top: 10%;min-height: 100%;" id="card_form'+data.card_id+'"> <i class="close icon"></i> <div class="content"> <form class="ui form" method="POST" enctype="multipart/form-data"> <div class="ui grid stackable"> <div class="six wide column"> <textarea class="card_name'+data.card_id+'" placeholder="Имя">'+data.card_name+'</textarea> <textarea class="card_phone'+data.card_id+'" placeholder="Телефон">'+data.card_phone+'</textarea> <textarea class="card_mail'+data.card_id+'" placeholder="Почта">'+data.card_mail+'</textarea> </div> <div class="ten wide column"> <textarea class="card_comment'+data.card_id+'" placeholder="Комментарий">'+data.card_comment+'</textarea> </div> <div class="sixteen wide column center aligned"> <a class="ui button blue tiny" onclick="edit_card('+data.card_id+')" id="'+data.card_id+'">Сохранить</a> </div> <div class="sixteen wide column"> <div class="ui divider full-w"></div> <div style="color: #222;font-weight: 600;text-align: center;font-size: 14px;">История изменений</div> </div> <div class="sixteen wide column cardhistory'+data.card_id+'" style="color: #6b6d72;font-size: 12px;"> </div> </div> </form> </div> </div>');
                    // form.appendTo('.crmbox' + id)
                }
            })        
        }
        else{
            $('.wrong_mail_error'+id).show()
            console.log('sdfsdf', id)
        }
    });
    update_schedule_lectures();
    function update_schedule_lectures(){
        var sum_width = 0;
        $(".lecture_const").each(function() {
            console.log('running')
            interval = parseInt($('.dataconst').attr('interval'))
            if ($(this).attr('height')) {
                height = (60/interval)*((parseFloat($(this).attr('height').replace(",", ".")))*28);            
            }
            time = $(this).attr('time');
            id = $(this).attr('id');
            hour = parseInt($(this).attr('hour')) * 28;
            minute = parseInt($(this).attr('minute'));
            day = $(this).attr('day');
            topp = (60/interval)*(hour + 2) + 28 * minute / interval + 40;
            count = 1
            $('.wait'+ day).each(function() {
                if ($(this).attr('id') != id) {
                    hour2 = parseInt($(this).attr('hour')) * 28;
                    minute2 = parseInt($(this).attr('minute'));
                    topp2 = (60/interval)*(hour2 + 2) + 28 * minute2 / interval + 40;
                    height2 = (60/interval)*((parseFloat($(this).attr('height').replace(",", ".")))*28);
                    down2 = topp2+height2
                    friends = $('.dataconst').attr('friends')
                    $('.dataconst').attr('friends', friends+ 'd'+down2 )
                    friends = $('.dataconst').attr('friends')
                    if ((topp2 < topp + height && topp2 >= topp) || (down2>topp&&down2<= topp + height)) {
                        if (friends.indexOf('d'+topp2) == -1) {
                            count += 1
                        }
                    }
                }
            })
            $('.dataconst').attr('friends', '')
            maxcount = count
            dayp1 = parseInt(day) + 1
            if (parseInt($('.dataconst').attr('max'+dayp1)) < count ) {
                $('.dataconst').attr('max'+dayp1, count)
            }
            else{maxcount = parseInt($('.dataconst').attr('max'+dayp1))}
            $('#constday'+day).css('width', 100*maxcount);

            sum = 0
            for (var i = 1; i < dayp1; i++) {
                sum += parseInt($('.dataconst').attr('max' + i))
            }
            $('.constback'+dayp1).css('margin-left', sum*100+53);        
            $('.constback'+dayp1).css('width', 100*maxcount);
            $('.schedule_lines').css('width', sum*100+53+100*maxcount)
            left = 55 + (sum-1)*100 + 100*count;
            oldleft = parseInt($(this).css('margin-left'));
            oldtop = parseInt($(this).css('margin-top'));
            $(this).css('margin-top', oldtop+topp);
            $(this).css('margin-left', oldleft+left);
            if ($(this).attr('height')) {
                $(this).css('height', height);
            }
            $(this).removeClass('wait' + day);
        });
        return 'ended'
    }
    $('.crm_option').on('change', function(e) {
        id = $(this).attr('id')
        this_ = document.getElementById(id);
        object_id = this_.options[this_.selectedIndex].value;
        url = $(this).attr('url')
        option = $(this).attr('option')
        $('.loading').show()
        $.ajax({
            url: url,
            data: {
                'object_id':object_id,
                'option':option,
            },
            dataType: 'json',
            success: function (data) {
                if ($('.data_update').attr('status')=='yes') {
                    location.reload()
                }
                else{
                    $( "#calendar" ).load(document.URL +  ' #calendar', function(){
                        x = update_schedule_lectures()
                    });
                }
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
    $('.change_squad_office').on('change', function(e) {
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
    $('.continue').click(function (event){
        $(this).hide()
        $(".continue_div").show()
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
                    $('.grade'+id).removeClass('green')
                    this_.addClass('green')
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

