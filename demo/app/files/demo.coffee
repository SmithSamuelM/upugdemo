# To compile do
# $ coffee -c japn.coffee 
# this creates japn.js in same directory
# To automatically compile
# $ coffee -w -c japn.coffee &


# angular.module() call registers japn for injection into other angular components
# assign to window.japn if we want to have a global handle to the module

# Main App Module 
japn = angular.module("japn", ['myBlurFocus'])

japn.config ["$locationProvider", "$routeProvider",
    ($locationProvider, $routeProvider) ->
        $locationProvider.html5Mode(true)
        
        #using absolute urls here in html5 mode
        base = '/japn' # for use in coffeescript string interpolation #{base}
        $routeProvider.when("#{base}/app",
            templateUrl: "#{base}/static/files/home.html"
            controller: "HomeCtlr"
        ).when("#{base}/app/home",
            templateUrl: "#{base}/static/files/home.html"
            controller: "HomeCtlr"
        ).otherwise redirectTo: "#{base}/app"
        return true
]

japn.controller('HomeCtlr', ['$scope', '$location', '$route',
    ($scope, $location, $route) ->
        $scope.$location = $location
        $scope.$route = $route
        $scope.location = window.location
        
        $scope.test = "hello world"
        $scope.doMyBlur = ($event) -> 
            $scope.test = $scope.burp
            
            
        $scope.doMyFocus = ($event) -> 
            $scope.test = $scope.burp
            
        
        console.log("HomeCtlr")
        return true
])
