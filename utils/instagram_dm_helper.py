"""Ferramenta segura para analisar DMs exportadas e sugerir respostas carinhosas.

Este utilitário **não** faz login no Instagram e **não** envia mensagens automaticamente.
Ele foi desenhado para uso humano no fluxo: analisar a primeira mensagem de uma conversa
já exportada e gerar uma sugestão de resposta no estilo solicitado.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class AnalysisResult:
    participant: str
    first_message: str
    sentiment: str
    keywords: List[str]
    suggested_reply: str


POSITIVE_KEYWORDS = {"amei", "adorei", "lindo", "incrível", "maravilhoso", "gostei", "top"}
QUESTION_KEYWORDS = {"como", "quando", "onde", "pq", "por que", "porque", "?"}


def load_export(path: Path) -> List[Dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de conversas.")
    return data


def pick_random_conversation(conversations: List[Dict], seed: Optional[int] = None) -> Dict:
    if not conversations:
        raise ValueError("Nenhuma conversa encontrada no arquivo informado.")
    rng = random.Random(seed)
    return rng.choice(conversations)


def get_first_participant_message(conversation: Dict, influencer_username: str) -> str:
    messages = conversation.get("messages", [])
    if not messages:
        raise ValueError("A conversa selecionada não possui mensagens.")

    ordered = sorted(messages, key=lambda m: m.get("timestamp", 0))
    for message in ordered:
        sender = message.get("sender", "")
        text = str(message.get("text", "")).strip()
        if sender != influencer_username and text:
            return text

    raise ValueError("Não foi encontrada mensagem inicial de participante nesta conversa.")


def detect_sentiment(message: str) -> str:
    lowered = message.lower()
    if any(word in lowered for word in POSITIVE_KEYWORDS):
        return "positivo"
    if any(word in lowered for word in QUESTION_KEYWORDS):
        return "curioso"
    return "neutro"


def extract_keywords(message: str) -> List[str]:
    tokens = [t.strip(".,!?:;()[]{}\"'").lower() for t in message.split()]
    tokens = [t for t in tokens if len(t) > 3]
    return tokens[:5]


def build_caring_reply(first_message: str, sentiment: str) -> str:
    if sentiment == "positivo":
        opener = "Oii, meu bem! Fiquei muito feliz com sua mensagem 💖"
    elif sentiment == "curioso":
        opener = "Oii, meu amor! Amei sua pergunta e adorei te ver por aqui ✨"
    else:
        opener = "Oii, lindona! Obrigada por me escrever com tanto carinho 💕"

    hook = (
        "Me conta uma coisa: qual tipo de conteúdo você quer ver mais por aqui? "
        "Quero preparar os próximos posts pensando em você 😘"
    )
    return f"{opener}\n\nSobre o que você falou: \"{first_message}\"\n{hook}"


def analyze_and_suggest(conversations: List[Dict], influencer_username: str, seed: Optional[int] = None) -> AnalysisResult:
    conversation = pick_random_conversation(conversations, seed=seed)
    participant = conversation.get("participant", "participante")
    first_message = get_first_participant_message(conversation, influencer_username)
    sentiment = detect_sentiment(first_message)
    keywords = extract_keywords(first_message)
    suggested_reply = build_caring_reply(first_message, sentiment)

    return AnalysisResult(
        participant=participant,
        first_message=first_message,
        sentiment=sentiment,
        keywords=keywords,
        suggested_reply=suggested_reply,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analisa a primeira mensagem de uma conversa exportada e gera "
            "uma resposta carinhosa para revisão humana."
        )
    )
    parser.add_argument("--input", required=True, type=Path, help="JSON com lista de conversas.")
    parser.add_argument("--influencer", required=True, help="Username da influenciadora no histórico.")
    parser.add_argument("--seed", type=int, default=None, help="Semente para seleção aleatória reproduzível.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    conversations = load_export(args.input)
    result = analyze_and_suggest(conversations, args.influencer, seed=args.seed)

    print(f"Participante escolhido: {result.participant}")
    print(f"Primeira mensagem: {result.first_message}")
    print(f"Sentimento detectado: {result.sentiment}")
    print(f"Palavras-chave: {', '.join(result.keywords) if result.keywords else '(nenhuma)'}")
    print("\nSugestão de resposta:\n")
    print(result.suggested_reply)


if __name__ == "__main__":
    main()
