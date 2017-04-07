$(document).ready(function(){
// $.when().
// $.when( $("#navbar").load("/static/html/navbar.html") ).done(function(x){
//     var pathname = window.location.pathname;
//     if (pathname.indexOf("/task") >= 0){
//         console.log("if");
//         $("#nav1").parent().addClass("active");
//     }
// });
var pathname = window.location.pathname;
console.log($("#authPresent").data("auth"))
if($("#authPresent").data("auth") == "yes"){
    console.log("if statement")
    $("#nav5").html("Logout")
    $("#nav5").attr("href", "/logout")
    $("#navBodyBar").html("<li><a href='/profile/' id='nav6'>Profile</a></li>" + $("#navBodyBar").html())
    //$("#profileNav").html("<li><a href='/profile/' id='nav6'>Profile</a></li>")
} 
if (pathname.indexOf("/task") >= 0){
    $("#nav1").parent().addClass("active");
}
if (pathname.indexOf("/user") >= 0){
    $("#nav2").parent().addClass("active");
}
if (pathname.indexOf("/review") >= 0){
    $("#nav3").parent().addClass("active");
}
if (pathname.indexOf("/login") >= 0){
    $("#nav5").parent().addClass("active");
}
if (pathname.indexOf("/signup") >= 0){
    $("#nav4").parent().addClass("active");
}
if (pathname.indexOf("/profile") >= 0){
    $("#nav6").parent().addClass("active");
}

$('#reviewModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  //var recipient = button.data('poster') // Extract info from data-* attributes
  var postee = button.data('postee')
  var poster = button.data('poster')
  var task = button.data('task')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // var modal = $(this)
  // modal.find('.modal-title').text('New message to ' + recipient)
  // modal.find('.modal-body input').val(recipient)
  $('#posterField').val(poster)
  $('#posteeField').val(postee)
  $('#taskField').val(task)

})

$("#create-review-form").on('submit', function(e){
    if($('#message-title').val() == "" || !$('#message-title').val()){
        alert("Must fill the message title");
        return false;
    }
    if($('#message-text').val() == "" || !$('#message-text').val()){
        alert("Must fill the message body");
        return false;
    }

    $.ajax({
        url: "/createReview/",
        type: "POST",
        data: $("#create-review-form").serialize(),
        success: function(data){
            alert("Successfully submitted.")
        }
    });

})




// console.log(pathname)

})

function createReview(){
    alert("call this on click");
}
