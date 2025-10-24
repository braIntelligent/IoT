"""
main.py - API principal FastAPI del servidor
Recibe frames, procesa reconocimiento facial y gestiona asistencia
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import logging
from datetime import datetime
import uvicorn

from config import (
    SERVER_HOST, SERVER_PORT, CORS_ORIGINS, 
    COOLDOWN_SECONDS, LED_CONTROL_TIMEOUT
)
from database import db
from face_processor import face_processor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Asistencia IoT",
    description="API para reconocimiento facial y registro de asistencia",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos Pydantic
class FrameRequest(BaseModel):
    image: str  # Base64 encoded image
    device_id: str


class RegistroRequest(BaseModel):
    id_estudiante: int
    device_id: str = None


# Cache para IPs de dispositivos (evitar consultas constantes)
dispositivos_cache = {}


def enviar_comando_led(device_id: str, color: str, duration: int = 2):
    """
    Envía comando para controlar LED en la Raspberry Pi
    
    Args:
        device_id (str): ID del dispositivo
        color (str): 'green' o 'red'
        duration (int): Duración en segundos
    """
    try:
        # Obtener IP del dispositivo desde cache o BD
        if device_id not in dispositivos_cache:
            # Aquí podrías consultar BD para obtener IP
            # Por ahora, asumimos formato: device_id = "pi-aula-101" -> IP en config
            logger.warning(f"IP de {device_id} no encontrada en cache")
            return
        
        device_ip = dispositivos_cache[device_id]
        url = f"http://{device_ip}:5000/api/led"
        
        payload = {
            "color": color,
            "duration": duration
        }
        
        response = requests.post(
            url, 
            json=payload, 
            timeout=LED_CONTROL_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"✅ LED {color} activado en {device_id}")
        else:
            logger.warning(f"⚠️  Error activando LED: {response.status_code}")
            
    except requests.exceptions.Timeout:
        logger.warning(f"⏱️  Timeout al conectar con {device_id}")
    except Exception as e:
        logger.error(f"Error al enviar comando LED: {e}")


@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio - Cargar encodings y configuración
    """
    logger.info("🚀 Iniciando servidor de asistencia...")
    
    # Verificar si hay encodings cargados
    if not face_processor.encodings_loaded:
        logger.warning("⚠️  Encodings no cargados. Generando desde fotos...")
        estudiantes = db.obtener_estudiantes()
        if estudiantes:
            face_processor.generar_encodings_desde_fotos(estudiantes)
    
    logger.info("✅ Servidor listo")


@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "sistema": "Asistencia IoT v2.0",
        "estado": "activo",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "procesar_frame": "POST /api/procesar-frame",
            "estudiantes": "GET /api/estudiantes",
            "asistencia_hoy": "GET /api/asistencia/hoy",
            "registrar": "POST /api/registrar"
        }
    }


@app.post("/api/procesar-frame")
async def procesar_frame(request: FrameRequest):
    """
    Procesa un frame recibido de la Raspberry Pi
    Detecta rostros, los compara y registra asistencia
    
    Args:
        request: FrameRequest con imagen en base64 y device_id
        
    Returns:
        JSON con resultado del procesamiento
    """
    try:
        device_id = request.device_id
        
        # Registrar dispositivo en cache si no existe
        if device_id not in dispositivos_cache:
            # Extraer IP del request (para futura referencia)
            # dispositivos_cache[device_id] = request.client.host
            pass
        
        # Decodificar imagen
        img_array = face_processor.decode_image_from_base64(request.image)
        
        if img_array is None:
            raise HTTPException(status_code=400, detail="Error al decodificar imagen")
        
        # Procesar frame
        resultado = face_processor.procesar_frame(img_array)
        
        if resultado['faces_found'] == 0:
            return {
                "status": "no_face",
                "message": "No se detectaron rostros"
            }
        
        # Si hay coincidencias (matches)
        if len(resultado['matches']) > 0:
            # Tomar la primera coincidencia (podría haber múltiples personas)
            match = resultado['matches'][0]
            id_estudiante = match['id']
            nombre = match['name']
            confidence = match['confidence']
            
            # Verificar cooldown
            en_cooldown = db.verificar_cooldown(id_estudiante, COOLDOWN_SECONDS)
            
            if not en_cooldown:
                # Registrar asistencia
                registro = db.registrar_asistencia(id_estudiante, device_id)
                
                if registro['success']:
                    # Enviar comando LED verde
                    enviar_comando_led(device_id, "green", 2)
                    
                    logger.info(f"✅ Asistencia registrada: {nombre} (ID: {id_estudiante})")
                    
                    return {
                        "status": "recognized",
                        "nombre": nombre,
                        "id_estudiante": id_estudiante,
                        "confidence": confidence,
                        "registrado": True,
                        "resultado": registro['resultado']
                    }
                else:
                    logger.error(f"Error al registrar: {registro.get('error')}")
                    return {
                        "status": "error",
                        "message": "Error al registrar en BD"
                    }
            else:
                # Ya fue registrado recientemente
                logger.info(f"⏭️  {nombre} ya registrado (cooldown activo)")
                return {
                    "status": "recognized",
                    "nombre": nombre,
                    "id_estudiante": id_estudiante,
                    "confidence": confidence,
                    "registrado": False,
                    "mensaje": "Ya registrado hoy"
                }
        
        # No se reconoció ningún rostro
        enviar_comando_led(device_id, "red", 1)
        
        return {
            "status": "unknown",
            "message": "Rostro no reconocido",
            "faces_found": resultado['faces_found']
        }
        
    except Exception as e:
        logger.error(f"Error procesando frame: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/estudiantes")
async def obtener_estudiantes():
    """
    Obtiene la lista completa de estudiantes registrados
    
    Returns:
        Lista de estudiantes
    """
    try:
        estudiantes = db.obtener_estudiantes()
        return {
            "total": len(estudiantes),
            "estudiantes": estudiantes
        }
    except Exception as e:
        logger.error(f"Error obteniendo estudiantes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/asistencia/hoy")
async def obtener_asistencia_hoy():
    """
    Obtiene los registros de asistencia del día actual
    
    Returns:
        Lista de asistencias de hoy
    """
    try:
        asistencias = db.obtener_asistencia_hoy()
        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        logger.error(f"Error obteniendo asistencia: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/registrar")
async def registrar_manual(request: RegistroRequest):
    """
    Endpoint para registrar asistencia manualmente (legacy/backup)
    
    Args:
        request: RegistroRequest con id_estudiante
        
    Returns:
        Confirmación del registro
    """
    try:
        resultado = db.registrar_asistencia(
            request.id_estudiante, 
            request.device_id
        )
        
        if resultado['success']:
            estudiante = db.obtener_estudiante_por_id(request.id_estudiante)
            return {
                "success": True,
                "estudiante": estudiante,
                "resultado": resultado['resultado']
            }
        else:
            raise HTTPException(status_code=400, detail=resultado.get('error'))
            
    except Exception as e:
        logger.error(f"Error en registro manual: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recargar-encodings")
async def recargar_encodings():
    """
    Recarga los encodings desde las fotos (útil cuando se agregan nuevos estudiantes)
    
    Returns:
        Confirmación de recarga
    """
    try:
        estudiantes = db.obtener_estudiantes()
        face_processor.generar_encodings_desde_fotos(estudiantes)
        
        return {
            "success": True,
            "message": f"Encodings recargados: {len(face_processor.known_encodings)} rostros"
        }
    except Exception as e:
        logger.error(f"Error recargando encodings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "encodings_loaded": face_processor.encodings_loaded,
        "total_encodings": len(face_processor.known_encodings)
    }


# Registrar IP de dispositivos cuando envían frames
@app.middleware("http")
async def add_device_ip(request: Request, call_next):
    """Middleware para cachear IPs de dispositivos"""
    response = await call_next(request)
    
    # Si es un request de procesar-frame, cachear la IP
    if request.url.path == "/api/procesar-frame":
        try:
            device_id = request.headers.get("X-Device-ID")
            if device_id:
                client_ip = request.client.host
                dispositivos_cache[device_id] = client_ip
        except:
            pass
    
    return response


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║      SERVIDOR DE ASISTENCIA IoT - v2.0           ║
    ║        Reconocimiento Facial Centralizado        ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level="info"
    )