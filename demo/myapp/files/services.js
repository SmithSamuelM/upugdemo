// Generated by CoffeeScript 1.4.0
(function() {

  angular.module("genericDirectives", []).directive('myBlur', [
    '$parse', function($parse) {
      var link;
      link = function($scope, elm, attrs) {
        var fn;
        fn = $parse(attrs.myBlur);
        elm.bind('blur', function(event) {
          return $scope.$apply(function() {
            return fn($scope, {
              $event: event
            });
          });
        });
        return true;
      };
      return link;
    }
  ]).directive('myFocus', [
    '$parse', function($parse) {
      var link;
      link = function($scope, elm, attrs) {
        var fn;
        fn = $parse(attrs.myFocus);
        elm.bind('focus', function(event) {
          return $scope.$apply(function() {
            return fn($scope, {
              $event: event
            });
          });
        });
        return true;
      };
      return link;
    }
  ]).directive('myControl', function() {
    var ddo;
    ddo = {
      restrict: 'A',
      require: '?ngModel',
      link: function($scope, elm, attrs, ngModel) {
        var read;
        if (!ngModel) {
          return;
        }
        $scope.$watch(attrs.myControl, function(value) {
          attrs.$set('myControl', !!value);
          if (!!value) {
            return elm.attr('contenteditable', '');
          } else {
            return elm.removeAttr('contenteditable');
          }
        });
        read = function() {
          return ngModel.$setViewValue(elm.html());
        };
        read();
        ngModel.$render = function() {
          return elm.html(ngModel.$viewValue || '');
        };
        return elm.bind('blur keyup change', function() {
          return $scope.$apply(read);
        });
      }
    };
    return ddo;
  });

  angular.module("teamService", ["ngResource"]).factory("TeamService", [
    '$resource', function($resource) {
      return $resource("/demo/backend/teams/:id", {
        id: '@id'
      }, {
        put: {
          method: 'PUT',
          params: {}
        }
      });
    }
  ]);

  angular.module("playerService", ["ngResource"]).factory("PlayerService", [
    '$resource', function($resource) {
      return $resource("/demo/backend/players/:id", {
        id: '@id'
      }, {
        put: {
          method: 'PUT',
          params: {}
        }
      });
    }
  ]);

}).call(this);
