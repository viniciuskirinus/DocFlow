from io import BytesIO
from PyPDF2 import PdfReader

def show_pdf(pdf_blob):
    # Decodifica o conteúdo binário do PDF
    pdf_file = BytesIO(pdf_blob)
    
    # Use o PyPDF2 para ler o conteúdo do PDF
    pdf_reader = PdfReader(pdf_file)
    
    # Inicialize uma lista para armazenar o conteúdo de cada página do PDF
    pdf_content = []
    
    # Itera sobre todas as páginas do PDF e adiciona o conteúdo de cada página à lista
    for page_num in range(len(pdf_reader.pages)):
        page_content = pdf_reader.pages[page_num].extract_text()
        # Adiciona quebras de linha para formatar o texto
        page_content_with_breaks = add_line_breaks(page_content)
        pdf_content.append(page_content_with_breaks)
    
    # Retorna o conteúdo do PDF como uma lista de strings
    return pdf_content

def add_line_breaks(text):
    # Adiciona quebras de linha a cada 100 caracteres
    max_line_length = 100
    lines = [text[i:i+max_line_length] for i in range(0, len(text), max_line_length)]
    return '\n'.join(lines)