(function () {
	var app = angular.module("Quiz", []);
	
	app.controller("GreetController", ["$scope", "$http", function($scope, $http) {
		$scope.username = "finally!";
		
		$scope.check = function(val) {
			if (!val) {
				return false;
			}
			var result = val.replace(/[^\w]/gi, '');
			if (result) {

			}			
			return result;
		};
		$scope.output = function($scope) {
			$http({
			method: "get",
			url: "/blog"
			}).
			then(function(response) {
				console.log(response.data);
				return response.data;
			})
		}

	}]);
	app.directive("myBlur", function() {
		return {
			restrict: "A",
			link: function($scope, element, attrs) {
				element.on('mouseenter', function () {
                  element.css('opacity', '0.5');
              });
			}
		};
	});
	app.controller("QuizController", "$http", function($http) {
		this.questions = $http.get("questions.json").then(function(response) {
			console.log(response.data);
			return response.data;
		});
	});
})();