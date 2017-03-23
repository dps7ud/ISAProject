$(document).ready(function(){
// $.when().
// $.when( $("#navbar").load("/static/html/navbar.html") ).done(function(x){
//     var pathname = window.location.pathname;
//     if (pathname.indexOf("/task") >= 0){
//         console.log("if");
//         $("#nav1").parent().addClass("active");
//     }
// });
$("#navbar").load("/static/html/navbar.html", function(){
    var pathname = window.location.pathname;
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
        $("#nav4").parent().addClass("active");
    }
});

// console.log(pathname)

})