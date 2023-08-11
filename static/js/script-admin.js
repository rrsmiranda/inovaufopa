var mycolors = [
  "#476088",
  "#7d61e8",
  "#61a8e8",
  "#4fddc3",
  "#abde6d",
  "#60cf83",
  "#ffc562",
  "#cf60bc",
  "#ff6d74",
  "#60cf83",
];

var radarChartOptions = {
  w: 200,
  h: 200,
  //margin: margin,
  maxValue: 60,
  levels: 6,
  roundStrokes: false,
  color: d3.scaleOrdinal().range(mycolors),
  format: ".0f",
  legend: { title: "", translateX: 100, translateY: 40 },
  unit: "",
};


var radarChartOptions2 = {
  w: 200,
  h: 200,
  //margin: margin,
  maxValue: 5,
  levels: 5,
  roundStrokes: false,
  color: d3.scaleOrdinal().range(mycolors),
  format: ".0f",
  legend: { title:'' , translateX: 100, translateY: 40 },
  unit: "",
};

var chartOption = {
  w: 200,
  h: 200,
  color: d3.scaleOrdinal().range(mycolors),
};

// var data = [{
//   axes: [
//     {axis: 'Clima', value: 4},
//     {axis: 'Sucesso', value: 2},
//     {axis: 'Recursos', value: 6},
//     {axis: 'Comportamento', value: 2.6},
//     {axis: 'Valores', value: 3.5},
//     {axis: 'Processo', value: 2}
//   ]
// }]

function processaDados() {
  
  console.log('dadosgerais',dadosgerais)
  let svg_radar2 = RadarChart("#radarChart", dadosgerais, radarChartOptions2);
}

function remove_empty_bins(source_group) {
  return {
    all: function () {
      return source_group.all().filter(function (d) {
        return d.value != 0;
      });
    },
  };
}

var dadosGerais;
var timeFiltro;
$(document).ready(function () {
  processaDados()

  // function getRespostas(ano, unidade, area, cargo) {
  //   $.ajax({
  //     url: `/filtro?ano=${ano}&unidade=${unidade}&area=${area}&cargo=${cargo}`,
  //     type: "GET",
  //     success: function (result) {
  //       console.log(result);
  //       dadosGerais = result['geral']
  //       processaDados()
  //       // var lat_lng = {{ lat_lng|tojson|safe }};
  //       // document.location.reload(true);
  //       // window.location.replace("/");
  //     },
  //   });
  // }
  // getRespostas(2022, '', '', '')
});
