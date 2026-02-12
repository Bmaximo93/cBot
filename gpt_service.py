import os
import time
from datetime import datetime
from typing import Union
from pydantic import BaseModel
from openai import OpenAI



class CalendarEvent(BaseModel):
    is_event: bool
    name: str
    date: str
    start_time: str
    end_time: str
    all_day: bool
    end_date: Union[str, None]
    location: Union[str, None]
    description: str


class ChatGPTProcessor:

    def __init__(self, api_key):
     
        self.client = OpenAI(api_key=api_key)


    def extract_event_info(self, clipboard_data):

        client = self.client

        if not clipboard_data:
            return None

        today = datetime.now().strftime("%d/%m/%Y (%A)")
        prompt_text = f"""Hoje é {today}. observe o conteudo e extraia informações de evento. Regras:
- is_event = true apenas se o conteúdo indica um evento
- o conteúdo pode ser considerado um evento contanto que possa ser obtido no minimo uma data ou referencia a uma data (exemplo: amanhã, daqui a uma semana, dia 2 de fevereiro, etc)
- evento também pode ser inválido se for uma data impossivel, (IMPORTANTE: verifique possível erro de digitação antes de considerar inválido, substituindo  mas não seja demasiadamente leniente, exemplo de data impossivel: 40/13/2200) 
- evento pode ser inválido se a data ocorrer no passado em relação ao dia de hoje (exemplo: evento no ano de 1800))
- Se evento for dia inteiro, start_time/end_time = 11:11 e all_day=true
- caso não haja nenhuma informação de horário, start_time/end_time = 11:11 e all_day=true
- Se o evento durar multiplos dias, start_time/end_time = 11:11, all_day=true, especificar end_date:
- Formato de mes é uma string separada por espaços e com o mês em três letras do ingles (e.g., 2 feb 2026)
- Se não houver horários de inicio ou fim bem definidos mas o evento não for dia inteiro, se possivel deduza horários razoáveis
- Descrição inclui detalhes relevantes, evite informações redundantes como data,hora e localização na descrição
- Se não for um evento válido: is_event : false
- caso is_event: false, description deverá descrever de forma concisa, no maximo 10 palavras, que descreve o porquê do input não ser valido
"""

        user_items = []
        file_id = None
        img_path = None

        try:

            if clipboard_data["type"] == "image":
                img_path = clipboard_data["content"]


                with open(img_path, "rb") as f:
                    file_obj = client.files.create(file=f, purpose="vision")
                    file_id = file_obj.id

                user_items.append({"type": "input_text", "text": prompt_text})
                user_items.append({"type": "input_image", "file_id": file_id})

            else:
                time.sleep(1)
                full_text = f"{prompt_text}\n\nConteúdo: {clipboard_data['content']}"
                user_items.append({"type": "input_text", "text": full_text})



            response = client.responses.parse(
                model="gpt-4.1-mini",
                input=[
                    {"role": "system", "content": "Você é um extrator de eventos preciso com o objetivo de criar eventos de calendario. Voce recebe dados e os formata de acordo com o schema."},
                    {"role": "user", "content": user_items}
                ],
                text_format=CalendarEvent
            )

            return response.output_parsed

        except Exception as e:
            print(f"Erro na extração: {e}")
            return None

        finally:


            if img_path and os.path.exists(img_path):
                try:
                    os.remove(img_path)
                    print(f"Arquivo local {img_path} removido.")
                except Exception as e:
                    print(f"Erro ao deletar arquivo local: {e}")


            if file_id:
                try:
                    client.files.delete(file_id)
                    print(f"Arquivo cloud {file_id} removido.\n")
                except Exception as e:
                    print(f"Erro ao deletar arquivo na OpenAI: {e}")