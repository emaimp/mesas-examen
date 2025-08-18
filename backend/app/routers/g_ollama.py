from app import schemas, core, models
from ollama import chat
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(tags=["Chat BOT"])

# Caché en memoria para el historial de chat
chat_history_cache = {} # La clave es el ID del usuario, el valor es una lista de mensajes

#
# Endpoint: Interactua con el modelo Ollama
#
@router.post("/ollama/chat", response_model=schemas.MessageResponse)
async def ollama_chat(
    request: schemas.MessageRequest,
    current_user: Annotated[models.Usuarios, Depends(core.get_current_user)]
):
    # Recibe un mensaje del usuario y devuelve la respuesta del modelo
    try:
        user_id = current_user.id
        # Obtener el historial de chat para el usuario actual
        messages = chat_history_cache.get(user_id, []) # Si no existe, inicializa una lista vacía
        # Añadir el mensaje actual del usuario al historial
        messages.append({'role': 'user', 'content': request.message})
        # Llamar al modelo Ollama con el historial completo
        response = chat(model='qwen3:0.6b', messages=messages, think=False)
        # Añadir la respuesta del modelo al historial
        messages.append({'role': 'assistant', 'content': response['message']['content']})
        # Actualizar el caché con el historial modificado
        chat_history_cache[user_id] = messages

        return schemas.MessageResponse(response=response['message']['content']) # Devuelve la respuesta del modelo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Ollama chat: {e}") # Maneja cualquier error

#
# Endpoint: Limpia el historial de chat para el usuario actual
#
@router.delete("/ollama/chat/history")
async def clear_ollama_chat_history(
    current_user: Annotated[models.Usuarios, Depends(core.get_current_user)]
):
    user_id = current_user.id
    if user_id in chat_history_cache:
        del chat_history_cache[user_id]
    # Siempre devuelve un 200 OK, incluso si no hay historial que limpiar.
    # Esto evita que el frontend reciba un 404 y muestre un error en consola.
    return {"message": "Solicitud de limpieza de historial procesada."}
