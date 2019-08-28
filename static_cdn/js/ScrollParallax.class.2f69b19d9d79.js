var ScrollParallax = function(opt) 
{
	this.$window = $(window);
	this.$container = null;
	this.$layers = $();
	if ( typeof opt === 'object' )
	{
		if ( opt.window )
		{
			this.$window = $(opt.window);
		}
		if ( opt.container )
		{
			this.$container = $(opt.container);
		}
		
		if ( typeof opt.layers === 'object' && opt.layers.constructor === Array )
		{
			for ( var i = 0, l = opt.layers.length; i < l; ++i )
			{
				var layer = opt.layers[i],
					$layer = null;

				if ( this.$container )
					$layer = this.$container.find(layer['selector']);
				else
					$layer = $(layer['selector']);
				$layer.data('config', layer);
				this.$layers = this.$layers.add($layer);
			}
			
		}
	}
	else throw TypeError('Wrong option parameter');

	this.init();
};
ScrollParallax.prototype.init = function()
{
	var self = this;

	self.$layers.each(function(index, element)
	{
		var $this = $(this),
			config = $this.data('config');

		try
		{
			if ( config.moveBg )
			{
				$this.css('backgroundAttachment', 'fixed');
				var bgPos = $this.css('backgroundPosition').split(' '),
					x = bgPos[0],
					y = bgPos[1];

				// if ( bgPos[0] = bgPos[0].match(/(\d+)%$/) )
				// 	x = bgPos[0][1], x = $this.width() * x / 100;

				if ( bgPos[1] = bgPos[1].match(/(\d+)%$/) )
					y = bgPos[1][1], y = $this.height() * y / 100;

				config.orig = {
					xWithUnit: x,//parseInt(x) || 0,
					y: parseInt(y) || 0
				};
				if ( config.offsetRight )
				{
					config.orig.xWithUnit = $this.width() - config.offsetRight + 'px';
					$this.css('backgroundPosition', config.orig.xWithUnit + ' ' + config.orig.y + 'px');
				}
			}
			else
			{
				$this.css('position', 'fixed');
				config.orig = {
					x: 0,
					y: 0
				};
			}
		}
		catch (e) {}
	});

	this.windowHeight = this.$window.height();
	this.containerHeight = this.$container.height();
	// if ( this.containerHeight < this.windowHeight * 2 )
	// {
	// 	this.containerHeight = this.windowHeight * 2;
	// 	this.$container.height(this.containerHeight);
	// }
	
	this.containerOffset = self.$container.offset();
	this.containerMiddle = this.containerOffset.top + this.containerHeight / 2; // center of the container

	this.transformProp = Modernizr.prefixed('transform');//window.WebKitTransitionEvent ? '-webkit-transform' : '-moz-transform';
	this.$window.bind('scroll', $.proxy(this.onScroll_, this));
	// Initial position
	this.onScroll_();

	// TODO: rAF optimization
	// var self = this;
	// webkitRequestAnimationFrame(function a()
	// {
	// 	webkitRequestAnimationFrame(a);
	// 	self.onScroll_();
	// });
};
ScrollParallax.prototype.onScroll_ = function()
{
	var self = this,
		top  = this.$window.scrollTop(),
		viewPortMiddle = top + this.windowHeight / 2; // center of the user view

	if ( this.outOfView() )
		return;
	
	// console.log(offset, middle, viewPortY, 'diff:', viewPortY - containerY);
	
	this.$layers.each(function(/*index, element*/)
	{
		var $this = $(this),
			config = $this.data('config');
		
		//config.Y = (config.Y || 0) + -(top - last) * config.ratio; // based on scroll distance
		config.Y = - (viewPortMiddle - self.containerMiddle) * config.ratio;
		if ( config.moveBg )
		{
			$this.css('backgroundPosition', config.orig.xWithUnit + ' ' + (config.orig.y + config.Y) + 'px');
		}
		else
		{
			// $this.css('-webkit-transform', 'translate3d(0, #px, 0)'.replace('#', config.orig.y + config.Y));
			$this.css(self.transformProp, 'translateY(#px)'.replace('#', config.orig.y + config.Y));

			// conts[k].style[transformProp] = orig[k].y + lastYs[k]
			// conts[k].style.top = orig[k].y + lastYs[k] + "px"
			// conts[k].style.marginTop = orig[k].y + lastYs[k] + "px"
		}
	});
	// last = top;
};
ScrollParallax.prototype.outOfView = function()
{
	var top  = this.$window.scrollTop();
	return top > this.containerHeight + this.containerOffset.top || top + this.windowHeight < this.containerOffset.top;
};
ScrollParallax.prototype.scrollToMiddle = function()
{
};