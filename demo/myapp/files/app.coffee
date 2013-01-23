# To compile do
# $ coffee -c app.coffee 
# this creates app.js in same directory
# To automatically compile
# $ coffee -w -c app.coffee &


# angular.module() call registers demo for injection into other angular components
# assign to window.myApp if we want to have a global handle to the module

# Main App Module 
myApp = angular.module("myApp", ['genericDirectives', 'teamService', 'playerService'])

myApp.config ["$locationProvider", "$routeProvider",
    ($locationProvider, $routeProvider) ->
        $locationProvider.html5Mode(true)

        #using absolute urls here in html5 mode
        base = '/demo' # for use in coffeescript string interpolation #{base}
        $routeProvider.when("#{base}/app",
            templateUrl: "#{base}/static/files/home.html"
            controller: "HomeCtlr"
        ).when("#{base}/app/team",
            templateUrl: "#{base}/static/files/team.html"
            controller: "TeamCtlr"
        ).when("#{base}/app/team/:tid",
            templateUrl: "#{base}/static/files/team.html"
            controller: "TeamCtlr"
        ).when("#{base}/app/player",
            templateUrl: "#{base}/static/files/player.html"
            controller: "PlayerCtlr"
        ).when("#{base}/app/player/:pid",
            templateUrl: "#{base}/static/files/player.html"
            controller: "PlayerCtlr"
        ).when("#{base}/app/directive",
            templateUrl: "#{base}/static/files/directive.html"
            controller: "DirectiveCtlr"
        ).otherwise redirectTo: "#{base}/app"
        return true
]

myApp.controller('HomeCtlr', ['$scope', '$location', '$route', 
    'TeamService', 'PlayerService',
    ($scope, $location, $route, TeamService, PlayerService) ->
        $scope.$location = $location
        $scope.$route = $route
        $scope.location = window.location
        
        console.log("HomeCtlr")
        $scope.teams = TeamService.query({id: ""})
        $scope.players = PlayerService.query({id: ""})
        
        
        return true
])


myApp.controller('TeamCtlr', ['$scope', '$routeParams', '$location', '$route', 
    'TeamService', 'PlayerService',
    ($scope, $routeParams, $location, $route, TeamService, PlayerService) ->
        $scope.$location = $location
        $scope.$route = $route
        $scope.location = window.location
        
        console.log("TeamCtlr")
        
        $scope.tid = $routeParams.tid
        if not $scope.tid
            $scope.tid = 1
            
        $scope.team = TeamService.get({id: $scope.tid})
        
        return true
])

myApp.controller('PlayerCtlr', ['$scope', '$routeParams', '$location', '$route', 
    'TeamService', 'PlayerService',
    ($scope, $routeParams, $location, $route, TeamService, PlayerService) ->
        $scope.$location = $location
        $scope.$route = $route
        $scope.location = window.location
        
        console.log("PlayerCtlr")
        
        
        $scope.pid = $routeParams.pid
        if not $scope.pid
            $scope.pid = 1
            
        $scope.kindOptions = ['good','bad']

        $scope.player = PlayerService.get({id: $scope.pid},
            (data, headers) ->
                console.log("PlayerService get success")
                console.log(data)
                console.log(headers())
                console.log($scope.player)
            ,
            (response) ->
                console.log("PlayerService get fail")
                console.log(response)
                console.log(response.headers())
            )
        
        $scope.savePlayer = (pid) -> 
            $scope.errored=false
            $scope.alert=""
            if $scope.playerForm.$invalid
                $scope.playerForm.$dirty = true
                $scope.errored = true
                $scope.alert = "Some values are missing or invalid."
                return
            
            $scope.player.$put({},
                (data,headers)->
                    console.log("PlayerService put success")
                    console.log(data)
                    console.log(headers())
                ,
                (response)->
                    console.log("PlayerService put fail")
                    console.log(response)
                    console.log(response.headers())
            )
        
        return true
])


myApp.controller('DirectiveCtlr', ['$scope', '$location', '$route', 
    'TeamService', 'PlayerService',
    ($scope, $location, $route, TeamService, PlayerService) ->
        $scope.$location = $location
        $scope.$route = $route
        $scope.location = window.location
        console.log("DirectiveCtlr")

        
        return true
])