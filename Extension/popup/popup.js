function getStorage(){
	chrome.storage.local.get(function(callback){
		storage = callback;
		main();
	});
};

chrome.storage.onChanged = getStorage(); getStorage();

function UpdateStorage(path, action, value){
	chrome.storage.local.get(function(callback){
		storage = callback;
		if(path == 'settings.storeUrls'){
			if(action == 'set'){
				storage.settings.storeUrls = value;
			}
		}else if(path == 'settings.whitelist'){
			if(action == 'add' && value.length > 4 && callback.settings.whitelist.indexOf(value) == -1){
				storage.settings.whitelist.push(value)
			}else if(action == 'remove' && value.length > 4 && callback.settings.whitelist.indexOf(value) >= 0){
				index = storage.settings.whitelist.indexOf(value);
				storage.settings.whitelist.splice(index, 1);
			}
		};chrome.storage.local.set(storage);
	});
};

function main(){
	if(storage.settings.storeUrls){
		document.getElementsByName('storefiles')[0].checked = true;
	}else{
		document.getElementsByName('storefiles')[0].checked = false;
	};
};

document.querySelector("input[name=storefiles]").onchange = function(){
	if(this.checked){
		UpdateStorage('settings.storeUrls', 'set', true);
	}else{
		UpdateStorage('settings.storeUrls', 'set', false);
	}
};

document.getElementById('add').addEventListener('click', function(){
	UpdateStorage('settings.whitelist', 'add', document.getElementById('whitelist').value); document.getElementById('whitelist').value = '';
});
document.getElementById('remove').addEventListener('click', function(){
	UpdateStorage('settings.whitelist', 'remove', document.getElementById('whitelist').value); document.getElementById('whitelist').value = '';
});
document.getElementsByTagName('h1')[0].addEventListener('click', function(){
	window.open('/settings/urls.html', "", "width=1200,height=300");
})
document.getElementById('done').addEventListener('click', function(){
	list = document.getElementById('urllist').value.split(/,[^a-zA-Z]*/); document.getElementById('urllist').value == '';
	for(x in list){xhr = new XMLHttpRequest; xhr.open("GET", "http://localhost:8089/?url="+encodeURIComponent(list[x])); xhr.send()};
});
