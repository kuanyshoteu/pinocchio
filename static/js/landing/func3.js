$(function(){
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
    $('.login-btn2').click(function(e) {
        url = '/api/login/'
        username = $('.username2').val()
        password = $('.password2').val()
        $('.wrong_login').hide('fast')
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
                    $('.wrong_login').show('fast')
                }
            }
        })        
    });
    $('.show_forget_password').click(function(e) {
        $('.forget_password_modal2').fadeIn(500);
        $('.all').addClass('show_modal');
        $('.sectionl').addClass('darker');
        console.log('xxxxxxx', $('.forget_password_modal2'))
    })
    $('.show_request_form').click(function(e) {
    	$('.request_callback').fadeIn(500)
        $('.all').addClass('show_modal')
        $('.sectionl').addClass('darker')
    })
    $('.send_queryl').click(function(e) {
        url = $(this).attr('url')
        name = $('.query_name').val()
        phone = $('.query_phone').val()
        if (name.length > 0 && phone.length > 0) {
	    	$('.query_load').show()
	    	$('.success_load').hide()
	    	$(this).hide()
	        $.ajax({
	            url: url,
	            data: {
	                'name':name,
	                'phone':phone,
	            },
	            dataType: 'json',
	            success: function (data) {
			    	$('.query_load').hide()
			    	$('.success_load').show()
	            }
	        })        	
        }
    })
	$('.show_request_form').click(function(e){
	    e.stopPropagation();
	});
    $('.modal_segment').click(function(e){
        e.stopPropagation();
    });
    $('.update_pswd').click(function(e){
        e.stopPropagation();
    });
    $('.show_forget_password').click(function(e){
        e.stopPropagation();
    });
	$("body").click(function(e){
        $('.request_callback').fadeOut(500)
        $('.forget_password_modal2').fadeOut(500)
        $('.all').removeClass('show_modal')
        $('.sectionl').removeClass('darker')
	});
	$document=$(document)
	$html=$("html");
	$carousel=$("#carousel");
	$document.scroll(function(){
		99<$document.scrollTop()?$html.addClass("scroll"):$html.removeClass("scroll")
	});
	$document.scroll();
	$carousel.on("click","a.arrow",function(b){
		var a=parseInt($carousel.attr("data-step")),a=$(this).hasClass("arrow-left")?1==a?3:a-1:3==a?1:a+1;
		$carousel.attr("data-step",a);
		$('.land_img').hide()
		$('.land_img'+a).show()
		b.stopPropagation()
	});
	$carousel.on("click","nav a",function(b){
		var a=$(this).index()+1;
		$carousel.attr("data-step",a);
		$('.land_img').hide()
		$('.land_img'+a).show()
		b.stopPropagation()
	})
	$carousel.on("click",function(b){
		var a=parseInt($carousel.attr("data-step"))+1;
		if (a == 4) {
			a = 1
		}
		$carousel.attr("data-step",a);
		$('.land_img').hide()
		$('.land_img'+a).show()
		b.stopPropagation()
	})
})
