# Services modules
angular.module( "myBlurFocus", []).
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
    ])


