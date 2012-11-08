# To compile do
# $ coffee -c demo.coffee 
# this creates demo.js in same directory
# To automatically compile
# $ coffee -w -c demo.coffee &


# angular.module() call registers demo for injection into other angular components
# assign to window.demo if we want to have a global handle to the module

# Main App Module 
demo = angular.module("demo", ['myBlurFocus'])

demo.config ["$locationProvider", "$routeProvider",
    ($locationProvider, $routeProvider) ->
        $locationProvider.html5Mode(true)
        
        #using absolute urls here in html5 mode
        base = '/demo' # for use in coffeescript string interpolation #{base}
        $routeProvider.when("#{base}/app",
            templateUrl: "#{base}/static/files/home.html"
            controller: "HomeCtlr"
        ).when("#{base}/app/home",
            templateUrl: "#{base}/static/files/home.html"
            controller: "HomeCtlr"
        ).otherwise redirectTo: "#{base}/app"
        return true
]

demo.controller('HomeCtlr', ['$scope', '$location', '$route',
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
