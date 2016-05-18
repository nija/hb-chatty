"use strict";

// Define the success function aka callback
function loadMessagesOnPageLoad(results) {
    // Define a return string
    var history = "Test<br>";
    // for every object in the results list
    var messages = results.messages;
    // console.log("length: " + messages.length);
    // console.log("messages: " + messages);
    // var dataArray = [{"id":28,"class":"Sweden"}, {"id":56,"class":"USA"}, {"id":89,"class":"England"}];
    // debugger;
    for (var i = 0; i < messages.length; i++) { 
        // var userName = $('#username').val()
        // history += userName + ": " + messages[i].data + "<br>";
        history += messages[i].created_at + " &nbsp;&nbsp; " + messages[i].user_name + ": " + messages[i].data + "<br>";
        //
    };
 
    // $(jQuery.parseJSON(JSON.stringify(messages)))
    // $(jQuery.parseJSON(messages))

    // $(jQuery.parseJSON(JSON.stringify(dataArray))).each(function() {  
    //      var ID = this.id;
    //      var CLASS = this.class;
    // });
    // Pull out the results[iterator].data and results[iterator].user_id
    // Call the server to get the user object from /api/user/user_id
    // Add a <tr> user.name : results[iterator].data <tr> to the return string

    // Replace the return string
    $('#messageHistory').html(history);

    console.log("Finished replaceStatus");
}

// Define the event handler
function firstLoadOfChat(evt) {
    // AJAX call
    $.getJSON("/api/rooms/1/messages",loadMessagesOnPageLoad);
}

// Add the event handler to the click event for the button
$(document).ready(firstLoadOfChat);
