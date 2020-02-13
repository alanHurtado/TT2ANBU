/*
  Variables Globales para la obtención de tokens:
  
  -URL_SITE: URL del sítio principal del sistema.

  -ID_APP_INSTAGRAM: Identificador de la aplicación de Instagram. Este id se encuentra
  en la visualiación básica de aplicaciones en la cuenta developer de Facebook; 
  https://developers.facebook.com/apps/
*/
var URL_SITE = "https://gitlopez95.github.io/";
var ID_APP_INSTAGRAM = "186564886057575";
var ACCESS_TOKEN = "IGQVJWTTItb216am1YUzRET2hyZA0hvbE4zcnQwQk1zRnVXeW5SdkRHenFZANTNMeFk0U3RGR0dhZAm5FTThYaTdUaWNWUDI1TkVRN2hrNjlMSzRFRkZAWSW9QMlY3NkUtTVc0QkM1OVVNa3ZAPRmhhSkFKQlducmIwa3Y0enBn";

function getToken(){
  var auth_code = document.getElementById('auth_code').value;
  if(auth_code != ""){
    var formData = {
      'client_id' : "186564886057575",
      'client_secret' : "96d4011d17f660f9665fa9511f8963e9",
      'grant_type' : "authorization_code",
      'redirect_uri' : "https://gitlopez95.github.io/",
      'code' : auth_code
    };
    $.ajax({      
        type: 'POST',
        url:"https://api.instagram.com/oauth/access_token ",
        data: formData,
        dataType : 'json',
        encode : true,
        success: function(respuesta) {         
          ACCESS_TOKEN = respuesta.access_token;
          console.log(respuesta);
          alert("TOKEN Obtenido, Realizar Query Básico.");        
        },
        error: function(data) {
              alert(data.statusText);            
              console.log("No se ha podido obtener la información");
          }
      });  
  }else{
    alert("Introduce un código de autorización.");
  }/*if-else*/
}/*getToken*/


function basicQuery(){
  $.ajax({
    url:"https://graph.instagram.com/17855628364757034?fields=id,media_type,media_url,username,timestamp&access_token="+ACCESS_TOKEN,
    success: function(respuesta) {
      console.log(respuesta);
      var answData = JSON.stringify(respuesta);
      //alert(answData);
      //alert(respuesta.media_url);
      var mensaje = "Id de Publicación: "+respuesta.id+"\n";
      mensaje+= "Username: "+respuesta.username+"\n";
      mensaje+= "Tipo de Publicación: "+respuesta.media_type+"\n";
      mensaje+= "URL de Publicación: "+respuesta.media_url+"\n";
      mensaje+= "Fecha de Publicación: "+respuesta.timestamp+"\n";
      alert(mensaje);
    },
    error: function(data){
        alert(data.statusText);            
        console.log("No se ha podido obtener la información");
      }
  });
}/*basicQuery*/