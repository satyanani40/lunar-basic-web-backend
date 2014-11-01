//==============get about all profile information==================

var profile_page_info = angular.module('profile_page_info', ['ngSanitize',]);
profile_page_info.directive('dynamic', function ($compile) {
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


profile_page_info.controller("profile_page_info_cntrl",['$scope','$http','$sce',function($scope,$http,$sce,$compile){
    var selected_id = "";
    var url_parts = (document.URL).split("/")
    var username = url_parts[url_parts.length-2]

    $http.post('/theweber.in/get_profile_info/'+username+'/', { search_text:  $scope.search_text_box })
    .success(function(data, status, headers, config) {
    console.log(data)
    $scope.selected_user_info = data;
    console.log(data['friendstatus'])
        $scope.searched_person = data['basicinfo'].username
        selected_id = data['basicinfo'].id;

        if(data['canblock_status'] == 'canblock'){
            $scope.trustedHtml1 =  $sce.trustAsHtml('<button ng-click="block_person()">block selected friend</button>');
        }
        else if(data['canblock_status'] == 'canunblock'){
         $scope.trustedHtml1 =  $sce.trustAsHtml('<button ng-click="unblock_person()">unblock selected friend</button>');
        }else{
            //$scope.trustedHtml1 =  $sce.trustAsHtml('something went wrong');
        }


        if(data['friendstatus'] == 'blocked'){
            $scope.trustedHtml =  $sce.trustAsHtml('<b>blocked by searched person cannot send friend request</b>');
        }else if(data['friendstatus'] == 'ownaccount'){

            $scope.trustedHtml =  $sce.trustAsHtml('<button ng-click="update_info()">update info</button>');
        }else if(data['friendstatus'] == 'friends'){
            $scope.trustedHtml =  $sce.trustAsHtml('<button ng-click="cancel_request()">unfriend</button>');
        }else if(data['friendstatus'] == 'alredysent'){
            $scope.trustedHtml = $sce.trustAsHtml('<button ng-click="cancel_request()">cancel request</button>');
        }else if(data['friendstatus'] == 'addfriend'){
            $scope.trustedHtml = $sce.trustAsHtml('<button ng-click="add_friend()">add friend</button>');
        }else{
            $scope.trustedHtml =  $sce.trustAsHtml('<b>something went wrong</b>');
        }
        $scope.change_password = function(){
        $scope.trustedHtml = $sce.trustAsHtml('<form ng-submit="update_info1()" method="post">'+
        '<input type="text"  ng-model="password">' +
        '<input type="text"  ng-model="confirmpassword">'+
        '<input type="submit" value="update"></form>');

        }
        $scope.add_friend = function(){
            if(selected_id !="" || selected_id != undefined){
                    $http.post('/theweber.in/addfriend', { addfriendid : selected_id })
                    .success(function(data,status,headers,config){
                         if(data == 1)
                            console.log(data)
                            $scope.trustedHtml = $sce.trustAsHtml('<button ng-click="cancel_request()">cancel request</button>');

                    })
            }else{
                alert("please select one friend to add")
            }
        }
        $scope.update_info1 = function(){
            if ($scope.password == $scope.confirmpassword){
                $http.post('/theweber.in/change_password', { password : $scope.password })
                .success(function(data,status,headers,config){
                    console.log(data)


                    })
            }else{
            alert("password doen't match")
            }
           }

        $scope.cancel_request = function(){
            $http.post('/theweber.in/cancel_request', { cancelid : selected_id })
                    .success(function(data,status,headers,config){
                         if(data == 1)
                            $scope.trustedHtml = $sce.trustAsHtml('<button ng-click="add_friend()">add friend</button>');
                    })
                }

         $scope.block_person = function(){
            $http.post('/theweber.in/block_person', { block_personid : selected_id })
                    .success(function(data,status,headers,config){
                         if(data == 1)
                            $scope.trustedHtml1 = $sce.trustAsHtml('<button ng-click="unblock_person()">unblock selected friend</button>');
                    })
                }

          $scope.unblock_person = function(){
            $http.post('/theweber.in/unblock_person', { block_personid : selected_id })
                    .success(function(data,status,headers,config){
                         if(data == 1)
                            $scope.trustedHtml1 = $sce.trustAsHtml('<button ng-click="block_person()">block selected friend</button>');
                    })
                }


    }).error(function(data, status, headers, config) {
               console.log(data)
    });
}])

