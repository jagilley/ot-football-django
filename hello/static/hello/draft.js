var table = new Tabulator("#example-table", {
    height:500, // set height of table to enable virtual DOM
    ajaxURL: "/get_players/",
    layout:"fitColumns", //fit columns to width of table (optional)
    autoColumns:true,
    selectable:true,
    autoColumnsDefinitions:function(definitions){
        definitions.forEach((column) => {
            column.headerFilter = true;
            column.headerSort = true;
        });
        return definitions;
    },
    /*
    rowClick:function(e, row){ //trigger an alert message when the row is clicked
        alert("Row " + row.getIndex() + " Clicked!!!!");
    },*/
    /*
    rowSelectionChanged:function(data, rows){
        //update selected row counter on selection change
    	document.getElementById("select-stats").innerHTML = data.length;
    },*/
});

var draftHistory = new Tabulator("#draft-history", {
    height:200,
    ajaxURL: ("../../../" + "league/" + leegcode + "/draft/history"),
    layout:"fitColumns",
    autoColumns:true
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function draft_a_guy() {
    var x = document.getElementById("myBtn");
    x.disabled = true;
    var selectedRows = table.getSelectedData();
    var shouldBeAsync = true;

    var request = new XMLHttpRequest();
    request.onload = function () {
        var status = request.status; // HTTP response status, e.g., 200 for "200 OK"
        var data = request.responseText; // Returned data, e.g., an HTML document.
    }

    request.open("POST", "../../../draft_player/", shouldBeAsync);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("leaguecode", leegcode);
    request.send(JSON.stringify(selectedRows));
}

var myvar = setInterval(update_header, 1000);
function update_header(){
    console.log("trigg");
    var draftHeader = document.getElementById("draftHeader");
    var request = new XMLHttpRequest();
    request.onload = function () {
        var status = request.status;
        var data = request.responseText;
        var json_data = JSON.parse(data);
        draftHeader.innerHTML = (json_data["drafter"] + " has been drafting for " + json_data["draft_time"]);
    }
    request.open("GET", "/draft_info/", true);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("leaguecode", leegcode);
    request.send();
}

setInterval(function(){table.replaceData();}, 3000);
setInterval(function(){draftHistory.replaceData();}, 3000);
