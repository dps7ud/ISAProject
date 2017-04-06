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


// console.log(pathname)

})