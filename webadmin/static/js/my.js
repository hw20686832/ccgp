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

    var dt_1 = $('#main_tb_1').dataTable({
        "serverSide": true,
        "stateSave": true,
        "ordering": false,
        "pageLength": 25,
        "ajax": {
            "url": "/list?group=1"
        },
        "columns": [
            {
                'data': 'title',
                'width': '50%',
                'render': function ( data, type, full, meta ) {
                    return '<a href="/detail?bid='+full['id']+'" target="_blank">'+data+'</a>';
                }
            },
            {'data': 'zone'},
            {'data': 'publish_time'},
            {
                'data': 'url',
                'render': function ( data, type, full, meta ) {
                    return '<a href="'+data+'" target="_blank">访问</a>';
                }
            },
            {
                'data': 'atts',
                'width': '18%',
                'render': function ( data, type, full, meta ) {
                    var htms = new Array();
                    data.split('###').forEach(function(item) {
                        var atts = item.split('##');
                        htms.push("<a href='/download?aid="+atts[1]+"' target='_blank'>"+atts[0]+"</a>");
                    });
                    return htms.join('<br />');
                }
            }
        ]
    });

    var dt_2 = $('#main_tb_2').dataTable({
        "serverSide": true,
        "stateSave": true,
        "ordering": false,
        "pageLength": 25,
        "ajax": {
            "url": "/list?group=2"
        },
        "columns": [
            {
                'data': 'title',
                'width': '50%',
                'render': function ( data, type, full, meta ) {
                    return '<a href="/detail?bid='+full['id']+'" target="_blank">'+data+'</a>';
                }
            },
            {'data': 'zone'},
            {'data': 'publish_time'},
            {
                'data': 'url',
                'render': function ( data, type, full, meta ) {
                    return '<a href="'+data+'" target="_blank">访问</a>';
                }
            },
            {
                'data': 'atts',
                'width': '18%',
                'render': function ( data, type, full, meta ) {
                    var htms = new Array();
                    data.split('###').forEach(function(item) {
                        var atts = item.split('##');
                        htms.push("<a href='/download?aid="+atts[1]+"' target='_blank'>"+atts[0]+"</a>");
                    });
                    return htms.join('<br />');
                }
            }
        ]
    });
});
