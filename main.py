from pathlib import Path
from datetime import datetime
import shutil

# --- CONFIGURAÇÃO ---
# Caminho da pasta "organizador"
# Ajuste este caminho para onde está a sua pasta
caminho_base = Path(r'D:\Projetos\LanCode\Projetos\Projeto 2 - Gerenciamento de Arquivos\organizador')
arquivo_log = caminho_base / 'registro.log'

# Variáveis para o Relatório Final
total_movidos = 0
extensoes_encontradas = set() # 'set' guarda itens únicos (não repete)

# --- FUNÇÃO DE LOG ---
def registrar_log(nome_arquivo, pasta_destino):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')
    mensagem = f'{agora} | {nome_arquivo} -> Movido para: {pasta_destino}\n'
    
    with open(arquivo_log, mode='a', encoding='utf-8') as log:
        log.write(mensagem)

# --- INÍCIO DO PROGRAMA ---
print(f"--- Iniciando organização em: {caminho_base} ---\n")

# Verifica se a pasta existe antes de começar
if not caminho_base.exists():
    print("ERRO: A pasta 'organizador' não foi encontrada no caminho informado.")
else:
    for arquivo in caminho_base.iterdir():
        
        # 1. Ignorar pastas e arquivos de sistema do script
        if not arquivo.is_file():
            continue
        if arquivo.name == 'registro.log' or arquivo.name == Path(__file__).name:
            continue

        # 2. Identificar a extensão (ex: .pdf -> PDF)
        
        extensao = arquivo.suffix.lower()
        nome_pasta = extensao.replace('.', '').upper() 

        # Se o arquivo não tiver extensão, jogamos numa pasta "OUTROS"
        if not nome_pasta:
            nome_pasta = 'OUTROS'

        # 3. Criar a subpasta automaticamente 
        pasta_destino = caminho_base / nome_pasta
        pasta_destino.mkdir(exist_ok=True)

        # 4. Mover o arquivo
        # Usamos try/except caso dê erro 
        try:
            shutil.move(str(arquivo), str(pasta_destino))
            
            # 5. Registrar ação
            print(f'{arquivo.name} -> {nome_pasta}')
            registrar_log(arquivo.name, nome_pasta)
            
            # Atualizar contadores
            total_movidos += 1
            extensoes_encontradas.add(extensao)
            
        except Exception as e:
            print(f'Erro ao mover {arquivo.name}: {e}')

    # --- RESUMO FINAL ---
    print('\n' + '='*40)
    print('       RELATÓRIO DE ORGANIZAÇÃO       ')
    print('='*40)
    print(f'Arquivos organizados: {total_movidos}')
    
    # Transforma o conjunto em uma string bonita (ex: ".pdf, .jpg")
    lista_ext = ', '.join(extensoes_encontradas)
    print(f'Tipos encontrados:    {lista_ext if lista_ext else "Nenhum"}')
    print('='*40)