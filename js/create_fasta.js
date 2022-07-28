/* 
 * Creates a FASTA file based on search
 */

//makes FASTA file
function getData() {

    	//turns form inputs into a string
    	var frmStr = $('#search_te').serialize();
	
	//gets matching elements in FASTA format
	$.ajax({
		url: "./cgi/create_fasta.cgi",
		data: frmStr,
		dataType: "text",
        	success: function(data, textStatus, jqXHR) {

            		download(data);
        	}
	});
}

//downloads FASTA data
function download(data) {
	
	//creates dummy download element
	var download_elem = document.createElement('a');

	//sets up element with filename and data
	download_elem.setAttribute('href', 'data:text/plain;charset=utf-8,' +
						encodeURIComponent(data));
	download_elem.setAttribute('download', "dfam_results.fasta");
	download_elem.setAttribute('class', 'dummy_dl');

	//clicks dummy element to initiate download, then remove element
	document.body.appendChild(download_elem);
	download_elem.click();
	document.body.removeChild(download_elem);
}

//wait for page to load before running script
$(document).ready( function() {
	
    //create file when button is clicked
    $('#download').click( function() {
	
	if($('#search_term').val() || $('#search_seq').val()) {
        	getData();
	}

	else {
		alert("No data")
	}

        //prevents normal form submission
	return false;	
    });
});
