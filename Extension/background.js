function SendToServer(url){
	xhr = new XMLHttpRequest; xhr.open("GET", "http://localhost:8080/?url="+encodeURIComponent(url), false);
	urlDomain = url.split('/')[2];
	if(storage.settings.whitelist.length == 0 && urlDomain.indexOf(domain) >= 0){
		try{xhr.send();}catch(e){};		
	}else if(storage.settings.whitelist.length > 0){
		for(x in storage.settings.whitelist){
			if(urlDomain.indexOf(storage.settings.whitelist[x]) != -1){
				try{xhr.send();}catch(e){};	
			}else if(storage.settings.whitelist[x].split(/,[^*]*/).length >= 2 && storage.settings.whitelist[x].split(/,[^*]*/)[1] != ""){
				if(domain.indexOf(storage.settings.whitelist[x].split(/,[^*]*/)[0]) >= 0){
					try{xhr.send();}catch(e){};
				}
			}else if(storage.settings.whitelist[x].split(/,[^a-zA-Z]*/).length >= 2){
				for(y in storage.settings.whitelist[x].split(/,[^a-zA-Z]*/)){
					if(urlDomain.indexOf(storage.settings.whitelist[x].split(/,[^a-zA-Z]*/)[y]) >= 0){
						console.log(urlDomain)
					}
				}
			}
		};
	}
};

function StoreUrl(url){
	if(url.startsWith('http') && storage.settings.storeUrls && storage.urls.indexOf(url) == -1){
		if(storage.settings.whitelist.length > 0){
			for(y in storage.settings.whitelist){
				if(url.indexOf(storage.settings.whitelist[y]) != -1){
					UpdateStorage('urls', 'add', url);
				}
			}
		}else{
			UpdateStorage('urls', 'add', url);
		}
	}
};

function UpdateStorage(path, action, value){
	chrome.storage.local.get(function(callback){
		storage = callback;
		if(Object.keys(storage).length == 0){
			chrome.storage.local.set({"settings":{"storeUrls": false, "whitelist":[]}, "urls":[]})
		};
		if(path == 'settings.storeUrls'){
			if(action == 'set'){
				storage.settings.storeUrls = value;
			}
		}else if(path == 'urls'){
			if(action == 'add'){
				storage.urls.push(value)
			}else if(action == 'remove'){
				index = storage.urls.indexOf(value);
				storage.urls.splice(index, 1);
			}
		}else if(path == 'settings.whitelist'){
			if(action == 'add' && value.length >= 1 && callback.settings.whitelist.indexOf(value) == -1){
				storage.settings.whitelist.push(value)
			}else if(action == 'remove' && value.length >= 1 && callback.settings.whitelist.indexOf(value) >= 0){
				index = storage.settings.whitelist.indexOf(value);
				storage.settings.whitelist.splice(index, 1);
			}
		};chrome.storage.local.set(storage);
	});
};

chrome.runtime.onMessage.addListener(function(message, sender, respond){
	if(message.log){
		console.log(message.log);
	}else if(message.toServer){
		SendToServer(message.toServer);
		StoreUrl(message.toServer);
	}else if(message.domain){
		domain = message.domain;
	}else if(message.url_remove){
		UpdateStorage('urls', 'remove', message.url_remove);
	}else if(message.domain_remove){
		UpdateStorage('settings.whitelist', 'remove', message.domain_remove);
	}
});

chrome.storage.onChanged.addListener(function(){UpdateStorage()}); UpdateStorage();