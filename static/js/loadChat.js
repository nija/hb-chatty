"use strict";

// Define the success function aka callback
function loadMessagesOnPageLoad(results) {
    // Define a return string
    var history = "Test\n";
    // console.log(results)
    // console.log(history)
    // for every object in the results list
    // results.forEach(function (element, index, array) {
    //     console.log('a[' + index + '] = ' + element);
    // })
    // console.log("results: " + results.messages)
    var messages = results.messages
    // var messages = JSON.parse(results.messages);
    console.log("length: " + messages.length);
    console.log("data: " + messages);
    var dataArray = [{"id":28,"class":"Sweden"}, {"id":56,"class":"USA"}, {"id":89,"class":"England"}];
    debugger;
    for (var i = 0; i < messages.length; i++) { 
        console.log(messages[i].user_id + ": " + messages[i].data + "\n");
    };

    // var dataArray = [{"id":28,"class":"Sweden"}, {"id":56,"class":"USA"}, {"id":89,"class":"England"}];
    $(jQuery.parseJSON(JSON.stringify(dataArray))).each(function() {  
         var ID = this.id;
         var CLASS = this.class;
    });
    // Pull out the results[iterator].data and results[iterator].user_id
    // Call the server to get the user object from /api/user/user_id
    // Add a <tr> user.name : results[iterator].data <tr> to the return string

    // Replace the return string
    $('#messageHistory').html(history)

    // var new_msg = results.user_id + ": " + results.data;
    // console.log(new_msg);
    // $('#messageHistory').html(results.data);
    console.log("Finished replaceStatus");
}

// Define the event handler
function firstLoadOfChat(evt) {
    // var messageInput = {
    //     "data": $("#message_typing_box").val(),
    //     "user_id": 1
    // };
    $.getJSON("/api/rooms/1/messages",'',loadMessagesOnPageLoad)

    // $.post('/api/rooms/1/messages', messageInput, replaceStatus);
    // console.log("Finished sending AJAX for user_id " + messageInput.user_id + ": " + messageInput.data);
}

// Add the event handler to the click event for the button
$(document).ready(firstLoadOfChat)
// $('#message_typing_submit').load(firstLoadOfChat);