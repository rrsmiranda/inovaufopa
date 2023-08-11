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
  color: d3.scaleOrdinal().range(["#00ffbe"]),
  format: ".0f",
  labels:[],
  legend: { title: "Organization XYZ", translateX: 100, translateY: 40 },
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

var yearRingChart = new dc.PieChart("#chart-ring-year"),
  //spendHistChart = new dc.BarChart("#chart-hist-spend"),
  spenderRowChart = new dc.RowChart("#chart-row-setores"),
  femRowChart = new dc.RowChart("#chart-row-fem"),
  masRowChart = new dc.RowChart("#chart-row-mas"),
  outRowChart = new dc.RowChart("#chart-row-out"),
  cargoRowChart = new dc.RowChart("#chart-row-cargo"),
  areaRowChart = new dc.RowChart("#chart-row-area"),
  escoRowChart = new dc.RowChart("#chart-row-esco"),
  culRowChart = new dc.RowChart("#chart-row-cul"),
  relRowChart = new dc.RowChart("#chart-row-rel"),
  pesRowChart = new dc.RowChart("#chart-row-pes"),
  estRowChart = new dc.RowChart("#chart-row-est"),
  lidRowChart = new dc.RowChart("#chart-row-lid"),
  infRowChart = new dc.RowChart("#chart-row-inf");

function processaDados() {

  var ndxC = crossfilter(dadosCargo),
  allss = ndxC.groupAll(),
  cargoDim = ndxC.dimension(function (d) {
    return d.axis;
  });
  (qtdPerCargo = cargoDim.group().reduceSum(function (d) {
    return +d.value;
  }))
  cargoRowChart
    .width(350)
    .height(200)
    .dimension(cargoDim)
    .group(qtdPerCargo)
    .elasticX(true);

  var ndxA = crossfilter(dadosArea),
  allsA = ndxA.groupAll(),
  areaDim = ndxA.dimension(function (d) {
    return d.axis;
  });
  (qtdPerArea = areaDim.group().reduceSum(function (d) {
    return +d.value;
  }))
  areaRowChart
    .width(350)
    .height(200)
    .dimension(areaDim)
    .group(qtdPerArea)
    .elasticX(true);
      
  var ndxE = crossfilter(dadosEsco),
  allsE = ndxE.groupAll(),
  escoDim = ndxE.dimension(function (d) {
    return d.axis;
  });
  (qtdPerEsco = escoDim.group().reduceSum(function (d) {
    return +d.value;
  }))
  escoRowChart
    .width(350)
    .height(200)
    .dimension(escoDim)
    .group(qtdPerEsco)
    .elasticX(true);


  var ndx = crossfilter(dadosUnidades),
    all = ndx.groupAll(),
    yearDim = ndx.dimension(function (d) {
      return +d.ano;
    }),
    siglaDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    femDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    masDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    outDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    culDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    relDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    pesDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    estDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    infDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    lidDim = ndx.dimension(function (d) {
      return d.sigla;
    }),
    // spendDim = ndx.dimension(function (d) {
    //   return Math.floor(d.Spent / 10);
    // }),
    spendPerYear = yearDim.group().reduceSum(function (d) {
      return +d.sigla;
    }),
    spendPerSigla = siglaDim.group().reduceSum(function (d) {
      return 1;
    });
    
    //  spendHist = spendDim.group().reduceCount(),
    //  nonEmptyHist = remove_empty_bins(spendHist);

    siglaTypeGroup = siglaDim.group();

    (qtdPerFem = femDim.group().reduceSum(function (d) {
      return +d.fem;
    })),
    (qtdPerMas = masDim.group().reduceSum(function (d) {
      return +d.mas;
    })),
    (qtdPerOut = outDim.group().reduceSum(function (d) {
      return +d.out;
    })),
    (qtdPerCul = culDim.group().reduceSum(function (d) {
      return +d.processos;
    })),
    (qtdPerRel = relDim.group().reduceSum(function (d) {
      return +d.valores;
    })),
    (qtdPerInf = infDim.group().reduceSum(function (d) {
      return +d.clima;
    })),
    (qtdPerEst = estDim.group().reduceSum(function (d) {
      return +d.comportamentos;
    })),
    (qtdPerPes = pesDim.group().reduceSum(function (d) {
      return +d.recursos;
    })),
    (qtdPerLid = lidDim.group().reduceSum(function (d) {
      return +d.sucesso;
    })),
    //spendHistChart
    //  .width(300)
    //  .height(200)
    //  .dimension(spendDim)
    //  .group(nonEmptyHist)
    //  .x(d3.scaleBand())
    //  .xUnits(dc.units.ordinal)
    //  .elasticX(true)
    //  .elasticY(true);
    //
    //spendHistChart.xAxis().tickFormat(function (d) {
    //  return d * 10;
    //}); // convert back to base unit
    //spendHistChart.yAxis().ticks(2);

    yearRingChart
      .width(200)
      .height(200)
      .dimension(yearDim)
      .group(spendPerYear)
      .innerRadius(50);

    spenderRowChart
      .width(350)
      .height(200)
      .dimension(siglaDim)
      .group(spendPerSigla)
      .elasticX(true);

    femRowChart
      .width(350)
      .height(200)
      .dimension(femDim)
      .group(qtdPerFem)
      .elasticX(true);

    masRowChart
      .width(350)
      .height(200)
      .dimension(masDim)
      .group(qtdPerMas)
      .elasticX(true);

    outRowChart
      .width(350)
      .height(200)
      .dimension(outDim)
      .group(qtdPerOut)
      .elasticX(true);

    culRowChart
      .width(350)
      .height(200)
      .dimension(culDim)
      .group(qtdPerCul)
      .label((d) => d.key)
      .elasticX(true);

    relRowChart
      .width(350)
      .height(200)
      .dimension(relDim)
      .group(qtdPerRel)
      .elasticX(true);

    estRowChart
      .width(350)
      .height(200)
      .dimension(estDim)
      .group(qtdPerEst)
      .elasticX(true);

    lidRowChart
      .width(350)
      .height(200)
      .dimension(lidDim)
      .group(qtdPerLid)
      .elasticX(true);

    infRowChart
      .width(350)
      .height(200)
      .dimension(infDim)
      .group(qtdPerInf)
      .elasticX(true);

    pesRowChart
      .width(350)
      .height(200)
      .dimension(pesDim)
      .group(qtdPerPes)
      .elasticX(true);

    let svg_radar2 = RadarChart("#radarChart", dadosGerais, radarChartOptions2);
    dc.renderAll();
  }
// use static or load via d3.csv("dadosUnidades.csv").then(function(dadosUnidades) {/* do stuff */});

processaDados()


// let radarSetores = RadarChart(
//   "#radarChartSetores",
//   dadosUnidades,
//   radarChartOptions
// );

let setores_a_exibir = [];

function remove_empty_bins(source_group) {
  return {
    all: function () {
      return source_group.all().filter(function (d) {
        return d.value != 0;
      });
    },
  };
}

let lista_original = [];
function getListaOriginal() {
  let encontrados = $(".dc-chart rect");
  for (i = 0; i < encontrados.length; i++) {
    let setor = $(encontrados[i]).parent().find("text").text();
    if (!lista_original.includes(setor)) {
      lista_original.push(setor);
    }
  }
}
getListaOriginal();

function atualiza_radar(setores_selecionados_encontrados) {
  let setores_selecionados = [];
  if (!setores_selecionados_encontrados.length > 0)
    lista_original.forEach((e) => $("#" + e).show());
  else {
    for (i = 0; i < setores_selecionados_encontrados.length; i++) {
      let setor = $(setores_selecionados_encontrados[i])
        .parent()
        .find("text")
        .text();
      if (!setores_selecionados.includes(setor)) {
        setores_selecionados.push(setor);
      }
    }
    lista_original.forEach((e) => $("#" + e).hide());
    setores_selecionados.forEach((e) => $("#" + e).show());
  }
}

function atualiza_radar(setores_selecionados_encontrados) {
  let setores_selecionados = [];
  if (!setores_selecionados_encontrados.length > 0)
    lista_original.forEach((e) => $("#" + e).show());
  else {
    for (i = 0; i < setores_selecionados_encontrados.length; i++) {
      let setor = $(setores_selecionados_encontrados[i])
        .parent()
        .find("text")
        .text();
      if (!setores_selecionados.includes(setor)) {
        setores_selecionados.push(setor);
      }
    }
    lista_original.forEach((e) => $("#" + e).hide());
    setores_selecionados.forEach((e) => $("#" + e).show());
  }
}

function encontraPorPie() {
  let setores_selecionados_encontrados = $(".dc-chart rect[width!='0']");
  atualiza_radar(setores_selecionados_encontrados);
}

function encontraPorBar() {
  let setores_selecionados_encontrados = $(
    ".dc-chart rect.selected[width!='0']"
  );
  atualiza_radar(setores_selecionados_encontrados);
}

$(".dc-chart .pie-slice").click(function () {
  setTimeout(encontraPorPie, 800);
});

$(".dc-chart rect").click(function () {
  setTimeout(encontraPorBar, 800);
});

var timeFiltro;
$(document).ready(function () {
  $(".select2").select2();
  $(".select2#ano").select2({
    placeholder: "Ano",
    allowClear: true,
  });
  $(".select2#unidade").select2({
    placeholder: "Unidade",
    allowClear: true,
  });
  $(".select2#area").select2({
    placeholder: "Área",
    allowClear: true,
  });
  $(".select2#genero").select2({
    placeholder: "Gênero",
    allowClear: true,
  });

  function getRespostas(ano, unidade, area, cargo) {
    $.ajax({
      url: `/filtro?ano=${ano}&unidade=${unidade}&area=${area}&cargo=${cargo}`,
      type: "GET",
      success: function (result) {
        // console.log(result);
        dadosUnidades = result['lista']
        dadosGerais = result['geral']
        dadosCargo = result['dados_cargo']
        dadosArea = result['dados_area']
        dadosEsco = result['dados_esco']
        processaDados()
        // var lat_lng = {{ lat_lng|tojson|safe }};
        // document.location.reload(true);
        // window.location.replace("/");
      },
    });
  }

  $("#filtros :input").change(function () {
    clearTimeout(timeFiltro);
    timeFiltro = setTimeout(function () {
      ano = $("#ano").val();
      unidade = $("#unidade").val();
      area = $("#area").val();
      cargo = $("#cargo").val();
      // window.location.replace(`/filtro?ano=${ano}&unidade=${unidade}&area=${area}&genero=${genero}`)
      getRespostas(ano, unidade, area, cargo);

      //todo redirect page
    }, 2000);
  });
});
