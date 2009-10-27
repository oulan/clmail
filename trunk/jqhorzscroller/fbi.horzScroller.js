//
//
jQuery.fn.horzScroller = function(params) {
	var p = params || {
		container: "",
		scroller: "",
		ref: "",
		speed: 25,
		dir: true
	};
	
	var _container = $("#" + p.container);
	var _scroller  = $("#" + p.scroller);
	var _ref       = $("#" + p.ref);
	var _speed     = p.speed;
	var _marquee;
	var _dir       = p.dir;

	var scrollLeft = function() {
		if(_container.width() - _container.scrollLeft() <=0)
			_container.scrollLeft(0);
		else
			_container.scrollLeft(_container.scrollLeft() + 1);
	};

	var scrollRight = function() {
		if(_ref.offsetWidth() - _container.scrollLeft() <=0)
			_container.scrollLeft(_container.scrollLeft() - _scroller.offsetWidth());
		else
			_container.scrollLeft(_container.scrollLeft() + 1);
	};

	var init = function() {
		_ref.html(_scroller.html());

		if (_dir)
			_marquee = setInterval(scrollLeft, _speed);
		else
			_marquee = setInterval(scrollRight, _speed);
		_container.mouseover(function(e) {
					clearInterval(_marquee);
				}
		);
		_container.mouseout(function(e) {
				if (_dir)
					_marquee = setInterval(scrollLeft, _speed);
				else
					_marquee = setInterval(scrollRight, _speed);
				}
		);
	}

	init();
}

