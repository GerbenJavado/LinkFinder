chrome.storage.local.get(function(result){CreateTable(result)});

function CreateTable(storage){
	if(storage.urls.length > 0){
		var tr = ''; for(x in storage.urls){
				tr += '<tr><td>'+storage.urls[x]+'<a href="#url:'+x+'"class="remove">x</a></td></tr>';
		}; table = '<table id="urls">'+tr+'</table>'; document.getElementById('urls-container').innerHTML = table;
	}
};

function search(){
	input = document.getElementById('search-urls');
	filter = input.value.toUpperCase();
	table = document.getElementById('urls');
	tr = table.getElementsByTagName('tr');
	for(y = 0; y < tr.length; y++){
		td = tr[y].getElementsByTagName('td')[0];
		if(td && td.innerHTML.toUpperCase().indexOf(filter) == -1){
			tr[y].style.display = "none";
		}else if(td && td.innerHTML.toUpperCase().indexOf(filter) > -1){
			tr[y].style.display = "";
		}
	}
};

window.addEventListener('hashchange', function(){
	if(location.hash.startsWith('#url:')){
		url = document.getElementsByTagName('td')[Number(location.hash.slice(5))].innerHTML.split('<a href')[0];
		document.getElementsByTagName('td')[Number(location.hash.slice(5))].parentElement.style.display = "none";
		chrome.runtime.sendMessage({"url_remove":url});
	}
});

document.getElementById('search-urls').addEventListener('keyup', function(){search()});
document.getElementsByTagName('button')[0].addEventListener('click', function(){location = '/settings/domains.html'});