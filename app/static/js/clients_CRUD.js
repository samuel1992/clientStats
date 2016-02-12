  var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
  $(function(){
    $('#buttonSendForm').click(function(){
      $.ajax({
        url: $SCRIPT_ROOT + '/add_client',
        data: $('form').serialize(),
        type: 'POST',
        async: false,
        success: function(response){
          $('input').val('');
          $('#alertSucess').removeClass("hide");
          $.getJSON( $SCRIPT_ROOT + '/echo/', function(data){
            drawTable(data.ret_data);
            console.log(data);
          });
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
    $('#buttonCloseAlert').click(function(){
      $('.alert').addClass("hide");
    });
  });
  /**
   * Funcao para enviar os itens json e ir criando os TDs e TR
   */
  function drawTable(data){
    $("#personDataTable tbody").html('');
    for(var i = 0; i < data.length; i++){
      drawRow(data[i]);
    }
  }
  /**
   * Funcao que recebe cada item do json e cria o html em base disso
   */
  function drawRow(rowData) {
    var row = $("<tr></tr>");
    $("#personDataTable tbody").append(row);
    row.append($("<td>" + rowData.title + "</td>"));
    row.append($("<td>" + rowData.description + "</td>"));
    row.append($("<td>" + rowData.server + "</td>"));
    row.append($("<td>" + rowData.extensions + "</td>"));
    row.append($("<td><a href='/edit/"+ rowData.id +"'><span class='glyphicon glyphicon-pencil' aria-hidden='true'></span></a></td>"));
  }
