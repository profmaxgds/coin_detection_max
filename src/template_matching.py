import cv2
import numpy as np
import os
import multiprocessing
import logging
from image_processing import generate_variations
import logging


def apply_nms(boxes, confidences, threshold, nms_threshold):
    """Função para realizar a supressão de não-máximos."""

    try:
      indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=threshold, nms_threshold=nms_threshold)

      if len(indices) > 0:
          indices = indices.flatten()
          # Filtrando as caixas e confidências com base nos índices do NMS
          final_boxes = [boxes[i] for i in indices]
          final_confidences = [confidences[i] for i in indices]
          return final_boxes, final_confidences
          logging.info("Operações NMS aplicadas com sucesso")
    except Exception as e:
      logging.error(f"Erro ao aplicar NMS: {e}")

    return [], []


def match_single_template(args):
    """Realiza a correspondência de um único template em relação à imagem 'case'."""
    case_gray, variant = args
    result = cv2.matchTemplate(case_gray, variant, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    locations = np.where(result >= threshold)
    h, w = variant.shape

    boxes = []
    confidences = []

    for pt in zip(*locations[::-1]):
        top_left = pt
        boxes.append([top_left[0], top_left[1], w, h])
        confidences.append(result[top_left[1], top_left[0]])

    return boxes, confidences

class TemplateMatcher:
    def __init__(self, threshold=0.92, nms_threshold=0.3):
        self.threshold = threshold
        self.nms_threshold = nms_threshold

    def match_templates(self, case_gray, templates):
        """Dispara a correspondência de templates em paralelo."""
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.map(match_single_template, [(case_gray, t) for t in templates])

        # Juntar todos os resultados
        all_boxes = [box for res in results for box in res[0]]
        all_confidences = [conf for res in results for conf in res[1]]

        return all_boxes, all_confidences

    def process_images_in_directory(self, image_folder, case_gray, case):
        """Processa as imagens do diretório, gerando variações e realizando a correspondência de template."""
        all_boxes = []
        all_confidences = []

        for filename in os.listdir(image_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                template_path = os.path.join(image_folder, filename)
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

                if template is None:
                    print(f"Erro ao carregar {filename}")
                    logging.error(f"Erro ao carregar {filename}")
                    continue

                templates = generate_variations(template, filename)

                # Processamento paralelo para correspondência de templates
                boxes, confidences = self.match_templates(case_gray, templates)

                all_boxes.extend(boxes)
                all_confidences.extend(confidences)

        # Aplicar NMS
        final_boxes, final_confidences = apply_nms(all_boxes, all_confidences, threshold=self.threshold, nms_threshold=self.nms_threshold)

        # Desenhar as caixas na imagem
        for ind, ((x, y, w, h), conf) in enumerate(zip(final_boxes, final_confidences), start=1):
            cv2.rectangle(case, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print(f"🎯 {ind} Detecção em {x},{y} com confiança {conf:.2%}")
            logging.info(f"{ind} Detecção em {x},{y} com confiança {conf:.2%}")

        return final_boxes, final_confidences
