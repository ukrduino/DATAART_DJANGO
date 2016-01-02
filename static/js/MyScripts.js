$('#show_add_thread_form').click(function () {
    $("#new_thread_form").slideToggle("slow");
    $('#show_add_thread_form').hide()
});

$('#close_add_thread_form').click(function () {
    $("#new_thread_form").slideToggle("slow");
    $('#show_add_thread_form').show()
});

$('.show_add_reply_form').click(function () {
    $("#new_reply_form").slideToggle("slow");
    var reply_id = $(this).attr("data-reply_id");
    if (reply_id != "") {
        $.ajax({
            type: 'POST',
            url: 'set_reply_id/',
            data: {
                'reply_id': reply_id,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            }
        });
    }
});

$('#close_add_reply_form').click(function () {
    $("#new_reply_form").slideToggle("slow");
});

//$(document).ready(function () {
//    $.ajax({
//        type: 'GET',
//        url: 'get_thread_updates/',
//        success: function (data) {
//            $('#recently_updated_threads').html(data);
//        }
//    });
//});