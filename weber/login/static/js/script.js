	// create the module and name it scotchApp
	var indexpageapp = angular.module('indexpageapp', ['ngRoute']);

	// configure our routes
	indexpageapp.config(function($routeProvider) {
		$routeProvider

			// route for the home page
			.when('/theweber.in/login', {
				templateUrl : '/theweber.in/templates/pages/home.html',
				controller  : 'indexController'
			})

			// route for the about page
			.when('/about', {
				templateUrl : 'pages/about.html',
				controller  : 'aboutController'
			})

			// route for the contact page
			.when('/contact', {
				templateUrl : 'pages/contact.html',
				controller  : 'contactController'
			});
	});

	// create the controller and inject Angular's $scope
	indexpageapp.controller('indexController', function($scope) {
		// create a message to display in our view
		$scope.message = 'Everyone come and see how good I look!';
	});

	indexpageapp.controller('aboutController', function($scope) {
		$scope.message = 'Look! I am an about page.';
	});

	indexpageapp.controller('contactController', function($scope) {
		$scope.message = 'Contact us! JK. This is just a demo.';
	});