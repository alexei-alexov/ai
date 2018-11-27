const DELAY = 200; // delay in ms to add new data points
const DELTA_PACKETS = 10;

// create a graph2d with an (currently empty) dataset
var container = document.getElementById('graph');
var dataset = new vis.DataSet();

var bandwidth_rate = 10;

var packets_range = document.getElementById('packets_range');

var options = {
    start: vis.moment().add(-30, 'seconds'), // changed so its faster
    end: vis.moment(),
    dataAxis: {
        left: { range: { min: 0, max: 300 } }
    },
    drawPoints: {
        style: 'circle' // square, circle
    },
    shaded: {
        orientation: 'bottom' // top, bottom
    }
};
var graph2d = new vis.Graph2d(container, dataset, options);


function renderStep() {
    var now = vis.moment();
    var range = graph2d.getWindow();
    var interval = range.end - range.start;
    graph2d.setWindow(now - interval, now, {animation: false});
    requestAnimationFrame(renderStep);
    // setTimeout(renderStep, DELAY);
}


function low(rate){
    if (rate <= 80) return 1;
    if (rate >= 100) return 0;
    return (100 - rate) / 20;
}

function high(rate){
    if (rate <= 100) return 0;
    if (rate >= 120) return 1;
    return (rate - 100) / 20;
}

function step() {
    // add a new data point to the dataset
    var now = vis.moment();
    let packets = parseInt(packets_range.value);
    packets = Math.floor(packets + DELTA_PACKETS * (low(packets) - high(packets)));
    packets_range.value = packets;

    dataset.add({
        x: now,
        y: packets
    });
    // remove all data points which are no longer visible
    var range = graph2d.getWindow();
    var interval = range.end - range.start;
    var oldIds = dataset.getIds({
        filter: function (item) {
        return item.x < range.start - interval;
        }
    });
    dataset.remove(oldIds);
    setTimeout(step, DELAY);
}

// calculations
step();
// render
renderStep();