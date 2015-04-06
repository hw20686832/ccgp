$(document).ready(function() {
    $.extend($.fn.dataTable.defaults, {
        "processing": true,
        "language": {
            'processing': 'loading...',
            'infoEmpty': '...',
            'emptyTable': 'No data...',
            'paginate': {
                'first': '首页',
                'previous': '上一页',
                'next': '下一页',
                'last': '尾页'}
        }
    });

    var main_tb = $('#main_tb').dataTable({
        "stateSave": true,
        "processing": true,
        "ordering": true,
        "searching": true,
        "pageLength": 25,
        "ajax": "/crawler?g=hot",
        "rowCallback": function(row, data) {
            $(row).attr('status', 'show');
            var tag = $($('td', $(row))[3]).html();
            $(row).attr('datatype', tag);
        },
        "columns": [
            {'data': 'appid'},
            {'data': 'version_name'},
            {'data': 'group'},
            {'data': 'tag'},
            {'data': 'download'}
        ],
        "initComplete": function() {
            var api = this.api();

        }
    });

    var full_tb = $('#full_tb').dataTable({
        "stateSave": true,
        "processing": true,
        "ordering": false,
        "searching": true,
        "pageLength": 25,
        "ajax": "/crawler?g=full",
        "rowCallback": function(row, data) {
            $(row).attr('status', 'show');
            var tag = $($('td', $(row))[3]).html();
            $(row).attr('datatype', tag);
        },
        "columns": [
            {'data': 'appid'},
            {'data': 'version_name'},
            {'data': 'group'},
            {'data': 'tag'},
            {'data': 'download'}
        ]
    });
});
