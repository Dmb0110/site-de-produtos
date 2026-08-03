from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, jsonify, request


def gerar_token(usuario_id: int, validade_horas: int = 1) -> str:
    """Gera um token JWT para o usuario informado."""
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(hours=validade_horas),
    }
    return jwt.encode(payload, _obter_chave_secreta(), algorithm="HS256")


def decodificar_token(token: str) -> dict:
    """Valida e decodifica um token JWT."""
    return jwt.decode(token, _obter_chave_secreta(), algorithms=["HS256"])


def exigir_token(funcao):
    """Protege uma rota exigindo um token Bearer valido."""
    @wraps(funcao)
    def decorada(*args, **kwargs):
        cabecalho = request.headers.get("Authorization", "")
        partes = cabecalho.split()

        if len(partes) != 2 or partes[0].lower() != "bearer":
            return jsonify({"erro": "Token Bearer nao informado"}), 401

        try:
            payload = decodificar_token(partes[1])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token invalido"}), 401

        return funcao(*args, usuario_id=payload["sub"], **kwargs)

    return decorada


def _obter_chave_secreta() -> str:
    chave = current_app.config.get("JWT_SECRET_KEY") or current_app.config.get("SECRET_KEY")
    if not chave:
        raise RuntimeError("Configure SECRET_KEY ou JWT_SECRET_KEY na aplicacao Flask.")
    return chave
