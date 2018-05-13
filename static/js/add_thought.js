function add(event) {

	bootpopup.prompt("Thought", function(data) { 
		alert(data);
		 $.post("/thought/",
    		{
    		    txt: data
    		},

    		function(data, status){
                location.reload();
    		    console("Data: " + data + "\nStatus: " + status);
    		}); 

	}, "Add new Thought");
}
