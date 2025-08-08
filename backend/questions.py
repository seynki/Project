import random

# Questions database for the historical tic-tac-toe game
QUESTIONS = [
    {
        "id": 1,
        "question": "Em que ano o Brasil foi descoberto pelos portugueses?",
        "options": ["1498", "1500", "1502", "1505"],
        "correctAnswer": "1500",
        "period": "Descobrimento do Brasil"
    },
    {
        "id": 2,
        "question": "Quem foi o primeiro governador-geral do Brasil?",
        "options": ["Tomé de Sousa", "Duarte da Costa", "Mem de Sá", "Pedro Álvares Cabral"],
        "correctAnswer": "Tomé de Sousa",
        "period": "Brasil Colonial"
    },
    {
        "id": 3,
        "question": "Em que ano foi abolida a escravidão no Brasil?",
        "options": ["1885", "1888", "1889", "1890"],
        "correctAnswer": "1888",
        "period": "Brasil Imperial"
    },
    {
        "id": 4,
        "question": "Quem foi o último imperador do Brasil?",
        "options": ["Dom Pedro I", "Dom Pedro II", "Dom João VI", "Princesa Isabel"],
        "correctAnswer": "Dom Pedro II",
        "period": "Brasil Imperial"
    },
    {
        "id": 5,
        "question": "Em que ano foi proclamada a República no Brasil?",
        "options": ["1888", "1889", "1890", "1891"],
        "correctAnswer": "1889",
        "period": "Proclamação da República"
    },
    {
        "id": 6,
        "question": "Qual foi a primeira capital do Brasil?",
        "options": ["Rio de Janeiro", "Salvador", "São Vicente", "Olinda"],
        "correctAnswer": "Salvador",
        "period": "Brasil Colonial"
    },
    {
        "id": 7,
        "question": "Quem foi o navegador português que chegou ao Brasil em 1500?",
        "options": ["Vasco da Gama", "Pedro Álvares Cabral", "Bartolomeu Dias", "Fernando de Magalhães"],
        "correctAnswer": "Pedro Álvares Cabral",
        "period": "Descobrimento do Brasil"
    },
    {
        "id": 8,
        "question": "Em que ano foi assinada a Lei Áurea?",
        "options": ["13 de maio de 1887", "13 de maio de 1888", "15 de novembro de 1889", "13 de maio de 1890"],
        "correctAnswer": "13 de maio de 1888",
        "period": "Brasil Imperial"
    },
    {
        "id": 9,
        "question": "Quem foi o proclamador da República no Brasil?",
        "options": ["Deodoro da Fonseca", "Floriano Peixoto", "Benjamin Constant", "Rui Barbosa"],
        "correctAnswer": "Deodoro da Fonseca",
        "period": "Proclamação da República"
    },
    {
        "id": 10,
        "question": "Qual era o nome da primeira carta escrita sobre o Brasil?",
        "options": ["Carta de Pero Vaz de Caminha", "Carta de Tomé de Sousa", "Carta do Descobrimento", "Carta Real"],
        "correctAnswer": "Carta de Pero Vaz de Caminha",
        "period": "Descobrimento do Brasil"
    },
    {
        "id": 11,
        "question": "Qual foi o primeiro presidente do Brasil?",
        "options": ["Getúlio Vargas", "Deodoro da Fonseca", "Floriano Peixoto", "Prudente de Morais"],
        "correctAnswer": "Deodoro da Fonseca",
        "period": "Primeira República"
    },
    {
        "id": 12,
        "question": "Em que século ocorreu a corrida do ouro em Minas Gerais?",
        "options": ["Século XVI", "Século XVII", "Século XVIII", "Século XIX"],
        "correctAnswer": "Século XVIII",
        "period": "Brasil Colonial"
    },
    {
        "id": 13,
        "question": "Qual foi o nome do movimento de independência ocorrido em Minas Gerais em 1789?",
        "options": ["Conjuração Mineira", "Conjuração Baiana", "Revolução Farroupilha", "Cabanagem"],
        "correctAnswer": "Conjuração Mineira",
        "period": "Brasil Colonial"
    },
    {
        "id": 14,
        "question": "Quem foi o líder da Conjuração Mineira?",
        "options": ["Tiradentes", "Tomás Antônio Gonzaga", "Cláudio Manuel da Costa", "Alvarenga Peixoto"],
        "correctAnswer": "Tiradentes",
        "period": "Brasil Colonial"
    },
    {
        "id": 15,
        "question": "Em que ano Dom Pedro I declarou a independência do Brasil?",
        "options": ["1821", "1822", "1823", "1824"],
        "correctAnswer": "1822",
        "period": "Independência do Brasil"
    },
    {
        "id": 16,
        "question": "Onde foi proclamada a independência do Brasil?",
        "options": ["Rio de Janeiro", "às margens do rio Ipiranga", "Salvador", "São Paulo"],
        "correctAnswer": "às margens do rio Ipiranga",
        "period": "Independência do Brasil"
    },
    {
        "id": 17,
        "question": "Qual foi o nome do período em que Dom Pedro II governou o Brasil?",
        "options": ["Primeiro Reinado", "Segundo Reinado", "Período Regencial", "República Velha"],
        "correctAnswer": "Segundo Reinado",
        "period": "Brasil Imperial"
    },
    {
        "id": 18,
        "question": "Qual foi a principal atividade econômica no Brasil durante o período colonial?",
        "options": ["Mineração", "Agricultura (cana-de-açúcar)", "Pecuária", "Comércio"],
        "correctAnswer": "Agricultura (cana-de-açúcar)",
        "period": "Brasil Colonial"
    },
    {
        "id": 19,
        "question": "Quem foi a princesa que assinou a Lei Áurea?",
        "options": ["Princesa Isabel", "Princesa Leopoldina", "Princesa Januária", "Princesa Francisca"],
        "correctAnswer": "Princesa Isabel",
        "period": "Brasil Imperial"
    },
    {
        "id": 20,
        "question": "Em que ano foi criado o Distrito Federal (Brasília)?",
        "options": ["1956", "1957", "1960", "1961"],
        "correctAnswer": "1960",
        "period": "Brasil República"
    }
]

used_questions = set()

def get_random_question():
    """Get a random question, avoiding recently used ones when possible"""
    global used_questions
    
    # If we've used all questions, reset the used set
    if len(used_questions) >= len(QUESTIONS):
        used_questions.clear()
    
    # Get available questions
    available_questions = [q for q in QUESTIONS if q["id"] not in used_questions]
    
    if not available_questions:
        # Fallback to any question
        available_questions = QUESTIONS
    
    # Select random question
    question = random.choice(available_questions)
    used_questions.add(question["id"])
    
    return question