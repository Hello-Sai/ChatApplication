          var url = `${location.host}/chats/online`;
          if (location.protocol==="https:") 
              url = "wss://"+url;
          else
              url = 'ws://'+url;
          var websocket = new WebSocket(url)
          websocket.onopen = function(e){
              console.log("connected to")
          }
          websocket.onmessage = function(e){
              data = JSON.parse(e.data)
              console.log(data,data.status)
              var element = document.getElementById(data.id);
              console.log(element);
              if(element)
                if(data.status){
                    element.classList.add('status-indicator')
                }
                else{
                    element.classList.remove('status-indicator')
                }
              
          }
          websocket.onclose = function(e){
            console.log("DISCONNECTED")
          }