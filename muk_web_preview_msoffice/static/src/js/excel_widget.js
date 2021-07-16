flectra.define('muk_preview_msoffice.ExcelWidget', function (require) {
"use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var DebouncedField = require('web.basic_fields').DebouncedField;

    var PreviewDialog = require('muk_preview.ExcelDialog');

    var QWeb = core.qweb;
    var _t = core._t;

    var ExcelField = DebouncedField.extend({
        template: 'btnExcel',
        supportedFieldTypes: ['char, text'],
        events: {},

        _render: function () {
            this._super();
            var self = this;
            var $el = this.$el;
            var $wrapper = $('<div/>');
            var $button = $('<a type="button" class="btn btn-default btn-sm" aria-hidden="true"/>');
            $button.append($('<i class="fa fa-file-text"></i>'));
            $button.append(' Manage Data ');
            if (this.mode == 'edit')
                $button.click(function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    var value = self.value;
                    self.dialog = PreviewDialog.createPreviewDialog(self, "Manage Excel Data", value);
                });
            $wrapper.addClass($el.attr('class'));
            $el.removeClass("o_field_widget o_hidden");
            $wrapper.empty();
            $el.empty();
            this.replaceElement($wrapper);
            $wrapper.append($button);
            $wrapper.append($el);
        },
    });

    var registry = require('web.field_registry');
    registry.add('excel', ExcelField);
});