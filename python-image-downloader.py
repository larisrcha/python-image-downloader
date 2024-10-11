import requests
from bs4 import BeautifulSoup
import os

def imagedown(url, folder):
    
    # Cria a pasta para salvar as imagens, se ela não existir
    try:
        os.mkdir(folder) # Cria a pasta `folder`
    except FileExistsError:
        pass # Ignora o erro caso a pasta já exista
    
    # Faz uma requisição GET para a página web
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Encontra todas as tags `<img>` na página
    images = soup.find_all('img')


    for image in images:
        name = image.get('alt','image')
        link = image.get('src')

        # Verifica se o atributo `src` existe (algumas tags `<img>` podem não ter esse atributo)
        if not link: 
            continue
        extension = os.path.splitext(link)[1] or '.img'
        filename = f"{name.replace(' ', '-').replace('/', '')} {extension}"
        filepath = os.path.join(folder, filename)
      
        # Tenta baixar a imagem
        try:
            response = requests.get(link, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

                print(f'Downloaded: {filename}')
            else:
                print(f'Error downloading {link} (Status Code: {response.status_code})')
        except Exception as e:  
            print(f'Error downloading {link}: {e}')

# Editar o link da página e o nome da pasta - Exemplo de uso:
imagedown('https://seu-novo-link.com/pagina-com-imagens', 'NovaPastaParaAsImagens')