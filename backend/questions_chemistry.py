import random

# Questions database for the chemistry tic-tac-toe game
CHEMISTRY_QUESTIONS = [
    {
        "id": 1,
        "question": "Qual é o símbolo químico do oxigênio?",
        "options": ["O", "Ox", "O2", "Oy"],
        "correctAnswer": "O",
        "topic": "Elementos Químicos"
    },
    {
        "id": 2,
        "question": "Quantos prótons tem um átomo de carbono?",
        "options": ["4", "6", "8", "12"],
        "correctAnswer": "6",
        "topic": "Estrutura Atômica"
    },
    {
        "id": 3,
        "question": "Qual é a fórmula química da água?",
        "options": ["H2O", "HO2", "H2O2", "HO"],
        "correctAnswer": "H2O",
        "topic": "Compostos Químicos"
    },
    {
        "id": 4,
        "question": "Na tabela periódica, qual elemento tem símbolo Na?",
        "options": ["Nitrogênio", "Sódio", "Níquel", "Neônio"],
        "correctAnswer": "Sódio",
        "topic": "Tabela Periódica"
    },
    {
        "id": 5,
        "question": "Qual é o pH de uma solução neutra?",
        "options": ["0", "7", "14", "1"],
        "correctAnswer": "7",
        "topic": "Ácidos e Bases"
    },
    {
        "id": 6,
        "question": "Qual gás é liberado na fotossíntese?",
        "options": ["CO2", "H2", "N2", "O2"],
        "correctAnswer": "O2",
        "topic": "Química Orgânica"
    },
    {
        "id": 7,
        "question": "Qual é a fórmula do gás carbônico?",
        "options": ["CO", "CO2", "C2O", "CO3"],
        "correctAnswer": "CO2",
        "topic": "Compostos Químicos"
    },
    {
        "id": 8,
        "question": "Quantos elétrons tem um átomo neutro de hélio?",
        "options": ["1", "2", "3", "4"],
        "correctAnswer": "2",
        "topic": "Estrutura Atômica"
    },
    {
        "id": 9,
        "question": "Qual é o símbolo químico do ferro?",
        "options": ["Fr", "Fe", "F", "Fo"],
        "correctAnswer": "Fe",
        "topic": "Elementos Químicos"
    },
    {
        "id": 10,
        "question": "O que significa uma ligação covalente?",
        "options": ["Transferência de elétrons", "Compartilhamento de elétrons", "Perda de prótons", "Ganho de nêutrons"],
        "correctAnswer": "Compartilhamento de elétrons",
        "topic": "Ligações Químicas"
    },
    {
        "id": 11,
        "question": "Qual é a fórmula da amônia?",
        "options": ["NH3", "NH4", "N2H", "NH2"],
        "correctAnswer": "NH3",
        "topic": "Compostos Químicos"
    },
    {
        "id": 12,
        "question": "Em condições normais, qual é o estado físico do mercúrio?",
        "options": ["Sólido", "Líquido", "Gasoso", "Plasma"],
        "correctAnswer": "Líquido",
        "topic": "Estados da Matéria"
    },
    {
        "id": 13,
        "question": "Qual elemento tem número atômico 1?",
        "options": ["Hélio", "Hidrogênio", "Lítio", "Carbono"],
        "correctAnswer": "Hidrogênio",
        "topic": "Tabela Periódica"
    },
    {
        "id": 14,
        "question": "Qual é a fórmula do sal de cozinha?",
        "options": ["NaCl", "KCl", "CaCl2", "MgCl2"],
        "correctAnswer": "NaCl",
        "topic": "Compostos Iônicos"
    },
    {
        "id": 15,
        "question": "Quantos átomos de hidrogênio tem uma molécula de metano (CH4)?",
        "options": ["2", "3", "4", "5"],
        "correctAnswer": "4",
        "topic": "Química Orgânica"
    },
    {
        "id": 16,
        "question": "O que é um catalisador?",
        "options": ["Acelera reação", "Retarda reação", "Para reação", "Inverte produtos"],
        "correctAnswer": "Acelera reação",
        "topic": "Cinética Química"
    },
    {
        "id": 17,
        "question": "Qual é a massa molecular aproximada da água (H2O)?",
        "options": ["16", "18", "20", "22"],
        "correctAnswer": "18",
        "topic": "Massa Molecular"
    },
    {
        "id": 18,
        "question": "Qual gás é o mais abundante na atmosfera?",
        "options": ["Oxigênio", "Nitrogênio", "Argônio", "CO2"],
        "correctAnswer": "Nitrogênio",
        "topic": "Química Ambiental"
    },
    {
        "id": 19,
        "question": "Qual é o símbolo químico do ouro?",
        "options": ["Go", "Or", "Au", "Ag"],
        "correctAnswer": "Au",
        "topic": "Elementos Químicos"
    },
    {
        "id": 20,
        "question": "Em uma solução, o que dissolve é chamado de:",
        "options": ["Soluto", "Solvente", "Precipitado", "Catalisador"],
        "correctAnswer": "Solvente",
        "topic": "Soluções"
    }
]

def get_random_chemistry_question(used_questions=None):
    """
    Get a random chemistry question, avoiding previously used ones
    """
    if used_questions is None:
        used_questions = []
    
    available_questions = [q for q in CHEMISTRY_QUESTIONS if q["id"] not in used_questions]
    
    if not available_questions:
        # If all questions have been used, reset and use all questions
        available_questions = CHEMISTRY_QUESTIONS
    
    return random.choice(available_questions)