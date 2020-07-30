$(document).ready(function () {
    $('.squad_office_filter').on('change', function(e) {
        filter_squads()
    })
    filter_squads()
    async function filter_squads(){
        obj = $('.squad_filter.green').attr('option')
        if (obj == 'all') {
            $('.sq_all').show()
        }
        else{
            $('.sq_all').hide()
            squad_office = $('.squad_office_filter option:selected').val()
            if (obj == 'regular') {
                $('.online_False').show()
                $('.ind_False').show()            
            }
            else if (obj == 'online') {
                $('.online_True').show()
            }
            else if (obj == 'individual') {
                $('.ind_True').show()
            }
            if (obj == 'empty') {
                $('.empty_True').show()
            }
            else{
                $('.empty_True').hide()                
            }
        }
    }
    async function change_squad_filter(obj){
        console.log('obj', obj)
        $('.squad_filter').removeClass('green')
        $('.squad_filter').addClass('white')
        $('.'+obj+'_filter').addClass('green')
        $('.'+obj+'_filter').removeClass('white')        
    }
    $('.squad_filter').click(async function(e){
        await change_squad_filter($(this).attr('option'))
        filter_squads()
    })
    $('.subject_cat_filter').on('change', function(e) {
        filter_subjects()
    })
    filter_subjects()
    async function filter_subjects(){
        obj = $('.subject_filter.green').attr('option')
        if (obj == 'all') {
            $('.catall').show()
        }
        else{
            $('.catall').hide()
            if (obj == 'regular') {
                $('.online_False').show()
                $('.ind_False').show()            
            }
            else if (obj == 'online') {
                $('.online_True').show()
            }
            else if (obj == 'individual') {
                $('.ind_True').show()
            }
        }
    }
    async function change_subject_filter(obj){
        console.log('obj', obj)
        $('.subject_filter').removeClass('green')
        $('.subject_filter').addClass('white')
        $('.'+obj+'_filter').addClass('green')
        $('.'+obj+'_filter').removeClass('white')        
    }
    $('.subject_filter').click(async function(e){
        await change_subject_filter($(this).attr('option'))
        filter_subjects()
    })
    $('.online_option').click(function(e) {
        url = $('.data').attr('online_option_url')
        id = $('.data').attr('id')
        option = $(this).attr('option')
        $('.online_option_load').addClass('active')
        $.ajax({
            url: url,
            data: {
                'id':id,
                'option':option,
            },
            dataType: 'json',
            success: function (data) {
                $('.online_option_load').removeClass('active')
                $('.online_option').removeClass('green')
                $('.online_option').addClass('white')
                $('.online_option_'+option).addClass('green')
                $('.online_option_'+option).removeClass('white')
            }
        })
    })
    $('.individual_option').click(function(e) {
        url = $('.data').attr('individual_option_url')
        id = $('.data').attr('id')
        option = $(this).attr('option')
        $('.individual_option_load').addClass('active')
        $.ajax({
            url: url,
            data: {
                'id':id,
                'option':option,
            },
            dataType: 'json',
            success: function (data) {
                $('.individual_option_load').removeClass('active')
                $('.individual_option').removeClass('green')
                $('.individual_option').addClass('white')
                $('.individual_option_'+option).addClass('green')
                $('.individual_option_'+option).removeClass('white')
            }
        })
    })
    $('.right_option').click(function(e) {
        id = $(this).attr('id')
        $('.officefilter').hide()
        $('.office'+id).show()
        $('.right_option').removeClass('shadow_small')
        $(this).addClass('shadow_small')
    })
    $('.choose_color').click(function(e) {
        url = $('.choose_color_def').attr('url')
        id = $(this).attr('id')
        $.ajax({
            url: url,
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                $('.choose_color_def').css('background-color', id)
            }
        })
    })
    $('.make_alive').click(function(e) {
        this_ = $(this)
        url = this_.attr('url')
        id = this_.attr('id')
        $.ajax({
            url: url,
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                this_.hide()
                $('.success_alive'+id).show()
            }
        })
    })
    $('.constday_choose').click(function(e) {
        if ($(this).attr('class').indexOf("green") >= 0){
            $(this).removeClass('green')
        }
        else{
            $(this).addClass('green')            
        }
    })
    $('.search_group_show').on('click', function(e) {
        $('.hint_students_group').show()
    })
    $('.search_students_group').on('input', function(e) {
        text = $(this).val()
        url = $(this).attr('url')
        if (text.length == 0) {
            $('.hint_students_group').hide() 
        }
        else{
            $.ajax({
                url: url,
                data: {
                    'text':text,
                },
                dataType: 'json',
                success: function (data) {
                    $('.hint_students_group').show()
                    $('.hint_students_group').empty()                
                    console.log(data.res)
                    for (var i = 0; i < data.res.length; i++) {
                        id = data.res[i][0]
                        name = data.res[i][1]
                        image = data.res[i][2]
                        check = '<i class="icon check circle green studenticon'+id+'" style="display:none;"></i>'
                        sign = '+'
                        if (data.res[i][3]) {
                            check = '<i class="icon check circle green studenticon'+id+'"></i>'
                            sign = '-'
                        }
                        $('<div class="search_group_link"> <img class="search-group-img" src="'+image+'" alt="photo"> <span class="search-group-name">'+name+'</span> '+check+' <a class="ui button mini blue add_student add_student'+id+' search_group_add" onclick="add_student('+"'"+id+"'"+')" id="'+id+'">'+sign+'</a> </div>').appendTo('.hint_students_group')
                    }
                }
            })
        }
    });
    $('.start_searching_groups').on('input', function(e) {
        text = $(this).val()
        url = $(this).attr('url')
        if (text.length == 0) {
            $('.show_search_groups').hide() 
        }
        else{
            $.ajax({
                url: url,
                data: {
                    'text':text,
                },
                dataType: 'json',
                success: function (data) {
                    $('.show_search_groups').show()
                    $('.show_search_groups').empty()
                    for (var i = 0; i < data.res.length; i++) {
                        title = data.res[i][0]
                        url = data.res[i][1]
                        $('<div class="full-w "><a style="text-align:left;" href="'+url+'" class="no_padding ui button blue full-w search-item"> <span class="search-group-name">'+title+'</span> </a></div>').appendTo('.show_search_groups')
                    }
                }
            })
        }
    });
    $('.start_searching_subjects').on('input', function(e) {
        text = $(this).val()
        url = $(this).attr('url')
        if (text.length == 0) {
            $('.show_search_subjects').hide() 
        }
        else{
            $.ajax({
                url: url,
                data: {
                    'text':text,
                },
                dataType: 'json',
                success: function (data) {
                    $('.show_search_subjects').show()
                    $('.show_search_subjects').empty()
                    for (var i = 0; i < data.res.length; i++) {
                        title = data.res[i][0]
                        url = data.res[i][1]
                        image = data.res[i][2]
                        if (image == '') {
                            image = '/static/images/squad.png'
                        }
                        $('<div class="full-w "><a style="text-align:left;" href="'+url+'" class="full-w search-item textw ui button small blue pt5 pb5 pl10 pr10"><span class="search-group-name">'+title+'</span> </a></div>').appendTo('.show_search_subjects')
                    }
                }
            })
        }
    });
    $('.det').on('click', function(e) {
        this_ = $(this)
        console.log('work0')
        $.ajax({
            url: 'http://www.pinocchio.kz/subjects/api/squad_list/26/',
            method: "GET",
            data: {
            },
            success: function (data) {
                document.getElementById('detder').innerHTML = data.calendar;
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.change_teacher').on('change', function(e) {
        this_ = document.getElementById("change_teacher");
        teacher_id = this_.options[this_.selectedIndex].value
        $.ajax({
            url: this_.getAttribute('url'),
            method: "GET",
            data: {
                'teacher_id':teacher_id,
                'squad_id':this_.getAttribute('squad_id'),
            },
            success: function (data) {
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.day_window').on('click', function(e) {
        e.preventDefault();
        this_ = $(this)
        $('.day_id').attr('id', this_.attr('id'))
    });
    $('.add_squad_to_subject').on('click', function(e) {
        var url = $(this).attr('data-href');
        var subject_id = $(this).attr('id');
        select = document.getElementsByClassName('selecttt')[0]
        var squad_id = select.options[select.selectedIndex].value
        $.ajax({
            url: url,
            method: "GET",
            data: {
                'subject_id':subject_id,
                'squad_id':squad_id,
            },
            success: function (data) {
                location.reload()
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.delete_squad_from_subject').on('click', function(e) {
        var url = $(this).attr('data-href');
        var squad_id = $(this).attr('squad_id');
        var subject_id = $('.instance_id').attr('id')
        $.ajax({
            url: url,
            method: "GET",
            data: {
                'subject_id':subject_id,
                'squad_id':squad_id,
            },
            success: function (data) {
                location.reload()
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.set_squad_time').on('click', function(e) {
        var url = $(this).attr('data-href');
        var day = $(this).attr('day');
        var time = $(this).attr('time');
        var id = 'check' + day + time;
        var checked = document.getElementById(id).checked
        var instance_id = $('.instance_id').attr('id');
        $.ajax({
            url: url,
            method: "GET",
            data: {
                'day':day,
                'time':time,
                'checked':checked,
                'instance_id':instance_id,
            },
            success: function (data) {
                location.reload()
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.remove_lesson_from_subject').on('click', function(e) {
        var material_id = $(this).attr('material_id');
        var lesson_id = $(this).attr('lesson_id');
        var url = $(this).attr('url');
        $.ajax({
            url: url,
            method: "GET",
            data: {
                'material_id':material_id,
                'lesson_id':lesson_id,
            },
            success: function (data) {
                $("#lesson_in_material" + material_id + 'l' + lesson_id).hide('fast')
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.open_time_lessons').on('click', function(e) {
        id = $(this).attr('id')
        if ($(this).attr('status') == 'closed'){
            $('#time_lessons' + id).show('fast')
            $(this).attr('status', 'opened')
            // $('#icondown' + id).show()
            // $('#iconright' + id).hide()
        }
        else{
            $('#time_lessons' + id).hide('fast')
            $(this).attr('status', 'closed')
            // $('#icondown' + id).hide()
            // $('#iconright' + id).show()
        }
    });
    $('.open_option').on('click', function(e) {
        for (var i = 0; i < document.getElementsByClassName("option").length; i++){
            document.getElementsByClassName("option")[i].setAttribute('style', 'display:none;')
            document.getElementsByClassName("open_option")[i].setAttribute('class', 'open_option other_option')
        }
        var id = $(this).attr('name')
        $('#' + id).show()
        $(this).attr('class', 'open_option current_option')
    });
    $('.open_option2').on('click', function(e) {
        for (var i = 0; i < document.getElementsByClassName("option2").length; i++){
            document.getElementsByClassName("option2")[i].setAttribute('style', 'display:none;')
            document.getElementsByClassName("open_option2")[i].setAttribute('class', 'open_option2 other_option2')
        }
        var id = $(this).attr('name')
        $('#option2' + id).show()
        $(this).attr('class', 'open_option2 current_option2')
    });
    
    $('.add_paper').on('click', function(e) {
        this_ = $(this)
        var day_id = $('.day_id').attr('id');
        var paper_id = this_.attr('id');
        var group_id = $('.day_id').attr('group_id');
        url = this_.attr('data-href');
        $.ajax({
            url: url,
            method: "GET",
            data: {
                'day_id':day_id,
                'paper_id':paper_id,
                'group_id':group_id,
            },
            success: function (data) {
                location.reload()
                // segment = document.getElementById('lesson_list' + day_id)
                // if(document.getElementById('pusto' + day_id)){
                //     document.getElementById('pusto' + day_id).remove()
                // }
                // var title = document.createElement('span');
                // title.innerHTML = this_.attr('title');
                // var a = document.createElement('a');
                // a.setAttribute('href', data.href)
                // a.appendChild(title);
                // var div = document.createElement('div');
                // div.setAttribute('style', 'padding-top:10px;')
                // div.appendChild(a);

                // segment.appendChild(div);                    
                
                // $('#materials').modal('toggle');
            }, error: function (error) {
                console.log('error')
            }
        })
    });
    $(".open_folder").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        id = this_.attr('id')
        title = this_.attr('title')
        paper_title = document.getElementsByClassName('parent_title')[0]
        paper_title.innerHTML = this_.attr('title')
        span = document.createElement('span');
        span.setAttribute('class', 'parent_folder_id')
        span.setAttribute('parentId', id)
        span.setAttribute('parentTitle', title)
        span.setAttribute('style', 'display:none;')
        data_div = document.getElementsByClassName('data')[0]
        data_div.appendChild(span)
        $('.back_to_parent').show()
        console.log(this_.attr('title'))
        for (i = 0; i < document.getElementsByClassName('paper').length; i++){
            paper = document.getElementsByClassName('paper')[i]
            if(paper.getAttribute('parent') == id){
                paper.setAttribute('style', 'display:block')
            }
            else{
                paper.setAttribute('style', 'display:none')
            }
        }
        for (i = 0; i < document.getElementsByClassName('folder').length; i++){
            folder = document.getElementsByClassName('folder')[i]
            if(folder.getAttribute('parent') == id){
                folder.setAttribute('style', 'display:block')
            }
            else{
                folder.setAttribute('style', 'display:none')
            }
        }
    });
    $(".back_to_parent").click(function (event) {
        event.preventDefault();
        var this_ = $(this)
        number_of_last = document.getElementsByClassName('parent_folder_id').length - 1
        last_span = document.getElementsByClassName('parent_folder_id')[number_of_last]
        last_span.remove()
        pre_last_span = document.getElementsByClassName('parent_folder_id')[number_of_last-1]
        id = pre_last_span.getAttribute('parentId')
        if(id == 'none'){
            this_.hide()
        }
        console.log(number_of_last, pre_last_span, id)
        paper_title = document.getElementsByClassName('parent_title')[0]
        paper_title.innerHTML = pre_last_span.getAttribute('parentTitle')
        
        for (i = 0; i < document.getElementsByClassName('paper').length; i++){
            paper = document.getElementsByClassName('paper')[i]
            if(paper.getAttribute('parent') == id){
                paper.setAttribute('style', 'display:block')
            }
            else{
                paper.setAttribute('style', 'display:none')
            }
        }
        for (i = 0; i < document.getElementsByClassName('folder').length; i++){
            folder = document.getElementsByClassName('folder')[i]
            if(folder.getAttribute('parent') == id){
                folder.setAttribute('style', 'display:block')
            }
            else{
                folder.setAttribute('style', 'display:none')
            }
        }
    });
    $(".change-btn").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var changeUrl = this_.attr("data-href")
        var id2 = "#" + this_.attr("id2")
        var inpt = '.' + this_.attr("id2")
        if (changeUrl) {
            $.ajax({
                url: changeUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    if (this_.attr("value2") == 'free') {
                        $(id2).css('background-color', '#5181b8')
                        $(id2).attr('value2', 'busy')
                        $(inpt).attr('name', this_.attr("id2") + 'busy')
                    }
                    else {
                        $(id2).css('background-color', '#F2F2F2')
                        $(id2).attr('value2', 'free')
                        $(inpt).attr('name', this_.attr("id2") + 'free')
                    }
                }, error: function (error) {
                    console.log('error')
                }

            })
        }
    });
    $(".follow_btn").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        console.log('de')
        var regUrl = this_.attr("data-href")
        if (regUrl) {
            $.ajax({
                url: regUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    console.log(data.reg)
                    if (data.reg) {
                        $(".follow_btn").text('Отписаться')
                        $(".follow_btn").attr('class', 'ui button tiny follow_btn red')
                    }
                    else {
                        $(".follow_btn").text('Записаться')
                        $(".follow_btn").attr('class', 'ui button tiny follow_btn green')
                    }
                }, error: function (error) {
                    console.log(error)
                }
            })
        }
    });
    $(".leftt").click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        current_id = parseInt($('.week_id').attr('id'))
        id = current_id - 1;
        var max_week = $('.max_week').attr('id')
        if(id > 0){
            $('.week_id').attr('id', id)
            $('#week' + current_id).attr('style', 'display:none')
            $('#week' + id).show()
        }    
    });
    $(".rightt").click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        current_id = parseInt($('.week_id').attr('id'))
        id = current_id + 1;
        if( id <= parseInt( $('#calendar').attr('length') ) ){
            $('.week_id').attr('id', id)
            $('#week' + current_id).attr('style', 'display:none')
            $('#week' + id).show();
        }    
    });
    $(".lefttt").click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        def=$('.weekhead_id'+this_.attr('id')).attr('def')
        weekhead_current_id=parseInt($('.weekhead_id'+this_.attr('id')).attr('id'))
        weekhead_id=weekhead_current_id -1
        if(weekhead_id > 0){
            $('#weekhead'+def+weekhead_id).show('fast')
            $('#weekhead'+def+weekhead_current_id).hide()
            $('.weekhead_id'+this_.attr('id')).attr('id',weekhead_id)
            console.log(def+weekhead_current_id, weekhead_id)
            list = document.getElementsByClassName('week_id'+this_.attr('id'))
            for(var i=0; i<list.length;i++){
                current_id = parseInt(list[i].getAttribute('id'))
                id = current_id - 1;
                if(id > 0){
                    list[i].setAttribute('id', id)
                    document.getElementsByClassName('week'+ list[i].getAttribute('def') + current_id)[0].setAttribute('style', 'display:none')
                    document.getElementsByClassName('week'+list[i].getAttribute('def') + id)[0].setAttribute('style', 'display:block')
                }
            }
        }
    });
    $(".righttt").click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        def=$('.weekhead_id'+this_.attr('id')).attr('def')
        weekhead_current_id=parseInt($('.weekhead_id'+this_.attr('id')).attr('id'))
        weekhead_id=weekhead_current_id +1
        if(weekhead_id <= parseInt( $('#paper'+this_.attr('id')).attr('length') ) ) {
            $('#weekhead'+def+weekhead_id).show('fast')
            $('#weekhead'+def+weekhead_current_id).hide()
            $('.weekhead_id'+this_.attr('id')).attr('id',weekhead_id)
            console.log(def+weekhead_current_id, weekhead_id)
            list = document.getElementsByClassName('week_id'+this_.attr('id'))
            for(var i=0; i<list.length;i++){
                current_id = parseInt(list[i].getAttribute('id'))
                id = current_id + 1;
                if(id <= parseInt( $('#paper'+this_.attr('id')).attr('length') )) {
                    list[i].setAttribute('id', id)
                    document.getElementsByClassName('week'+ list[i].getAttribute('def') + current_id)[0].setAttribute('style', 'display:none')
                    document.getElementsByClassName('week'+list[i].getAttribute('def') + id)[0].setAttribute('style', 'display:block')
                }
            }
        }    
    });
})