describe('DiagnosisAddEpisodeCtrl', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, options, demographics, tagServiceSpy;
    var mockTagService, tagServiceToSave;


    var fields = {
        presenting_complaint: {
            name: 'presenting_complaint',
            fields: []
        }
    };

    demographics = { patient_id: 123 };
    tags = { tag: 'tropical', subtag: 'inpatients' };
    options = {
        'symptom_list': [
            'cough',
            'rash'
        ]
    };

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $httpBackend    = $injector.get('$httpBackend');
            $rootScope      = $injector.get('$rootScope');
            $modal          = $injector.get('$modal');
            $controller = $injector.get('$controller');
        });

        $rootScope.fields = fields;

        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});
        tagServiceToSave = jasmine.createSpy('toSave').and.returnValue({"inpatients": true});
        mockTagService = jasmine.createSpy('TagService').and.returnValue(
            {toSave: tagServiceToSave}
        );

        $controller('DiagnosisAddEpisodeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            options        : options,
            tags           : tags,
            demographics   : demographics,
            TagService: mockTagService,
            Episode: function(x){ return {
              newItem: function(){},
              presenting_complaint: [{}]
            };}
        });
    });

    describe('Freshly initialised', function() {
        it('should store the current tag and sub tag', function() {
            expect($scope.currentTag).toEqual('tropical');
            expect($scope.currentSubTag).toEqual('inpatients');
        });
    });

    describe('save()', function() {
        it('should save the episode data', function() {
            var episodeData = {
                tagging     : [ { inpatients: true }],
                location    : { hospital: "UCLH" },
                demographics: { patient_id: 123 }
            };
            var responseData = angular.copy(episodeData);
            responseData.location = [responseData.location];
            responseData.demographics = [responseData.demographics]
            $httpBackend.expectPOST('episode/', episodeData).respond(responseData);
            $httpBackend.expectGET('/templates/modals/presenting_complaint.html/').respond('notarealtemplate');
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $scope.save();
            $rootScope.$apply();
            $httpBackend.flush();
        });

    });

    describe('cancel()', function(){

        it('should close with null', function(){
            spyOn(modalInstance, 'close');
            $scope.cancel();
            expect(modalInstance.close).toHaveBeenCalledWith(null);
        });

    });

    describe('save', function(){
        it('should post on save', function(){
            spyOn($modal, "open").and.returnValue({
              result: {then: function(x){x(); } }
            });
            $scope.editing.date_of_admission = "10/02/2000";
            $scope.editing.demographics.date_of_birth = "10/02/1990";
            $scope.save();
            expect(tagServiceToSave).toHaveBeenCalled();
            $httpBackend.expectPOST('episode/', {
              "tagging":[{"inpatients": true}],
              "location":{"hospital":"UCLH"},
              "demographics":{
                "patient_id":1,
                "date_of_birth":"10/02/1990"
              },
              "date_of_admission": "10/02/2000",
            }).respond({demographics: [{patient_id: 1}]});
            $httpBackend.flush();
        });
    });
});
