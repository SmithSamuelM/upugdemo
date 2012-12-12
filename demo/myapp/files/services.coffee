# Services modules
angular.module( "genericDirectives", []).
directive( 'myBlur', 
    [ '$parse', ($parse) ->
        link = ($scope, elm, attrs) ->
            fn = $parse(attrs.myBlur); #attribute expression
            elm.bind('blur', (event) -> 
                $scope.$apply( () -> 
                    fn($scope, {$event: event})))
            return true
        return link
    ]).
directive('myFocus', 
    [ '$parse', ($parse) ->
        link = ($scope, elm, attrs) ->
            fn = $parse(attrs.myFocus); #attribute expression
            elm.bind('focus', (event) -> 
                $scope.$apply( () -> 
                    fn($scope, {$event: event})))
            return true
        return link
    ]).
directive('myControl', () ->
    ddo = 
        restrict: 'A' # only activate on element attribute
        require: '?ngModel' # get a hold of NgModelController pass into ctlr
        link: ($scope, elm, attrs, ngModel)->
            return if !ngModel # do nothing if no ng-model
            
            $scope.$watch(attrs.myControl, (value) ->
                attrs.$set('myControl', !!value)
                if !!value
                    elm.attr('contenteditable', '')
                else
                    elm.removeAttr('contenteditable')
            )
            # Write data to the model
            read = () -> ngModel.$setViewValue(elm.html())
            read(); # initialize
            
            #Specify how UI should be updated
            ngModel.$render = () ->
              elm.html(ngModel.$viewValue || '');
     
            # Listen for change events to enable binding
            elm.bind('blur keyup change', () -> $scope.$apply(read))
            
     
    return ddo        
    )

angular.module("teamService", ["ngResource"]).factory "TeamService", 
    ['$resource', ($resource) -> $resource "/demo/backend/teams/:id", 
        {id: '@id'},
        put: 
            method: 'PUT'
            params: {}
    ]
    
angular.module("playerService", ["ngResource"]).factory "PlayerService", 
    ['$resource', ($resource) -> $resource "/demo/backend/players/:id", 
        {id: '@id'},
        update: 
            method: 'PUT'
            params: {}
        create:
            method: 'POST'
            params: {id: ''}
    ]
