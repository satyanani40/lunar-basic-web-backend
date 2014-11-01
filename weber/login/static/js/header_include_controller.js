var header_include_app = angular.module("header_include_app",[]).controller("header_inc_cntrl",function($scope,$http){
    $scope.template = { name:'header.html',url:'/theweber.in/header'}

    //==================dynamic server sent code loading=============
    if(typeof(EventSource)!=="undefined"){
        var out = document.getElementById('messages');
        var source = new EventSource('/theweber.in/sse/');

        function log() {
            console.log(arguments);
        }
        source.onopen = function() {
            //console.log('connection opend')
            };
        source.onerror = function () {
             //console.log(arguments);
        };
        source.onmessage = function() {
          source.addEventListener('frnd_notifications', function(e) {
                console.log(data)
            }, false);
         };

}else
   alert('browser does not support server sent events');

source.addEventListener('frnd_notifications', function(e) {
var message = '';
        data = JSON.parse(e.data);
        //console.log(data)
        if(data['new_frnd_requests'].length >= 1){
            for(var i = 0; i<data['new_frnd_requests'].length;i++){
            $scope.hellow = "dddddddddddddddddddddd"
            console.log((data['new_frnd_requests'][i]).sender_frnd.id+"===========")
        message = message+'<input type="button" onclick="accept_friend(\''+(data['new_frnd_requests'][i]).id+'\',\''+(data['new_frnd_requests'][i]).sender_frnd.id+'\')" value="accept friend">';
        }
        }
        document.getElementById("frnd_request_info").innerHTML = message;
}, false);

//===========end of server sent events code

// check notifications are occured
$http.post('/theweber.in/frnd_notifications')
            .success(function(data, status, headers, config) {
                console.log(data)
           })
          .error(function(data, status, headers, config) {
                console.log(data)

          });
});


header_include_app.directive('dynamic', function ($compile) {
	  return {
	    restrict: 'A',
	    replace: true,
	    link: function (scope, ele, attrs) {
	      scope.$watch(attrs.dynamic, function(html) {
	        ele.html(html);
	        $compile(ele.contents())(scope);
	      });
	    }
	  };
	})
