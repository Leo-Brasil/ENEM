import requests
import streamlit as st
import json
import time
import pandas as pd
import os

def clean_question(question):
    if not isinstance(question, dict):
        return None

    # Extrair e limpar os campos context e alternativesIntroduction
    context_raw = str(question.get("context", "")).replace("\n", " ").strip()
    intro_raw = str(question.get("alternativesIntroduction", "")).replace("\n", " ").strip()
    
    cleaned_question = {
        "title": str(question.get("title", "")).replace("\n", " ").strip(),
        "index": question.get("index"),
        "discipline": str(question.get("discipline", "")).replace("\n", " ").strip(),
        "linguagem": question.get("language"),
        "year": question.get("year"),
        "conteudoSuporte": str(question.get("context", "")).replace("\n", " ").strip(),
        "comando": str(question.get("alternativesIntroduction", "")).replace("\n", " ").strip(),
        "correctAlternative": question.get("correctAlternative"),
        "alternativas": []
    }

    for alt in question.get("alternatives", []):
        cleaned_alt = {
            "letter": alt.get("letter"),
            "text": str(alt.get("text", "")).replace("\n", " ").strip(),
            "isCorrect": alt.get("isCorrect")
        }
        cleaned_question["alternativas"].append(cleaned_alt)

    return cleaned_question

def fetch_questions_by_year(year):
    base_url = f'https://api.enem.dev/v1/exams/{year}/questions'
    limit = 50
    offset = 0
    questions = []
    url = f'{base_url}?limit={limit}&offset={offset}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'questions' in data:
            questions = data['questions']
    return questions

def process_years(year, formato):
    questions = fetch_questions_by_year(year)
    cleaned = [clean_question(q) for q in questions if isinstance(q, dict)]
    if cleaned:
        for question in cleaned:
            # Expand alternatives into separate columns
            for i, alt in enumerate(question.get("alternativas", [])):
                question[f"alternative_{alt['letter']}"] = alt["text"]
            # Remove the original 'alternativas' key
            question.pop("alternativas", None)

            # Clean and convert conteudoSuporte to hyperlink if it contains a URL
            conteudo_suporte = question.get("conteudoSuporte", "")
            if "![](" in conteudo_suporte:  # Remove markdown image syntax
                conteudo_suporte = conteudo_suporte.split("![](")[-1].split(")")[0].strip()
            if conteudo_suporte.startswith("http"):
                question["conteudoSuporte"] = f"[Clique aqui]({conteudo_suporte})"
            else:
                question["conteudoSuporte"] = conteudo_suporte

        if formato == 'JSON':
            st.subheader(f'Questões do ENEM {year}')
            with st.container():
                st.code(json.dumps(cleaned, ensure_ascii=False, indent=4), language="json")
        else:
            st.subheader(f'Prévia das questões do ENEM {year}')
            st.write('Prévia dos 25 primeiros resultados')
            preview_df = pd.DataFrame(cleaned).head(25)

            # Rename columns to Portuguese
            column_mapping = {
                "title": "Título",
                "index": "Questão",
                "discipline": "Disciplina",
                "linguagem": "Linguagem",
                "year": "Ano",
                "conteudoSuporte": "Conteudo Suporte",
                "comando": "Comando",
                "correctAlternative": "Alternativa Correta",
                "alternative_A": "Alternativa A",
                "alternative_B": "Alternativa B",
                "alternative_C": "Alternativa C",
                "alternative_D": "Alternativa D",
                "alternative_E": "Alternativa E"
            }
            preview_df.rename(columns=column_mapping, inplace=True)

            # Use st.markdown to render clickable links in the dataframe preview
            preview_df["Conteudo Suporte"] = preview_df["Conteudo Suporte"].apply(
                lambda x: f'<a href="{x.split("(")[-1].split(")")[0]}" target="_blank">{x}</a>' if x.startswith("[Clique aqui]") else x
            )
            # Generate HTML with smaller font size and centered headers
            styled_html = preview_df.to_html(
                escape=False, index=False, classes="table table-bordered table-hover"
            )
            styled_html = styled_html.replace(
                "<thead>",
                '<thead style="text-align: center; font-size: 14px;">'
            )
            styled_html = styled_html.replace(
                "<th>",
                '<th style="text-align: center; font-size: 14px;">'
            )
            styled_html = styled_html.replace(
                "<td>",
                '<td style="font-size: 14px;">'
            )
            st.write(styled_html, unsafe_allow_html=True)
    else:
        st.warning(f"Nenhuma questão encontrada para o ano {year}.")

def exportar(year, formato):
    questions = fetch_questions_by_year(year)
    cleaned = [clean_question(q) for q in questions if isinstance(q, dict)]
    if cleaned:
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        if formato == 'JSON':
            file_path = os.path.join(download_folder, f"enem{year}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(cleaned, f, ensure_ascii=False, indent=4)
            st.success(f"Arquivo salvo com sucesso em: {file_path}")
        else:
            file_path = os.path.join(download_folder, f"enem{year}.csv")
            df = pd.DataFrame(cleaned)
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            st.success(f"Arquivo salvo com sucesso em: {file_path}")
    else:
        st.warning(f"Nenhuma questão encontrada para o ano {year}.")