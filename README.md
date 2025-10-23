# ENEM – Projeto Experimental

Este é um projeto **experimental** em constante evolução, com foco em funcionalidades voltadas para o ENEM. Atualmente, ele possui **duas páginas principais**:

- Uma página dedicada ao conteúdo e informações sobre o ENEM.
- Uma página de análise exploratória em construção.

## Sobre os dados

Os microdados originais do ENEM 2023 possuem mais de **1.6 GB**, o que ultrapassa o limite de 100 MB imposto pelo GitHub. Por esse motivo, optei por utilizar **apenas uma amostra dos dados** neste repositório.

Além disso:

- Não quis utilizar meu Google Drive para hospedagem externa.
- Este projeto é de caráter pessoal, então não tenho acesso a serviços como **Amazon S3** ou **Azure Data Lake Storage (ADLS)**.
- A amostra foi gerada por meio de uma **redução proporcional e aleatória**, mantendo a representatividade dos dados originais com base em variáveis como sexo e região.

Os arquivos originais foram excluídos do repositório e adicionados ao `.gitignore`.

Caso deseje reproduzir o projeto com os dados completos, você pode baixar os microdados diretamente do [site do INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem/microdados) e gerar sua própria amostra.

---

## Tentativa com arquivo ZIP

Como alternativa para contornar o limite de 100 MB imposto pelo GitHub, realizei uma compressão dos dados em um arquivo `dados_reduzidos.zip`, contendo o CSV com mais registros do ENEM 2023.

- ✅ Consegui subir o `.zip` para o GitHub com sucesso.
- ✅ A aplicação funcionou perfeitamente em ambiente local (localhost), lendo diretamente o CSV de dentro do `.zip`.
- ❌ No entanto, ao publicar no **Streamlit Cloud**, a aplicação apresentou erro ao tentar acessar o arquivo compactado.

Essa tentativa foi válida e permitiu manter uma amostra mais robusta dos dados no repositório. Para evitar problemas de compatibilidade com o Streamlit Cloud, optei por manter uma versão reduzida e descompactada dos dados no projeto.

---

## Análise complementar em Jupyter Notebook

Além da aplicação em Streamlit, este projeto também conta com uma análise exploratória realizada em Python via Jupyter Notebook. O notebook inclui:

- Tratamento e limpeza dos microdados originais
- Redução proporcional da base de dados
- Visualizações com Seaborn e Matplotlib
- Testes e validações antes da integração com o Streamlit

Você pode encontrar o notebook na pasta raiz do projeto com o nome `microdados.ipynb`. Ele serve como apoio técnico e documentação do processo de preparação dos dados.

## Como rodar localmente

Para executar o projeto na sua máquina local, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/Leo-Brasil/ENEM.git
   cd ENEM

2. Instale as dependências:
    pip install -r requirements.txt

3. Execute o aplicativo:
    streamlit run app.py

Certifique-se de estar com o Python instalado e configurado corretamente no seu ambiente.

Status do Projeto: Em desenvolvimento
Última atualização: Outubro de 2025
Versão inicial com estrutura básica e teste

Caso queira ver como o projeto ficou, acesse:
https://estudoenem.streamlit.app/

Licença: Este projeto está licenciado sob a MIT License.

Autor
Leonardo Brasil
GitHub: @Leo-Brasil