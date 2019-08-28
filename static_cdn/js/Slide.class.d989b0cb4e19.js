"use strict"; 
var Slide = function(opt)
{
	this.$window = $(window);
	this.$container = null;
	this.id = null;
	if ( typeof opt === 'object' )
	{
		if ( opt.container )
		{
			this.$container = $(opt.container);
		}
		else throw ArgumentError('You need to suply a container element');

		if ( opt.id )
			this.id = opt.id;

	}
	else throw TypeError('Wrong option parameter');

	this.init();
};
Slide.EVENT_VIEW = 'SLIDE_VIEW';
Slide.EVENT_EXIT = 'SLIDE_EXIT';
Slide.prototype.init = function()
{
	var self = this;
	this.$window.bind('scroll', function(e)
	{
		self.visibilityCheck();
		if ( self.mainView() )
		{
			if ( self.lastMainViewCheck )
				return;

			self.lastMainViewCheck = true;
			self.$container.addClass('viewed active');
			if ( self.id )
				self.$window.triggerHandler(Slide.EVENT_VIEW, self.id);
		}
		else if ( self.lastMainViewCheck )
		{
			self.lastMainViewCheck = false;
			self.$container.removeClass('active');
			if ( self.id )
				self.$window.triggerHandler(Slide.EVENT_EXIT, self.id);
		}
	});

	this.lastMainViewCheck = false;
	this.windowHeight = this.$window.height();
	this.containerHeight = this.$container.outerHeight();
	this.containerOffset = this.$container.offset();

	var diff = this.containerHeight / 2 - this.windowHeight / 2;
	// In case the content is taller than viewport, scroll to the beginning
	if ( diff > 0 )
		diff = -150;
	this.containerScroll = this.containerOffset.top + diff;

	// Bind instance for later use
	this.$container.data('slide', this);

	this.visibilityCheck();
};
// Hides some conflicting objects betwen slides
// Maybe improves performance?
Slide.prototype.visibilityCheck = function()
{
	// console.log('visibilityCheck');
	if ( Modernizr.interactive )
	this.$container.children(':not(.headline)')
		.toggle(!this.outOfView());
};
// Detects whether any portion of the slide is in the user viewport
Slide.prototype.outOfView = function()
{
	var top  = this.$window.scrollTop();
	
};
// Detects whether the slide is the main user focus
Slide.prototype.mainView = function()
{
	var top = this.$window.scrollTop(),
		// center of the user view, getting close to the bottom as user approaches to the bottom
		viewPortMiddle = top + this.windowHeight
			- Math.min(this.windowHeight, $body.height() - top - this.windowHeight) / 2 - /*threshold*/40;

};
Slide.prototype.scrollIntoView = function()
{
	Anchor.scrollTo(this.containerScroll);
};