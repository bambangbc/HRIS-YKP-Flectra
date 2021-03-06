/**********************************************************************************
* 
*    Copyright (C) 2017 MuK IT GmbH
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

flectra.define('muk_preview.PreviewWidgets', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var fields = require('web.basic_fields');

var PreviewHandler = require('muk_preview.PreviewHandler');
var PreviewGenerator = require('muk_preview.PreviewGenerator');
var PreviewDialog = require('muk_preview.PreviewDialog');

var QWeb = core.qweb;
var _t = core._t;

fields.FieldBinaryFile.include({
	_renderReadonly: function () {
		this._super();
		var self = this;
		var $el = this.$el;
		var $wrapper = $('<div/>');
		var $button = $('<a type="button" class="o_form_uri" aria-hidden="true" style="margin-right: 5px;"/>');
		$button.append($('<i class="fa fa-file-text-o"></i>'));
		$button.append(' View File ');
    	$button.click(function(e) {
            e.preventDefault();
    		e.stopPropagation();
            var value = self.get('value');
            var filename_fieldname = self.attrs.filename;
            var filename = self.recordData[filename_fieldname] || null;
            PreviewDialog.createPreviewDialog(self, '/web/content?' + $.param({
                'model': self.model,
                'id': self.res_id,
                'field': self.name,
                'filename_field': filename_fieldname,
                'filename': filename,
                'download': true,
                'data': utils.is_bin_size(value) ? null : value,
            }), false, filename ? filename.split('.').pop() : false, filename);
    	});
		$wrapper.addClass($el.attr('class'));
		$el.removeClass("o_field_widget o_hidden");
		this.replaceElement($wrapper);
    	$wrapper.append($button);
    	$wrapper.append($el);
    },
});

});