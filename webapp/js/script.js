
$( document ).ready( function() {
  // init Isotope
  for(var i = 0; i < csvdata.length; i++) {
    $(".isotope").append("<a href='#'' class='addChart'><div class='element-item " 
       + csvdata[i][1] + "' data-category='"+ csvdata[i][1] + "' data-series='" +
       csvdata[i][3] + "'><p><span class='name'>" + csvdata[i][0] + "</span> - <span class='number'>" +
       csvdata[i][4] + "</span></p></div></a>");
  }

  var $container = $('.isotope').isotope({
    itemSelector: '.element-item',
    layoutMode: 'fitRows',
    getSortData: {
      name: '.name',
      symbol: '.symbol',
      number: '.number parseInt',
      category: '[data-category]',
      weight: function( itemElem ) {
        var weight = $( itemElem ).find('.weight').text();
        return parseFloat( weight.replace( /[\(\)]/g, '') );
      }
    }
  });

  // filter functions
  var filterFns = {
    // show if number is greater than 50
    numberGreaterThan50: function() {
      var number = $(this).find('.number').text();
      return parseInt( number, 10 ) > 50;
    },
    // show if name ends with -ium
    ium: function() {
      var name = $(this).find('.name').text();
      return name.match( /ium$/ );
    }
  };

  // bind filter button click
  $('#filters').on( 'click', 'button', function() {
    var filterValue = $( this ).attr('data-filter');
    // use filterFn if matches value
    filterValue = filterFns[ filterValue ] || filterValue;
    $container.isotope({ filter: filterValue });
  });

  // bind sort button click
  $('#sorts').on( 'click', 'button', function() {
    var sortByValue = $(this).attr('data-sort-by');
    if (sortByValue === "random") {
      $container.isotope({ sortBy : 'random' });
    } else {
      $container.isotope({ sortBy: sortByValue, sortAscending: { 'number': false } });
    }
  });

  
  // change is-checked class on buttons
  $('.button-group').each( function( i, buttonGroup ) {
    var $buttonGroup = $( buttonGroup );
    $buttonGroup.on( 'click', 'button', function() {
      $buttonGroup.find('.is-checked').removeClass('is-checked');
      $( this ).addClass('is-checked');
    });
  });

  $('.addChart').on('click', 'div', function() {
    var data = $(this).attr('data-series').split(",");
    for(var i=0; i<data.length; i++) { data[i] = +data[i]; } 
    var label = $(this).find("span.name")[0].innerText;
    updateDataToPlot(data, label);
  });

  $("#clear").on('click', function() {
    dataToPlot = [];
    columnsToPlot = [];
    colorsToPlot = [];
    dataToPlot = [
        [new Date(2006,0)],
        [new Date(2007,0)],
        [new Date(2008,0)],
        [new Date(2009,0)],
        [new Date(2010,0)],
        [new Date(2011,0)],
        [new Date(2012,0)],
        [new Date(2013,0)],
        [new Date(2014,0)],
        [new Date(2015,0)]
    ];
    $("#chart").hide();
  });

  $("#subjects").click();
  $("#freq").click();
});

var originalData = [
        [new Date(2006,0)],
        [new Date(2007,0)],
        [new Date(2008,0)],
        [new Date(2009,0)],
        [new Date(2010,0)],
        [new Date(2011,0)],
        [new Date(2012,0)],
        [new Date(2013,0)],
        [new Date(2014,0)],
        [new Date(2015,0)]
];

var dataToPlot = originalData;
var columnsToPlot = [];
var colorsToPlot = [];

google.load('visualization', '1.1', {packages: ['line']});
//google.setOnLoadCallback(drawInstructions);


function drawChart() {
  $("#chart").show();
  var data = new google.visualization.DataTable();
  data.addColumn('date', 'Year');
  for (var i = 0; i < columnsToPlot.length; i++){
    data.addColumn('number', columnsToPlot[i]);
 }

  remove06 = dataToPlot.shift();
  data.addRows(dataToPlot);
  readd06 = dataToPlot.unshift(remove06);

  var options = {
    chart: {
      title: 'Tag Frequency Over Time',
      subtitle: 'as % of all tags from that tag group used that year',
      legend: {position: 'bottom' },
      hAxis: { format: 'yy', gridlines: { count: 10 } },
      vAxis: {format: '#\'%\'', gridlines: {color: '#333', count: 8} }
    },
    
    width: 800,
    height: 500,
    lineWidth: 10,
    colors: colorsToPlot,

  };

  var chart = new google.charts.Line(document.getElementById('linechart_material'));

  chart.draw(data, options);
}

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function updateDataToPlot(newLine, name) {
  for(var i = 0; i < dataToPlot.length; i++) {
    dataToPlot[i].push(newLine[i]);
  }
  columnsToPlot.push(name);
  colorsToPlot.push(getRandomColor());
  drawChart();
}

// debounce so filtering doesn't happen every millisecond
function debounce( fn, threshold ) {
  var timeout;
  return function debounced() {
    if ( timeout ) {
      clearTimeout( timeout );
    }
    function delayed() {
      fn();
      timeout = null;
    }
    timeout = setTimeout( delayed, threshold || 100 );
  }
}
