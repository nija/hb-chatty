"use strict";

function replaceStatus(results) {
    var new_msg = results;
    $('message_typing_box').html(new_msg);
    console.log("Finished replaceStatus");
}

function updateChatRoom() {
    $.post('/process_new_message', replaceStatus);
    console.log("Finished sending AJAX");
}

$('#message_typing_submit').click(updateChatRoom);