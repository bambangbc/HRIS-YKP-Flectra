flectra.define('web_map.FieldMap', function(require) {
"use strict";

var field_registry = require('web.field_registry');
var AbstractField = require('web.AbstractField');

var FormController = require('web.FormController');

FormController.include({
    _update: function () {
        var _super_update = this._super.apply(this, arguments);
        this.trigger('view_updated');
        return _super_update;
    },
});

var FieldMap = AbstractField.extend({
    template: 'FieldMap',
    start: function() {
        var self = this;

        this.getParent().getParent().on('view_updated', self, function() {
            self.update_map();
        });
        return this._super();
    },
    update_mode: function() {
        if(this.isMap) {
            if(this.mode === 'readonly') {
                this.map.setOptions({
                    disableDoubleClickZoom: true,
                    draggable: false,
                    scrollwheel: false,
                });
            } else {
                this.map.setOptions({
                    disableDoubleClickZoom: false,
                    draggable: true,
                    scrollwheel: true,
                });
            }
        }
    },
    update_map: function() {
        if(!this.isMap) {
            this.init_map();
        }
        this.update_mode();
    },

    init_map: function() {
        var self = this;

        this.map = new google.maps.Map(this.el, {
            center: {lat:-2.4151701,lng:108.8281671},
            zoom: 4,
            disableDefaultUI: true,
        });
        this.markers = [];

        function placeMarkerAssignEventAndPanTo(latLng, map, id) {
            var marker = new google.maps.Marker({
                position: latLng,
                map: map
            });
            marker.setOptions({
                draggable: true,
                cursor: 'pointer',
            });
            if (typeof id == 'undefined')
                marker.id = Math.floor((Math.random() * 100) + 1);
            marker.addListener('dblclick', function () {
                if(self.mode === 'edit') {
                    marker.setMap(null);
                    var found = -1;
                    for (var i = 0; i < self.markers.length; i++) {
                        if (self.markers[i].id == marker.id) {
                            found = i;
                            break;
                        }
                    }
                    if (found >= 0) {
                        self.markers.splice(found, 1);
                        var jsonValue = JSON.parse(self.value);
                        jsonValue.markers = self.markers;
                        self._setValue(JSON.stringify(jsonValue));
                    }
                }
            });
            marker.addListener('dragend', function() {
                var latLng = marker.getPosition();
                for (var i = 0; i < self.markers.length; i++) {
                    if (self.markers[i].id == marker.id) {
                        self.markers[i].position = latLng;
                        var jsonValue = JSON.parse(self.value);
                        jsonValue.markers = self.markers;
                        self._setValue(JSON.stringify(jsonValue));
                    }
                }

            });
            map.panTo(latLng);
            return marker;
        }

        var bounds = null;
        if(this.value) {
            var jsonValue = JSON.parse(this.value);
            if (typeof jsonValue.markers != 'undefined'){
                this.markers = jsonValue.markers;
                for (var i = 0; i< this.markers.length; i++) {
                    placeMarkerAssignEventAndPanTo(this.markers[i].position, self.map, this.markers[i].id)
                }
            }
            if (typeof jsonValue.position != 'undefined')
                this.map.setCenter(jsonValue.position);
            if (typeof jsonValue.zoom != 'undefined')
                this.map.setZoom(jsonValue.zoom);
            if (typeof jsonValue.geoJson != 'undefined') {
                if (jsonValue.geoJson.features[0] != "") {
                    this.map.data.addGeoJson(jsonValue.geoJson);
                    if (typeof jsonValue.zoom == 'undefined' || jsonValue.zoom < 0) {
                        bounds = new google.maps.LatLngBounds();
                        this.map.data.forEach(function(feature){
                            feature.getGeometry().forEachLatLng(function(latlng){
                                bounds.extend(latlng);
                            });
                        });
                        this.map.fitBounds(bounds);
                    }
                }
            }
            if (typeof jsonValue.latitude != 'undefined') {
                var marker = new google.maps.Marker({
                    position: {lat: jsonValue.latitude, lng: jsonValue.longitude},
                    map: self.map
                });
            }

        }

        this.map.addListener('click', function (e) {
            if (self.mode == 'edit') {
                var marker = placeMarkerAssignEventAndPanTo(e.latLng, self.map);
                self.markers.push({id: marker.id, position: e.latLng});
                var jsonValue = JSON.parse(self.value);
                if (jsonValue == false) jsonValue = {}
                jsonValue.markers = self.markers;
                self._setValue(JSON.stringify(jsonValue));
            }
        });

        this.map.addListener('zoom_changed', function(event) {
            debugger;
            if(self.mode === 'edit') {
                var jsonValue = JSON.parse(self.value);
                if (jsonValue == false) jsonValue = {}
                jsonValue.position = self.map.getCenter();
                jsonValue.zoom = self.map.getZoom();
                self._setValue(JSON.stringify(jsonValue));
            }
        });

//        var bound_changed = function(event) {
//            if (bounds != null) {
//                self.map.fitBounds(bounds);
//            }
//        }
//        this.map.addListener('bounds_changed', bound_changed);
        this.isMap = true;
    },
});

field_registry.add('map', FieldMap);

return {
    FieldMap: FieldMap,
};

});