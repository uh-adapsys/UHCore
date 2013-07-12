/** Questions*/

	var myTimeout;

	Function.prototype.bind = function(scope) {
	  var _function = this;
	  
	  return function() {
	    return _function.apply(scope, arguments);
	  }
	}

	function uiHelper() {
		
	}
	
	uiHelper.prototype = {
		load : function(questions) {
			var dao = new dataHelper();
			dao.pollResponses(this.fill.bind(this), questions, -1);
		},

		fill : function(root, lastId, data) {
			if (lastId != data['query']) {
				$(root).empty();
				$(root).hide();
				if (data['query'] != 'none') {
					//$('.question')
					//for (index in data['responses']) {
						var response = data['responses'][0]
						var newQuery = $('<div></div>')
						var self = this;
//						$(newQuery).click(function() {
//							self.answerQuestion(this, data['query']);
//						});
						newQuery.attr('responseId', response['guiResponseId']);
						newQuery.attr('size', response['size']);
						newQuery.text(response['message']);
						$(root).append(newQuery);
					//}
					
					var dialog_buttons = {}; 
					dialog_buttons['Yes, Please'] = function(){ self.answerQuestionDialog(1, data['query']); }
					dialog_buttons['No, Thanks'] = function(){ self.answerQuestionDialog(-1, data['query']); }
					dialog_buttons['Remind Me Later'] = function(){ self.answerQuestionDialog(2, data['query']); }
//																	$(root).dialog('close');
//																	myTimeout = setTimeout(function(){
//																		 self.openDialog(root, 'open', response['message']);
//																		}, 30000); }  
					var w = $(window).width() * 0.85 ;
					$(root).dialog({
						dialogClass: "no-close",
						closeOnEscape: false,
						autoOpen : false,
						draggable: false,
						modal: true,
						width : w,
						title : "Robot Request",
						resizable: false,
						buttons: dialog_buttons
					});
					//$('.ui-button-text-only .ui-button-text').css('font-size', 30);
					this.openDialog(root, 'open', response['message']);
					
					//$(root).dialog('widget').animate({'left': '+=' + w + 'px'}, 1000);	
					
				} else {
					
					if($(root).hasClass('ui-dialog-content')) {

						//$(root).dialog('widget').animate({'left': '-=' + w + 'px'}, 1000);
						$(root).hide();
						$(root).dialog('close');
						clearTimeout(myTimeout);
					}
					
				}
				
			}		

			return data['query']
		},
		openDialog: function(dialog, status, speech) {
			$(dialog).dialog(status);
			$(dialog).show();
			
			var url = '/command';
			var result = {};
			var obj = {
				'speech' : speech
			};
			$.ajax({
				url : url,
				data : JSON.stringify(obj),
				async : false,
				contentType : 'application/json',
				error : function(jqXHR, status, error) {
					result = {
						status : status,
						error : jqXHR.responseText
					};
				},
				success : function(data, status, jqXHR) {
					result = {
						status : status,
						data : data
					};
				},
				type : 'POST'
			});
		},
		answerQuestionDialog : function(id, question) {
			var url = '/data/' + question;
			var result = {};
			var obj = {
				'response' : id
			};
			$.ajax({
				url : url,
				data : JSON.stringify(obj),
				async : false,
				contentType : 'application/json',
				error : function(jqXHR, status, error) {
					result = {
						status : status,
						error : jqXHR.responseText
					};
				},
				success : function(data, status, jqXHR) {
					result = {
						status : status,
						data : data
					};
				},
				type : 'POST'
			});

			if (result.status == 'success') {
				//location.reload(true);
			} else {
				//Handle errors?
				alert(result.status);
			}
		},
		setTime : function(){
			var url = '/userdata/time';
			var object = { 'time' : '' };
			$.ajax({
				url : url,
				data : JSON.stringify(object),
				async : false,
				contentType : 'application/json',
				error : function(jqXHR, status, error) {
					result = {
						status : status,
						error : jqXHR.responseText
					};
				},
				success : function(data, status, jqXHR) {
					result = {
						status : status,
						data : data
					};
				},
				type : 'POST'
			});
		},
		setHeader: function() {
			var dao = new dataHelper().getResponse('/userdata/username');
	        $('#welcomeMessage').text("Welcome, " + dao[0]['nickname']);
		},
		
		setUserPrefs : function() {
			var dao = new dataHelper().getResponse('/userdata/persona');
			$('.myButton').css('font-size', dao[0]['fontSize']); //40 maximum
			$('.myButtonRoom').css('font-size', dao[0]['fontSize']); //40 maximum
			$('.ui-dialog .ui-dialog-content').css('font-size', dao[0]['fontSize']); //35 maximum
			$('.ui-button-text-only .ui-button-text').css('font-size', dao[0]['fontSize']); //35 maximum
			$('.welcome').css('font-size' , dao[0]['fontSize']); //40 maximum
		},
		
		sendCommand: function(room, tray){
			var url = '/command'
			var result = {};
			var obj = {
				'location' : room,
				'tray' : tray
			};
			$.ajax({
				url : url,
				data : JSON.stringify(obj),
				async : false,
				contentType : 'application/json',
				error : function(jqXHR, status, error) {
					result = {
						status : status,
						error : jqXHR.responseText
					};
				},
				success : function(data, status, jqXHR) {
					result = {
						status : status,
						data : data
					};
				},
				type : 'POST'
			});

			if (result.status == 'success') {
				//location.reload(true);
			} else {
				//Handle errors?
				alert(result.status);
			}
			
		},
		
		getPreferences: function(){
	        return new dataHelper().getResponse('/userdata/preferences');
		},
		
		getInterface: function(){
			return new dataHelper().getResponse('/userdata/persona');
		},
		
		changePreferences: function(object){
			var url = '/userdata/preferences';
			$.ajax({
				url : url,
				data : JSON.stringify(object),
				async : false,
				contentType : 'application/json',
				error : function(jqXHR, status, error) {
					result = {
						status : status,
						error : jqXHR.responseText
					};
				},
				success : function(data, status, jqXHR) {
					result = {
						status : status,
						data : data
					};
				},
				type : 'POST'
			});
		}
		
	}
	
	function dataHelper() {
	}

	dataHelper.prototype = {
		getResponse : function(url) {
			var response = null;
			$.ajax({
				url : url,
				dataType : 'json',
				async : false,
				timeout: 3000,
				success : function(data, textStatus, jqXHR) {
					response = data
				},
			});

			return response;
		},
		pollResponses : function(callback, root, lastId) {
			var self = this;
			var data = self.getResponse('/data/current');
			var id = callback(root, lastId, data);
			setTimeout(function() {
				self.pollResponses(callback, root, id);
			}, 2000);
		}
	}

	$(function() {		
		var ui = new uiHelper();
		//Welcome messages
		ui.setHeader();

		//Question dialog
		if($('#dialog').length == 0) {
			$('body').append('<div id="dialog"/></div>');						
		}
		
		ui.load('#dialog');
		
		//Font preferences
		ui.setUserPrefs();
	});
