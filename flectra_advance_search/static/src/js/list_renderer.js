flectra.define('flectra_advance_search.Listrenderer', function(require) {
    "use strict";
    var core = require('web.core');
    var session = require('web.session');
    var ListRenderer = require('web.ListRenderer');
    var _t = core._t;
    var pyeval = require('web.pyeval');
    var flectra_advance_search_utils = require('flectra_advance_search.utils');
    ListRenderer.include({
//        _renderHeader: function(isGrouped) {
//            var $thead = this._super(isGrouped);
//            var self = this;
//            if (self.def_column_val === undefined) {
//                self.def_column_val = {}
//            }
//            var initial_view = '';
//            if (!this.getParent().hasSidebar && this.getParent().getParent()) {
//                if (this.getParent().getParent().options) {
//                    initial_view = this.getParent().getParent().options.initial_view;
//                }
//            }
//            if (this.getParent().hasSidebar || initial_view === 'search') {
//                var context = {}
//                if (self.getParent().searchView !== undefined && self.getParent().searchView.dataset) {
//                    context = pyeval.eval('contexts', [self.getParent().searchView.dataset.get_context()]);
//                }
//                else if (this.getParent().getParent() && this.getParent().getParent().searchview) {
//                    var context = pyeval.eval('contexts', [this.getParent().getParent().searchview.dataset.get_context()]);
//                }
//                var $tr2 = $("<tr class='advance_search_row'>").append(_.map(this.columns, function(column) {
//                    var $td = $('<td>');
//                    var name = column.attrs.name;
//                    var field = self.state.fields[name];
//                    if (!field || !field.searchable || (column.attrs.widget !== undefined && column.attrs.widget === 'handle')) {
//                        return $td;
//                    }
//                    var field_value = self.def_column_val[field.name]
//                    if (!field_value) {
//                        field_value = ''
//                    }
//                    if (field.type === 'integer' || field.type === 'float' || field.type === 'monetary') {
//                        var input_tag = "<input type='number' class='flectra_field_search_expan o_list_number' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'" + " value='" + field_value + "'>";
//                        var $input = $(input_tag);
//                    }
//                    else if (field.type === 'many2one') {
//                        var $input1 = $('<input type="hidden"/>').attr('class', 'flectra_field_search_expan o_list_text');
//                        $input1.attr('name', field.name);
//                        $input1.attr('field_type', field.type);
//                        $input1.attr('style', 'width:100%;');
//                        $input1.attr('search_model', field.relation);
//                        $input1.attr('placeholder', 'select');
//                        $input1.attr('ctx', JSON.stringify(context));
//                        $input1.data('new_id_vals', field_value);
//                        $input1.attr('value', field_value);
//                        var $input = $('<div/>').append($input1);
//                        flectra_advance_search_utils.setAsRecordSelect($input1);
//                    }
//                    else if (field.type === 'text' || field.type === 'char' || field.type === 'one2many' || field.type === 'many2many') {
//                        var input_tag = "<input type='text' class='flectra_field_search_expan o_list_text' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'" + " value='" + field_value + "'>";
//                        var $input = $(input_tag);
//                    }
//                    else if (field.type === 'boolean') {
//                        var input_tag = "<select class='flectra_field_search_expan' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'" + ">";
//                        var $input = $(input_tag);
//                        $input[0].add($('<option>')[0])
//                        field_value === 'true' ? $input[0].add($("<option selected=true value='true'>").text(_t("Yes"))[0]) : $input[0].add($("<option value='true'>").text(_t("Yes"))[0]);
//                        field_value === 'false' ? $input[0].add($("<option selected=true value='false'>").text(_t("No"))[0]) : $input[0].add($("<option value='false'>").text(_t("No"))[0]);
//                    }
//                    else if (field.type === 'date' || field.type === 'datetime') {
//                        if (session.has_advance_search_group) {
//                            var field_value_from = self.def_column_val[field.name + '_from']
//                            var field_value_to = self.def_column_val[field.name + '_to']
//                            if (!field_value_from) {
//                                field_value_from = ''
//                            }
//                            if (!field_value_to) {
//                                field_value_to = ''
//                            }
//                            var input_tag1 = "<div><input type='date' class='flectra_field_search_expan' name='" + field.name + "_from' field_type='" + field.type + "' placeholder='From :' style='float:left;width:100%;line-height: inherit;' value='" + field_value_from + "'></div>";
//                            var input_tag2 = "<div><input type='date' class='flectra_field_search_expan' name='" + field.name + "_to' field_type='" + field.type + "' placeholder='To :' style='float:left;width:100%;line-height: inherit;margin-top:5px;' value='" + field_value_to + "'></div>";
//                            var input_tag = input_tag1 + input_tag2;
//                        }
//                        else {
//                            var input_tag = "<input type='date' class='flectra_field_search_expan' name='" + field.name + "' field_type='" + field.type + "' style='float:left;width:100%;line-height: inherit;' value='" + field_value + "'>";
//                        }
//                        var $input = $(input_tag);
//                    }
//                    else if (field.type === 'selection') {
//                        var input_tag = "<select class='flectra_field_search_expan' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'>"
//                        var $input = $(input_tag);
//                        $input[0].add($('<option>')[0]);
//                        $.each(field.selection, function(index) {
//                            var key = field.selection[index][0];
//                            var value = field.selection[index][1];
//                            var selected = self.def_column_val[field.name] === key
//                            if (selected) {
//                                var option_tag = "<option selected='selected' value='" + key + "'>";
//                                $input[0].add($(option_tag).text(value)[0]);
//                            }
//                            else {
//                                var option_tag = "<option value='" + key + "' >";
//                                $input[0].add($(option_tag).text(value)[0]);
//                            }
//                        })
//                    }
//                    $td.append($input)
//                    return $td;
//                }));
//                if (this.hasSelectors) {
//                    $tr2.prepend($('<td>'));
//                }
//                if (isGrouped) {
//                    $tr2.prepend($('<td>').html('&nbsp;'));
//                }
//                if ($thead.find("th.o_list_row_number_header").length > 0) {
//                    $tr2.prepend($('<td class="o_list_row_number_header">').html('&nbsp;'));
//                }
//                $thead.append($tr2);
//            }
//            return $thead;
//        },
        _renderRows: function () {
            var $rows = this._super();
            var self = this;
            if (self.def_column_val === undefined) {
                self.def_column_val = {}
            }
            var initial_view = '';
            if (!this.getParent().hasSidebar && this.getParent().getParent()) {
                if (this.getParent().getParent().options) {
                    initial_view = this.getParent().getParent().options.initial_view;
                }
            }
            if (this.getParent().hasSidebar || initial_view === 'search') {
                var context = {}
                if (self.getParent().searchView !== undefined && self.getParent().searchView.dataset) {
                    context = pyeval.eval('contexts', [self.getParent().searchView.dataset.get_context()]);
                }
                else if (this.getParent().getParent() && this.getParent().getParent().searchview) {
                    var context = pyeval.eval('contexts', [this.getParent().getParent().searchview.dataset.get_context()]);
                }
                var $tr2 = $("<tr class='advance_search_row'>").append(_.map(this.columns, function(column) {
                    var $td = $('<td>');
                    var name = column.attrs.name;
                    var field = self.state.fields[name];
                    if (!field || !field.searchable || (column.attrs.widget !== undefined && column.attrs.widget === 'handle')) {
                        return $td;
                    }
                    var field_value = self.def_column_val[field.name]
                    if (!field_value) {
                        field_value = ''
                    }
                    if (field.type === 'integer' || field.type === 'float' || field.type === 'monetary') {
                        var input_tag = "<input type='number' class='flectra_field_search_expan o_list_number' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'" + " value='" + field_value + "'>";
                        var $input = $(input_tag);
                    }
                    else if (field.type === 'many2one') {
                        var $input1 = $('<input type="hidden"/>').attr('class', 'flectra_field_search_expan o_list_text');
                        $input1.attr('name', field.name);
                        $input1.attr('field_type', field.type);
                        $input1.attr('style', 'width:100%;');
                        $input1.attr('search_model', field.relation);
                        $input1.attr('placeholder', 'select');
                        $input1.attr('ctx', JSON.stringify(context));
                        $input1.data('new_id_vals', field_value);
                        $input1.attr('value', field_value);
                        var $input = $('<div/>').append($input1);
                        flectra_advance_search_utils.setAsRecordSelect($input1);
                    }
                    else if (field.type === 'text' || field.type === 'char' || field.type === 'one2many' || field.type === 'many2many') {
                        var input_tag = "<input type='text' class='flectra_field_search_expan o_list_text' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'" + " value='" + field_value + "'>";
                        var $input = $(input_tag);
                    }
                    else if (field.type === 'boolean') {
                        var input_tag = "<select class='flectra_field_search_expan' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'" + ">";
                        var $input = $(input_tag);
                        $input[0].add($('<option>')[0])
                        field_value === 'true' ? $input[0].add($("<option selected=true value='true'>").text(_t("Yes"))[0]) : $input[0].add($("<option value='true'>").text(_t("Yes"))[0]);
                        field_value === 'false' ? $input[0].add($("<option selected=true value='false'>").text(_t("No"))[0]) : $input[0].add($("<option value='false'>").text(_t("No"))[0]);
                    }
                    else if (field.type === 'date' || field.type === 'datetime') {
                        if (session.has_advance_search_group) {
                            var field_value_from = self.def_column_val[field.name + '_from']
                            var field_value_to = self.def_column_val[field.name + '_to']
                            if (!field_value_from) {
                                field_value_from = ''
                            }
                            if (!field_value_to) {
                                field_value_to = ''
                            }
                            var input_tag1 = "<div><input type='date' class='flectra_field_search_expan' name='" + field.name + "_from' field_type='" + field.type + "' placeholder='From :' style='float:left;width:100%;line-height: inherit;' value='" + field_value_from + "'></div>";
                            var input_tag2 = "<div><input type='date' class='flectra_field_search_expan' name='" + field.name + "_to' field_type='" + field.type + "' placeholder='To :' style='float:left;width:100%;line-height: inherit;margin-top:5px;' value='" + field_value_to + "'></div>";
                            var input_tag = input_tag1 + input_tag2;
                        }
                        else {
                            var input_tag = "<input type='date' class='flectra_field_search_expan' name='" + field.name + "' field_type='" + field.type + "' style='float:left;width:100%;line-height: inherit;' value='" + field_value + "'>";
                        }
                        var $input = $(input_tag);
                    }
                    else if (field.type === 'selection') {
                        var input_tag = "<select class='flectra_field_search_expan' name='" + field.name + "' field_type='" + field.type + "' style='width:100%;'>"
                        var $input = $(input_tag);
                        $input[0].add($('<option>')[0]);
                        $.each(field.selection, function(index) {
                            var key = field.selection[index][0];
                            var value = field.selection[index][1];
                            var selected = self.def_column_val[field.name] === key
                            if (selected) {
                                var option_tag = "<option selected='selected' value='" + key + "'>";
                                $input[0].add($(option_tag).text(value)[0]);
                            }
                            else {
                                var option_tag = "<option value='" + key + "' >";
                                $input[0].add($(option_tag).text(value)[0]);
                            }
                        })
                    }
                    $td.append($input)
                    return $td;
                }));
                if (this.hasSelectors) {
                    $tr2.prepend($('<td>'));
                }
                $rows.unshift($($tr2));
            }
            return $rows;
        },
    });
});