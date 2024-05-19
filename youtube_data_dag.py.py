from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from teste_eng_de_dados import main_process  # Importa a função principal do script teste_eng_de_dados.py

# Definição dos argumentos padrão da DAG
default_args = {
    'owner': 'airflow',  # Proprietário da DAG
    'depends_on_past': False,  # Define se a execução depende do sucesso das execuções anteriores
    'start_date': datetime(2024, 5, 17),  # Data de início da DAG
    'email_on_failure': False,  
    'email_on_retry': False,  
    'retries': 1,  # Número de tentativas em caso de falha
    'retry_delay': timedelta(minutes=5),  # Intervalo entre as tentativas em caso de falha
}

# Definição da DAG
dag = DAG(
    'youtube_data_extraction',  # Nome da DAG
    default_args=default_args,  # Argumentos padrão
    description='DAG para extração de dados do YouTube e processamento',  # Descrição da DAG
    schedule_interval='30 1 * * *',  # Executar diariamente às 01:30 AM
    catchup=False,  # Evitar a execução de tarefas para o período antes da data de início
)

# Definição das tarefas
extract_youtube_data_task = PythonOperator(
    task_id='extract_youtube_data',  # Identificador da tarefa
    python_callable=main_process,  # Função a ser executada pela tarefa (função principal do script teste_eng_de_dados.py)
    dag=dag,  # Referência à DAG
)

# Configurando a ordem das tarefas
extract_youtube_data_task

if __name__ == "__main__":
    dag.cli()  # Permite executar a DAG a partir da linha de comando
