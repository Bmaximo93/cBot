import os
import threading
from queue import Queue
from dotenv import load_dotenv

from utils import *
from gpt_service import ChatGPTProcessor
from calendar_bot import GoogleCalendarAutomation


load_dotenv()


def main():

    print("=" * 60)
    print("Cbot, o robô agendador")
    print("=" * 60)


    api_key = os.getenv('OPENAI_API_KEY')


    print("\n[1/4] Lendo conteúdo do clipboard...")
    clipboard_data = Clipboard.read()

    if not clipboard_data:
        print("✗ Nenhum conteúdo encontrado no clipboard!")
        return


    event_queue = Queue()
    stop_loading = threading.Event()

    def process_ai():
        try:
            processor = ChatGPTProcessor(api_key)
            event = processor.extract_event_info(clipboard_data)
            event_queue.put(event)
        finally:
            stop_loading.set()

    print("\n[2/4] Extraindo dados...")
    ai_thread = threading.Thread(target=process_ai)
    loading_thread = threading.Thread(target=loading_animation, args=(stop_loading, "Processando"))

    ai_thread.start()
    loading_thread.start()

   # testEvent = CalendarEvent(
   #     is_event=True,
   #     name="placeholder",
   #     date="23 mar 2026",
   #     start_time="10:10",
   #     end_time="20:30",
   #     all_day=True,
   #     end_date="23 mar 2026",
   #     location="Rua Teste da silva 111",
   #     description="evento placeholder para testes",
   # )

    automation = GoogleCalendarAutomation()
    automation.create_event(event_queue)

    print("=" * 60)

    ai_thread.join()
    loading_thread.join()

if __name__ == "__main__":
    main()