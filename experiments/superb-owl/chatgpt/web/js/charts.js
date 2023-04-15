const OUTPUT_BASE = window.location.href.includes("web") ? ".." : ".";
const users = [''];

function renderPage() {
  $('select').html(`
    ${users.map(user => `
    <option value="${user.id}">${user.title}</option>
    `)}
  `);
  const startUserID = window.location.hash.replace('#', '') || "curious-frame"
  $('select').val(startUserID);
  pickUser();
}

function renderUser(user) {
  $("#Chart").html("");
  renderChart(user)
}

function renderMessage(datum) {
  $("#Message").text(datum.msg);
}

const attributeColors = {
  'pain': 'red',
  'pleasure': 'green',
  'concentration': 'steelblue',
  'peak_experience': 'orange',
  'visual_phenomena': '#593DAB',
  'auditory_phenomena': '#7257C5',
  'tactile_phenomena': '#917CD3',
  'energetic_phenomena': '#B1A1E0',
  'gratitude': 'aquamarine',
  'compassion': 'darkgreen',
  'bitterness': 'brown',
  'fear': 'black',
  'equanimity': 'dimgrey',
  'insight': 'deeppink',
}

function renderChart(data) {
  console.log("render chart", data);
  const attributes = Object.keys(data[0]).filter(key => key !== "date" && key != "msg_id" && key != "msg");
  let chart = LineChart(data, {
    title: d => attributes.map(attr => `${attr}: ${d[attr]}`).join("\n"),
    x: d => new Date(d.date),
    ys: attributes.map(attr => d => d[attr] || 0),
    defined: d => true,
    yDomain: [1, 5],
    width: 600,
    height: 500,
    colors: attributes.map(attr => attributeColors[attr]),
    selected: d => renderMessage(d),
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
