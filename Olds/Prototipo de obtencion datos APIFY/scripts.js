/*
  En el sítio de APIFY tenemos un "actorTaskId" que es el identificador
  de actor que realizará la tarea de scrapping en Instagram.
  El sítio nos proporciona un "token" permanente con el cuál accederemos
  a los servicios.
*/
var actorTaskId = "PE7drWyJCrT9z2wj8";
var token = "RR2h79SdNi6nrWecwM5XGAutQ";

/*Esta función se encarga de realizar la búsqueda con la API del sítio APIFY*/
function apify() {
  document.getElementById('data_table').innerHTML= "";
  var name_usr = document.getElementById('name_usr').value;
  var max_results = document.getElementById('max_results').value;
  if(name_usr==""){
    alert("Introduzca un nombre válido\n");
    return 0;
  }
  
  document.getElementById('status').innerHTML = "Buscando...espere";
  var request = new XMLHttpRequest();
  
  request.open('POST', 'https://api.apify.com/v2/actor-tasks/'+actorTaskId+'/run-sync?token='+token+'&outputRecordKey=OUTPUT',"false");
  request.setRequestHeader('Content-Type', 'application/json');
  
  request.onreadystatechange = function () {
    if (this.readyState === 4) {
      document.getElementById('status').innerHTML = "Búsqueda realizada con éxito";
      console.log('Status:', this.status);
      console.log('Headers:', this.getAllResponseHeaders());
      console.log('Body:', this.responseText);
      get_last_dataset();
    }
  };

  var body = {
    "search": name_usr,
    "searchType": "user",
    "searchLimit": parseInt(max_results),
    "resultsType": "posts",
    "resultsLimit": 1,
    "proxy": {
      "useApifyProxy": true,
      "apifyProxyGroups": []
    }
  };

  request.send(JSON.stringify(body));
  /*-----------------------------------------------*/
}/*APIFY_function*/

/*Esta función recupera los datos obtenidos de la búsqueda en la 
función apify(), recupera los items de un DataSet almacenado en 
el sítio de APIFY*/
function get_last_dataset(){
  var request_recv = new XMLHttpRequest();
  request_recv.open('GET', 'https://api.apify.com/v2/actor-tasks/'+actorTaskId+'/runs/last/dataset/items?token='+token+'&status=SUCCEEDED');
  request_recv.setRequestHeader('Content-Type', 'application/json');
  
  request_recv.onreadystatechange = function () {
    if (this.readyState === 4) {
      console.log('Status:', this.status);
      console.log('Headers:', this.getAllResponseHeaders());
      //console.log('Body:', this.responseText);
      var str_response = this.responseText.replace(/#debug/g,"debug");
      
      /*Parte de la vista----*/
      data_view(str_response);
      /*-------------------*/
        
    }
  };/*onreadystate-function*/
  request_recv.send();
}/*recover_data*/

/*Función para mostrar los datos en la página de búsqueda*/
function data_view(strData) {
  var data = JSON.parse(strData);
  
  var str_table = "<table border=1>"+
  "<tr><th>#</th><th>Username</th><th>Nombre</th><th>URL Perfil</th>"+
  "</tr>";
  
  for(var i in data){
    index = parseInt(i)+1;
    str_table+="<tr><td>"+index+"</td>"+
    "<td>@"+data[i].debug.userUsername+"</td>"+
    "<td>"+data[i].debug.userFullName+"</td>"+
    "<td><a href="+data[i].debug.url+" target='_blank'>"+data[i].debug.url+
    "</tr>";
  }

  document.getElementById('data_table').innerHTML=str_table;
  
}/*data_view*/