# utils/chunking.py

from nltk.tokenize import sent_tokenize
import nltk

# Descargar recursos necesarios (puedes hacerlo una vez en tu entorno)
nltk.download('punkt')

def text_splitter(text: str, max_words: int = 300, overlap: int = 50) -> list[str]:
    """
    Divide un texto en chunks respetando párrafos y oraciones,
    con un máximo de palabras por chunk y superposición entre ellos.

    Args:
        text (str): Texto completo a dividir.
        max_words (int): Máximo número de palabras por chunk.
        overlap (int): Número de palabras a solapar entre chunks consecutivos.

    Returns:
        list[str]: Lista de fragmentos de texto (chunks).
    """
    paragraphs = [p.strip() for p in text.split('\n') if p.strip() and len(p.strip().split()) >= 3]
    chunks = []

    for para in paragraphs:
        words = para.split()
        if len(words) <= max_words:
            chunks.append(para)
        else:
            sentences = sent_tokenize(para, language="spanish")
            chunk = []
            count = 0
            for sent in sentences:
                sent_words = sent.split()
                if count + len(sent_words) <= max_words:
                    chunk.append(sent)
                    count += len(sent_words)
                else:
                    chunks.append(" ".join(chunk))
                    # overlap en oraciones: tomar las últimas 'overlap' oraciones del chunk anterior
                    chunk = chunk[-overlap:] if overlap < len(chunk) else chunk
                    chunk.append(sent)
                    count = sum(len(s.split()) for s in chunk)
            if chunk:
                chunks.append(" ".join(chunk))

    return chunks