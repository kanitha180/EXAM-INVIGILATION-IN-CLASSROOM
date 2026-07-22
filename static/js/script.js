async function updateDashboard() {

    try {

        const response = await fetch("/status");

        const data = await response.json();

        document.getElementById("persons").innerHTML = data.persons;

        document.getElementById("head").innerHTML = data.head_pose;

        document.getElementById("phone").innerHTML = data.phone;

        document.getElementById("alerts").innerHTML = data.alerts;

        document.getElementById("risk").innerHTML =
            data.risk_score + "% (" + data.risk_level + ")";

    }

    catch(error){

        console.log(error);

    }

}

updateDashboard();

setInterval(updateDashboard,1000);