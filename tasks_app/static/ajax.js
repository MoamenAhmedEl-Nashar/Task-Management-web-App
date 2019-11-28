$(document).ready(function(){

    $("div.card-body > h5.card-title").click(function(){
          var task_id = $(this).parent().parent().attr("id");
          $("#" +task_id + " > div.card-body > ul").toggle();
      });
    // $("h1:first").load("http://127.0.0.1:8000/api/tasks/?format=json");

});
console.log("test test alo alo");