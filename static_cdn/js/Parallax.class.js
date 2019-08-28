var Parallax = function(opt) 
{
	this.$container = null;
	this.$layers = $();
	if ( typeof opt === 'object' )
	{
		if ( opt.container )
		{
			this.$container = $(opt.container);
		}
		
		if ( typeof opt.layers === 'object' && opt.layers.constructor === Array )
		{
			for ( var i = 0, l = opt.layers.length; i < l; ++i )
			{
				var layer = opt.layers[i],
					$layer = $(layer['selector']).data('config', layer);
				if ( layer['moveBg'] === true )
				{
					try
					{
						layer['orig'] = {
							x: parseInt($layer.css('background-position-x')),
							y: parseInt($layer.css('background-position-y'))
						}
					}
					catch(e) {}
				}
				this.$layers = this.$layers.add($layer);
			}
		}
	}
	else throw TypeError('Wrong option parameter');
	
	this.init();
};
Parallax.prototype.init = function()
{
	var self = this,
		pos = this.$container.css('position'),
		width = this.$container.width(),
		height = this.$container.height();
	
	if ( pos !== 'relative' && pos !== 'absolute' )
	{
		this.$container.css('position', 'relative');
	}
	
	this.$container.bind('mousemove', function(e)
	{
		//console.log('move', e.pageX, this.offsetLeft, this);
		//self.$layers.css('right', - (width - e.pageX) * .08);
		//self.$layers.css('bottom', - (height - e.pageY) * .04);
		
		self.$layers.each(function(index, element)
		{
			var $this = $(this),
				config = $this.data('config');
			//$this.css('right', - (width - e.pageX) * $this.data('ratio'));
			var x = (width / 2 - e.pageX) * (config['ratioX'] || config['ratio']),
				y = (height / 2 - e.pageY) * (config['ratioY'] || config['ratio']);
			
			console.log(config);
			if ( config['moveBg'] === true )
			{
				$this.css('background-attachment', 'initial');
				// $this.css('background-position', (config['orig'].x + x) + 'px ' + (config['orig'].y + y) + 'px');
			}
			// else
			{
				$this.css('-webkit-transform', 'translate3d(' + x + 'px,' + y + 'px,0)');
				$this.css('-moz-transform', 'translate(' + x + 'px,' + y + 'px)');
				$this.css('-o-transform', 'translate(' + x + 'px,' + y + 'px)');
			}
		});
	});
};