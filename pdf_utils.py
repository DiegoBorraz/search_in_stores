from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Image as RLImage, Spacer)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch  # Importe a unidade 'inch'

def criar_pdf_reportlab(nome_arquivo, dados):
    """Cria um PDF usando reportlab com lista de pessoas"""
    doc = SimpleDocTemplate(
      nome_arquivo,
      pagesize=letter,
      leftMargin=0.1*inch,    # Margem esquerda reduzida (padrão: 0.75*inch)
      rightMargin=0.1*inch,    # Margem direita reduzida (padrão: 0.75*inch)
      topMargin=0.1*inch,      # Margem superior
      bottomMargin=0.1*inch    # Margem inferior
    )
    elementos = []
    
    estilos = getSampleStyleSheet()
    # Estilo personalizado para informações do produto
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=estilos["Normal"],
        fontSize=12,
        leading=16,
        spaceAfter=12,
        alignment=1  # Centralizado
    )
    
    titulo = Paragraph("Lista de Itens", estilos["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.2*inch))
    
    for produto in dados:
        try:
            # Cria a imagem para o PDF
            produto['img_data'].seek(0)  # Volta ao início do buffer
            img = RLImage(produto['img_data'], width=2.5*inch, height=3.5*inch)
            img.hAlign = 'CENTER'
            
            
            # Informações do produto (uma abaixo da outra)
            info_produto = [
                Paragraph(f"<b>{produto['nome']}</b>", info_style),
                Paragraph(f"<b>Preço:</b> {produto['preco_atual']}", info_style),
                Paragraph(f"<b>Loja:</b> {produto['loja']}", info_style),
                Spacer(0.1, 0.1*inch)  # Espaço entre produtos
            ]
            
            # Tabela para organizar imagem e informações
            tabela = Table(
                [[img], *[[info] for info in info_produto]],
                colWidths=[10.5*inch],
                hAlign='CENTER'
            )
            
            estilo_tabela = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.white),
            ])
            
            tabela.setStyle(estilo_tabela)
            elementos.append(tabela)
            
        except Exception as e:
            print(f"⚠️ Erro ao processar produto: {str(e)}")
            continue
    
    doc.build(elementos)