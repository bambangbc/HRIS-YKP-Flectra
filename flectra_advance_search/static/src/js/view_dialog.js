flectra.define('flectra_advance_search.view_dialogs', function(require) {
    "use strict";
    var core = require('web.core');
    var view_dialogs = require('web.view_dialogs');
    var SearchView = require('web.SearchView');
    var ListView = require('web.ListView');
    var ListController = require('web.ListController');
    var _t = core._t;
    var SelectCreateListController = ListController.extend({
        custom_events: _.extend({}, ListController.prototype.custom_events, {
            open_record: function(event) {
                var selectedRecord = this.model.get(event.data.id);
                this.trigger_up('select_record', {
                    id: selectedRecord.res_id,
                    display_name: selectedRecord.data.display_name,
                });
            },
        }),
    });
    view_dialogs.SelectCreateDialog.include({
        setup: function(search_defaults, fields_views) {
            var self = this;
            var fragment = document.createDocumentFragment();
            var searchDef = $.Deferred();
            var $header = $('<div/>').addClass('o_modal_header').appendTo(fragment);
            var $pager = $('<div/>').addClass('o_pager').appendTo($header);
            var options = {
                $buttons: $('<div/>').addClass('o_search_options').appendTo($header),
                search_defaults: search_defaults,
            };
            var searchview = new SearchView(this, this.dataset, fields_views.search, options);
            debugger;
            this.searchview = searchview;
            searchview.prependTo($header).done(function() {
                var d = searchview.build_search_data();
                if (self.initial_ids) {
                    d.domains.push([["id", "in", self.initial_ids]]);
                    self.initial_ids = undefined;
                }
                var searchData = self._process_search_data(d.domains, d.contexts, d.groupbys);
                searchDef.resolve(searchData);
            });
            return $.when(searchDef).then(function(searchResult) {
                var listView = new ListView(fields_views.list, _.extend({
                    context: searchResult.context,
                    domain: searchResult.domain,
                    groupBy: searchResult.groupBy,
                    modelName: self.dataset.model,
                    hasSelectors: !self.options.disable_multiple_selection,
                    readonly: true,
                }, self.options.list_view_options));
                listView.setController(SelectCreateListController);
                return listView.getController(self);
            }).then(function(controller) {
                self.list_controller = controller;
                self.__buttons = [{
                    text: _t("Cancel"),
                    classes: "btn-default o_form_button_cancel",
                    close: true,
                }];
                if (!self.options.no_create) {
                    self.__buttons.unshift({
                        text: _t("Create"),
                        classes: "btn-primary",
                        click: self.create_edit_record.bind(self)
                    });
                }
                if (!self.options.disable_multiple_selection) {
                    self.__buttons.unshift({
                        text: _t("Select"),
                        classes: "btn-primary o_select_button",
                        disabled: true,
                        close: true,
                        click: function() {
                            var records = self.list_controller.getSelectedRecords();
                            var values = _.map(records, function(record) {
                                return {
                                    id: record.res_id,
                                    display_name: record.data.display_name,
                                };
                            });
                            self.on_selected(values);
                        },
                    });
                }
                return self.list_controller.appendTo(fragment);
            }).then(function() {
                searchview.toggle_visibility(true);
                self.list_controller.do_show();
                self.list_controller.renderPager($pager);
                return fragment;
            });
        },
    })
});