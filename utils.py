from PIL import ImageGrab
import pyperclip
import sys
import time
import itertools

class Clipboard:

    @staticmethod
    def read():

        try:

            img = ImageGrab.grabclipboard()
            if img is not None:
                print("\033[32m✓ Imagem coletada da area de transferencia.\033[0m")

                img_path = "temp_img.png"
                img.save(img_path)

                return {"type": "image", "content": img_path}


            text = pyperclip.paste().strip()
            if text:
                print("\033[32m✓ Texto coletado da area de transferencia.\033[0m")
                return {'type': 'text', 'content': text}

        except Exception as e:
            print(f"erro ao ler area de transferencia: {e}")

        return None



def loading_animation(stop_event, message="Processando"):

    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])

    while not stop_event.is_set():

        sys.stdout.write(f'\r{message} \033[36m{next(spinner)}\033[0m ')
        sys.stdout.flush()
        time.sleep(0.08)


    sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
    sys.stdout.flush()