flectra.define('debranding.base', function(require) {
    var WebClient = require('web.WebClient');
    var core = require('web.core');

    var _t = core._t;

    WebClient.include({
        init: function(parent, action, options) {
            this._super.apply(this, arguments);
            var self = this;
            this.set('title_part', {"zopenerp": ''});
            flectra.debranding_new_name = 'SIM HR';
            flectra.debranding_new_website = 'SIM HR';
            flectra.debranding_new_title = 'SIM HR';
        }
    });

});
