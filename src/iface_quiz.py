def riskProfileQuiz():
    # Constants for responses
    concordo = "concordo"
    discordo = "discordo"
    neutro = "neutro"

    # Questions and answers
    questions = [
        "Aceito assumir riscos no longo prazo, pois acredito que no longo prazo o retorno será maior.",
        "Ganhar o máximo que puder é importante para mim, mesmo que tenha risco de perder parte do capital.",
        "Prefiro ver meus investimentos crescendo constantemente, sem altos e baixos, mesmo que no longo prazo eu tenha retorno menor.",
        "Evitar perdas neste ano é mais importante do que crescimento a longo prazo. Eu quero proteger minha poupança a curto prazo."
    ]

    answers = [
        [discordo, neutro, concordo],
        [discordo, neutro, concordo],
        [concordo, neutro, discordo],
        [concordo, neutro, discordo]
    ]

    # Ask questions and get responses
    profile_counter = 0
    for i, question in enumerate(questions):
        print(question)
        for j, answer in enumerate(answers[i]):
            print(f"{j+1}: {answer}")

        response = input("Your answer (1/2/3): ")
        while response not in ['1', '2', '3']:
            response = ("Invalid response. Please enter 1, 2 or 3:")
        if response == '1':
            profile_counter += 0
        elif response == '2':
            profile_counter += 1
        elif response == '3':
            profile_counter += 3

    #Determinando perfil

    if profile_counter < 4:
        profile = "Conservador."
    elif profile_counter > 8:
        profile = "Agressivo."
    else:
        profile = "Moderado."

    return profile

#Aplicação
resposta = riskProfileQuiz()
print("Seu perfil de risco é:", resposta)