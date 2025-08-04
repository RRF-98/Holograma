import speech_recognition as mic
import spacy 
from gtts import gTTS as voz
from playsound import playsound 
import os
import glob
import time

#Para caso o ambiente virtual não leia pelo powershell use esse comando "Python: Select Interpreter" em português

def captura_e_reconhece_fala(): 
    
    gravador = mic.Recognizer()
    
    
    with mic.Microphone() as source:
       
        gravador.adjust_for_ambient_noise(source, duration=1)
        
        print("Ouvindo... Por favor, fale alguma coisa.")
        
        try:
           
            audio = gravador.listen(source, timeout=5)
            
            
            print("Processando...")
            texto = gravador.recognize_google(audio, language='pt-BR')
            
            print(f"Texto reconhecido: {texto}")
            
            
            return texto
            
        
        except mic.UnknownValueError:
            print("Não foi possível entender o áudio.")
            return None 
        except mic.RequestError:
            print("Falha na conexão com o serviço do Google.")
            return None 
        except mic.WaitTimeoutError:
            print("Nenhuma fala detectada. Tempo esgotado.")
            return None 

caminho_do_arquivo = 'olograma/musica'
buscar_arquivo = os.path.join(caminho_do_arquivo, '*.mp3')
arquivos_de_musica_encontrados = glob.glob(buscar_arquivo)


def analize_e_resposta(Texto_principal, npl, Arquivos_Musica):
    if not Texto_principal:
        print(">>>Nenhum texto foi encontrado")

    print("\nAnalisando texto com NPL")
    doc = npl(Texto_principal)
    lemas = [token.lemma_ for token in doc]
    for caminho_do_arquivo in Arquivos_Musica:
        nome_do_arquivo = os.path.basename(caminho_do_arquivo)
        nome_final = nome_do_arquivo.replace('.mp3', '').lower() 
        if Texto_principal in nome_final:
            print(f"\n>>> Música encontrada! Tocando: '{nome_do_arquivo}'...")
            try: 
                playsound(caminho_do_arquivo)    
                print(">>>A musica terminou")
            except Exception as e:
                print(f"ERRO: Problema ao tocar o arquivo de som: {e}")
                return
    print(f"\nResultado: Não encontrei uma música com o nome '{Texto_principal}'.")
    print("Verifique se o nome está correto.")
    
       

print("\nCarregando modelo de PLN...")
npl = spacy.load("pt_core_news_lg")
print("Modelo carregado. Assistente pronto.")

if not arquivos_de_musica_encontrados:
    print("\nAVISO: Nenhum arquivo de música .mp3 foi encontrado na pasta 'olograma/musica'.")
    print("Por favor, adicione músicas à pasta para usar a função de tocar.")

while True:
    print("="*30)
    print("Aguardando seu comando (diga 'tocar música' ou 'sair')...")
    comando_usuario = captura_e_reconhece_fala()
    if not comando_usuario:
        continue
    if 'sair' in comando_usuario:
        print("Encerrando o assistente. Até mais!")
        break # Encerra o laço while

    doc = npl(comando_usuario)
    lemas = [token.lemma_ for token in doc]
    palavras_chave_musica = ["tocar", "ouvir", "escutar", "música", "canção", "som"]
    if any(palavra in lemas for palavra in palavras_chave_musica):
        if not arquivos_de_musica_encontrados:
            print("Não posso tocar músicas porque não encontrei nenhum arquivo .mp3.")
            continue

        print("\n--- Músicas Disponíveis ---")
        # Mostra ao usuário as músicas que ele pode escolher
        for caminho_do_arquivo in arquivos_de_musica_encontrados:
            nome_do_arquivo = os.path.basename(caminho_do_arquivo)
            nome_final = nome_do_arquivo.replace('.mp3', '')
            print(f"- {nome_final}")

        print("\nDiga o nome da música que você quer ouvir:")
        nome_da_musica_falado = captura_e_reconhece_fala()
        
        # Chama a função para encontrar e tocar a música solicitada
        analize_e_resposta(nome_da_musica_falado, npl, arquivos_de_musica_encontrados)
    else:
        print("\nResultado: não entendi seu comando. Tente dizer 'tocar música'.")