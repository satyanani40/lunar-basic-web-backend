// login controllers for angular js
var loginapp = angular.module("loginapp",[]).controller("validationcntrl",function($scope,$http,$location){
    $scope.username = "";
    $scope.password = "";
    $scope.submit = function() {
        $http.post('/theweber.in/login_check', {username: $scope.username,
                                                password: $scope.password})
            .success(function(data, status, headers, config) {
               // console.log(data)
            if(data == 1){
                 window.location.href="/theweber.in/home";
             }else{
                 $scope.formsubmitresponse = "invalid username and password";
             }
           })
          .error(function(data, status, headers, config) {
                console.log(data)
                //$scope.formsubmitresponse = data
          });
    };
})
.config(['$httpProvider', function($httpProvider,$interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);


//============include home controllers==============
function accept_friend(accept_id,sender_id){
alert(accept_id+"=="+sender_id)
$.ajax({
  url: "/theweber.in/accept_friend",
  data: {'senderid':sender_id},
  method: 'post',
}).done(function(data) {
  console.log(data)
});
}
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


//==============home function load userposts=================
var loadposts = angular.module("loadposts",[]).controller("disply_user_posts_cntrl",function($scope,$http){

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
          source.addEventListener('myevent', function(e) {
                console.log(data)
            }, false);
         };

}else
   alert('browser does not support server sent events');

source.addEventListener('myevent', function(e) {

        data = JSON.parse(e.data);
        console.log(e.data)
        var parentdiv = document.getElementById("userpostdiv")
        var childdiv = document.createElement("div")
        childdiv.innerHTML = e.data+"<br/>=======================================";
        parentdiv.insertBefore(childdiv,parentdiv.firstChild);

        console.log(data)
}, false);

//===========end of server sent events code

   $http.post('/theweber.in/loaded_userposts')
            .success(function(out_data) {
            $scope.test = out_data
            //console.log(out_data)
            })
});
loadposts.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});


//===================new post controller===================

// login controllers for angular js
var newpost = angular.module("new_post_app",[]).controller("new_post_cntrl",function($scope,$http,$location){
    $scope.permissions = [
    {name: 'private', value:1},
    {name: 'public', value: 2},
    {name: 'friends', value: 3}]
    $scope.permission_type=$scope.permissions[1];
    //console.log($scope.permission_type.value);

    $scope.submit = function() {
      alert('submit')
        $http.post('/theweber.in/post_status', { post_text: $scope.post_text,
                                                permission_type: $scope.permission_type.value
                                                })
            .success(function(data, status, headers, config) {
                console.log(data)

           })
          .error(function(data, status, headers, config) {
                console.log(data)

          });
    };
})
.config(['$httpProvider', function($httpProvider,$interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);

newpost.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

//=============image upload controller============

var imageuploadapp = angular.module("imageuploadapp",['ngUpload']).controller("imageupload",function($scope,$http,$location){

$scope.complete = function(content) {
      //console.log(JSON.parse(content));
    }

});
//============profile pic upload code===============


var myApp = angular.module('myApp', []);

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        //console.log(file)
        $http.post(uploadUrl,fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(data, status, headers, config){
        document.getElementById("myImg").src = data;
        //console.log(JSON.stringify(data))
        })
        .error(function(data){
       // console.log("error="+data)
        });
    }
}]);

myApp.controller('myCtrl', ['$scope', 'fileUpload', function($scope, fileUpload){

    $scope.uploadFile = function(){
        var file = ($scope.myFile);
        //console.log('file is ' + JSON.stringify(file));
        var uploadUrl = "/theweber.in/upload_profile_pic";
        fileUpload.uploadFileToUrl(file, uploadUrl);
        //console.log(response)
    };

}]);
//============end of profile pic===============


//================search bar==============

var searchfriend = angular.module('searchfriend', []);
searchfriend.controller('searchfriend_cntrl',['$scope','$http',function($scope,$http){

    $scope.keyup = function() {

        $http.post('/theweber.in/search', { search_text:  $scope.search_text_box })
            .success(function(data, status, headers, config) {
                console.log(data)
                $scope.names_list = data;
           })
          .error(function(data, status, headers, config) {
               // console.log(data)
          });
    };
}])
searchfriend.config(function($interpolateProvider){
$interpolateProvider.startSymbol('[[').endSymbol(']]');
})
//========================================



 angular.element(document).ready(function() {
      angular.bootstrap(document, ['header_include_app','loadposts','searchfriend','new_post_app','myApp','imageuploadapp']);
    });
