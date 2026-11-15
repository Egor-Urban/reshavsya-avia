// frontend/app.js


let chart = null;
function tok() { return localStorage.getItem("t"); }


function logout() {
    localStorage.removeItem("t");
    location.href = "/login.html";
}


function h() {
    return {"Content-Type": "application/json", "Authorization": "Bearer " + tok()};
}


async function init() {
    if (!tok()) { location.href = "/login.html"; return; }
    const res = await fetch("/api/routes", {headers: h()});
    if (res.status === 401) { location.href = "/login.html"; return; }
    const routes = await res.json();
    const sel = document.getElementById("route");

    routes.forEach(r => {
        const o = document.createElement("option");
        o.value = r.route;
        o.textContent = r.name;
        sel.appendChild(o);
    });
}


async function loadDates() {
    const route = document.getElementById("route").value;
    const sel = document.getElementById("date");

    sel.innerHTML = "";

    if (!route) return;
    const res = await fetch("/api/dates/" + route, {headers: h()});
    const dates = await res.json();

    dates.forEach(d => {
        const o = document.createElement("option");
        o.value = d;
        o.textContent = d;
        sel.appendChild(o);
    });
}


async function run() {
    const route = document.getElementById("route").value;
    const date = document.getElementById("date").value;
    const price = parseFloat(document.getElementById("price").value);
    const err = document.getElementById("err");

    err.textContent = "";

    if (!route || !date || isNaN(price) || price < 0) {
        err.textContent = "Заполните все поля";
        return;
    }

    const res = await fetch("/api/forecast", {
        method: "POST",
        headers: h(),
        body: JSON.stringify({route, date, price})
    });

    if (!res.ok) { err.textContent = "Рейс не найден"; return; }
    show(await res.json());
}


function show(d) {
    document.getElementById("v-seats").textContent = d.seats;
    document.getElementById("v-want").textContent = Math.round(d.want);
    document.getElementById("v-buy").textContent = Math.round(d.buy);
    document.getElementById("v-rec").textContent = d.rec_price.toLocaleString("ru-RU");
    document.getElementById("res").style.display = "block";
    document.getElementById("chart-block").style.display = "block";
    drawChart(d.chart, d.seats);
}

function drawChart(data, seats) {
    const labels = data.map(x => "Q" + x.q);
    const wants = data.map(x => x.want);
    const buys = data.map(x => x.buy);
    const line = data.map(() => seats);

    if (chart) chart.destroy();
    chart = new Chart(document.getElementById("chart"), {
        data: {
            labels,
            datasets: [
                {type: "bar", label: "Хотят купить", data: wants, backgroundColor: "#aaa"},
                {type: "bar", label: "Купят", data: buys, backgroundColor: "#222"},
                {type: "line", label: "Мест в самолёте", data: line,
                    borderColor: "#c00", backgroundColor: "transparent",
                    borderWidth: 2, pointRadius: 0, borderDash: [6, 4]}
            ]
        },

        options: {
            responsive: true,
            scales: {
                y: {beginAtZero: true, grid: {color: "#eee"}},
                x: {grid: {display: false}}
            },
            plugins: {legend: {position: "top"}}
        }
    });
}



// INIT functions
init();