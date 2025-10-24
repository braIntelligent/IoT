"""
captura_cliente.py - Cliente de captura de video para Raspberry Pi
Captura frames y los envía al servidor para procesamiento
"""

import time
import base64
import requests
import io
from picamera2 import Picamera2
from PIL import Image
from config import (
    SERVER_URL, DEVICE_ID, FRAME_WIDTH, FRAME_HEIGHT,
    CAPTURE_INTERVAL, JPEG_QUALITY, REQUEST_TIMEOUT
)

class CapturaCliente:
    def __init__(self):
        """Inicializar cámara y configuración"""
        print("🎥 Inicializando cámara...")
        self.camera = Picamera2()
        
        # Configurar cámara
        config = self.camera.create_preview_configuration(
            main={"size": (FRAME_WIDTH, FRAME_HEIGHT)}
        )
        self.camera.configure(config)
        self.camera.start()
        
        # Esperar a que la cámara se estabilice
        time.sleep(2)
        
        self.server_url = f"{SERVER_URL}/api/procesar-frame"
        self.device_id = DEVICE_ID
        
        print(f"✅ Cámara inicializada: {FRAME_WIDTH}x{FRAME_HEIGHT}")
        print(f"🌐 Servidor: {SERVER_URL}")
        print(f"🔖 Device ID: {DEVICE_ID}")
        
    def capturar_frame(self):
        """
        Captura un frame de la cámara y lo convierte a JPEG base64
        
        Returns:
            str: Frame en formato base64
        """
        try:
            # Capturar frame
            frame = self.camera.capture_array()
            
            # Convertir a PIL Image
            img = Image.fromarray(frame)
            
            # Comprimir a JPEG en memoria
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=JPEG_QUALITY)
            buffer.seek(0)
            
            # Convertir a base64
            img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            print(f"❌ Error al capturar frame: {e}")
            return None
    
    def enviar_frame(self, img_base64):
        """
        Envía el frame al servidor para procesamiento
        
        Args:
            img_base64 (str): Frame en base64
            
        Returns:
            dict: Respuesta del servidor
        """
        try:
            payload = {
                "image": img_base64,
                "device_id": self.device_id
            }
            
            headers = {
                "Content-Type": "application/json",
                "X-Device-ID": self.device_id
            }
            
            response = requests.post(
                self.server_url,
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️  Servidor respondió con código: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("⏱️  Timeout al conectar con servidor")
            return None
        except requests.exceptions.ConnectionError:
            print("🔌 Error de conexión con servidor")
            return None
        except Exception as e:
            print(f"❌ Error al enviar frame: {e}")
            return None
    
    def procesar_respuesta(self, respuesta):
        """
        Procesa la respuesta del servidor y muestra información
        
        Args:
            respuesta (dict): Respuesta del servidor
        """
        if not respuesta:
            return
        
        status = respuesta.get('status')
        
        if status == 'recognized':
            nombre = respuesta.get('nombre', 'Desconocido')
            print(f"✅ RECONOCIDO: {nombre}")
            
        elif status == 'unknown':
            print("❌ ROSTRO NO RECONOCIDO")
            
        elif status == 'no_face':
            # No imprimir nada para evitar spam
            pass
            
        else:
            print(f"⚠️  Respuesta inesperada: {respuesta}")
    
    def run(self):
        """
        Bucle principal de captura y envío
        """
        print("\n" + "="*50)
        print("🚀 INICIANDO CAPTURA Y TRANSMISIÓN")
        print("="*50 + "\n")
        
        frame_count = 0
        
        try:
            while True:
                # Capturar frame
                img_base64 = self.capturar_frame()
                
                if img_base64:
                    frame_count += 1
                    
                    # Enviar al servidor
                    respuesta = self.enviar_frame(img_base64)
                    
                    # Procesar respuesta
                    self.procesar_respuesta(respuesta)
                    
                    # Mostrar contador cada 10 frames
                    if frame_count % 10 == 0:
                        print(f"📊 Frames procesados: {frame_count}")
                
                # Esperar antes del siguiente frame
                time.sleep(CAPTURE_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n⚠️  Deteniendo captura...")
            self.cleanup()
    
    def cleanup(self):
        """
        Limpieza al cerrar
        """
        print("🧹 Liberando recursos...")
        self.camera.stop()
        self.camera.close()
        print("✅ Cámara cerrada correctamente")


def main():
    """
    Función principal
    """
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║   SISTEMA DE ASISTENCIA - CLIENTE RASPBERRY PI    ║
    ║              Captura y Transmisión                ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    try:
        cliente = CapturaCliente()
        cliente.run()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()