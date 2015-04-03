$(document).ready(function() {
    $.getJSON('/profile').done(function(data) {
        $.each(data, function(name, item) {
            $("#select_acct").append('<option value=' + name + '>' + item['uid'] + '</option>');
        });
    });
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

    var dt_ready = $('#main_table_ready').dataTable({
        "serverSide": true,
        "stateSave": true,
        "ordering": false,
        "pageLength": 25,
        "ajax": {
            "url": "/rlist"
        }
    });

    $('#main_table_ready').on('draw.dt', function () {
        var all_appids = Array();
        $('#main_table_ready input[id*=check]').each(function(_, el) {
            all_appids.push($(el).val());
        });
        $.ajax({
            "url": "/bulkprice",
            "method": "POST",
            "data": {'appids': all_appids.join(',')},
            "success": function(data) {
                var n = 0;
                $('#main_table_ready span[id=price]').each(function(_, el) {
                    $(el).html(data[n]);
                    n++;
                });
            },
            "dataType": "json"
        });
    });

    var dt_download = $('#main_table_download').dataTable({
        "serverSide": true,
        "ordering": false,
        "paging": false,
        "ajax": {
            "url": "/dqueue"
        },
        "columns": [
            {'data': 'appid'},
            {'data': 'uid'},
            {'data': 'start_time'},
            {'data': 'status'}
        ]
    });

    var interval = null;
    $("#download_tab").on("show.bs.tab", function() {
        interval = setInterval(function() {
            dt_download.api().ajax.reload(null, false);
        }, 30000);
    }).on("hide.bs.tab", function() {
        clearInterval(interval);
    });

    var dt_paid = $('#main_table_paid').dataTable({
        "serverSide": true,
        "processing": true,
        "ordering": false,
        "paging": true,
        "pageLength": 25,
        "ajax": {
            "url": "/paidlist"
        },
        "columns": [
            {'data': 'appid'},
            {'data': 'name'},
            {'data': 'uid'},
            {'data': 'price'},
            {'data': 'create_time'},
        ]
    });

    var interval_paid = null;
    $("#paid_tab").on("show.bs.tab", function() {
        interval_paid = setInterval(function() {
            dt_paid.api().ajax.reload(null, false);
        }, 60000);
    }).on("hide.bs.tab", function() {
        clearInterval(interval_paid);
    });

    $("#chk_all").on("change", function(e) {
        var chkd = this.checked;
        $('#main_table_ready tbody input[id*=check]').prop('checked', this.checked).each(function() {
            if (chkd) {
                $(this).parent().parent().addClass('selected');
            } else {
                $(this).parent().parent().removeClass('selected');
            }
        });
    });
    $("#main_table_ready tbody").on("click", 'tr', function(e) {
        $(this).toggleClass("selected");
        $('input[id*=check_]', this).prop('checked', $(this).hasClass("selected"));
    });

    $("#indb").on("click", function(e) {
        var $btn = $(this).button('loading');
        var appid_list = Array();
        dt_ready.api().rows('.selected').data().each(function(item) {
            appid_list.push($(item[0]).val());
        });
        var appids = appid_list.join(',');
        $.post('/schd', {'config': $("#select_acct").val(), 'appids': appids}).done(function(data) {
            dt_ready.api().rows('.selected').remove().draw(false);
        }).always(function() {
            $btn.button('reset');
        });
    });

    $("#remdb").on("click", function(e) {
        var $btn = $(this).button('loading');
        var appid_list = Array();
        dt_ready.api().rows('.selected').data().each(function(item) {
            appid_list.push($(item[0]).val());
        });
        var appids = appid_list.join(',');
        $.ajax({
            'url': '/rlist?appids=' + appids,
            'type': 'DELETE',
            'success': function(data) {
                dt_ready.api().rows('.selected').remove().draw(false);
                $btn.button('reset');
            }
        });
    });

    var append_acct = function(profile_name, item) {
        $("#acct_show").append('\
        <form class="form-inline" id="gprofile" role="form">\
          <div class="form-group">\
            <label id="cid" cid="'+ profile_name +'">'+ profile_name +': </label>\
            <label class="sr-only" for="exampleInputEmail1">Email</label>\
            <input class="form-control input-sm" name="uid" type="email" id="exampleInputEmail1" placeholder="Enter User" value="'+ item['uid'] +'">\
          </div>\
          <div class="form-group">\
            <label class="sr-only" for="exampleInputPassword1">Password</label>\
            <input type="password" name="passwd" class="form-control" id="exampleInputPassword1" placeholder="Password" value="'+ item['passwd'] +'">\
          </div>\
          <div class="form-group">\
            <label class="sr-only" for="android_id">AndroidId</label>\
            <input type="input" name="device_id" class="form-control input-sm" id="device_id" placeholder="Android ID", value="'+ item['device_id'] +'">\
          </div>\
          <button type="button" id="edit_profile" data-loading-text="Adding..." class="btn btn-primary" autocomplete="off">\
              Edit\
          </button>\
          <button type="button" id="remove_profile" class="btn btn-warning" autocomplete="off">\
              Remove\
          </button>\
        </form>\
                               ');
    };

    $.getJSON('/profile').done(function(data) {
        $.each(data, function(key, item) {
            append_acct(key, item);
        });
    });

    $("#add_profile").on("click", function(e) {
        var params = {};
        $.each(
            $('#add_profile_form').serializeArray(),
            function(_, item) {
                params[item['name']] = item['value'];
            });

        $.post('/profile', params).done(function(data) {
            append_acct(params['cid'], params);
        });
    });

    $(".modal-body").on('click', '#gprofile button[id=remove_profile]', function(e) {
        $.ajax({
            'url': '/profile?cid=' + $('#cid', $(this).parent).attr('cid'),
            'type': 'DELETE',
            'success': function(data) {
                $(this).parent().remove();
            }
        });
    }).on('click', '#gprofile button[id=edit_profile]', function(e) {
        $(this).button('loading');
        $.post('/profile', $(this).parent().serialize());
        $(this).button('reset');
    });

    $("#add2list").on('submit', function(e) {
        var postData = $(this).serializeArray();
        var formURL = $(this).attr("action");
        var formDom = $(this)[0];
        $.ajax({
            url : formURL,
            type: "POST",
            data : postData,
            success: function(data, textStatus, jqXHR) {
                formDom.reset();
                $("#plusModal").modal("hide");
                dt_ready.api().ajax.reload(null, false);
            }
        });
        e.preventDefault(); //STOP default action
        e.unbind(); //unbind. to stop multiple form submit.
    });
});
