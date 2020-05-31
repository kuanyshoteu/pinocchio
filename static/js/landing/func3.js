$(function(){
    $('.show_request_form').click(function(e) {
    	$('.request_callback').fadeIn(500)
        $('.all').addClass('show_modal')
        $('.sectionl').addClass('darker')
    })
    $('.send_queryl').click(function(e) {
    	$('.query_load').show()
    	$('.success_load').hide()
    	$(this).hide()
        url = $(this).attr('url')
        name = $('.query_name').val()
        phone = $('.query_phone').val()
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
    })
	$('.show_request_form').click(function(e){
	    e.stopPropagation();
	});
	$('.modal_segment').click(function(e){
	    e.stopPropagation();
	});
	$("body").click(function(e){
    	$('.request_callback').fadeOut(500)
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
