var  url = `${location.host}/chat/{{profile.user.id}}`
console.log(location.hostname,location.protocol)
if (location.protocol==="https:") 
  url = "wss://"+url;
else
  url = 'ws://'+url;
  var websocket = new WebSocket(url)
  console.log(websocket)
  websocket.onopen = function(e){
      console.log("connected",websocket)
  }
  websocket.onmessage = function(e){
      console.log(e.data)
      data = JSON.parse(e.data)
      if(data?.message){
        updatemsg(data.message,data.sender)
      }
  }
  websocket.onclose = function(e){
      console.log(e)
  }
  function sendMessage(){
    var message = document.getElementById('message').value;
    message = message.trim()  
    if(message)
      websocket.send(JSON.stringify({'message':message,'sender':'{{user}}','recepient':'{{profile.pk}}'}));
    
  }
  function updatemsg(message,sender)
  {
      var lhtml = `
        <div class="card-text  m-3 text-left"><span class = "bg-primary text-light  pt-2 pb-2 pl-3 pr-3 rounded-pill ">${message}</span></div>`;
      var rhtml = ` 
        <div class="card-text  m-3 text-right"><span class = "bg-success text-light pt-2 pb-2 pl-3 pr-3 rounded-pill">${message}</span></div>`; 
      if(sender==='{{user.profile}}')
        document.querySelector('#chatContainer').innerHTML+=rhtml;
      else
        document.body.querySelector('#chatContainer').innerHTML+=lhtml;
      document.getElementById('message').value=""
  }
  document.getElementById('message').addEventListener('keydown',function(e){
     if(e.key=="Enter")
      sendMessage();
  })