
import requests
import json
import os

# ASCII Art Logo XCAKE com cores ANSI
def get_xcake_logo():
    purple = "\033[95m"
    green = "\033[92m"
    blue = "\033[94m"
    reset = "\033[0m"

    logo = f"""
{purple}X{reset}{green}C{reset}{blue}A{reset}{purple}K{reset}{green}E{reset}
{purple} _  _  _ {reset}
{green}| || || |{reset}
{blue}| || || |{reset}
{purple}|_||_||_|_{reset}
    """
    return logo

# Lógica de chat com a API do Gemini (adaptada do Win Cosmic)
GEMINI_API_KEY = "AIzaSyARMU85SFP_zPwNAyRkBVywgvbXypXx5jk" # Sua chave de API do Gemini
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

async def get_aoi_reply(history, current_language='pt'):
    request_body = {
        "contents": history + [{"role": "user", "parts": [{"text": f"(Responda em {current_language})"}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 2048,
            "topP": 0.95
        }
    }

    try:
        response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(request_body))
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)

        data = response.json()
        if data.get("candidates") and data["candidates"][0].get("content") and data["candidates"][0]["content"].get("parts"):
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        elif data.get("promptFeedback") and data["promptFeedback"].get("blockReason"):
            return f"Miau... minha visão foi bloqueada ({data['promptFeedback']['blockReason']})."
        else:
            return "Miau... energias confusas nas estrelas."
    except requests.exceptions.RequestException as e:
        return f"Miau! Curto-circuito na conexão astral! Erro: {e}"
    except json.JSONDecodeError:
        return "Miau! Resposta inválida da API."

async def main():
    print(get_xcake_logo())
    print("Bem-vindo ao Terminal XCAKE! Digite 'sair' para encerrar.")

    chat_history = []
    current_language = 'pt' # Pode ser configurado para 'en', 'ja', 'fr' se desejar

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() == 'sair':
            print("Até a próxima, humano!")
            break

        if not user_input:
            continue

        chat_history.append({"role": "user", "parts": [{"text": user_input}]})
        print("Aoi está consultando o cosmos...")

        # Como requests.post é síncrono, não precisamos de await aqui no contexto de um script simples
        # Mas mantive a assinatura async para consistência com o Win Cosmic e para futura expansão
        aoi_response = await get_aoi_reply(chat_history, current_language)
        
        chat_history.append({"role": "model", "parts": [{"text": aoi_response}]})
        print(f"Aoi: {aoi_response}")

if __name__ == "__main__":
    # Para executar a função assíncrona main, precisamos de um loop de eventos
    # No Python 3.7+, podemos usar asyncio.run()
    import asyncio
    asyncio.run(main())
