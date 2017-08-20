chrome.storage.local.get(function(result){CreateTable(result)});

function CreateTable(storage){
	if(storage.settings.whitelist.length > 0){
		var tr = ''; for(x in storage.settings.whitelist){
			tr += '<tr><td>'+storage.settings.whitelist[x]+'<a href="#domain:'+x+'"class="remove">x</a></td></tr>';
		}; table = '<table id="domains">'+tr+'</table>'; document.getElementById('domains-container').innerHTML = table;
	}
};

function search(){
	input = document.getElementById('search-domains');
	filter = input.value.toUpperCase();
	table = document.getElementById('domains');
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
	if(location.hash.startsWith('#domain:')){
		url = document.getElementsByTagName('td')[Number(location.hash.slice(8))].innerHTML.split('<a href')[0];
		document.getElementsByTagName('td')[Number(location.hash.slice(8))].parentElement.style.display = "none";
		chrome.runtime.sendMessage({"domain_remove":url});
	}
});

document.getElementById('search-domains').addEventListener('keyup', function(){search()});
document.getElementsByTagName('button')[0].addEventListener('click', function(){location = '/settings/urls.html'});