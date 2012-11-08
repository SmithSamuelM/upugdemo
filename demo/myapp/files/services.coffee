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
directive('contenteditable', () ->
    ddo = 
        restrict: 'A' # only activate on element attribute
        require: '?ngModel' # get a hold of NgModelController pass into ctlr
        link: ($scope, elm, attrs, ngModel)->
            return if !ngModel # do nothing if no ng-model
            
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