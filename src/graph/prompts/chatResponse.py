from pydantic import BaseModel
from typing import Optional, List
import json


class JobIntentSchema(BaseModel):
    role: Optional[str] = None
    location: Optional[str] = None
    seniority: Optional[str] = None
    preferred_companies: Optional[List[str]] = None
    remote: Optional[bool] = None
    key_preferences: str
    important_context: Optional[str] = None


class ChatResponseSchema(BaseModel):
    message: str
    preferences: Optional[JobIntentSchema] = None
    shouldSavePreferences: bool
    shouldSearchJobs: bool


def get_system_prompt(user_context, jobs):

    return json.dumps({
        "role": "Job Search Assistant (Search + Matching Engine)",

        "task": (
            "Você responde mensagens e executa busca de vagas. "
            "Você recebe uma lista de vagas retornadas por uma API. "
            "Você deve analisar essas vagas e responder com base nelas."
        ),

        "user_context": user_context if user_context else "first message",

        "behavior_rules": [
            "Nunca diga apenas que vai procurar vagas; sempre execute ou finalize a análise",
            "Se o usuário fornecer cargo, isso deve gerar shouldSearchJobs = true",
            "Se a lista de vagas estiver vazia, tente interpretar o cargo em inglês e considere isso no raciocínio",
            "Se após considerar equivalência em inglês ainda não houver vagas, retorne mensagem informando que não foram encontradas vagas e finalize o fluxo",
            "Não fique em loop de tentativa de busca",
            "Responda sempre em português"
        ],

        "search_strategy": {
            "language_normalization": [
                "Converta cargos do português para inglês antes de interpretar resultados",
                "Ex: cientista de dados → data scientist",
                "engenheiro de dados → data engineer",
                "desenvolvedor → software engineer"
            ],

            "empty_results_policy": [
                "Se jobs estiver vazio, tente reinterpretar o cargo em inglês",
                "Se continuar vazio, finalize e informe ausência de vagas",
                "Não solicitar nova busca automaticamente"
            ]
        },

        "jobs": jobs,

        "fields_to_extract": {
            "role": "Preferred job role",
            "location": "Preferred work location",
            "seniority": "Preferred seniority level",
            "preferred_companies": "Companies mentioned positively",
            "remote": "Whether user prefers remote work",
            "key_preferences": "Concise summary of job goals",
            "important_context": "Extra professional context"
        }
    }, indent=2)


def get_user_prompt(conversation_history, question, previous_summary=None):

    return json.dumps({
        "conversation": "\n".join(
            f"{msg.__class__.__name__}: {msg.content}"
            for msg in conversation_history
        ),

        "user_message": question,

        "previous_summary": previous_summary or "None",

        "instructions": [
            "Analise intenção de carreira como ação ativa de busca de vagas",
            "Se houver cargo + senioridade + modalidade, defina shouldSearchJobs = true",
            "Se jobs estiver vazio, tente interpretar o cargo em inglês antes de concluir",
            "Se mesmo assim não houver vagas, finalize a resposta sem nova tentativa de busca",
            "Nunca entre em loop de busca repetida",
            "Retorne apenas JSON estruturado"
        ]
    }, indent=2)