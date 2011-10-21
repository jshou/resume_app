$("document").ready(function(){
    var description_counter = 0;
    var institution_counter = 0;
    var counter = 0;

    function add_node(original,destination,section_name,ctr){
        ctr += 1;
        var newNode = $(original).clone(true);
        newNode.attr("id",section_name+ctr);
        var oldFields = $(original).children();
        var newFields = newNode.children();
        for(var i=0;i<newFields.length;i++){
            var theName = oldFields[i].name;
            if(theName){
                newFields[i].name = theName + ctr;
            }
        }
        newNode.insertBefore($(destination));
        newNode.removeClass("template");
        return ctr;
    }

    $(".add-description").click(
        function(){
            description_counter = add_node("#resume-description-content",$(this),"resume-description-content",description_counter);
        }
    );

    $(".add-institution").click(
        function(){
            institution_counter = add_node("#resume-institution-content",$(this),"resume-institution-content",institution_counter);
        }
    );

    $(".remove").click(
        function(){
            $(this).parent().remove();
        }
    );

    $("#add-text-button").click(
        function(){
            counter = add_node("#resume-text","#writeroot","resume-section",counter);
        }
    );
    $("#add-descriptions-button").click(
        function(){
            counter = add_node("#resume-descriptions","#writeroot","resume-section",counter);
        }
    );
    $("#add-institutions-button").click(
        function(){
            counter = add_node("#resume-institutions","#writeroot","resume-section",counter);
        }
    );
});
