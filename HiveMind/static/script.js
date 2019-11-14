$("AvailableOBJ").click(function() {
	$.getJSON( "obj.json", function(obj) { 
		$.each(obj, function(key, value) {
			$("tr").append("<td>"+value.Name+"</td>");
		});
	});

});