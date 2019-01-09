var $window = $(window),
	$document = $(document),
	$body = null;
$document.ready(function()
{
	Modernizr.addTest('interactive', function(){
		return !Modernizr.ipad && !Modernizr.iphone/*&& !Modernizr.ie*/
		// .mq('@media only screen and (max-device-width: 1024px) and (orientation:landscape)');
	});
});
$window.on('load', function()
{
	$body = $(document.body);

	var slides = [
		{id: 'intro', 'class': 'SlideIntro'},
	];
	$body.addClass('active');
	for ( var k = 0, l = slides.length; k < l; ++ k )
	{
		var slide = typeof slides[k] === 'string'
			? {'class': 'Slide', id: slides[k], container: '#' + slides[k]}
			: slides[k];
		
		try
		{
			window[slide.id] = new window[slide['class']]({
				container: slide.container ? slide.container : '#' + slide.id,
				id: slide.id
			});
		}
		catch (e)
		{
		}
	}
});