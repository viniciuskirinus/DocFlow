from .models import conectar_db

def show_pdf(pdf_id):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT location FROM pdf WHERE id_pdf = '{pdf_id}'")
    result = cursor.fetchone()

    if result is None:
        print("PDF não encontrado no banco de dados.")
        return None

    filename = result[0]  # Acessando o primeiro elemento da tupla, que deve conter o valor 'location'
    pdf_location = f"http://127.0.0.1:5000/docs/{filename}"
    return pdf_location
