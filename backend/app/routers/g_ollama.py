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
        user_id = current_user.id # Obtiene el ID del usuario actual
        # Obtener el historial de chat para el usuario actual
        messages = chat_history_cache.get(user_id, []) # Si no existe, inicializa una lista vacía

        # Si es la primera interacción del usuario en esta sesión
        if not messages:
            # Mensaje de sistema para instruir al modelo a responder en español
            messages.append({'role': 'system', 'content': 'Responde siempre en español.'})
            # Añadir el mensaje del usuario al historial
            messages.append({'role': 'user', 'content': request.message})
            # La primera respuesta es siempre el mensaje por defecto
            final_response = core.DEFAULT_CHAT_RESPONSE
            messages.append({'role': 'assistant', 'content': final_response}) # Añade la respuesta por defecto al historial
            chat_history_cache[user_id] = messages # Actualiza el caché con el historial modificado
            return schemas.MessageResponse(response=final_response) # Devuelve la respuesta por defecto
        else:
            # Para interacciones posteriores, añadir el mensaje del usuario y llamar al modelo Ollama
            messages.append({'role': 'user', 'content': request.message}) # Añade el mensaje actual del usuario al historial
            response = chat(model='qwen3:0.6b', messages=messages, think=False) # Llama al modelo Ollama con el historial completo
            model_response_content = response['message']['content'] # Extrae el contenido de la respuesta del modelo

            # Lógica para usar el mensaje por defecto si la respuesta del modelo es inválida
            if not model_response_content or len(model_response_content.strip()) < 5: # Verifica si la respuesta del modelo es vacía o muy corta
                final_response = core.DEFAULT_CHAT_RESPONSE # Usa el mensaje por defecto
            else:
                final_response = model_response_content # Usa la respuesta del modelo

            messages.append({'role': 'assistant', 'content': final_response}) # Añade la respuesta (del modelo o por defecto) al historial
            chat_history_cache[user_id] = messages # Actualiza el caché con el historial modificado
            return schemas.MessageResponse(response=final_response) # Devuelve la respuesta final
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Ollama chat: {e}") # Maneja cualquier error y devuelve un error HTTP 500

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
