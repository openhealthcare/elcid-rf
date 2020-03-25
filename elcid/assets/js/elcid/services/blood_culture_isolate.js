angular.module('opal.services').service(
  'BloodCultureIsolate', function($http, $q, $window, Referencedata){
  var DATE_FORMAT = 'DD/MM/YYYY'

  const baseUrl = "/elcid/v0.1/blood_culture_isolate/";

  var dateFields = ["date_positive"];

  class BloodCultureIsolate{
    constructor(blood_culture_set, item){
      if(item){
        this.isolateUrl = baseUrl + item.id + "/"
        this.isNew = false;
        this.editing = _.clone(item);
        _.each(dateFields, dateField => {
          if(this.editing[dateField]){
            this.editing[dateField] = moment(this.editing[dateField], DATE_FORMAT).toDate();
          }
        });
      }
      else{
        this.isolateUrl = baseUrl;
        this.editing = {
          consistency_token: "",
          blood_culture_set_id: blood_culture_set.id
        }
        this.isNew = true;
      }

      var isolate = this;

      Referencedata.load().then(function(referenceData){
        // lists should be alphabetical but with
        // Negative always as the last result
        // if the list contains negative
        var lists = [
          "gramstainoutcome_list",
          "quickfishoutcome_list",
          "gpcstaphoutcome_list",
          "gpcstrepoutcome_list"
        ]
        var lookupLists = referenceData.toLookuplists();

        _.each(lists, list => {
          isolate[list] = lookupLists[list];
          var removed = _.without(isolate[list], 'Negative');
          if(removed.length !== isolate[list].length){
            removed.push("Negative");
            isolate[list] = removed;
          }
        });
      });
    }

    save(){
      var deferred = $q.defer();
      var method = "post";
      var toSave = _.clone(this.editing);
      _.each(dateFields, dateField => {
        if(toSave[dateField]){
          toSave[dateField] = moment(this.editing[dateField]).format(DATE_FORMAT);
        }
      });

      if(this.editing.id){
        method = "put";
      }
      $http[method](this.isolateUrl, toSave).then(
        function(){
          deferred.resolve()
        },
        function(response){
          if (response.status == 409) {
            $window.alert('Item could not be saved because somebody else has \
recently changed it - refresh the page and try again');
          } else {
              $window.alert('Item could not be saved');
          }
        }
      );

      return deferred.promise;
    }

    delete(){
      var deferred = $q.defer();
      $http.delete(this.isolateUrl).then(
        function() {
          deferred.resolve();
        },
        function(response) {
        // handle error better
        $window.alert('Item could not be deleted');
      });

      return deferred.promise;
    }
  }

  return BloodCultureIsolate;
});