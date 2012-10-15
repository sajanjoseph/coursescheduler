$(document).ready(function(){
	$('#id_submission_date').datetimepicker({
		dateFormat:'yy-mm-dd',
		showSecond: true,
		timeFormat: 'hh:mm:ss',
		
	});
	
	$.fn.peity.defaults.pie = {
			  colours: ["#FF0000", "#008000"],
			  delimeter: "/",
			  diameter: 27
			};
	
	$("span.pie").peity("pie");
	
	
	
});