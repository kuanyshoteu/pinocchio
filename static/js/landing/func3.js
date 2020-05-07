$(function(){ 
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
	$('.get_request_land_top').on("click",function(){
		document.getElementById('start_request').scrollIntoView();
	})
	$('.get_request_land').on("click",function(){
		console.log('iiii')
		id = $(this).attr('id')
		var name = $('.request_name' + id).val()
		var phone = $('.request_phone' + id).val()
    	$('.success_query').hide();
		$('.land_fill_error'+id).hide()
		if (name == '' || phone == '') {
			$('.land_fill_error'+id).show()
		}
		else {
        	$('.loading').show()
			$('.land_fill_error'+id).hide()
			url = $('.request_url').attr('url')
	        $.ajax({
	            url: url,
	            data: {
	            	'name':name,
	            	'phone':phone,
	            	'code':'nfrejkNWcsdkls588w5sdkewdhs',
	            },
	            dataType: 'json',
	            success: function (data) {
	            	$('.get_request_land').hide()
	            	$('.loading').hide()
	            	$('.success_query').show()
	            }
	        })
		}
	})
})
