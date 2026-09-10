"""
RiskMatrix v2.9.1
Plataforma integrada de análise e cruzamento de riscos operacionais e estratégicos.
Aplica metodologias COSO ERM e ISO 31000.
"""

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from io import BytesIO
import os
from datetime import datetime
import traceback

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Criar pastas se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_risk_catalog(filepath):
    """Carrega o catálogo de 29 riscos estratégicos"""
    try:
        df = pd.read_excel(filepath, sheet_name=0)
        return df
    except Exception as e:
        return None

def extract_keywords(text):
    """Extrai palavras-chave de um texto"""
    if pd.isna(text):
        return set()
    text = str(text).lower()
    words = set(word.strip() for word in text.split(';') if word.strip())
    return words

def calculate_similarity(control_text, risk_keywords, exclusion_keywords=None):
    """
    Calcula similaridade entre um controle e palavras-chave de risco.
    
    Pass 1: Keyword matching com exclusão
    - Se contém exclusion_keywords, retorna 0
    - Se contém risk_keywords, retorna confiança alta
    """
    if pd.isna(control_text):
        return 0.0, []
    
    control_text = str(control_text).lower()
    control_words = set(control_text.split())
    
    # Verificar exclusion keywords (Pass 1 - exclusão)
    if exclusion_keywords:
        for excl_word in exclusion_keywords:
            if excl_word.lower() in control_text:
                return 0.0, []
    
    # Verificar risk keywords (Pass 1 - correspondência positiva)
    if risk_keywords:
        matches = []
        confidence = 0.0
        
        for keyword in risk_keywords:
            if keyword.lower() in control_text:
                matches.append(keyword)
                confidence = max(confidence, 0.95)  # Alta confiança para match exato
        
        if matches:
            return confidence, matches
    
    # Pass 2: TF-IDF para matches parciais (opcional)
    return 0.0, []

def process_risk_matrix(matrix_file, catalog_file):
    """
    Processa a matriz de riscos e controles contra o catálogo de riscos.
    
    Retorna:
    - DataFrame com anotações
    - Dashboard com resumo
    - Relatório de auditoria
    """
    try:
        # Carregar arquivos
        matrix_df = pd.read_excel(matrix_file, sheet_name=0)
        catalog_df = pd.read_excel(catalog_file, sheet_name=0)
        
        if catalog_df.empty or matrix_df.empty:
            return None, "Arquivos vazios ou inválidos"
        
        # Preparar dados do catálogo
        # Estrutura esperada: Col A = Risco, Col G = keywords, Col H = exclusion
        risks = {}
        for idx, row in catalog_df.iterrows():
            risk_name = str(row.iloc[0]) if not pd.isna(row.iloc[0]) else f"Risco_{idx}"
            keywords = extract_keywords(row.iloc[6] if len(row) > 6 else None)  # Col G
            exclusions = extract_keywords(row.iloc[7] if len(row) > 7 else None)  # Col H
            
            risks[risk_name] = {
                'keywords': keywords,
                'exclusions': exclusions
            }
        
        # Processar matriz
        annotated_df = matrix_df.copy()
        
        # Adicionar colunas de resultado se não existirem
        if 'Risco Estratégico - Proposta' not in annotated_df.columns:
            annotated_df['Risco Estratégico - Proposta'] = ''
        if 'Percentual de certeza' not in annotated_df.columns:
            annotated_df['Percentual de certeza'] = 0.0
        if 'Justificativa da análise' not in annotated_df.columns:
            annotated_df['Justificativa da análise'] = ''
        
        # Classificar cada linha
        audit_log = []
        
        for idx, row in matrix_df.iterrows():
            control_name = row.iloc[0] if len(row) > 0 else f"Controle_{idx}"
            control_text = ' '.join(str(v) for v in row.values if not pd.isna(v))
            
            best_risk = None
            best_confidence = 0.0
            best_matches = []
            
            # Comparar contra todos os riscos
            for risk_name, risk_data in risks.items():
                confidence, matches = calculate_similarity(
                    control_text,
                    risk_data['keywords'],
                    risk_data['exclusions']
                )
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_risk = risk_name
                    best_matches = matches
            
            # Atualizar linha
            if best_risk:
                annotated_df.at[idx, 'Risco Estratégico - Proposta'] = best_risk
                annotated_df.at[idx, 'Percentual de certeza'] = best_confidence
                annotated_df.at[idx, 'Justificativa da análise'] = f"Palavras-chave encontradas: {', '.join(best_matches)}"
                
                audit_log.append({
                    'Controle': control_name,
                    'Risco Classificado': best_risk,
                    'Confiança': f"{best_confidence*100:.1f}%",
                    'Justificativa': ', '.join(best_matches) if best_matches else 'Baixa confiança'
                })
        
        audit_df = pd.DataFrame(audit_log)
        
        # Criar resumo/dashboard
        summary_data = {
            'Total de Controles': len(matrix_df),
            'Controles Classificados': len([x for x in annotated_df['Risco Estratégico - Proposta'] if x]),
            'Confiança Média': f"{annotated_df['Percentual de certeza'].mean()*100:.1f}%",
            'Data de Processamento': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        summary_df = pd.DataFrame([summary_data])
        
        return {
            'annotated': annotated_df,
            'audit': audit_df,
            'summary': summary_df
        }, None
        
    except Exception as e:
        return None, f"Erro ao processar: {str(e)}\n{traceback.format_exc()}"

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def api_process():
    """API para processar arquivos"""
    try:
        # Verificar se os arquivos foram enviados
        if 'matrix_file' not in request.files or 'catalog_file' not in request.files:
            return jsonify({'error': 'Arquivos não enviados'}), 400
        
        matrix_file = request.files['matrix_file']
        catalog_file = request.files['catalog_file']
        
        if matrix_file.filename == '' or catalog_file.filename == '':
            return jsonify({'error': 'Selecione ambos os arquivos'}), 400
        
        if not (allowed_file(matrix_file.filename) and allowed_file(catalog_file.filename)):
            return jsonify({'error': 'Arquivos devem estar em formato .xlsx ou .xls'}), 400
        
        # Salvar arquivos temporários
        matrix_path = os.path.join(app.config['UPLOAD_FOLDER'], 'matrix_' + secure_filename(matrix_file.filename))
        catalog_path = os.path.join(app.config['UPLOAD_FOLDER'], 'catalog_' + secure_filename(catalog_file.filename))
        
        matrix_file.save(matrix_path)
        catalog_file.save(catalog_path)
        
        # Processar
        results, error = process_risk_matrix(matrix_path, catalog_path)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Gerar arquivo de saída
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'RiskMatrix_Result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            results['annotated'].to_excel(writer, sheet_name='Matriz Anotada', index=False)
            results['audit'].to_excel(writer, sheet_name='Auditoria', index=False)
            results['summary'].to_excel(writer, sheet_name='Resumo', index=False)
        
        return jsonify({
            'success': True,
            'message': 'Processamento concluído com sucesso!',
            'download_url': f'/download/{os.path.basename(output_path)}',
            'stats': {
                'total_controls': int(results['summary'].iloc[0]['Total de Controles']),
                'classified': int(results['summary'].iloc[0]['Controles Classificados']),
                'avg_confidence': results['summary'].iloc[0]['Confiança Média']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download do arquivo de resultado"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if not os.path.exists(file_path):
            return "Arquivo não encontrado", 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Erro ao fazer download: {str(e)}", 500

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'version': '2.9.1'}), 200

if __name__ == '__main__':
    # Desenvolvimento
    app.run(debug=True, host='0.0.0.0', port=5000)
    # Produção: usar gunicorn
    # gunicorn app:app --bind 0.0.0.0:5000
