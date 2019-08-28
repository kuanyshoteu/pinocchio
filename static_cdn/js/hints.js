 $(document).ready(function() { 
    var hint = parseInt( $('.hint_data').attr('id'))
    $('.help' + hint).addClass('highliter');
    $(('.help' + hint)+hint+'hb').addClass('help_button');
    if(hint % 10 == 0 && hint!=100){
        $('.help00').addClass('help_button');
        $('.help200').addClass('help_button');
        $('.help400').addClass('help_button');
        $('.help600').addClass('help_button');
    }
    $('.sec').css('display', 'none');
    $('.help_div'+hint).css('display', 'block')
    $('.next').click(function(){
        id = parseInt($(this).attr('id'))
        $('.help_div' + id).css('display', 'none');
        $('.help_div' + (id+1)).css('display', 'block');
        $('.hint' + id).removeClass('highliter');
        $('.help' + id).removeClass('highliter');
        $('.hint' + (id + 1)).addClass('highliter');
        $('.help' + (id + 1)).addClass('highliter');
        if (id >= 4 || id == 0 || id == 1 || id == 2 || id == 22 || id == 42){
            $(('.help'+(id+1)) + (id+1)+'hb').addClass('help_button');
            $(('.help'+id) + id+'hb').removeClass('help_button');
        }
        if (id == 41 || id == 61){
            if($(this).attr('hint_type')=='library') {
                $('.help'+(id+1)).addClass('help_big_button');
            }
        }
        if (id == 60){$("html, body").animate({ scrollTop: $(".help" + (id+1)).offset().top }, 600)}
        if (id == 61){$("html, body").animate({ scrollTop: $(".help62").offset().top }, 600)}
        $.ajax({
            url: $('.hint_data').attr('url'),
            data: {
                'dir':'next',
                'hint_type':$('.hint_data').attr('hint_type'),
            },
            dataType: 'json',
            success: function (data) {
            }
        })    
    })
    $('.prev').click(function(){
        id = parseInt($(this).attr('id'))
        $('.help_div' + id).css('display', 'none');
        $('.help_div' + (id-1)).css('display', 'block');
        $('.hint' + id).removeClass('highliter');
        $('.help' + id).removeClass('highliter');
        $('.hint' + (id - 1)).addClass('highliter');
        $('.help' + (id - 1)).addClass('highliter');
        if (id >= 7 || id == 1  || id == 3 || id == 2 || id == 24 || id == 44){
            $(('.help'+id) + id+'hb').removeClass('help_button');
            $(('.help'+(id-1)) + (id-1)+'hb').addClass('help_button');
        }
        if (id == 4 || id == 23 || id == 43){
            $("html, body").animate({ scrollTop: 500 }, 500)
        }
        if (id == 63){$("html, body").animate({ scrollTop: 700 }, 600)}
        if (id == 3 || id == 22 || id == 42 || id == 62){
            $("html, body").animate({ scrollTop: 0 }, 500)                
        }
        if (id == 42 || id == 62){
            if($(this).attr('hint_type')=='library') {
                $('.help'+(id)).removeClass('help_big_button');
            }
        }
        $.ajax({
            url: $('.hint_data').attr('url'),
            data: {
                'dir':'prev',
                'hint_type':$('.hint_data').attr('hint_type'),
            },
            dataType: 'json',
            success: function (data) {
            }
        })    
    })
    $('.close_hint').click(function(){
        $('.bg-dark').removeClass();
        $('.help_div' + $(this).attr('id')).css('display', 'none')
        $.ajax({
            url: $('.hint_data').attr('url'),
            data: {
                'dir':'end',
                'hint_type':$('.hint_data').attr('hint_type'),
            },
            dataType: 'json',
            success: function (data) {
            }
        })    
    })
    $('.close_profchange_hint').click(function(){
        $('.bg-dark').removeClass();
        $('.help_div' + $(this).attr('id')).css('display', 'none')
        $.ajax({
            url: $('.hint_data').attr('url'),
            data: {
                'dir':'end',
            },
            dataType: 'json',
            success: function (data) {
            }
        })    
    })

});