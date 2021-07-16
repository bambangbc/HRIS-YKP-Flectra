flectra.define('muk_preview.ExcelDialog', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var framework = require('web.framework');

var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

var PreviewDialog = Widget.extend({
	init: function(parent, title, value) {
		this._super(parent);
		this.parent = parent;
        this._opened = $.Deferred();
        this.title = title || _t('Preview');
        this.value = value;
	},
	 willStart: function() {
		var self = this; 
		return $.when(ajax.loadLibs(this), this._super()).then(function() {
    		self.$modal = $(QWeb.render('ExcelDialog', {title: self.title}));
		});
    },
    start: function() {
    	var self = this;
        return this._super().then(function() {
        	self.$modal.on('hidden.bs.modal', _.bind(self.destroy, self));
        });
    },
    renderElement: function() {
        this._super();
        var self = this;
        var options = {
            excel: {
                proxyURL: "https://demos.telerik.com/kendo-ui/service/export"
            },
            pdf: {
                proxyURL: "https://demos.telerik.com/kendo-ui/service/export"
            },
            change: function () {
                self.parent._setValue(self._getValue());
            }
        };
        setTimeout(function () {
            self.sp = self.$el.wvSpreadsheet(options);
            self.sp.addClass('excel-fullscreen')
            self.excel = self.sp.data("wvSpreadsheet");
            var newValue = JSON.parse(self.value);
            if (self.excel.toJSON() !== newValue) {
                self.excel.fromJSON(newValue);
            }
        }, 200)
	},
    open: function() {
        var self = this;
        $('.tooltip').remove();
        this.appendTo($('<div/>')).then(function() {
        	self.$modal.find(".modal-body").append(self.$el);
            self.$modal.modal('show');
            self._opened.resolve();
        });
        return self;
    },
    opened: function (handler) {
        return (handler)? this._opened.then(handler) : this._opened;
    },
    close: function() {
    	this.destroy();
    },
    destroy: function (reason) {
        if (!this.__closed) {
            this.__closed = true;
            this.trigger("closed", reason);
        }
        if (this.isDestroyed()) {
            return;
        }
        this._super();

        $('.tooltip').remove();
        if (this.$modal) {
            this.$modal.modal('hide');
            this.$modal.remove();
        }
        var modals = $('body > .modal').filter(':visible');
        if (modals.length) {
            modals.last().focus();
            $('body').addClass('modal-open');
        }

    },
    _getValue: function () {
        if (this.excel) {
            var data = this.excel.toJSON();
            return JSON.stringify(data);
        }else
            return "";
    }
});

PreviewDialog.createPreviewDialog = function (parent, title, value) {
    return new PreviewDialog(parent, title, value).open();
};

return PreviewDialog;

});