
$(document).ready(function(){
    $("#shout").on('click', function() {
        text = $("#body").val()
        $.ajax({
            url: "/new",
            type: "POST",
            dataType: "text",
            data: text,
            success: function(data) {
                $("#body").val('')
            }
        });
    });

    $(body).on('keypress', function(e) {
        if (e.keyCode == 13) {
            text = $("#body").val()
            $.ajax({
                url: "/new",
                type: "POST",
                dataType: "text",
                data: text,
                success: function(data) {
                    $("#body").val('')
                }
            });
        }
    });

    updater.poll();
});

var updater = {
    cursor: null,
    poll: function() {
        tmp_cursor = null;

        $.ajax({
            url:"/update",
            type:"POST",
            dateType:"text",
            data:tmp_cursor,
            success: function(data){
                $("#body").select();
                updater.newMessages(data);
                updater.poll();
            }
        })
    },

    newMessages: function(response) {
        if(!response) return;
        var node = $(response.message.html);
        $("#screen").append(node);
        node.slideDown();
    }


};