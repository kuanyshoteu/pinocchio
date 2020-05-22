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
})
