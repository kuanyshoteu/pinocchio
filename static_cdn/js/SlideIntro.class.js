// "use strict"; 
/**
* @constructor
* @requires ScrollParallax, Slide
*/
var SlideIntro = function(opt)
{
	base(this, opt);

	if ( Modernizr.interactive )
	this.parallax = new ScrollParallax({
		container: this.$container,
		layers: [
			{selector: '.icon_bg', ratio: .05, moveBg: true},
			{selector: '.icon_fg', ratio: .25, moveBg: true},
			{selector: '.logo_piffle', ratio: .4, moveBg: true},
			{selector: 'h1', ratio: .35},
			{selector: 'a.scroll', ratio: .35},
		]
	});
	
	if ( Modernizr.interactive )
		setTimeout($.proxy(this.defaultScroll_, this), 10);

	// new Parallax({
	// 	container: '#intro',
	// 	layers: [
	// 		{selector: 'img', ratio: .05},
	// 		{selector: 'h1', ratio: .01},
	// 		// {selector: '.container_center', ratio: .01},
	// 		{selector: '.icon_fg', ratio: .025, moveBg: true},
	// 		{selector: '.icon_bg', ratio: .01, moveBg: true}
	// 	]
	// });

	this.$button = this.$container.find('a.scroll');
	this.$button.click(function(e){
		e.preventDefault();
		if ( window.problem && window.problem.scrollIntoView )
		{
			window.problem.scrollIntoView();
		}
	});
};
inherits(SlideIntro, Slide);

SlideIntro.prototype.defaultScroll_ = function()
{
	// Scroll to the middle if appropriate
	if ( this.$window.scrollTop() < this.containerHeight / 2 )
		this.scrollIntoView();
};

SlideIntro.prototype.scrollIntoView = function()
{
	if ( Modernizr.interactive )
		this.parallax.scrollToMiddle();
	else
		base(this, 'scrollIntoView');
};