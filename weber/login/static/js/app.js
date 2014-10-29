var app = angular.module('plunker', []);
alert("hai")
app.directive('dynamic', function ($compile) {
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

app.controller('MainCtrl', function($scope, $sce) {
  alert("hellow")
		$scope.trustedHtml = $sce.trustAsHtml('<button ng-click="testAlert()">Submit</button>');  

		$scope.testAlert = function () {
			alert('testing');
		};
		
});
