import cv2
import os
from template_matching import TemplateMatcher
from utils import load_image_gray, prepare_image
import logging


def listar_imagens(diretorio):
    imagens = [f for f in os.listdir(diretorio) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    if not imagens:
        print("❌ Nenhuma imagem encontrada no diretório.")
        return []
    
    print("\n📂 Imagens disponíveis:")
    for i, img in enumerate(imagens[:9], 1):
        print(f"{i}. {img}")
    # print(f"{len(imagens) + 1}. Outros (carregar imagem do PC)")
    
    return imagens

def selecionar_imagem(imagens):
    while True:
        try:
            escolha = int(input("\n🔢 Escolha o número da imagem para analisar: "))
            if 1 <= escolha <= len(imagens):
                return imagens[escolha - 1]
            # elif escolha == len(imagens) + 1:
            #     return carregar_imagem_pc()
            else:
                print("⚠️ Escolha um número válido da lista.")
                logging.info("O usuário não escolheu um número válido da lista")
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número.")
            logging.info("O usuário não digitou um número")


# def carregar_imagem_pc():
#     print("🔄 Faça o upload de uma imagem...")
#     try:
#         # Código comentado para usar tkinter no futuro:
#         # import tkinter as tk
#         # from tkinter import filedialog
#         # root = tk.Tk()
#         # root.withdraw()  # Não exibe a janela principal
#         # image_path = filedialog.askopenfilename(title="Escolha a imagem", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        
#         # Para agora, pode ser substituído por outro método de upload, como por exemplo:
#         image_path = input("Digite o caminho completo da imagem: ")
        
#         if not image_path:
#             print("❌ Nenhuma imagem carregada.")
#             return None
        
#         print(f"✅ Imagem carregada: {image_path}")
#         return image_path
#     except Exception as e:
#         print(f"⚠️ Erro ao carregar imagem: {e}")
#         return None

def main():
    print(f"🔍 Iniciando o processamento...\n")
    logging.info("Iniciando o processamento...")

    
    # Define a pasta com as imagens disponíveis
    assets_folder = "./assets/"
    imagens_disponiveis = listar_imagens(assets_folder)
    if not imagens_disponiveis:
        return
    
    # Usuário seleciona uma imagem
    imagem_escolhida = selecionar_imagem(imagens_disponiveis)
    if imagem_escolhida is None:
        return
    
    if imagem_escolhida.startswith("/"):  # Se a imagem foi carregada do PC
        case_path = imagem_escolhida
    else:
        case_path = os.path.join(assets_folder, imagem_escolhida)
        print(case_path)

    
    # Define a pasta com as imagens a serem procuradas
    image_folder = "./assets/search"
    
    # Caminho para salvar a imagem processada
    output_path = "/content/Coin_Detection/result.png"
    
    # Carrega a imagem case 
    case_gray, case = prepare_image(case_path)

    # Instancia o detector
    matcher = TemplateMatcher(threshold=0.92, nms_threshold=0.3)
    
    # Processa todas as imagens no diretório
    all_boxes, all_confidences = matcher.process_images_in_directory(image_folder, case_gray, case)
    
    # Salva o resultado final
    cv2.imwrite(output_path, case)
    print(f"\n✅ Resultado salvo em: {output_path}")
    logging.info(f"Resultado salvo em: {output_path} \n")


if __name__ == "__main__":
    main()
