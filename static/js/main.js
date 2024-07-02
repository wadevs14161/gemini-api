$(function(){
    $("#submit").click(chatWithLLM);
    $("#message").keypress(function(e){
        if(e.which == 13){
            chatWithLLM();
        }
    });
});

function chatWithLLM(){
    var message = $("#message").val();
    $("#dialog").append("我 : "+message+"\n");
    var data = {
        message: message
    };
    $.post("/call_llm", data, function(data){
        $("#dialog").append("AI : "+data+"\n");
        //make teacher scroll to the bottom
        $("#dialog").scrollTop($("#dialog")[0].scrollHeight);
    });
    $("#message").val("");
    //make teacher scroll to the bottom
    $("#dialog").scrollTop($("#dialog")[0].scrollHeight);
}