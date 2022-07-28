//uses AJAX to search the TE database based on user search
function runSearch( term ) {

    //clears previous results table
    $('#results').hide();
    $('tbody').empty();

    //turns form inputs into a string
    var frmStr = $('#search_te').serialize();

    $.ajax({
        url: './cgi/search_te.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {

            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}


//populates results table with matching elements that were found in database 
function processJSON( data ) {
    //displays the number of search results
    $('#match_count').text( data.match_count );
    
    //tracks row numbers
    var next_row_num = 1;
    
    //add each match to the table
    $.each( data.matches, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
    
        // create a row and append it to the body of the table
        $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
        
	//add the ID column to the row
        $('<td/>', {"text" : item.id} ).appendTo('#' + this_row_id);
        
        //add the Type column to the row
        $('<td/>', {"text" : item.type} ).appendTo('#' + this_row_id);

        //add the Family column to the row
        $('<td/>', {"text" : item.family} ).appendTo('#' + this_row_id);

        //add the Sequence column to the row
        $('<td/>', {"text": item.seq, "class": "seq"}).appendTo(
							'#' + this_row_id);

	//add the Organism column to the row
	$('<td/>', {"text": item.organism} ).appendTo('#' + this_row_id);
    });

    //show results table
    $('#results').show();
}



//wait for page to load before running script
$(document).ready( function() {
	
    //search database when submit button is clicked
    $('#submit').click( function() {
	
	//only searches if at least one input is filled in
	if($('#search_term').val() || $('#search_seq').val()) {
        	runSearch();
	}

        //prevents normal form submission
	return false;	
    });
});
