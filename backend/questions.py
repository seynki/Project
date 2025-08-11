import random

# Questions database for the historical tic-tac-toe game
HISTORY_QUESTIONS = [
    {
        "id": 1,
        "question": "Em que ano o Brasil foi descoberto pelos portugueses?",
        "options": ["1498", "1500", "1502", "1505"],
        "correctAnswer": "1500",
        "period": "Descobrimento do Brasil",
        "subject": "historia"
    },
    {
        "id": 2,
        "question": "Quem foi o primeiro governador-geral do Brasil?",
        "options": ["Tomé de Sousa", "Duarte da Costa", "Mem de Sá", "Pedro Álvares Cabral"],
        "correctAnswer": "Tomé de Sousa",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 3,
        "question": "Em que ano foi abolida a escravidão no Brasil?",
        "options": ["1885", "1888", "1889", "1890"],
        "correctAnswer": "1888",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 4,
        "question": "Quem foi o último imperador do Brasil?",
        "options": ["Dom Pedro I", "Dom Pedro II", "Dom João VI", "Princesa Isabel"],
        "correctAnswer": "Dom Pedro II",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 5,
        "question": "Em que ano foi proclamada a República no Brasil?",
        "options": ["1888", "1889", "1890", "1891"],
        "correctAnswer": "1889",
        "period": "Proclamação da República",
        "subject": "historia"
    },
    {
        "id": 6,
        "question": "Qual foi a primeira capital do Brasil?",
        "options": ["Rio de Janeiro", "Salvador", "São Vicente", "Olinda"],
        "correctAnswer": "Salvador",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 7,
        "question": "Quem foi o navegador português que chegou ao Brasil em 1500?",
        "options": ["Vasco da Gama", "Pedro Álvares Cabral", "Bartolomeu Dias", "Fernando de Magalhães"],
        "correctAnswer": "Pedro Álvares Cabral",
        "period": "Descobrimento do Brasil",
        "subject": "historia"
    },
    {
        "id": 8,
        "question": "Em que ano foi assinada a Lei Áurea?",
        "options": ["13 de maio de 1887", "13 de maio de 1888", "15 de novembro de 1889", "13 de maio de 1890"],
        "correctAnswer": "13 de maio de 1888",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 9,
        "question": "Quem foi o proclamador da República no Brasil?",
        "options": ["Deodoro da Fonseca", "Floriano Peixoto", "Benjamin Constant", "Rui Barbosa"],
        "correctAnswer": "Deodoro da Fonseca",
        "period": "Proclamação da República",
        "subject": "historia"
    },
    {
        "id": 10,
        "question": "Qual era o nome da primeira carta escrita sobre o Brasil?",
        "options": ["Carta de Pero Vaz de Caminha", "Carta de Tomé de Sousa", "Carta do Descobrimento", "Carta Real"],
        "correctAnswer": "Carta de Pero Vaz de Caminha",
        "period": "Descobrimento do Brasil",
        "subject": "historia"
    },
    {
        "id": 11,
        "question": "Qual foi o primeiro presidente do Brasil?",
        "options": ["Getúlio Vargas", "Deodoro da Fonseca", "Floriano Peixoto", "Prudente de Morais"],
        "correctAnswer": "Deodoro da Fonseca",
        "period": "Primeira República",
        "subject": "historia"
    },
    {
        "id": 12,
        "question": "Em que século ocorreu a corrida do ouro em Minas Gerais?",
        "options": ["Século XVI", "Século XVII", "Século XVIII", "Século XIX"],
        "correctAnswer": "Século XVIII",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 13,
        "question": "Qual foi o nome do movimento de independência ocorrido em Minas Gerais em 1789?",
        "options": ["Conjuração Mineira", "Conjuração Baiana", "Revolução Farroupilha", "Cabanagem"],
        "correctAnswer": "Conjuração Mineira",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 14,
        "question": "Quem foi o líder da Conjuração Mineira?",
        "options": ["Tiradentes", "Tomás Antônio Gonzaga", "Cláudio Manuel da Costa", "Alvarenga Peixoto"],
        "correctAnswer": "Tiradentes",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 15,
        "question": "Em que ano Dom Pedro I declarou a independência do Brasil?",
        "options": ["1821", "1822", "1823", "1824"],
        "correctAnswer": "1822",
        "period": "Independência do Brasil",
        "subject": "historia"
    },
    {
        "id": 16,
        "question": "Onde foi proclamada a independência do Brasil?",
        "options": ["Rio de Janeiro", "às margens do rio Ipiranga", "Salvador", "São Paulo"],
        "correctAnswer": "às margens do rio Ipiranga",
        "period": "Independência do Brasil",
        "subject": "historia"
    },
    {
        "id": 17,
        "question": "Qual foi o nome do período em que Dom Pedro II governou o Brasil?",
        "options": ["Primeiro Reinado", "Segundo Reinado", "Período Regencial", "República Velha"],
        "correctAnswer": "Segundo Reinado",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 18,
        "question": "Qual foi a principal atividade econômica no Brasil durante o período colonial?",
        "options": ["Mineração", "Agricultura (cana-de-açúcar)", "Pecuária", "Comércio"],
        "correctAnswer": "Agricultura (cana-de-açúcar)",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 19,
        "question": "Quem foi a princesa que assinou a Lei Áurea?",
        "options": ["Princesa Isabel", "Princesa Leopoldina", "Princesa Januária", "Princesa Francisca"],
        "correctAnswer": "Princesa Isabel",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 20,
        "question": "Em que ano foi criado o Distrito Federal (Brasília)?",
        "options": ["1956", "1957", "1960", "1961"],
        "correctAnswer": "1960",
        "period": "Brasil República",
        "subject": "historia"
    },
    # Novas questões de História do Brasil
    {
        "id": 21,
        "question": "Qual foi o tratado que definiu os limites entre Brasil e Portugal com a Espanha?",
        "options": ["Tratado de Madrid", "Tratado de Tordesilhas", "Tratado de Santo Ildefonso", "Tratado de Badajós"],
        "correctAnswer": "Tratado de Madrid",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 22,
        "question": "Qual foi a primeira universidade criada no Brasil?",
        "options": ["USP", "UFRJ", "Universidade do Brasil", "Universidade de São Paulo"],
        "correctAnswer": "UFRJ",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 23,
        "question": "Em que ano começou a Era Vargas?",
        "options": ["1928", "1930", "1932", "1934"],
        "correctAnswer": "1930",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 24,
        "question": "Qual foi o nome da constituição promulgada durante o governo de Getúlio Vargas em 1937?",
        "options": ["Constituição Polaca", "Constituição Cidadã", "Constituição do Estado Novo", "Constituição Democrática"],
        "correctAnswer": "Constituição Polaca",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 25,
        "question": "Quem foi o líder da Revolta da Chibata?",
        "options": ["João Cândido", "Antônio Conselheiro", "Lampião", "Prestes"],
        "correctAnswer": "João Cândido",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 26,
        "question": "Em que ano ocorreu a Semana de Arte Moderna?",
        "options": ["1920", "1922", "1924", "1926"],
        "correctAnswer": "1922",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 27,
        "question": "Qual foi o nome da campanha militar liderada por Luís Carlos Prestes?",
        "options": ["Coluna Prestes", "Marcha dos 300", "Expedição Rondon", "Campanha do Acre"],
        "correctAnswer": "Coluna Prestes",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 28,
        "question": "Em que cidade foi fundada a primeira vila do Brasil?",
        "options": ["Salvador", "São Vicente", "Porto Seguro", "Olinda"],
        "correctAnswer": "São Vicente",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 29,
        "question": "Qual era o nome do sistema de administração colonial dividindo o Brasil em lotes?",
        "options": ["Capitanias Hereditárias", "Sesmarias", "Governos Gerais", "Vilas"],
        "correctAnswer": "Capitanias Hereditárias",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 30,
        "question": "Quem foi o bandeirante que descobriu ouro em Minas Gerais?",
        "options": ["Fernão Dias", "Antônio Raposo Tavares", "Borba Gato", "Domingos Jorge Velho"],
        "correctAnswer": "Borba Gato",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 31,
        "question": "Qual foi a revolta que ocorreu na Bahia em 1798?",
        "options": ["Conjuração Baiana", "Sabinada", "Balaiada", "Cabanagem"],
        "correctAnswer": "Conjuração Baiana",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 32,
        "question": "Em que ano a família real portuguesa chegou ao Brasil?",
        "options": ["1806", "1807", "1808", "1809"],
        "correctAnswer": "1808",
        "period": "Período Joanino",
        "subject": "historia"
    },
    {
        "id": 33,
        "question": "Qual foi a primeira medida econômica tomada por Dom João VI no Brasil?",
        "options": ["Abertura dos Portos", "Criação do Banco do Brasil", "Criação da Imprensa Régia", "Fundação da Biblioteca Nacional"],
        "correctAnswer": "Abertura dos Portos",
        "period": "Período Joanino",
        "subject": "historia"
    },
    {
        "id": 34,
        "question": "Qual foi a guerra em que o Brasil lutou contra o Paraguai?",
        "options": ["Guerra da Cisplatina", "Guerra do Paraguai", "Guerra dos Farrapos", "Guerra de Canudos"],
        "correctAnswer": "Guerra do Paraguai",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 35,
        "question": "Em que período ocorreu a Guerra do Paraguai?",
        "options": ["1864-1870", "1860-1866", "1865-1871", "1862-1868"],
        "correctAnswer": "1864-1870",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 36,
        "question": "Qual foi o nome da lei que proibiu o tráfico negreiro no Brasil?",
        "options": ["Lei Áurea", "Lei do Ventre Livre", "Lei Eusébio de Queirós", "Lei dos Sexagenários"],
        "correctAnswer": "Lei Eusébio de Queirós",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 37,
        "question": "Em que ano foi promulgada a Lei do Ventre Livre?",
        "options": ["1869", "1871", "1873", "1875"],
        "correctAnswer": "1871",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 38,
        "question": "Quem foi o líder da Revolta dos Malês?",
        "options": ["Luís Sanim", "Manuel Calafate", "Pacífico Licutan", "Todos os anteriores"],
        "correctAnswer": "Todos os anteriores",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 39,
        "question": "Em que ano ocorreu a Revolução Farroupilha?",
        "options": ["1835-1845", "1830-1840", "1832-1842", "1838-1848"],
        "correctAnswer": "1835-1845",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 40,
        "question": "Qual foi o nome da república proclamada durante a Revolução Farroupilha?",
        "options": ["República Rio-Grandense", "República Juliana", "República Farroupilha", "República Gaúcha"],
        "correctAnswer": "República Rio-Grandense",
        "period": "Brasil Imperial",
        "subject": "historia"
    },
    {
        "id": 41,
        "question": "Quem foi o presidente que fundou Brasília?",
        "options": ["Getúlio Vargas", "Juscelino Kubitschek", "Jânio Quadros", "João Goulart"],
        "correctAnswer": "Juscelino Kubitschek",
        "period": "Brasil Contemporâneo",
        "subject": "historia"
    },
    {
        "id": 42,
        "question": "Em que ano começou a Ditadura Militar no Brasil?",
        "options": ["1964", "1965", "1966", "1968"],
        "correctAnswer": "1964",
        "period": "Ditadura Militar",
        "subject": "historia"
    },
    {
        "id": 43,
        "question": "Qual foi o primeiro presidente militar do Brasil?",
        "options": ["Castelo Branco", "Costa e Silva", "Médici", "Geisel"],
        "correctAnswer": "Castelo Branco",
        "period": "Ditadura Militar",
        "subject": "historia"
    },
    {
        "id": 44,
        "question": "Em que ano foi promulgada a atual Constituição brasileira?",
        "options": ["1986", "1987", "1988", "1989"],
        "correctAnswer": "1988",
        "period": "Nova República",
        "subject": "historia"
    },
    {
        "id": 45,
        "question": "Quem foi o primeiro presidente civil após a ditadura militar?",
        "options": ["Tancredo Neves", "José Sarney", "Fernando Collor", "Itamar Franco"],
        "correctAnswer": "José Sarney",
        "period": "Nova República",
        "subject": "historia"
    },
    {
        "id": 46,
        "question": "Qual foi o plano econômico que conseguiu controlar a hiperinflação no Brasil?",
        "options": ["Plano Cruzado", "Plano Bresser", "Plano Collor", "Plano Real"],
        "correctAnswer": "Plano Real",
        "period": "Brasil Contemporâneo",
        "subject": "historia"
    },
    {
        "id": 47,
        "question": "Em que ano o Brasil sediou a Copa do Mundo de Futebol pela primeira vez?",
        "options": ["1948", "1950", "1952", "1954"],
        "correctAnswer": "1950",
        "period": "Brasil Contemporâneo",
        "subject": "historia"
    },
    {
        "id": 48,
        "question": "Qual foi a capital do Brasil durante o período colonial?",
        "options": ["Rio de Janeiro", "Salvador", "São Vicente", "Recife"],
        "correctAnswer": "Salvador",
        "period": "Brasil Colonial",
        "subject": "historia"
    },
    {
        "id": 49,
        "question": "Quem foi o arquiteto responsável pelo projeto de Brasília?",
        "options": ["Oscar Niemeyer", "Lúcio Costa", "Roberto Burle Marx", "Vilanova Artigas"],
        "correctAnswer": "Lúcio Costa",
        "period": "Brasil Contemporâneo",
        "subject": "historia"
    },
    {
        "id": 50,
        "question": "Qual foi o nome da operação militar que depôs João Goulart?",
        "options": ["Operação Brother Sam", "Operação Limpeza", "Operação Popeye", "Operação Condor"],
        "correctAnswer": "Operação Brother Sam",
        "period": "Ditadura Militar",
        "subject": "historia"
    },
    {
        "id": 51,
        "question": "Em que ano foi criada a Petrobras?",
        "options": ["1951", "1953", "1955", "1957"],
        "correctAnswer": "1953",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 52,
        "question": "Qual foi o nome da campanha que levou Getúlio Vargas ao poder em 1930?",
        "options": ["Revolução de 1930", "Aliança Liberal", "Movimento Tenentista", "Marcha para o Oeste"],
        "correctAnswer": "Revolução de 1930",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 53,
        "question": "Quem foi o último presidente da República Velha?",
        "options": ["Washington Luís", "Artur Bernardes", "Epitácio Pessoa", "Rodrigues Alves"],
        "correctAnswer": "Washington Luís",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 54,
        "question": "Qual foi o nome do regime político instaurado por Getúlio Vargas em 1937?",
        "options": ["Estado Novo", "Nova República", "Segunda República", "Era de Ouro"],
        "correctAnswer": "Estado Novo",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 55,
        "question": "Em que ano terminou a Primeira Guerra Mundial, impactando a economia brasileira?",
        "options": ["1917", "1918", "1919", "1920"],
        "correctAnswer": "1918",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 56,
        "question": "Qual foi a principal consequência da Crise de 1929 para o Brasil?",
        "options": ["Queda do preço do café", "Aumento das exportações", "Crescimento industrial", "Estabilidade política"],
        "correctAnswer": "Queda do preço do café",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 57,
        "question": "Quem foi o presidente que criou a CLT (Consolidação das Leis do Trabalho)?",
        "options": ["Getúlio Vargas", "Juscelino Kubitschek", "Eurico Dutra", "João Goulart"],
        "correctAnswer": "Getúlio Vargas",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 58,
        "question": "Em que ano foi criada a CLT?",
        "options": ["1941", "1943", "1945", "1947"],
        "correctAnswer": "1943",
        "period": "Era Vargas",
        "subject": "historia"
    },
    {
        "id": 59,
        "question": "Qual foi o nome da expedição que explorou o interior do Brasil no século XX?",
        "options": ["Expedição Rondon", "Expedição Langsdorff", "Expedição Nimuendaju", "Expedição Fawcett"],
        "correctAnswer": "Expedição Rondon",
        "period": "República Velha",
        "subject": "historia"
    },
    {
        "id": 60,
        "question": "Quem foi o general que liderou a Expedição Rondon?",
        "options": ["Cândido Rondon", "Euclides da Cunha", "Couto Magalhães", "Alberto Santos-Dumont"],
        "correctAnswer": "Cândido Rondon",
        "period": "República Velha",
        "subject": "historia"
    }
]

CHEMISTRY_QUESTIONS = [
    {
        "id": 101,
        "question": "Qual é o símbolo químico do ouro?",
        "options": ["Au", "Ag", "Go", "Or"],
        "correctAnswer": "Au",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 102,
        "question": "Quantos prótons tem o átomo de carbono?",
        "options": ["4", "6", "8", "12"],
        "correctAnswer": "6",
        "period": "Estrutura Atômica",
        "subject": "quimica"
    },
    {
        "id": 103,
        "question": "Qual é a fórmula química da água?",
        "options": ["H2O", "HO2", "H3O", "H2O2"],
        "correctAnswer": "H2O",
        "period": "Química Inorgânica",
        "subject": "quimica"
    },
    {
        "id": 104,
        "question": "Qual é o gás mais abundante na atmosfera terrestre?",
        "options": ["Oxigênio", "Nitrogênio", "Dióxido de carbono", "Argônio"],
        "correctAnswer": "Nitrogênio",
        "period": "Química Atmosférica",
        "subject": "quimica"
    },
    {
        "id": 105,
        "question": "Qual é o número atômico do hidrogênio?",
        "options": ["1", "2", "3", "4"],
        "correctAnswer": "1",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 106,
        "question": "Como se chama a ligação entre átomos que compartilham elétrons?",
        "options": ["Ligação iônica", "Ligação covalente", "Ligação metálica", "Ligação de hidrogênio"],
        "correctAnswer": "Ligação covalente",
        "period": "Ligações Químicas",
        "subject": "quimica"
    },
    {
        "id": 107,
        "question": "Qual é a fórmula do ácido sulfúrico?",
        "options": ["H2SO3", "H2SO4", "HSO4", "H3SO4"],
        "correctAnswer": "H2SO4",
        "period": "Química Inorgânica",
        "subject": "quimica"
    },
    {
        "id": 108,
        "question": "Qual é o elemento químico mais leve?",
        "options": ["Hélio", "Hidrogênio", "Lítio", "Berílio"],
        "correctAnswer": "Hidrogênio",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 109,
        "question": "Qual é o pH de uma solução neutra?",
        "options": ["0", "7", "14", "1"],
        "correctAnswer": "7",
        "period": "Ácidos e Bases",
        "subject": "quimica"
    },
    {
        "id": 110,
        "question": "Qual gás é liberado na reação entre ácido e metal?",
        "options": ["Oxigênio", "Nitrogênio", "Hidrogênio", "Dióxido de carbono"],
        "correctAnswer": "Hidrogênio",
        "period": "Reações Químicas",
        "subject": "quimica"
    },
    {
        "id": 111,
        "question": "Qual é a fórmula do metano?",
        "options": ["CH4", "C2H4", "C2H6", "CH3"],
        "correctAnswer": "CH4",
        "period": "Química Orgânica",
        "subject": "quimica"
    },
    {
        "id": 112,
        "question": "Quantos elétrons cabem na primeira camada eletrônica?",
        "options": ["2", "8", "18", "32"],
        "correctAnswer": "2",
        "period": "Estrutura Atômica",
        "subject": "quimica"
    },
    {
        "id": 113,
        "question": "Qual é o símbolo químico do ferro?",
        "options": ["Fr", "Fe", "Fo", "Ir"],
        "correctAnswer": "Fe",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 114,
        "question": "Qual é a fórmula do sal de cozinha?",
        "options": ["NaCl", "KCl", "CaCl2", "MgCl2"],
        "correctAnswer": "NaCl",
        "period": "Química Inorgânica",
        "subject": "quimica"
    },
    {
        "id": 115,
        "question": "Qual é o processo de transformação de sólido diretamente em gás?",
        "options": ["Fusão", "Vaporização", "Sublimação", "Condensação"],
        "correctAnswer": "Sublimação",
        "period": "Estados da Matéria",
        "subject": "quimica"
    },
    {
        "id": 116,
        "question": "Qual é a temperatura de ebulição da água ao nível do mar?",
        "options": ["90°C", "100°C", "110°C", "120°C"],
        "correctAnswer": "100°C",
        "period": "Estados da Matéria",
        "subject": "quimica"
    },
    {
        "id": 117,
        "question": "Qual elemento é essencial para a respiração?",
        "options": ["Nitrogênio", "Carbono", "Oxigênio", "Hidrogênio"],
        "correctAnswer": "Oxigênio",
        "period": "Química e Vida",
        "subject": "quimica"
    },
    {
        "id": 118,
        "question": "Qual é a fórmula do dióxido de carbono?",
        "options": ["CO", "CO2", "C2O", "CO3"],
        "correctAnswer": "CO2",
        "period": "Química Inorgânica",
        "subject": "quimica"
    },
    {
        "id": 119,
        "question": "Qual é o elemento mais abundante no universo?",
        "options": ["Oxigênio", "Carbono", "Hidrogênio", "Hélio"],
        "correctAnswer": "Hidrogênio",
        "period": "Química Cósmica",
        "subject": "quimica"
    },
    {
        "id": 120,
        "question": "Qual é a unidade básica da quantidade de matéria?",
        "options": ["Grama", "Mol", "Litro", "Átomo"],
        "correctAnswer": "Mol",
        "period": "Estequiometria",
        "subject": "quimica"
    },
    {
        "id": 121,
        "question": "Qual é o símbolo químico da prata?",
        "options": ["Pr", "Ag", "Si", "Pt"],
        "correctAnswer": "Ag",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 122,
        "question": "Quantas ligações covalentes o carbono pode fazer?",
        "options": ["2", "3", "4", "5"],
        "correctAnswer": "4",
        "period": "Ligações Químicas",
        "subject": "quimica"
    },
    {
        "id": 123,
        "question": "Qual é a fórmula do hidróxido de sódio?",
        "options": ["NaOH", "Na2OH", "NaO", "Na(OH)2"],
        "correctAnswer": "NaOH",
        "period": "Bases",
        "subject": "quimica"
    },
    {
        "id": 124,
        "question": "Qual é o gás produzido na fotossíntese?",
        "options": ["Dióxido de carbono", "Nitrogênio", "Oxigênio", "Metano"],
        "correctAnswer": "Oxigênio",
        "period": "Bioquímica",
        "subject": "quimica"
    },
    {
        "id": 125,
        "question": "Qual é o elemento químico com símbolo Ca?",
        "options": ["Carbono", "Cálcio", "Césio", "Califórnio"],
        "correctAnswer": "Cálcio",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 126,
        "question": "Qual é a fórmula do ácido clorídrico?",
        "options": ["HCl", "HClO", "HClO2", "HClO3"],
        "correctAnswer": "HCl",
        "period": "Ácidos",
        "subject": "quimica"
    },
    {
        "id": 127,
        "question": "Qual é o processo de separação de misturas usando diferença de pontos de ebulição?",
        "options": ["Filtração", "Destilação", "Decantação", "Centrifugação"],
        "correctAnswer": "Destilação",
        "period": "Separação de Misturas",
        "subject": "quimica"
    },
    {
        "id": 128,
        "question": "Qual é o número de Avogadro?",
        "options": ["6,02 × 10²³", "6,02 × 10²²", "6,02 × 10²⁴", "6,02 × 10²¹"],
        "correctAnswer": "6,02 × 10²³",
        "period": "Estequiometria",
        "subject": "quimica"
    },
    {
        "id": 129,
        "question": "Qual é o símbolo químico do potássio?",
        "options": ["P", "K", "Po", "Pt"],
        "correctAnswer": "K",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 130,
        "question": "Qual tipo de reação ocorre quando um ácido reage com uma base?",
        "options": ["Síntese", "Decomposição", "Neutralização", "Combustão"],
        "correctAnswer": "Neutralização",
        "period": "Reações Químicas",
        "subject": "quimica"
    },
    {
        "id": 131,
        "question": "Qual é a fórmula do etanol?",
        "options": ["C2H5OH", "C2H4OH", "C3H7OH", "CH3OH"],
        "correctAnswer": "C2H5OH",
        "period": "Química Orgânica",
        "subject": "quimica"
    },
    {
        "id": 132,
        "question": "Qual é o elemento com maior eletronegatividade?",
        "options": ["Oxigênio", "Nitrogênio", "Flúor", "Cloro"],
        "correctAnswer": "Flúor",
        "period": "Propriedades Periódicas",
        "subject": "quimica"
    },
    {
        "id": 133,
        "question": "Qual é a fórmula da amônia?",
        "options": ["NH3", "NH4", "N2H4", "NH2"],
        "correctAnswer": "NH3",
        "period": "Química Inorgânica",
        "subject": "quimica"
    },
    {
        "id": 134,
        "question": "Qual é o principal componente do ar atmosférico?",
        "options": ["Oxigênio (21%)", "Nitrogênio (78%)", "Dióxido de carbono", "Vapor d'água"],
        "correctAnswer": "Nitrogênio (78%)",
        "period": "Química Atmosférica",
        "subject": "quimica"
    },
    {
        "id": 135,
        "question": "Qual é o símbolo químico do mercúrio?",
        "options": ["Me", "Hg", "Mc", "Mr"],
        "correctAnswer": "Hg",
        "period": "Tabela Periódica",
        "subject": "quimica"
    },
    {
        "id": 136,
        "question": "Qual é o tipo de ligação predominante nos metais?",
        "options": ["Ligação iônica", "Ligação covalente", "Ligação metálica", "Ligação de hidrogênio"],
        "correctAnswer": "Ligação metálica",
        "period": "Ligações Químicas",
        "subject": "quimica"
    },
    {
        "id": 137,
        "question": "Qual é a fórmula do peróxido de hidrogênio?",
        "options": ["H2O", "H2O2", "HO2", "H3O2"],
        "correctAnswer": "H2O2",
        "period": "Química Inorgânica",
        "subject": "quimica"
    },
    {
        "id": 138,
        "question": "Qual é o elemento químico presente em todas as substâncias orgânicas?",
        "options": ["Hidrogênio", "Oxigênio", "Carbono", "Nitrogênio"],
        "correctAnswer": "Carbono",
        "period": "Química Orgânica",
        "subject": "quimica"
    },
    {
        "id": 139,
        "question": "Qual é a propriedade que mede a tendência de um átomo atrair elétrons?",
        "options": ["Raio atômico", "Energia de ionização", "Eletronegatividade", "Afinidade eletrônica"],
        "correctAnswer": "Eletronegatividade",
        "period": "Propriedades Periódicas",
        "subject": "quimica"
    },
    {
        "id": 140,
        "question": "Qual é o produto da reação entre um metal e um ácido?",
        "options": ["Sal + água", "Sal + gás hidrogênio", "Óxido + água", "Base + gás"],
        "correctAnswer": "Sal + gás hidrogênio",
        "period": "Reações Químicas",
        "subject": "quimica"
    }
]

# Mathematics Questions
MATH_QUESTIONS = [
    {
        "id": 201,
        "question": "Quanto é 15 + 27?",
        "options": ["40", "41", "42", "43"],
        "correctAnswer": "42",
        "period": "Aritmética",
        "subject": "matematica"
    },
    {
        "id": 202,
        "question": "Qual é o resultado de 8 × 9?",
        "options": ["71", "72", "73", "74"],
        "correctAnswer": "72",
        "period": "Aritmética",
        "subject": "matematica"
    },
    {
        "id": 203,
        "question": "Quanto é 144 ÷ 12?",
        "options": ["11", "12", "13", "14"],
        "correctAnswer": "12",
        "period": "Aritmética",
        "subject": "matematica"
    },
    {
        "id": 204,
        "question": "Qual é a raiz quadrada de 64?",
        "options": ["6", "7", "8", "9"],
        "correctAnswer": "8",
        "period": "Radiciação",
        "subject": "matematica"
    },
    {
        "id": 205,
        "question": "Quanto é 5²?",
        "options": ["20", "25", "30", "35"],
        "correctAnswer": "25",
        "period": "Potenciação",
        "subject": "matematica"
    },
    {
        "id": 206,
        "question": "Se x + 12 = 20, qual é o valor de x?",
        "options": ["6", "7", "8", "9"],
        "correctAnswer": "8",
        "period": "Álgebra",
        "subject": "matematica"
    },
    {
        "id": 207,
        "question": "Qual é o perímetro de um quadrado com lado de 5 cm?",
        "options": ["15 cm", "20 cm", "25 cm", "30 cm"],
        "correctAnswer": "20 cm",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 208,
        "question": "Qual é a área de um retângulo de 6 cm × 4 cm?",
        "options": ["20 cm²", "22 cm²", "24 cm²", "26 cm²"],
        "correctAnswer": "24 cm²",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 209,
        "question": "Quantos graus tem um ângulo reto?",
        "options": ["45°", "60°", "90°", "180°"],
        "correctAnswer": "90°",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 210,
        "question": "Qual é 20% de 150?",
        "options": ["25", "30", "35", "40"],
        "correctAnswer": "30",
        "period": "Porcentagem",
        "subject": "matematica"
    },
    {
        "id": 211,
        "question": "Se 3x = 21, qual é o valor de x?",
        "options": ["6", "7", "8", "9"],
        "correctAnswer": "7",
        "period": "Álgebra",
        "subject": "matematica"
    },
    {
        "id": 212,
        "question": "Qual é o resultado de (-5) + 8?",
        "options": ["2", "3", "4", "13"],
        "correctAnswer": "3",
        "period": "Números Inteiros",
        "subject": "matematica"
    },
    {
        "id": 213,
        "question": "Quantos lados tem um hexágono?",
        "options": ["5", "6", "7", "8"],
        "correctAnswer": "6",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 214,
        "question": "Qual é o valor de π (pi) aproximadamente?",
        "options": ["3,14", "3,41", "4,13", "4,31"],
        "correctAnswer": "3,14",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 215,
        "question": "Se um produto custa R$ 80 e tem 25% de desconto, qual é o preço final?",
        "options": ["R$ 55", "R$ 60", "R$ 65", "R$ 70"],
        "correctAnswer": "R$ 60",
        "period": "Porcentagem",
        "subject": "matematica"
    },
    {
        "id": 216,
        "question": "Qual é a soma dos ângulos internos de um triângulo?",
        "options": ["90°", "180°", "270°", "360°"],
        "correctAnswer": "180°",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 217,
        "question": "Quanto é 2³?",
        "options": ["6", "8", "9", "16"],
        "correctAnswer": "8",
        "period": "Potenciação",
        "subject": "matematica"
    },
    {
        "id": 218,
        "question": "Se uma pizza é dividida em 8 fatias e você comeu 3, que fração da pizza você comeu?",
        "options": ["3/5", "3/8", "5/8", "8/3"],
        "correctAnswer": "3/8",
        "period": "Frações",
        "subject": "matematica"
    },
    {
        "id": 219,
        "question": "Qual é o resultado de 7 × (-4)?",
        "options": ["-28", "-24", "24", "28"],
        "correctAnswer": "-28",
        "period": "Números Inteiros",
        "subject": "matematica"
    },
    {
        "id": 220,
        "question": "Quantos minutos há em 2 horas e 30 minutos?",
        "options": ["120", "130", "140", "150"],
        "correctAnswer": "150",
        "period": "Medidas de Tempo",
        "subject": "matematica"
    },
    {
        "id": 221,
        "question": "Qual é a média aritmética de 10, 15 e 20?",
        "options": ["15", "16", "17", "18"],
        "correctAnswer": "15",
        "period": "Estatística",
        "subject": "matematica"
    },
    {
        "id": 222,
        "question": "Se 2x - 5 = 11, qual é o valor de x?",
        "options": ["6", "7", "8", "9"],
        "correctAnswer": "8",
        "period": "Álgebra",
        "subject": "matematica"
    },
    {
        "id": 223,
        "question": "Qual é a área de um círculo com raio de 3 cm? (Use π = 3,14)",
        "options": ["28,26 cm²", "28,27 cm²", "28,28 cm²", "28,29 cm²"],
        "correctAnswer": "28,26 cm²",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 224,
        "question": "Quantos graus tem um ângulo de meia volta?",
        "options": ["90°", "180°", "270°", "360°"],
        "correctAnswer": "180°",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 225,
        "question": "Qual é o resultado de 15% + 25%?",
        "options": ["35%", "40%", "45%", "50%"],
        "correctAnswer": "40%",
        "period": "Porcentagem",
        "subject": "matematica"
    },
    {
        "id": 226,
        "question": "Se um triângulo tem lados de 3, 4 e 5 cm, qual é seu perímetro?",
        "options": ["10 cm", "11 cm", "12 cm", "13 cm"],
        "correctAnswer": "12 cm",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 227,
        "question": "Qual é a raiz cúbica de 27?",
        "options": ["2", "3", "4", "9"],
        "correctAnswer": "3",
        "period": "Radiciação",
        "subject": "matematica"
    },
    {
        "id": 228,
        "question": "Se você tem 24 balas para dividir igualmente entre 6 crianças, quantas balas cada uma recebe?",
        "options": ["3", "4", "5", "6"],
        "correctAnswer": "4",
        "period": "Divisão",
        "subject": "matematica"
    },
    {
        "id": 229,
        "question": "Qual é o valor de |−15|? (módulo de -15)",
        "options": ["-15", "0", "15", "30"],
        "correctAnswer": "15",
        "period": "Números Inteiros",
        "subject": "matematica"
    },
    {
        "id": 230,
        "question": "Se uma corrida tem 42,195 km, quantos metros são?",
        "options": ["4219,5 m", "42195 m", "421950 m", "4219500 m"],
        "correctAnswer": "42195 m",
        "period": "Sistema Métrico",
        "subject": "matematica"
    },
    {
        "id": 231,
        "question": "Qual é o máximo divisor comum (MDC) de 12 e 18?",
        "options": ["2", "3", "6", "9"],
        "correctAnswer": "6",
        "period": "Divisibilidade",
        "subject": "matematica"
    },
    {
        "id": 232,
        "question": "Se x² = 49, quais são os possíveis valores de x?",
        "options": ["7", "-7", "7 e -7", "49"],
        "correctAnswer": "7 e -7",
        "period": "Equações",
        "subject": "matematica"
    },
    {
        "id": 233,
        "question": "Quantos centímetros há em 2,5 metros?",
        "options": ["25 cm", "250 cm", "2500 cm", "25000 cm"],
        "correctAnswer": "250 cm",
        "period": "Sistema Métrico",
        "subject": "matematica"
    },
    {
        "id": 234,
        "question": "Qual é o resultado de 3/4 + 1/4?",
        "options": ["4/8", "4/4", "1", "2"],
        "correctAnswer": "1",
        "period": "Frações",
        "subject": "matematica"
    },
    {
        "id": 235,
        "question": "Se um número é divisível por 2 e por 3, também é divisível por qual número?",
        "options": ["5", "6", "8", "9"],
        "correctAnswer": "6",
        "period": "Divisibilidade",
        "subject": "matematica"
    },
    {
        "id": 236,
        "question": "Qual é o resultado de 10²?",
        "options": ["20", "100", "200", "1000"],
        "correctAnswer": "100",
        "period": "Potenciação",
        "subject": "matematica"
    },
    {
        "id": 237,
        "question": "Se um relógio marca 15:30, que horas são no formato 12 horas?",
        "options": ["3:30 AM", "3:30 PM", "15:30 AM", "15:30 PM"],
        "correctAnswer": "3:30 PM",
        "period": "Medidas de Tempo",
        "subject": "matematica"
    },
    {
        "id": 238,
        "question": "Qual é o menor múltiplo comum (MMC) de 4 e 6?",
        "options": ["10", "12", "18", "24"],
        "correctAnswer": "12",
        "period": "Divisibilidade",
        "subject": "matematica"
    },
    {
        "id": 239,
        "question": "Se você tem um ângulo de 45° e adiciona 30°, qual é o ângulo resultante?",
        "options": ["65°", "70°", "75°", "80°"],
        "correctAnswer": "75°",
        "period": "Geometria",
        "subject": "matematica"
    },
    {
        "id": 240,
        "question": "Qual é o valor de 0,5 em fração?",
        "options": ["1/2", "1/3", "2/3", "5/10"],
        "correctAnswer": "1/2",
        "period": "Frações e Decimais",
        "subject": "matematica"
    }
]

# Combine all questions
QUESTIONS = HISTORY_QUESTIONS + CHEMISTRY_QUESTIONS + MATH_QUESTIONS

used_questions = {}

def get_random_question(subject=None):
    """Get a random question, avoiding recently used ones when possible"""
    global used_questions
    
    # Initialize used_questions for subject if not exists
    if subject not in used_questions:
        used_questions[subject] = set()
    
    # Filter questions by subject if specified
    if subject:
        available_pool = [q for q in QUESTIONS if q.get("subject") == subject]
    else:
        available_pool = QUESTIONS
    
    # If we've used all questions for this subject, reset the used set
    if len(used_questions[subject]) >= len(available_pool):
        used_questions[subject].clear()
    
    # Get available questions (not recently used)
    available_questions = [q for q in available_pool if q["id"] not in used_questions[subject]]
    
    if not available_questions:
        # Fallback to any question from the pool
        available_questions = available_pool
    
    if not available_questions:
        # Final fallback - return a default question
        return {
            "id": 1,
            "question": "Pergunta não encontrada",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": "A",
            "period": "Erro",
            "subject": subject or "historia"
        }
    
    # Select random question
    question = random.choice(available_questions)
    used_questions[subject].add(question["id"])
    
    return question