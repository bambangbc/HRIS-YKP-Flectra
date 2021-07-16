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

flectra.define('muk_preview_msoffice.PreviewHandler', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');

var PreviewHandler = require('muk_preview.PreviewHandler');

var QWeb = core.qweb;
var _t = core._t;

var WordHandler = PreviewHandler.PDFHandler.extend({
	checkExtension: function(extension) {
		return ['.doc', '.docx', '.docm', 'doc', 'docx', 'docm'].includes(extension);
    },
    checkType: function(mimetype) {
		return ['application/msword', 'application/ms-word', 'application/vnd.ms-word.document.macroEnabled.12',
			'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(mimetype);
    },
    createHtml: function(url, mimetype, extension, title) {
    	var convertUrlTempalte = _.template('/web/preview/converter/msoffice?url=<%= url %>');
    	return this._super(convertUrlTempalte({url: encodeURIComponent(url)}));
    },
});

var PowerPointHandler = PreviewHandler.PDFHandler.extend({
	checkExtension: function(extension) {
		return ['.ppt', '.pptx', '.pptm', 'ppt', 'pptx', 'pptm'].includes(extension);
    },
    checkType: function(mimetype) {
		return ['application/vnd.mspowerpoint', 'application/vnd.ms-powerpoint',
			'application/vnd.openxmlformats-officedocument.presentationml.presentation',
			'application/vnd.ms-powerpoint.presentation.macroEnabled.12'].includes(mimetype);
    },
    createHtml: function(url, mimetype, extension, title) {
    	var convertUrlTempalte = _.template('/web/preview/converter/msoffice?url=<%= url %>');
    	return this._super(convertUrlTempalte({url: encodeURIComponent(url)}));
    },
});

var ExcelHandler = PreviewHandler.BaseHandler.extend({
    cssLibs: [
    ],
    jsLibs: [
        '/muk_web_preview_msoffice/static/lib/jQueryBinaryTransport/jquery-binarytransport.js',
    ],
	checkExtension: function(extension) {
		return ['.xls', '.xlsx', '.xlsm', '.xlsb', 'xls', 'xlsx', 'xlsm', 'xlsb'].includes(extension);
    },
    checkType: function(mimetype) {
		return ['application/vnd.ms-excel', 'application/vnd.msexcel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
			'application/vnd.ms-excel.sheet.binary.macroEnabled.12', 'application/vnd.ms-excel.sheet.macroEnabled.12'].includes(mimetype);
    },
    createHtml: function(url, mimetype, extension, title) {
        console.log(url)
    	const urlParams = new URLSearchParams(url.split('?')[1]);
    	const model = urlParams.get('model');
        const id = urlParams.get('id');
        const field = urlParams.get('field');
        const filename = urlParams.get('filename');

        var widget = this.widget
    	var result = $.Deferred();
    	var $content = $(QWeb.render('ExcelHTMLContent'))
        ajax.loadLibs(this).then(function() {
    	    var widget1 = widget
    	    $.ajax(url, {
				type: "GET",
				dataType: "binary",
				responseType:'arraybuffer',
				processData: false,
				success: function(arraybuffer) {
				    var xlsblob = new Blob([arraybuffer]);
				    var xlsfile = new File([xlsblob], filename, {type: "application/vnd.ms-excel", lastModified: new Date().getTime()})
				    var options = {
				        excel: {
                            proxyURL: "https://demos.telerik.com/kendo-ui/service/export"
                        },
                        pdf: {
                            proxyURL: "https://demos.telerik.com/kendo-ui/service/export"
                        },
                        fileName: filename,
                        widget: widget1,
                        excelExport: function (e) {
                            e.preventDefault();
                            // Get the Excel file as a data URL.
                            var dataURL = new wv.ooxml.Workbook(e.workbook).toDataURL();
                            // Strip the data URL prologue.
                            var base64 = dataURL.split(";base64,")[1];
                            var data = {}
                            data[field] = base64
                            this.options.widget._rpc({
                                model: model,
                                method: 'write',
                                args: [parseInt(id), data]
                            }).then(function (success) {
                                window.location.reload()
                            })
                        }
                    };
				    var sp = $content.wvSpreadsheet(options);
				    var excel =sp.data("wvSpreadsheet");
				    excel.fromFile(xlsfile);
				    setTimeout(function () {
				        $('.preview-maximize').click(function(e) {
				            excel.resize()
                        })
                        $('.preview-minimize').click(function(e) {
                            excel.resize()
                        })
				    }, 1000)
				},
				error: function(request, status, error) {
			    	console.error(request.responseText);
			    },
			});
    	});
        result.resolve($content);
		return result;
    },
});

return {
	ExcelHandler: ExcelHandler,
	WordHandler: WordHandler,
	PowerPointHandler: PowerPointHandler,
}

});