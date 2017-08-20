chrome.runtime.sendMessage({"log":"Devtools started..."});

chrome.devtools.network.onRequestFinished.addListener(function(request){
    if(request.response.content.mimeType == "application/javascript" && request.response.status == 200){
			chrome.runtime.sendMessage({"toServer":request.request.url}); 
	}
});

//-----------------------------------------------------TODO-----------------------------------------------------
//Add Domain check functionality
//
//function RemoveSubdomains(){
//	characters = domain.split(''); dots = 0;
//	for(i = characters.length-1; i > 0; i--){
//		if(characters[i] == '.' && dots < 2){
//			dots++;
//		}else if(dots == 2){
//			domain = domain.slice(i+2);
//			break
//		}
//	}
//}
//
//if(typeof domain != undefined && request.response.content.mimeType == "application/javascript" && request.response.status == 200){
//		if(domain in request.request.url){;
//			SendToServer(request.request.url);
//		}
//	}
