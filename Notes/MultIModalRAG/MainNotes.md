## **Text emmbeddings:**

Os RAGS operam por embeds, tanto texto e imagens viram vetores para que máquinas entendam o significado das imagens e palavras.

## O problema:

O problema dos RAG que só entendem texto é que o mundo é muito complexo com diferentes tipos de entradas.
Ou seja ele falha para extrair dados de graficos por exemplo.
E por fim leva a respostas incorretas e incompletas de fluxos multi modais.

**A importancia de RAG multimodal:**

Alinha texto e imagem para algo com sentido.
Le graficos, diagramas e até screenshots.
Produz respostas mais completas e precisas.

Eles compartilham o mesmo espaço semantico, ou seja, o mesmo embedding para texto e imagem,
o que é importante para a compreensão do contexto.

**Alguns cuidados:**

Diferentes encoders produzem embeddings diferentes, o que torna os diferentes modelos (imagem e texto)
incompatíveis.

Como ranquear e combinar os resultados heterogeneos de busca.

Quando misturamos multiplas coisas, podemos perdoar nuance visual, não é possivel traduzir da imagem para o textual.

## RAG multimodal:

O RAG multimodal é um modelo que entende imagens e texto ao mesmo tempo.

## Implementacoes:

PS: Eles não são excludentes.

**(1) CLIP**

O clip permite que imagens e texto fiquem no mesmo text embedding, ele entende imagens e texto ao mesmo tempo.

Ou seja, relaciona imagem com texto.

Pseudo código:

```
from transformers import CLIPTextModel, CLIPImageModel

model = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

text = "A cat is sitting on a mat"
image = Image.open("cat.jpg")

inputs = processor(text=text, images=image, return_tensors="pt")
outputs = model(**inputs)

# verify similarity
similarity = cosine_similarity(outputs.image_embeds, outputs.text_embeds)
```

**(2)Hibrido multi-store arquitetura:**

É a arquitetura ao qual diferentes formatos de bancos vetoriais guardam separadamente as coisas.
Podemos ter um banco de imagens e um banco de textos, e esses bancos podem inclusive ter encoders diferentes.

A busca é feita nos dois bancos e depois se executa um hibrido de busca, que combina os resultados de ambos.

Pseudo código:

```
import faiss

text_index = faiss.IndexFlatL2(768)
image_index = faiss.IndexFlatL2(768)

# indexa os textos
for text in texts:
    text_index.add(text)

# indexa as imagens
for image in images:
    image_index.add(image)

# busca
query = "A cat is sitting on a mat"

text_results = text_index.search(query, 10)
image_results = image_index.search(query, 10)

#re rank
reranker = CrossEncoder('ms-marco-MiniLM-L6-v2')

final_results = reranker.predict(query, text_results, image_results)[:10]
```

**(3)grounding**

Para mover para a produção, sempre é bom analisar estratégias de caching.
Podemos fazer um check cache flow ao produzir queries, e com isso retornar o resultado do cache.

Query > Check cache > Cache hit > Return result
Query > Check cache > Cache miss > Execute query > Cache result

**Imagem para texto:**

Podemos usar OCR (Tesseract, Azure AI Vistion)
Podemos criar descrficoes para imagens (BLIP, GIT)
Gráfico para textos (MatCha, ChartQA)
Detecçao de objetos (YOLO, Detectron 2)

Tudo isso enriquece a imagem para texto.

**OCR:**

Extrai textos de graficos, imagens e diagramas e com isso permite pesquisa por texto.

Pseudo código:

```
import pytesseract

image = Image.open("chart_revenue.png")
text = pytesseract.image_to_string(image)

print(text)
```

output:
{
    "text": "Revenues for the year 2020 were $1.2 billion, up from $1.1 billion in 2019.",
}
