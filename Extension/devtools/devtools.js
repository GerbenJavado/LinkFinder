chrome.runtime.sendMessage({"log":"Devtools started..."});

chrome.devtools.network.onNavigated.addListener(function(callback){
	domain = callback.split('/')[2]; domain = domain.split('.')[domain.split('.').length-2]+'.'+domain.split('.')[domain.split('.').length-1];
	chrome.runtime.sendMessage({"domain":domain});
});

chrome.devtools.network.onRequestFinished.addListener(function(request){
	if(request.response.content.mimeType == "application/javascript" || request.response.content.mimeType == "text/javascript" && request.response.status == 200){
		chrome.runtime.sendMessage({"toServer":request.request.url});
	};
});