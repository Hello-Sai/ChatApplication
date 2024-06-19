const path =location.pathname; // This gives you "/some/path/24"
function containsOnlyDigits(str) {
    return /^\d+$/.test(str);
}
// Find the index of the last "/"
const lastIndex = path.lastIndexOf('/');

// Extract the last segment using slice
const profileId = path.slice(lastIndex + 1);
var url;
if (location.protocol === "https:") {
    url = `wss://${location.host}/chats/notifications`;
  } else {
    url = `ws://${location.host}/chats/notifications`;
  }
// url = `wss://redis://red-cpp2nfuehbks73bqo4l0:6379/chats/notifications`
var notification_socket = new WebSocket(url);
notification_socket.onopen = function(e){
    console.log('profile',profileId)
console.log('connected',containsOnlyDigits(profileId))
if(containsOnlyDigits(profileId)){

    notification_socket.send(JSON.stringify({'id':profileId}))
    console.log('sent')
}

} 
function playNotificationSound() {
    new Audio('/static/media/mixkit-correct-answer-tone-2870.wav').play();
    console.log('played')
}
notification_socket.onmessage = function(e){
console.log(e.data)
var data = JSON.parse(e.data)
containsOnlyDigits(profileId) && (data = data.filter(item => item.chat__sender != profileId) )
//data = new Set(data)

// if(document.getElementById('profile_id')){
//     console.log(document.getElementById('profile_id'))
// }
// console.log(profileId)
// data = profileId ?  data.filter(item => item.chat.user_id !== profileId): data

console.log(data)

data.forEach(item => {
    const profile_id = item.chat__sender;
    const notificationCount = item.count;
    const notificationBadge = document.getElementById(`notification-${profile_id}`)
    console.log(notificationBadge)
    !containsOnlyDigits(profileId) && playNotificationSound();
    console.log('digits only',containsOnlyDigits(profileId))
    if (notificationBadge) {
        notificationBadge.textContent = notificationCount > 0 ? notificationCount : '';
    }
});

//document.getElementById("notification_count").innerHTML += `<h1>${data['count']}`
}