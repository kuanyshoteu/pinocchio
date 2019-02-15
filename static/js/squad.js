$(document).ready(function () {
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
    $('.start').on('change', function(e) {
        this_ = $(this)
        $.ajax({
            url: this_.attr('url'),
            method: "GET",
            data: {
                'date':document.getElementsByClassName("start")[0].value,
                'subject_id':this_.attr('subject_id'),
            },
            success: function (data) {
            }, 
            error: function (error) {
                console.log('error')
            }
        })
    });
    $('.end').on('change', function(e) {
        this_ = $(this)
        $.ajax({
            url: this_.attr('url'),
            method: "GET",
            data: {
                'date':document.getElementsByClassName("end")[0].value,
                'subject_id':this_.attr('subject_id'),
            },
            success: function (data) {
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
                'subject_id':this_.getAttribute('subject_id'),
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
    $('.open_mysquads').on('click', function(e) {
        $('.allsquads').hide()
        $('.mysquads').show()
        $(this).attr('class', 'open_mysquads current_squads')
        $('.open_allsquads').attr('class', 'open_allsquads other_squads')
    });
    $('.open_allsquads').on('click', function(e) {
        $('.allsquads').show()
        $('.mysquads').hide()
        $(this).attr('class', 'open_allsquads current_squads')
        $('.open_mysquads').attr('class', 'open_mysquads other_squads')
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