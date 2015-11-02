function func_release() {
	$("#id_status").prop("value", "release")
	$("#button-id-save").prop("disabled", false);
	$("#button-id-savenext").prop("disabled", false);	
	$("#button-id-next").prop("disabled", true);	
	$("#button-id-release").removeClass("btn-default").addClass("btn-success")
	$("#button-id-review").removeClass("btn-info").addClass("btn-default")	
}

function func_review() {
	$("#id_status").prop("value", "review")
	$("#button-id-save").prop("disabled", false);
	$("#button-id-savenext").prop("disabled", false);	
	$("#button-id-next").prop("disabled", true);	
	$("#button-id-release").removeClass("btn-success").addClass("btn-default")
	$("#button-id-review").removeClass("btn-default").addClass("btn-info")
}

function func_cancel(form_id) {
	$("#id_status").prop("value", "");
	$( "#id_navigation" ).prop("value", "");
	$( "#"+form_id ).submit();
}

function func_previous(form_id) {
	$("#id_status").prop("value", "")
	$( "#id_navigation" ).prop("value", "previous");
	$( "#"+form_id ).submit();
}

function func_next(form_id) {
	$("#id_status").prop("value", "")
	$( "#id_navigation" ).prop("value", "next");
	$( "#"+form_id ).submit();
}

function func_save(form_id) {
	$( "#id_navigation" ).prop("value", "");
	$( "#"+form_id ).submit();
}

function func_savenext(form_id) {
	$( "#id_navigation" ).prop("value", "savenext");
	$( "#"+form_id ).submit();
}