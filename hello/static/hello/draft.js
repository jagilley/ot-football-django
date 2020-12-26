var table = new Tabulator("#example-table", {
    height:500, // set height of table to enable virtual DOM
    ajaxURL: "/get_players",
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
console.log(leegcode);
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
    // You REALLY want shouldBeAsync = true.
    // Otherwise, it'll block ALL execution waiting for server response.
    var shouldBeAsync = true;

    var request = new XMLHttpRequest();

    // Before we send anything, we first have to say what we will do when the
    // server responds. This seems backwards (say how we'll respond before we send
    // the request? huh?), but that's how Javascript works.
    // This function attached to the XMLHttpRequest "onload" property specifies how
    // the HTTP response will be handled. 
    request.onload = function () {

    // Because of javascript's fabulous closure concept, the XMLHttpRequest "request"
    // object declared above is available in this function even though this function
    // executes long after the request is sent and long after this function is
    // instantiated. This fact is CRUCIAL to the workings of XHR in ordinary
    // applications.

    // You can get all kinds of information about the HTTP response.
    var status = request.status; // HTTP response status, e.g., 200 for "200 OK"
    var data = request.responseText; // Returned data, e.g., an HTML document.
    }

    request.open("POST", "../../../draft_player/", shouldBeAsync);

    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("leaguecode", leegcode);
    //compositeJson = selectedRows + JSON.parse(('{' + leegcode + '}'));
    // Actually sends the request to the server.
    request.send(JSON.stringify(selectedRows));
  }

setInterval(function(){table.replaceData();}, 3000);
setInterval(function(){draftHistory.replaceData();}, 3000);