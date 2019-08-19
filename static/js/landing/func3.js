$(function(){
	$document=$(document)
	$html=$("html");
	$carousel=$("#carousel");
	$document.scroll(function(){
		99<$document.scrollTop()?$html.addClass("scroll"):$html.removeClass("scroll")
	});
	$document.scroll();
	$carousel.on("click","a.arrow",function(b){
		var a=parseInt($carousel.attr("data-step")),a=$(this).hasClass("arrow-left")?1==a?5:a-1:5==a?1:a+1;
		$carousel.attr("data-step",a);
		$('.slide_images').empty();
		$('<img src="images/'+a+'.png" class="full_size">').appendTo('.slide_images');		
		b.stopPropagation()
	});
	$carousel.on("click","nav a",function(b){
		var a=$(this).index()+1;
		$carousel.attr("data-step",a);
		$('<img src="images/'+a+'.png" class="full_size">').appendTo('.slide_images');		
		b.stopPropagation()
	})
	$carousel.on("click",function(){
		var b=parseInt($carousel.attr("data-step"));
		$carousel.attr("data-step",5==b?1:b+1)
		$('<img src="images/'+a+'.png" class="full_size">').appendTo('.slide_images');		
	})
	$('.get_request_land').on("click",function(){
		console.log('iiii')
		var name = $('.request_name1').val()
		var phone = $('.request_phone1').val()
		console.log('iiii')
    	$('.success_query').hide();
		if (name == '' || phone == '') {
			var name = $('.request_name2').val()
			var phone = $('.request_phone2').val()
		}
		if (name != '' && phone != '') {
        	$('.loading').show()
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
	            	console.log('yo')
	            	$('.get_request_land').hide()
	            	$('.loading').hide()
	            	$('.success_query').show()
	            }
	        })
		}
	})
})
