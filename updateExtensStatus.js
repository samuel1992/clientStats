//Importando as bibliotecas necessarias para a conexao com o ami e mysql
var config = require('./config.json');
var mysql = require('mysql');
var manager = require('asterisk-manager');
var format = require('string-format');

//Extende o método "format" para objetos do tipo String
format.extend(String.prototype);

// Inicia o ami do asterisk
var ami = manager(config.pabx.port, config.pabx.host, config.pabx.username, config.pabx.secret, true);

// Inicia conexao com o banco de dados
var conn = mysql.createConnection({
  host: config.db.host,
  user: config.db.username,
  password: config.db.password,
  database: config.db.database
});

// Conectando ao banco
conn.connect();

// Eventos de quando a app eh carregada
ami.on('fullybooted', function(e) {
  ami.action({
    'action': 'command',
    'command': 'core show hints'
  }, function(err, res){
    updateStatus(extractJson(res));
  });
});

ami.on('extensionstatus', function(e) {
	updateStatusExten(e.exten,getStatus(e.status));
});

/**
 * Funcao para deixar o processamento parado em milisegundos determinados
 */
function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

/**
 * Através do retorno do comando "core show hints", extrai os dados para um objeto json com o ramais e status
 * dados: retorno do comando "core show hints"
 * retorno: objeto json com os ramais e sesu respsctivos status
 */
function extractJson(dados) {
	//Divide a string em uma lista, contendo os dados do ramais
	var ramais = dados.content.split('Watchers');
	var retorno = new Array();

	ramais.forEach(function(e) {
		e = e.substring(e.indexOf("=-"));

		//Extrai o Ramal
		var ramal = e.substring(e.indexOf(": "), e.indexOf("State"));
		ramal = ramal.replace(":", "").replace(" ", "").trim();

		// Extrai o Status
		var status = e.substring(e.indexOf("State:"), e.lastIndexOf(" ")).replace("State:", "").trim();

		//Criar o objeto e insere na lista de retorno
		retorno.push(new Object({ ramal: ramal, status: status }));
	}, this);

	//Remove o último item da lista, por ser inválido
	retorno.pop();

	return retorno;
}

/**
 * Atualiza no banco de dados o status dos ramais cadastrados no asterisk
 * data: dados a serem inseridos
 */
function updateStatus(data){
  // Limpa a tabela
  conn.query('TRUNCATE TABLE statusExtens', function(err, rows, fields) {});

  //Inserindo os dados na tabela
  data.forEach(function(e){
    var exten = e.ramal.split('/');
    var query = "INSERT INTO statusExtens (exten, status) VALUES ('{0}','{1}')".format(exten[1], getStatus(e.status));
    conn.query(query, function(err, rows, fields) {});
  }, this);
}

/**
 * Atualiza bo bancode dados o status de um ramal específico
 * ramal: Ramal a ser atualizado
 * status: Novo status a ser aplicado
 */
function updateStatusExten(exten, status) {
	var query = "UPDATE statusExtens SET status = '{0}' WHERE exten = '{1}'".format(status, exten);
	conn.query(query, function(err, rows, fields) {});
}

/**
 * Retorna co código do status do ramal no Asterisk
 * status: objeto do tipo String com a descrição do status
 */
 function getStatus(status) {
 	switch (status) {
 		case "Idle":
    case '0':
 			return "Livre";
 		case "In Use":
    case '1':
 			return "Em uso";
 		case "Busy":
    case '2':
 			return "Ocupado";
 		case "Unavailable":
    case '3':
 			return "Indisponível";
 		case "Ringing":
    case '4':
 			return "Chamando";
 		case "On Hold":
    case '5':
 			 return "Em espera";
 		default:
 			return "Livre";
 	}
 }
