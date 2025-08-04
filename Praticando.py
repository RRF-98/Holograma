import speech_recognition as mic
import spacy
from gtts import gTTS
from playsound import playsound
import glob
import os
import unicodedata
#import time
def removedor_de_acento(acento):
    normal = unicodedata.normalize('NFD', acento)
    return normal.encode('ascii', 'ignore').decode('utf8').casefold()
 

def Microfone():
    gravador = mic.Recognizer()

    with mic.Microphone() as source:
        
        gravador.adjust_for_ambient_noise(source, duration=1)
        
        print("="*50)
        
        print("\n>>>> Ouvindo... <<<<")
        
        try: 
            audio = gravador.listen(source, timeout=5)
            
            print("\n>>>>> Processando <<<<<")

            texto = gravador.recognize_google(audio, language = 'pt-BR' )

            print(f"\n>>>>>> Texto reconhecido: {texto} <<<<<<")
            print("="*50)
            return texto
        except mic.UnknownValueError: 
            
            print("*"*50)
            
            print("\n>>> Microfone não encrotrado !!!!")
           
            print("*"*50)
            
            return None
        except mic.RequestError:
           
            print("*"*50)
            
            print("\n>>> Falha na conexão com o serviço do google !!!!a ")
            
            print("*"*50)
            
            return None
        except mic.WaitTimeoutError:
            
            print("*"*50)
            
            print("\n>>> Nenhuma fala detectada. Tempo esgotado. ")
            
            print("*"*50)

caminho_dos_audios = 'olograma/musica'
buscar_musica = os.path.join(caminho_dos_audios, '*.mp3')
musicas_encontradas = glob.glob(buscar_musica)
npl_pt = spacy.load('pt_core_news_lg')

caminhos_das_historias = 'olograma/Historias'
buscar_historia = os.path.join(caminhos_das_historias, '*.mp3')
historias_encontradas = glob.glob(buscar_historia)
npl_en= spacy.load('en_core_web_sm')

def N_L_P_PT(texto_principal, npl, musica):
    if not texto_principal:
        print("*"*50)
        print("\n>>> Nenhum texto foi encontrado !!!")
        print("*"*50)
    print("="*50)
    print("\nAnalisando texto ")
    doc = npl(texto_principal)
    lemas = [token.lemma_ for token in doc]
    for caminho_Arquivos in musica:
        nome_dos_arquivos = os.path.basename(caminho_Arquivos)
        nome_final = nome_dos_arquivos.replace('*.mp3', '').lower()
        if texto_principal in nome_final:
            print(f"\n>>>> Musica encontrada! Tocando musica: | {nome_final} |")
            try:
                playsound(caminho_Arquivos)
                print("\n>>>> Musica acabou <<<<")
                print("="*50)
            except Exception as e:
                print("*"*50)
                print(f"\n>>>>ERRO: não foi possivel tocar a musica:  {nome_final}  pelo erro{e}")
                print("*"*50)
                return
    print("*"*50)
    print(f"\n>>>> Não foi possivel encontrar a musica com o nome {texto_principal}")
    print("\n>>>>Verifique o nome")
    print("*"*50) 

def N_L_P_EN(texto_principal, npl, musica):
    if not texto_principal:
        print("*"*50)
        print("\n>>> Nenhum texto foi encontrado !!!")
        print("*"*50)
    print("="*50)
    print("\nAnalisando texto ")
    doc = npl(texto_principal)
    lemas = [token.lemma_ for token in doc]
    for caminho_Arquivos in musica:
        nome_dos_arquivos = os.path.basename(caminho_Arquivos)
        nome_final = nome_dos_arquivos.replace('*.mp3', '').lower()
        if texto_principal in nome_final:
            print(f"\n>>>> Musica encontrada! Tocando musica: | {nome_final} |")
            try:
                playsound(caminho_Arquivos)
                print("\n>>>> Musica acabou <<<<")
                print("="*50)
            except Exception as e:
                print("*"*50)
                print(f"\n>>>>ERRO: não foi possivel tocar a musica:  {nome_final}  pelo erro{e}")
                print("*"*50)
                return
    print("*"*50)
    print(f"\n>>>> Não foi possivel encontrar a musica com o nome {texto_principal}")
    print("\n>>>>Verifique o nome")
    print("*"*50) 


print("="*50)
print("\n >>>> Iniciando o programa <<<<")

if not musicas_encontradas:
    
    print("*"*50)
    
    print(">>>> AVISO: nenhuma musica foi encontrada '.mp3' no caminho 'olograma/musica' <<<<")
    
    print("\n>>>>Verifique o caminho ou adicione a musica '.mp3' no caminho 'olograma/musica' <<<<")
    
    print("*"*50)

if not historias_encontradas:
    
    print("*"*50)
    
    print(">>>> AVISO: nenhuma musica foi encontrada '.mp3' no caminho 'olograma/Historias' <<<<")
    
    print("\n>>>>Verifique o caminho ou adicione a musica '.mp3' no caminho 'olograma/Historias' <<<<")
    
    print("*"*50)

while True:
    
    print("="*50)
    
    print("\n>>>> Aguardado o comando <<<<")
    
    print("\n>>> Opções: \nTocar musica \nContar historia \nSair")
    
    comando_usuario = Microfone()
    
    if not comando_usuario:
        continue
    if 'sair' in comando_usuario:
        print("\n>>>> Saindo <<<<")
        break
    
    doc = npl_pt(comando_usuario)
    lemas = [token.lemma_ for token in doc ]
    palavras_chave_musica = ["tocar", "ouvir", "escutar", "música", "canção", "som"]
    palavras_chave_historia = ["contar", "narrar", "dizer", "relatar", "criar", "inventar", "imaginar", "descrever", "falar sobre", "me fale"]
    
    if any(palavras in lemas for palavras in palavras_chave_musica):
        if not musicas_encontradas:
            print("\n>>>Não posso tocar músicas porque não encontrei nenhum arquivo .mp3.")
            continue

        print("\n------------- Musicas disponiveis -------------")
        for musicas_disponiveis in musicas_encontradas:
            
            nome_das_musicas = os.path.basename(musicas_disponiveis)
            
            nome_final_musica = nome_das_musicas.replace('*.mp3', '')
            
            print(f"\n {nome_final_musica}")
        
        print("\nDiga o nome da música que você quer ouvir:")
        
        nome_musica = Microfone()
        
        nome_musica_final = removedor_de_acento(nome_musica)
        nome_musica_final_en = nome_musica
        
        N_L_P_PT(nome_musica_final, npl_pt, musicas_encontradas)
        N_L_P_EN(nome_musica_final_en, npl_en, musicas_encontradas)
    else:
     print("\nResultado: não entendi seu comando. Tente dizer 'tocar música'.")

    if any(palavra in lemas for palavra in palavras_chave_historia):
        if not historias_encontradas:
            print(">>> Não posso tocar músicas porque não encontrei nenhum arquivo .mp3.")
            continue
        
        print("\n------------- Historias disponiveis -------------")
        for historias_disponiveis in historias_encontradas:
            
            nome_das_historias = os.path.basename(historias_disponiveis)
            
            nome_final_historia = nome_das_historias.replace('*.mp3', '')
            
            print(f"\n {nome_final_historia}")

        print(f"\n>>>Diga o nome da historia que você quer ouvir:")
        
        nome_historia = Microfone()
        
        nome_historia_final = removedor_de_acento(nome_historia)
        
        N_L_P_PT(nome_historia_final, npl_pt, historias_encontradas)
    else:
        print("\nResultado: não entendi seu comando. Tente dizer 'Contar historia'.")

print("="*50)

    
    