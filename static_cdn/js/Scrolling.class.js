"use strict"; 
/**
* Adds scrolling class to target element during scrolling
* @requires ExtendingBlocker
*/
var Scrolling = function(opt)
{
	this.$window = $(window);
	this.$element = null;
	this.blocker = new ExtendingBlocker(1000);

	if ( typeof opt === 'object' )
	{
		if ( opt.element )
		{
			this.$element = $(opt.element);
		}
		else throw ArgumentError('You need to suply an element');
	}
	else throw TypeError('Wrong option parameter');

	this.init();
};

Scrolling.prototype.init = function()
{
	this.$window.bind('scroll', $.proxy(this.onScroll_, this));
	this.$window.bind(this.blocker.EVENT_UNBLOCK, $.proxy(this.clearScrolling_, this));
};

// @private
Scrolling.prototype.onScroll_ = function(e)
{
	if ( this.blocker.blocking() )
		return;

	this.$element.addClass('scrolling');
};

//@private
Scrolling.prototype.clearScrolling_ = function(e)
{
	this.$element.removeClass('scrolling');
};