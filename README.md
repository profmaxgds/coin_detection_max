# Documentação do Projeto: Sistema de Detecção de Objetos em Imagens

## 1. Visão Geral

Este projeto implementa um sistema para detectar objetos em imagens, utilizando técnicas de processamento digital, correspondência de templates e aprendizado profundo. A solução está dividida em módulos para melhor organização e reutilização do código.

## 2. Estrutura do Código

A estrutura do projeto segue a seguinte organização:

```plaintext
📂 Projeto_Deteccao
│── 📂 assets                # Diretório para armazenar imagens e máscaras
│    ├── 📂 search           # Diretório para salvar os objetos que se quer localizar
│    │    ├── coin.png       # Objeto a procurar (moeda)
│    ├── case-180.png        # Imagem para procurar o objeto rotação de -180°
│    ├── case-270.png        # Imagem para procurar o objeto rotação de -270°
│    ├── case-45.png         # Imagem para procurar o objeto rotação de -45°
│    ├── case-90.png         # Imagem para procurar o objeto rotação de -90°
│    ├── case.png            # Imagem para procurar o objeto sem rotação
│    ├── case180.png         # Imagem para procurar o objeto rotação de 180°
│    ├── case270.png         # Imagem para procurar o objeto rotação de 270°
│    ├── case45.png          # Imagem para procurar o objeto rotação de 45°
│    ├── case90.png          # Imagem para procurar o objeto rotação de 90°
│── 📂 logs                  # Armazena arquivos de log gerados
│── 📂 src                   # Código-fonte principal
│    ├── image_processing.py # Processamento e pré-processamento de imagens
│    ├── template_matching.py # Algoritmo de correspondência de templates
│    ├── utils.py            # Funções auxiliares e utilitárias
│    ├── main.py             # Script principal para integração
│── requirements.txt         # Dependências do projeto
│── README.md                # Documentação e instruções gerais
```

## 3. Descrição dos Módulos

### 3.1 `image_processing.py`

Este módulo contém funções para carregar e processar imagens antes da detecção.

#### Principais Funções:

```python
def treat_image(case_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Carrega a imagem principal, converte para escala de cinza e aplica operações morfológicas.
    """
```

```python
def generate_variations(template: np.ndarray, filename: str) -> List[np.ndarray]:
    """
    Gera variações do template aplicando transformações como rotação, espelhamento e ajuste de brilho.
    """
```

### 3.2 `template_matching.py`

Módulo responsável pela correspondência de templates.

#### Principais Funções:

```python
def match_templates(case_gray: np.ndarray, templates: List[np.ndarray]) -> Tuple[List[Tuple[int, int, int, int]], List[float]]:
    """
    Aplica cv2.matchTemplate() para encontrar regiões similares.
    """
```

```python
def apply_nms(boxes: List[Tuple[int, int, int, int]], scores: List[float], threshold: float, nms_threshold: float) -> Tuple[List[Tuple[int, int, int, int]], List[float]]:
    """
    Aplica supressão não máxima (NMS) para remover detecções redundantes.
    """
```

### 3.3 `utils.py`

Módulo contendo funções auxiliares e de suporte para o projeto.

#### Principais Funções:

```python
class CustomFormatter(logging.Formatter):
    """ Formatter que aplica o timezone correto """
```

```python
def adjust_brightness_contrast(image, alpha, beta):
    """
    Ajusta o brilho e o contraste da imagem.
    :param image: Imagem de entrada
    :param alpha: Fator de contraste
    :param beta: Fator de brilho
    :return: Imagem ajustada
    """
```

```python
def load_image_gray(image_path):
    """
    Carrega uma imagem em escala de cinza.
    :param image_path: Caminho da imagem
    :return: Imagem em escala de cinza
    """
```

```python
def prepare_image(case_path):
    """
    Carrega a imagem 'case', converte para escala de cinza e aplica operações morfológicas.
    :param case_path: Caminho da imagem 'case'
    :return: Imagem em escala de cinza e a imagem original
    """
```

### 3.4 `main.py`

Script principal que integra os módulos e executa o fluxo de processamento completo.

#### Fluxo de Execução:

1. Carrega e pré-processa a imagem principal (`case.png`).
2. Percorre a pasta de search (objetos a serem procurados) e aplica as variações.
3. Realiza a correspondência de templates e aplica NMS.
4. Gera logs detalhados e exibe os resultados.

## 4. Controle e Registro de Logs

O sistema utiliza a biblioteca `logging` para monitorar todas as etapas do processo.

### Eventos Registrados:

✅ Erros no carregamento de imagens  
✅ Processamento de templates e geração de variações  
✅ Resultados das detecções e refinamentos  
✅ Parâmetros utilizados em cada execução  

Os logs são armazenados no diretório `logs/`, garantindo rastreabilidade e auditoria.

## 5. Testes e Validação

O código foi testado com diferentes conjuntos de imagens para validar:

- **Precisão da detecção** via `cv2.matchTemplate()`.
- **Eficiência do pré-processamento** e das transformações.
- **Desempenho da supressão não máxima (NMS)**.

## 6. Instalação e Execução

### 6.1 Dependências

Antes de rodar o projeto, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 6.2 Como Executar

Para rodar a detecção de objetos, utilize o comando:

```bash
python src/main.py
```

## 7. Conclusão

Esta documentação fornece uma visão clara da arquitetura do código e das funcionalidades implementadas. O sistema foi projetado para ser modular, eficiente e extensível, garantindo facilidade de manutenção e evolução futura.
