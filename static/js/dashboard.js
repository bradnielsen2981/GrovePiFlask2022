/* This is your dashboard javascript, it has been embedded into dashboard.html */
//Load the Grove
function load_grove()
{
    document.getElementById("load").style.display = 'none';
    new_ajax_helper('/groveload', show_dashboard);
}

//Shutdown the Grove
function shutdown_grove()
{
    hide_dashboard();
    document.getElementById("load").style.display = 'none';
    new_ajax_helper('/groveshutdown', showloadbutton);
}

function showloadbutton()
{
    document.getElementById("load").style.display = 'block';
}

//Show the dashboard
function show_dashboard(results)
{
    document.getElementById("load").style.display = 'none';
    document.getElementById("dashboard").style.display = 'block';
    document.getElementById("videofeed").innerHTML = '<img src="/videofeed" width=100% />';
    console.log(results);
}

//Hide the dashboard
function hide_dashboard()
{
    document.getElementById("load").style.display = 'block';
    document.getElementById("dashboard").style.display = 'none';
    document.getElementById("videofeed").innerHTML = "";
}

//hide or show dashboard based on initial value from server on page load
if (grove_enabled == 1) {
    show_dashboard();
} else {
    hide_dashboard();
}

//print a message to the screen
function printmessage(results)
{
    document.getElementById("message").innerText = results.message;
}

//shutdown the application
function shutdown()
{
    alert("shutdown");
    new_ajax_helper('/shutdown');
}
