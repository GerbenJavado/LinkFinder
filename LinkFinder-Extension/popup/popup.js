$(document).ready(function() {
    $(".dropdown-trigger").dropdown();

    $("#extension-switch").click(function() {
        if ($(this).is(':checked')) {
            checked = true;
        } else {
        	checked = false;
        }

        Obj.popup.enabled = checked;
        UpdateStorage(Obj);
    })

    $("#save-urls-switch").click(function() {
        if($(this).is(':checked')) {
            checked = true;
        } else {
            checked = false;
        }

        Obj.popup.save_urls = checked;
        UpdateStorage(Obj);
    })

    // Set switches to stored values
    $("#extension-switch")[0].checked = Obj.popup.enabled;
    $("#save-urls-switch")[0].checked = Obj.popup.save_urls;

    $("#regex").blur(function(event){
        if(event.target.value.length > 0) {
            r = event.target.value;
            Obj.popup.regex = r;

            UpdateStorage(Obj);
        }
    })

    $("#clear_urls").click(function(){
        localStorage.removeItem("urls");
    })

    $("#clear_graph_data").click(function(){
        localStorage.removeItem("graph_data");
    })

    $("#download_urls").click(function(){
        if(localStorage.getItem("urls")) {    
            urls = localStorage.getItem("urls").toString();

            anchor = $("<a>")[0];
            anchor.setAttribute("href", "data:text/plain,"+urls);
            anchor.setAttribute("download", "urls.txt");
            anchor.click();
        }
    })

    $("#graph-tab").click(function(event){
        function handler(event) {
            if(event.data == "loaded") {
                event.source.postMessage({"graph_data": localStorage.getItem("graph_data")}, "*")
            }
            window.removeEventListener("message", handler);
        }

        window.addEventListener("message", handler);
        graph_tab = window.open("/popup/graph/graph.html", "", "width=750,height=500");
    })

    $("#keywords").blur(function(){
        Array.prototype.clean = function(deleteValue) {
            for (var i = 0; i < this.length; i++) {
                if (this[i] == deleteValue) {         
                    this.splice(i, 1);
                    i--;
                }
            }
            return this;
        };

        keywords = $("#keywords").val().split("\n").clean("")

        Obj.popup.keywords = keywords;

        UpdateStorage(Obj);
    })

    $("#uniques-indicator").text(localStorage.getItem("urls") ? localStorage.getItem("urls").split(",").length : "0");
    $("#regex").val(Obj.popup.regex);

    $("#keywords")[0].innerHTML = $('<div/>').text(Obj.popup.keywords.join("&#10;")).html().replace(/&amp;/g, "&");

    if(Obj.general.connected) {
        $("#status")[0].setAttribute("fill", "lightgreen");
    } else {
        $("#status")[0].setAttribute("fill", "red");
    }
});

function UpdateStorage(dataObj){
	chrome.storage.local.set(dataObj)
}

// Adding some event listeners.
window.onhashchange = function() {
    tabs = ["default", "settings", "statistics"];
    tab = location.hash.slice(1);

    if (tabs.indexOf(tab) > -1) {
        tabcontent = $(".tabContent");

        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        $(location.hash)[0].style.display = "block";
    }
}

window.onstorage = function() {
    if(typeof graph_tab != "undefined") {
        if(localStorage.getItem("graph_data") != graph_data) {
            graph_data = JSON.parse(localStorage.getItem("graph_data"));
            graph_tab.postMessage({"graph_data": graph_data}, "*")
            Plotly.newPlot(graph, graph_data)

            $("uniques-indicator").text(localStorage.getItem("urls") ? localStorage.getItem("urls").split(",").length : "0");
        }
    }
}

chrome.storage.local.get(function(s){ 
    Obj = s;
});

chrome.storage.onChanged.addListener(function(){chrome.storage.local.get(function(s){ 
        Obj = s;

        if(Obj.popup.enabled && !$("#extension-switch").is(':checked')) { 
            $("#extension-switch").click();
        } else if(!Obj.popup.enabled && $("#extension-switch").is(':checked')) {
            $("#extension-switch").click();
        }

        if(Obj.general.connected) {
            $("#status")[0].setAttribute("fill", "lightgreen");
        } else {
            $("#status")[0].setAttribute("fill", "red");
        }
    });
})