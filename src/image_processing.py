import cv2
import numpy as np
from utils import adjust_brightness_contrast
import logging

def generate_variations(image, image_name):
    """Gera variações da imagem com diferentes transformações."""
    print(f"\n🛠️ Gerando variações para: {image_name}\n")

    variations = [image]

    # Escalas
    scales = np.arange(0.2, 1.4, 0.05)
    variations.extend([cv2.resize(image, (int(image.shape[1] * s), int(image.shape[0] * s))) for s in scales])

    # Rotações
    for resized in variations.copy():
        variations.extend([cv2.warpAffine(resized, cv2.getRotationMatrix2D((resized.shape[1] // 2, resized.shape[0] // 2), angle, 1), (resized.shape[1], resized.shape[0])) for angle in range(0, 360, 5)])

    # Espelhamentos
    flips = [cv2.flip(image, mode) for mode in [1, 0, -1]]
    variations.extend(flips)

    # Brilho e contraste
    settings = [(1.0, 50), (1.0, -50), (1.50, 0), (0.50, 0), (1.50, 30), (0.50, -30), (1.50, -30), (0.50, 30)]
    variations.extend([adjust_brightness_contrast(image, alpha, beta) for alpha, beta in settings])

    # Baixa resolução
    variations.extend([cv2.resize(cv2.resize(image, (int(image.shape[1] * s), int(image.shape[0] * s))), (image.shape[1], image.shape[0])) for s in np.arange(0.3, 0.6, 0.05)])

    logging.info(f"Total de variações geradas para {image_name}: {len(variations)}")


    print(f"📂 Total de variações geradas para {image_name}: {len(variations)} \n")

    return variations
