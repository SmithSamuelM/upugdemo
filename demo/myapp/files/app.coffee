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
        ).when("#{base}/app/home",
            templateUrl: "#{base}/static/files/home.html"
            controller: "HomeCtlr"
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
        
        $scope.teams = TeamService.query({team: ""})
        $scope.team = TeamService.get({team: 'Red'})
        
        
        $scope.test1 = TeamService.get({team: 'Blue'},
            (data, headers) ->
                console.log("TeamService success")
                console.log(data)
                console.log(headers())
            ,
            (response) ->
                console.log("TeamService fail")
                console.log(response)
                console.log(response.headers())
        )
        
        $scope.players = PlayerService.query({team: "Red", player: ""})
        
        $scope.betty = PlayerService.get({team: "Red", player: "Betty"},
            (data, headers) ->
                console.log("Got Betty")
                $scope.betty.attack = 0
                $scope.betty.$save({team: 'Red'})
        )
        
        
        $scope.player = PlayerService.get({team: "Red", player: "John"})
        $scope.player.speed = 5
        $scope.player.health = 10
        $scope.player.$save({team: "Red", player: "John"},
            (data, headers) ->
                console.log("PlayerService Constructor Save Success")
                console.log(data)
                console.log(headers())
                $scope.test4 = $scope.player.$remove({team: 'Red', player: "John"},
                    (data, headers) ->
                        console.log("PlayerService Constructor Remove John Success")
                        console.log(data)
                        console.log(headers())
                    ,
                    (response) ->
                        console.log("PlayerService Constructor Remove John Fail")
                        console.log(response)
                        console.log(response.headers())
                )
            ,
            (response) ->
                console.log("PlayerService Constructor Save Fail")
                console.log(response)
                console.log(response.headers())
        )
        
        
        
        $scope.test2 = PlayerService.save({team: 'Red', player: "George"}, {name: 'George', kind: 'bad'},
            (data, headers) ->
                console.log("PlayerService Constructor Save Success")
                console.log(data)
                console.log(headers())
                $scope.test3 = PlayerService.remove({team: 'Red', player: "George"}, {},
                    (data, headers) ->
                        console.log("PlayerService Constructor Remove George Success")
                        console.log(data)
                        console.log(headers())
                    ,
                    (response) ->
                        console.log("PlayerService Constructor Remove George Fail")
                        console.log(response)
                        console.log(response.headers())
                    )
            ,
            (response) ->
                console.log("PlayerService Constructor Save Fail")
                console.log(response)
                console.log(response.headers())
        )
        
        

        return true
])
