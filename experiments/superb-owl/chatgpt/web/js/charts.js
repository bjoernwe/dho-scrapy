const OUTPUT_BASE = window.location.href.includes("web") ? ".." : ".";
const users = [''];

function renderPage() {
  $('select').html(`
    ${users.map(user => `
    <option value="${user.id}">${user.title}</option>
    `)}
  `);
  const startUserID = window.location.hash.replace('#', '') || "something-frame"
  $('select').val(startUserID);
  pickUser();
}

function renderUser(user) {
  $("#Chart").html("");
  renderChart(user)
}

function renderChart(data) {
  console.log("render chart", data);
  let chart = LineChart(data, {
    title: d => `Pleasure: ${d.pleasure}\nPain: ${d.pain}\nConcentration: ${d.concentration}\nPeak Experience: ${d.peak_experience}`,
    x: d => new Date(d.date),
    ys: [
      d => d.pleasure,
      d => d.pain,
      d => d.concentration,
      d => d.peak_experience,
    ],
    defined: d => true,
    yDomain: [1, 5],
    width: 600,
    height: 500,
    colors: ['green', 'red', 'steelblue', 'orange'],
  });
  $("#Chart").append(chart);
}

function pickUser(userID) {
  userID = userID || $('select').val();
  window.location.hash = userID;
  d3.json(`${OUTPUT_BASE}/data.json`).then(userDetails => {
    renderUser(userDetails);
  });
}

renderPage();
