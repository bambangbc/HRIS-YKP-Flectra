flectra.define('dynamic_list.ViewsDropdown', function(require) {
    "use strict";
    var core = require('web.core');
    var config = require('web.config');
    var Widget = require('web.Widget');
    var _t = core._t;
    var QWeb = core.qweb;
    var ViewsDropdown = Widget.extend({
        template: 'dynamic_list.ViewsDropdown',
        init: function(parent, model) {
            this._super.apply(this, arguments);
            this.model = model;
        },
        willStart: function() {
            var def = this._rpc({
                kwargs: {
                    model: this.model,
                },
                model: 'dynamic_list.view',
                method: 'get_views',
            }).then(function(result) {
                console.log(result);
            });
            return $.when(this._super.apply(this, arguments), def);
        },
    });
    return ViewsDropdown;
});