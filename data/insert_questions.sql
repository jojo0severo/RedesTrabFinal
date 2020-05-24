
-- https://moodle.pucrs.br/pluginfile.php/2219278/mod_resource/content/4/Introducao2.pdf
INSERT INTO question (question, id_subject) VALUES ("Sobre WPAN (Wireless Personal Area Network)", 1);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Taxas de transmissao sao maiores do que as encontradas nas Lans", 1);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Podem ser redes temporarias, mas apenas quando estao conectadas por fio", 1);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nao sao redes informais de pequeno alcance que funcionam com fios, tambem chamada de rede adhoc", 1);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Sao redes informais de pequeno alcance que funcionam sem fios, tambem chamada de rede ad hoc", 1);



INSERT INTO question (question, id_subject) VALUES ("Sobre LAN (Local Area Network)", 1);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Sistema de TV a cabo", 2);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Conectam entre si ou a uma rede fixa atraves de pontos de acesso (access point)", 2);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Tradicionalmente, utilizam de mecanismos de broadcast para realizar transmissao. Porem, e menor que da WANs", 2);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Normalmente, e de uma unica organizacao. Todos os dispositivos estao acessiveis ao gerente da organizacao", 2);



INSERT INTO question (question, id_subject) VALUES ("Sobre WLAN (Wireless Local Area Network)", 1);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("pode ser visto tambem como uma evolucao da comutacao de circuitos", 3);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Exemplos de tecnologias: Frame Relay, ATM, 10 Gigabit Ethernet", 3);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Tipicamente, consiste de um conjunto de nos interconectados.", 3);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Oferecem ligacoes livres de cabos entre notebooks, computadores de mesa, impressoras, PDAs", 3);



INSERT INTO question (question, id_subject) VALUES ("WLAN (Wireless Local Area Network)", 1);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Usuario depende de empresas prestadoras de servicos de comunicacao, tendo que pagar pelos mesmos", 4);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Tipicamente, consiste de um conjunto de nos interconectados. A funcao destes nos e prover facilidades de comutacao para transportar dados de nodo a nodo ate alcancar o destino.", 4);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Versao ampliada das LANs. Normalmente, abrange um conjunto de predios ou ate mesmo uma cidade", 4);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Redes locais sem fio. Oferecem ligacoes livres de cabos entre notebooks, computadores de mesa, impressoras, PDAs", 4);




-- https://moodle.pucrs.br/pluginfile.php/2187818/mod_resource/content/3/Modelos.pdf
INSERT INTO question (question, id_subject) VALUES ("Informe o assunto que esta sendo abordado na seguinte frase: Converte um canal de transmissao fisico nao confiavel em um canal confiavel de transmissao 1", 2);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de Transporte", 5);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de Rede", 5);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel Fisico", 5);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Nivel de Enlace", 5);



INSERT INTO question (question, id_subject) VALUES ("Informe a sequencia correta sobre Modelo de Referencia OSI", 2);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nenhuma anterior", 6);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel Fisico, Nivel de Enlace, Nivel de Rede, Nivel de Transporte, Nivel de Sessao, Nivel de Apresentacao e Nivel de Aplicacao", 6);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de Enlace, Nivel de Transporte, Nivel Fisico, Nivel de Rede, Nivel de Sessao, Nivel de Apresentacao e Nivel de Aplicacao", 6);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Nivel de Aplicacao, Nivel de Apresentacao, Nivel de Sessao, Nivel de Transporte, Nivel de Rede, Nivel de Enlace, Nivel Fisico", 6);



INSERT INTO question (question, id_subject) VALUES ("Informe o nivel dito na frase a seguir: Foi necessario adaptar o modelo OSI para aplicacao no contexto de redes locais. Objetivo; conseguir que o subnivel superior, o LLC, se tornasse independente da topologia, do meio de transmissao e do metodo de acesso usados na rede local.", 2);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel Fisico", 7);
INSERT INTO wrong_alternatives (texto, id_question) VALUES (" Nivel de Transporte", 7);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de Aplicacao", 7);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Nivel de Enlace", 7);



INSERT INTO question (question, id_subject) VALUES ("Informe os topicos que mais descrevem o nivel de sessao", 2);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Interface do modelo OSI com os processos do usuario, Diversos elementos de servicos genericos e (Service Element)", 8);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Enderecamento, seqüenciamento e roteamento e Interconexao entre redes heterogeneas. ", 8);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Comunicacao fim-a-fim transparente e confiavel, Multiplexacao, Espalhamento e Segmentacao", 8);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Sintaxe, gerencia de token, controle de dialogo, pontos de sincronismo e Gerencia de atividades", 8);






-- https://moodle.pucrs.br/pluginfile.php/2187826/mod_resource/content/3/Equipamentos-interc.pdf
INSERT INTO question (question, id_subject) VALUES ("O que sao Hubs?", 3);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Pontes com multiplas portas", 9);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Subgrupo logico dentro de uma LAN, criado por software, sem precisar mover e separar fisicamente dispositivos", 9);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Interligam redes que diferem bastante entre si", 9);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Dispositivo que conecta dois ou mais equipamentos de rede.", 9);



INSERT INTO question (question, id_subject) VALUES ("O que sao Roteadores?", 3);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Projetado com um objetivo especifico: segmentar uma LAN, ou seja, um dominio de colisao, em diversos dominios de colisao independentes, e assim fornecer banda adicional à rede.", 10);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Switch conectando 3 VLANs", 10);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Criam dominios de broadcast para as portas do switch", 10);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Interligam redes que diferem bastante entre si. Usa protocolos de roteamento para aprender a melhor rota", 10);



INSERT INTO question (question, id_subject) VALUES ("Em que nivel se encontra o Repetidores", 3);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de enlace", 11);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de rede", 11);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nivel de aplicacao", 11);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Nivel fisico", 11);



INSERT INTO question (question, id_subject) VALUES ("Selecione a informacao correta sobre VLANs (Virtual LANs)", 3);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Diferente de um switch e uma bridge que somente olham o nivel MAC, um roteador pode segmentar redes baseadas nas sub-redes IP", 12);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Usa protocolos de roteamento para aprender a melhor rota", 12);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Filtragem e re-envio baseado no endereco de nivel de Rede (endereco IP)", 12);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Subgrupo logico dentro de uma LAN, criado por software, sem precisar mover e separar fisicamente dispositivos", 12);




-- https://moodle.pucrs.br/pluginfile.php/2245403/mod_resource/content/2/NAT.pdf
INSERT INTO question (question, id_subject) VALUES ("Pode-se dizer que a traducao da fase Nat compreende quantas fases?", 4);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("7", 13);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("12", 13);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("4", 13);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("3", 13);



INSERT INTO question (question, id_subject) VALUES ("Caracteristicas comuns do NAT", 4);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nenhuma das anteriores", 14);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nao economiza enderecos IP e controle e baseado nas conexoes", 14);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Roteamento transparente e quase totalmente transparente", 14);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Alocacao transparente de enderecos e Roteamento transparente", 14);



INSERT INTO question (question, id_subject) VALUES ("Informe o que confere com as informacoes sobre IP Masquerading ou NAPT", 4);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Traduz enderecos do cabecalho IP para que contenha enderecos roteaveis do proprio NAT-router", 15);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Especificado na RFC 1631 e varios drafts", 15);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Oculta o layout da rede interna.", 15);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Nela, muitos enderecos IP sao representados por 1 unico endereco publico", 15);



INSERT INTO question (question, id_subject) VALUES ("Afirme com ajuda das sugestoes dadas para definir NAT Estatico", 4);

INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Nenhuma resposta esta certa", 16);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Oferece o maior nivel de seguranca entre todas as tecnicas.", 16);
INSERT INTO wrong_alternatives (texto, id_question) VALUES ("Controle e baseado nas conexoes, tambem conhecida como NAPT, e a traducao m:1 e oferece o maior nivel de seguranca entre todas as tecnicas", 16);
INSERT INTO correct_alternatives (texto, id_question) VALUES ("Quase totalmente transparente, nao economiza enderecos IP e hosts com endereco na tabela sao traduzidos, os demais sao descartados", 16);

