angular.module('opal.controllers').controller(
    'ClinicalTimeline',
    function(
        $scope, recordLoader, ngProgressLite, $cookies,
        Referencedata, $q, ClinicalAdvice, $modal
    ){
        "use strict";

        var self = this;
        this.changed = false;

        this.watchMicroFields = function(mi){
            // apart from the keys when, _client, initials, are any of the fields not falsy, ie undeinfed
            self.changed = !!_.compact(_.filter(mi, function(val, key){
                return !(key == 'when' || key == '_client' || key == "initials" || key == 'micro_input_icu_round_relation');
            })).length;
        };

        this.hasIcuOrObservation = function(item){
            //
            // This was removed, and this check is no longer useful.
            // TODO Remove more permanently
            //
            // if(item.reason_for_interaction !== 'ICU round'){
            //     return false;
            // }
            // var icuSize = _.size(item.micro_input_icu_round_relation.icu_round)
            // var observation = _.size(item.micro_input_icu_round_relation.observation)
            // if(icuSize || observation){
            //     return true;
            // }
            return false;
        }

        self.getClinicalAdvice = function(){
            var result = [];
            _.each($scope.patient.episodes, function(episode){
                _.each(episode.microbiology_input, function(input){
                    result.push(input)
                });
            });
            self.clinicalAdvice = _.sortBy(result, "when").reverse();
        };

        this.getClinicalAdvice();

        this.editItem = function(item){
            var ctrl = "GeneralEditCtrl";
            var templateUrl = "/templates/modals/microbiology_input.html/"
            var formItem = self.getClinicalAdviceFormObject(item);

            var modal_opts = {
                backdrop: 'static',
                templateUrl: templateUrl,
                controller: ctrl,
                resolve: {
                    formItem: function() { return formItem; },
                    metadata: function(Metadata) { return Metadata.load(); },
                    referencedata: function(Referencedata){ return Referencedata.load(); },
                    callBack: function(){ return function(){
                        self.getClinicalAdvice();
                    }}
                }
            }
            $modal.open(modal_opts);
        };

        this.getClinicalAdviceFormObject = function(item){
            if(!item){
                item = $scope.episode.newItem("microbiology_input");
            }
            return new ClinicalAdvice(item);
        }

        $q.all([Referencedata.load(), recordLoader.load()]).then(function(datasets){
            angular.extend($scope, datasets[0].toLookuplists());
            self.formItem = self.getClinicalAdviceFormObject();

            $scope.$watch("clinicalTimeline.formItem.editing", self.watchMicroFields, true);
            self.save = function(form, defaults){
                ngProgressLite.set(0);
                ngProgressLite.start();
                _.extend(self.formItem.editing, defaults);
                self.formItem.save($scope.episode).then(function() {
                    ngProgressLite.done();
                    self.changed = false;
                    self.formItem = self.getClinicalAdviceFormObject();
                    self.getClinicalAdvice();
                    form.$setPristine()
                });
            };
        });
    }
);
