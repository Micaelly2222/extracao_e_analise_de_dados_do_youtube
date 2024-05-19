# Importação das bibliotecas necessárias
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from getpass import getpass
import pandas as pd
from loguru import logger
from tabulate import tabulate

# 1. Acesse a API do YouTube e utilizando um script Python, traga as seguintes informações:

# a) Informações de um canal específico à sua escolha:
# - id do canal;
# - título do canal;
# - descrição;
# - viewCount;
# - subscriberCount;
# - videoCount.

# Solicitando ao usuário para inserir a chave de API do YouTube usando getpass
API_KEY = getpass("Por favor, insira sua chave de API do YouTube: ")

# Solicitando ao usuário para inserir o link do canal
channel_link = input("Por favor, insira o link do canal do YouTube: ")

# Extraindo o ID do canal a partir do link
channel_id = channel_link.split('/')[-1]
logger.info(f'ID do Canal: {channel_id}')  # Log do ID do canal

# Criando o objeto da API do YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Criando uma lista para armazenar as informações do canal
channel_info_list = []

try:
    # Fazendo uma solicitação para obter as informações do canal
    channel_response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()

    # Obtendo as informações do canal
    channel_info = channel_response['items'][0]
    channel_title = channel_info['snippet']['title']
    channel_description = channel_info['snippet']['description']
    view_count = channel_info['statistics']['viewCount']
    subscriber_count = channel_info['statistics']['subscriberCount']
    video_count = channel_info['statistics']['videoCount']

    # Adicionando as informações do canal à lista
    channel_info_list.append({
        'id': channel_id,
        'title': channel_title,
        'description': channel_description,
        'viewCount': view_count,
        'subscriberCount': subscriber_count,
        'videoCount': video_count
    })

except HttpError as e:
    logger.exception('Ocorreu um erro ao acessar a API do YouTube: {e}')
    exit(1)
except KeyError:
    logger.exception('O canal especificado não foi encontrado ou não possui informações públicas.')
    exit(1)

# Criando um DataFrame com as informações do canal
channel_df = pd.DataFrame(channel_info_list)
logger.info(f'Informações do Canal:\n{tabulate(channel_df, headers="keys", tablefmt="psql")}')

# b) Informações de 10 vídeos deste mesmo canal:
# - id do vídeo;
# - título do vídeo;
# - duration;
# - viewCount;
# - likeCount;
# - favoriteCount;
# - commentCount.

# Criando uma lista para armazenar as informações dos vídeos
videos_info_list = []

try:
    # Fazendo uma solicitação para obter os vídeos do canal
    videos_response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=10,  # Limitando a 10 vídeos
        order='date',  # Obtendo os vídeos mais recentes
        type='video'
    ).execute()

    # Para cada vídeo, obtendo suas informações
    for video in videos_response['items']:
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']

        # Fazendo uma solicitação adicional para obter estatísticas do vídeo
        video_stats_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=video_id
        ).execute()

        # Extraindo as estatísticas do vídeo
        video_stats = video_stats_response['items'][0]['statistics']
        video_content_details = video_stats_response['items'][0]['contentDetails']

        # Adicionando as informações do vídeo à lista
        video_info = {
            'id': video_id,
            'title': video_title,
            'duration': video_content_details['duration'],
            'viewCount': video_stats.get('viewCount', 0),
            'likeCount': video_stats.get('likeCount', 0),
            'favoriteCount': video_stats.get('favoriteCount', 0),
            'commentCount': video_stats.get('commentCount', 0)
        }
        videos_info_list.append(video_info)

except HttpError as e:
    logger.exception('Ocorreu um erro ao acessar a API do YouTube: {e}')
    exit(1)
except KeyError:
    logger.exception('O canal especificado não foi encontrado ou não possui informações públicas.')
    exit(1)

# Criando um DataFrame com as informações dos vídeos
videos_df = pd.DataFrame(videos_info_list)

# Realizando tratamentos necessários, convertendo a duração para um formato mais legível
videos_df['duration'] = pd.to_timedelta(videos_df['duration'])

# Exportando o DataFrame para um arquivo CSV
videos_df.to_csv('videos_info.csv', index=False)
logger.info(f'Informações dos Vídeos:\n{tabulate(videos_df, headers="keys", tablefmt="psql")}')

# 2. Transforme os dados recebidos na etapa anterior em uma única tabela, realize tratamentos que julgar necessários e exporte um arquivo ".csv".
# Realizando uma junção entre as informações do canal e dos vídeos em uma única tabela usando um join SQL

combined_df = pd.merge(channel_df.assign(key=1), videos_df.assign(key=1), on='key').drop('key', axis=1)

# Exportando o DataFrame combinado para um arquivo CSV
combined_df.to_csv('combined_info.csv', index=False)
logger.info(f'Tabela Combinada:\n{tabulate(combined_df, headers="keys", tablefmt="psql")}')
