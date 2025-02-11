import cv2
import numpy as np
import os
import logging
import time
from datetime import datetime
import pytz


# Define o fuso horário desejado
TZ = "America/Sao_Paulo"  # Altere para o seu timezone, se necessário
os.environ['TZ'] = TZ
time.tzset()  # Aplica a configuração no ambiente Linux

# Diretório do log
log_dir = "/content/Coin_Detection/logs"
os.makedirs(log_dir, exist_ok=True)

# Configuração do logging
log_file = os.path.join(log_dir, "log_utils.txt")

class CustomFormatter(logging.Formatter):
    """ Formatter que aplica o timezone correto """
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, pytz.timezone(TZ))
        return dt.timetuple()

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, pytz.timezone(TZ))
        return dt.strftime(datefmt if datefmt else "%Y-%m-%d %H:%M:%S,%f")[:-3]

formatter = CustomFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(log_file, mode='a')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logging.info("Sistema de logging inicializado.")

def adjust_brightness_contrast(image, alpha, beta):
    """
    Ajusta o brilho e o contraste da imagem.
    :param image: Imagem de entrada
    :param alpha: Fator de contraste
    :param beta: Fator de brilho
    :return: Imagem ajustada
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def load_image_gray(image_path):
    """
    Carrega uma imagem em escala de cinza.
    :param image_path: Caminho da imagem
    :return: Imagem em escala de cinza
    """
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def prepare_image(case_path):
    """
    Carrega a imagem 'case', converte para escala de cinza e aplica operações morfológicas.
    :param case_path: Caminho da imagem 'case'
    :return: Imagem em escala de cinza e a imagem original
    """
    # Carregar a imagem principal (case.png)
    case = cv2.imread(case_path, cv2.IMREAD_COLOR)

    # Converter para escala de cinza
    case_gray = cv2.cvtColor(case, cv2.COLOR_BGR2GRAY)

    # # Definir o kernel para operações morfológicas
    # kernel = np.ones((1, 1), np.uint8)

    # # Ajustar o contraste (aumentar 100%)
    # case_gray = adjust_brightness_contrast(case_gray, alpha=2.0, beta=0)

    # # Abertura pode remover pequenos ruídos
    # case_gray = cv2.morphologyEx(case_gray, cv2.MORPH_OPEN, kernel)

    # # Fechamento ajuda a preencher buracos dentro das moedas
    # case_gray = cv2.morphologyEx(case_gray, cv2.MORPH_CLOSE, kernel)

    logging.info(f"A imagem {case_path} foi pré-processada com sucesso")

    return case_gray, case
