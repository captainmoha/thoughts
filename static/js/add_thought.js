function add(event) {

	bootpopup.prompt("Thought", function(data) { 
		alert(data);
		 $.post("/thought/",
    		{
    		    txt: data
    		},

    		function(data, status){
    		    alert("Data: " + data + "\nStatus: " + status);
    		}); 

	}, "Add new Thought");
}
