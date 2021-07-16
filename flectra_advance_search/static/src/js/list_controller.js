flectra.define('flectra_advance_search.ListController', function(require) {
    "use strict";
    var core = require('web.core');
    var BasicController = require('web.BasicController');
    var ListController = require('web.ListController');
    var SearchView = require('web.SearchView');
    var _t = core._t;
    ListController.include({
        events: _.extend({}, BasicController.prototype.events, {
            'change tbody .flectra_field_search_expan': '_change_flectra_field_search_expan',
            'keydown tbody .flectra_field_search_expan': '_onkeydownAdvanceSearch',
        }),
        _onkeydownAdvanceSearch: function(event) {
            if (event.keyCode == 13) {
                event.preventDefault();
                event.stopPropagation();
                var searchView = this.getParent().searchview;
                if (searchView) {
                    var search = searchView.build_search_data();
                    this.trigger_up('search', search);
                }
            }
        },
        _change_flectra_field_search_expan: function(event) {
            event.preventDefault();
            event.stopPropagation();
            var searchView = this.getParent().searchview;
            if (searchView) {
                var search = searchView.build_search_data();
                this.trigger_up('search', search);
            }
        },
    });
});