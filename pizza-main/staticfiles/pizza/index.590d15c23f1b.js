// Creating listening to the form
document.addEventListener('DOMContentLoaded', load);
function load()
{

document.querySelectorAll("form").onclick = function (){
let request = new XMLHttpRequest();
request.onload = () => {
    const contents = JSON.parse(request.responseText);

}

return false;
}
}

// Sending info for each form and keeping active the same page

// Updating info so as to client looks at which order has been added

