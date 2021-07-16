flectra.define('flectra_advance_search.utils', function(require) {
    'use strict';
    var ajax = require("web.ajax");
    var core = require('web.core');
    var _t = core._t;
    function setAsRecordSelect($select, data=false) {
        var select2Options = {
            allowClear: true,
            multiple: true,
            minimumInputLength: 1,
            formatResult: function(record, resultElem, searchObj) {
                return $("<div/>", {
                    text: record.name
                }).addClass('o_sign_add_partner');
            },
            formatSelection: function(record) {
                return $("<div/>", {
                    text: record.name
                }).html();
            },
            ajax: {
                data: function(term, page) {
                    return {
                        'term': term,
                        'page': page
                    };
                },
                transport: function(args) {
                    var flectra_model = this.getAttributes().search_model;
                    if (flectra_model === undefined) {
                        return []
                    }
                    var context = this.getAttributes().ctx;
                    if (!context) {
                        context = "{}";
                    }
                    var ctx = JSON.parse(context);
                    ajax.rpc('/web/dataset/call_kw/' + flectra_model + '/name_search', {
                        model: flectra_model,
                        method: 'name_search',
                        args: [args.data.term],
                        kwargs: {
                            limit: 30,
                            context: ctx
                        }
                    }).done(args.success).fail(args.failure);
                },
                results: function(data) {
                    var last_page = data.length !== 30
                    var new_data = [];
                    _.each(data, function(record) {
                        new_data.push({
                            'id': record[0],
                            'name': record[1]
                        })
                    });
                    return {
                        'results': new_data,
                        'more': !last_page
                    };
                },
                quietMillis: 250,
            },
            initSelection: function(element, callback) {
                if ($(element).data('new_id_vals')) {
                    var new_id_vals = $(element).data('new_id_vals');
                    data = []
                    for (var key in new_id_vals) {
                        data.push({
                            id: key,
                            name: new_id_vals[key],
                            isNew: false
                        });
                    }
                    callback(data);
                }
                else {
                    callback({});
                }
            }
        };
        $select.select2('destroy');
        $select.addClass('form-control');
        $select.select2(select2Options);
        $select.off('change').on('change', function(e) {
            if (e.added) {
                $(this).data('new_id_vals', $(this).data('new_id_vals') || {});
                $(this).data('new_id_vals')[e.added.id] = e.added.name;
                $(e.target).attr('title', e.added.name)
            } else if (e.removed) {
                delete $(this).data('new_id_vals')[e.removed.id];
                $(e.target).attr('title', '')
            }
        });
        setTimeout(function() {
            $select.data('select2').clearSearch();
        });
    }
    return {
        setAsRecordSelect: setAsRecordSelect,
    }
});