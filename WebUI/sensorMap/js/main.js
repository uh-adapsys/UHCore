Function.prototype.bind = function(scope) {
  var _function = this;
  
  return function() {
    return _function.apply(scope, arguments);
  }
}

function uiHelper() {
}

uiHelper.prototype = {
	load : function(img) {
		this.autoRefresh(img);
	},

	autoRefresh : function(img) {
		var self = this;
		setTimeout(function() {
			//$(img).attr("src", "image");
			//should be safe as image is served with no-cache header
			$(img).attr("src", "image?cachebust=" + new Date().getTime());
			self.autoRefresh(img);
		}, 2000);
	},
}
