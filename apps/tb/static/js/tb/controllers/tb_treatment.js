angular.module('opal.controllers').controller('TBTreatmentCtrl',
function($modal, $q, ngProgressLite, $controller, treatmentUtils, scope, step, episode) {
    "use strict";

    /*
    * so with weight we'll store another row in observations if the
    * weighthas changed, otherwise keep it the same
    */
    var currentWeight;

    if(!_.isArray(scope.editing.observation)){
        if(_.isObject(scope.editing.observation) && scope.editing.observation.weight){
          scope.editing.observation = [scope.editing.observation];
        }
        else{
          scope.editing.observation = [];
        }
    }

    // we should sort this via datetime
    if(!_.isArray(scope.editing.treatment)){
        if(_.isObject(scope.editing.treatment)){
            scope.editing.treatment = [scope.editing.treatment];
        }
        else{
          scope.editing.treatment = [{}];
        }
    }

    var existingTreatment = angular.copy(scope.editing.treatment);
    // lets add an empty row at the bottom for new treatments
    existingTreatment.push({});

    scope.existingTreatmentFilter = function(x){
        return !x.id
    }

    scope.localEditing = {treatmentPlan: existingTreatment};

    scope.localMetadata = {treatmentStartDate:new Date()};
    if(scope.editing.observation.length){
      var lastObservation = _.last(_.sortBy(scope.editing.observation, function(x){
          // this should be a moment, not a date
          return x.datetime;
      }));

      currentWeight = lastObservation.weight;
    }
    scope.localEditing.weight = currentWeight;

    var smearId;
    var smearConsistencyToken;
    var cultureId;
    var cultureConsistencyToken;
    var diagnosisConsistencyToken;

    var tests = [
      "Culture",
      "Smear",
      "GeneXpert"
    ];
    scope.tests = [];

    _.each(tests, function(testTitle){
        var test = _.find(scope.editing.investigation, function(e){
            return e.test === testTitle;
        });

        if(!test){
            test = {test: testTitle, result: "Not Done"};
        }
        scope.tests.push(test);
    });

    scope.localEditing.hasPulmonary = false;
    scope.localEditing.otherSites = false;

    scope.preSave = function(editing){
        editing.investigation = [];
        _.each(scope.tests, function(test){
          editing.investigation.push(test);
        });

         if(!scope.editing.patient_consultation.discussion || !scope.editing.patient_consultation.discussion.length){
            delete editing.patient_consultation;
         }

         if(scope.localEditing.weight && scope.localEditing.weight.length && scope.localEditing.weight != currentWeight){
           editing.observation.push({
             weight: scope.localEditing.weight,
             datetime: moment()
           });
         }

        editing.treatment = _.filter(scope.localEditing.treatmentPlan, function(t){ return t.drug });
    };

    scope.addTreatment = function(){
        scope.localEditing.treatmentPlan.push({});
    };

    scope.removeTreatment = function($index){
        scope.localEditing.treatmentPlan.splice($index, 1);
    };

    scope.stopTreatment = function($index){
        scope.localEditing.treatmentPlan[$index].end_date = new Date();
    }

    scope.today = function(date){
      if(!date){
        return false;
      }
      return moment(new Date()).format("DD/MM/YYYY") === moment(date).format("DD/MM/YYYY");
    }

    scope.useTreatmentPlan = function(){
        var rifampicin_dose = '600mg';
        var pyrazinamide_dose = '2g';
        if(parseInt(scope.localEditing.weight) < 50){
            rifampicin_dose = '450mg';
            pyrazinamide_dose = '1.5g';
        }
        var ethambutol_dose = 15 * parseInt(scope.localEditing.weight);
        ethambutol_dose += 'mg';
        if(_.isDate(scope.localMetadata.treatmentStartDate)){
            var start = scope.localMetadata.treatmentStartDate;
        }else{
            var start = moment(scope.localMetadata.treatmentStartDate,'DD/MM/YYYY').toDate();
        }

        scope.localEditing.treatmentPlan = _.filter(
            scope.localEditing.treatmentPlan,
            function(tp){ return tp == {} }).concat([
            {
                drug: 'Isoniazid',
                dose: '300mg',
                start_date: scope.localMetadata.treatmentStartDate,
                planned_end_date: moment(start).add(6, 'months').toDate()
            },
            {
                drug: 'Pyridoxine',
                dose: '10mg',
                start_date: scope.localMetadata.treatmentStartDate,
                planned_end_date: moment(start).add(6, 'months').toDate()
            },
            {
                drug: 'Rifampicin',
                dose: rifampicin_dose,
                start_date: scope.localMetadata.treatmentStartDate,
                planned_end_date: moment(start).add(6, 'months').toDate()
            },
            {
                drug: 'Pyrazinamide',
                dose: pyrazinamide_dose,
                start_date: scope.localMetadata.treatmentStartDate,
                planned_end_date: moment(start).add(2, 'months').toDate()
            },
            {
                drug: 'Ethambutol',
                dose: ethambutol_dose,
                start_date: scope.localMetadata.treatmentStartDate,
                planned_end_date: moment(start).add(2, 'months').toDate()
            },
                {}
            ]);
    }
});
