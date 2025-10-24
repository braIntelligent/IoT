"""
generate_encodings.py - Script para generar encodings desde fotos
Ejecutar este script después de agregar fotos a la carpeta fotos_conocidas/
"""

import os
import sys
from face_processor import face_processor
from database import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║       GENERADOR DE ENCODINGS FACIALES             ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    # Obtener estudiantes de la BD
    logger.info("📚 Obteniendo lista de estudiantes desde BD...")
    estudiantes = db.obtener_estudiantes()
    
    if not estudiantes:
        logger.error("❌ No se encontraron estudiantes en la base de datos")
        logger.info("Por favor, primero inserta estudiantes en la tabla 'estudiantes'")
        sys.exit(1)
    
    logger.info(f"✅ Encontrados {len(estudiantes)} estudiantes")
    
    # Verificar que existan fotos
    from config import FOTOS_DIR
    
    if not os.path.exists(FOTOS_DIR):
        logger.error(f"❌ Carpeta de fotos no encontrada: {FOTOS_DIR}")
        sys.exit(1)
    
    fotos = [f for f in os.listdir(FOTOS_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
    logger.info(f"📸 Encontradas {len(fotos)} fotos en {FOTOS_DIR}")
    
    # Generar encodings
    logger.info("\n🔄 Iniciando generación de encodings...")
    face_processor.generar_encodings_desde_fotos(estudiantes)
    
    if face_processor.encodings_loaded:
        print("\n" + "="*50)
        print("✅ ENCODINGS GENERADOS EXITOSAMENTE")
        print("="*50)
        print(f"Total de rostros procesados: {len(face_processor.known_encodings)}")
        print("\nEstudiantes registrados:")
        for i, (id_est, nombre) in enumerate(zip(face_processor.known_ids, face_processor.known_names), 1):
            print(f"  {i}. {nombre} (ID: {id_est})")
    else:
        print("\n❌ ERROR: No se pudieron generar encodings")
        sys.exit(1)


if __name__ == "__main__":
    main()