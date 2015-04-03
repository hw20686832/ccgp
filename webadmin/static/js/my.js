$(document).ready(function() {
    $.extend($.fn.dataTable.defaults, {
        'searching': false,
        "language": {
            'processing': 'loading...', 'infoEmpty': '...',
            'emptyTable': '',
            'paginate': {
                'first': '首页',
                'previous': '上一页',
                'next': '下一页',
                'last': '尾页'}
        }
    });

    var dt = $('#main_tb').dataTable({
        "serverSide": true,
        "stateSave": true,
        "ordering": true,
        "pageLength": 25,
        "ajax": {
            "url": "/list"
        },
        "columns": [
            {'data': 'id'},
            {'data': 'title'},
            {'data': 'zone'},
            {'data': 'publish_time'},
            {
                'data': 'url',
                'render': function ( data, type, full, meta ) {
                    return '<a href="'+data+'" target="_blank">访问</a>';
                }
            },
            {
                'data': 'id',
                'render': function ( data, type, full, meta ) {
                    return '<a href="/detail?bid='+data+'" target="_blank">打开</a>';
                }
            },
            {
                'data': 'atts',
                'render': function ( data, type, full, meta ) {
                    var htms = new Array();
                    data.split('###').forEach(function(item) {
                        var atts = item.split('##');
                        htms.put("<a href='/download?aid="+atts[1]+"' target='_blank'>"+atts[0]+"</a>");
                    });
                    return htms.join('<br />');
                }
            }
        ]
    });
});
