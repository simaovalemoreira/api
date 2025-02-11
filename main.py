from fastapi import FastAPI
import pandas as pd
from faker import Faker
import random
from fastapi.responses import FileResponse

app = FastAPI()
fake = Faker("pt_BR")

# Função para gerar os dados fictícios
def gerar_dados():
    # 1. Pacientes
    pacientes = pd.DataFrame({
        "ID_Paciente": range(1, 21),
        "Nome": [fake.name() for _ in range(20)],
        "Idade": [random.randint(18, 80) for _ in range(20)],
        "Gênero": [random.choice(["Masculino", "Feminino"]) for _ in range(20)],
        "Data_Consulta": pd.date_range(start="2024-01-01", periods=20, freq="D")
    })

    # 2. Atendimentos
    atendimentos = pd.DataFrame({
        "ID_Paciente": range(1, 21),
        "Especialidade": random.choices(["Cardiologia", "Ortopedia", "Pediatria", "Clínica Geral", "Dermatologia"], k=20),
        "Médico_Responsável": random.choices(["Dr. A", "Dr. B", "Dr. C", "Dr. D", "Dr. E"], k=20),
        "Tempo_Espera_Min": [random.randint(5, 30) for _ in range(20)],
        "Duração_Atendimento_Min": [random.randint(15, 60) for _ in range(20)]
    })

    # 3. Financeiro
    financeiro = pd.DataFrame({
        "Data": pd.date_range(start="2024-01-01", periods=20, freq="D"),
        "Receita": [random.randint(1000, 5000) for _ in range(20)],
        "Despesas": [random.randint(500, 3000) for _ in range(20)]
    })
    financeiro["Lucro"] = financeiro["Receita"] - financeiro["Despesas"]

    # 4. Satisfação do Paciente
    satisfacao = pd.DataFrame({
        "ID_Paciente": range(1, 21),
        "NPS": [random.randint(1, 10) for _ in range(20)],
        "Feedback": random.choices(["Ótimo", "Bom", "Regular", "Ruim", "Péssimo"], k=20)
    })

    # Salvar em Excel
    caminho_arquivo = "healthdata_insights.xlsx"
    with pd.ExcelWriter(caminho_arquivo) as writer:
        pacientes.to_excel(writer, sheet_name="Pacientes", index=False)
        atendimentos.to_excel(writer, sheet_name="Atendimentos", index=False)
        financeiro.to_excel(writer, sheet_name="Financeiro", index=False)
        satisfacao.to_excel(writer, sheet_name="Satisfação", index=False)
    
    return caminho_arquivo

# Endpoint para gerar e baixar o arquivo
@app.get("/gerar-dados")
def gerar_dados_excel():
    arquivo = gerar_dados()
    return FileResponse(arquivo, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="healthdata_insights.xlsx")

# Endpoint de teste
@app.get("/")
def root():
    return {"message": "API de Geração de Dados para Saúde - Acesse /gerar-dados para baixar o Excel"}
