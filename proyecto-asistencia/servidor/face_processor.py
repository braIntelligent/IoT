"""
face_processor.py - Módulo de reconocimiento facial
Carga encodings y compara rostros
"""

import face_recognition
import numpy as np
import pickle
import os
from PIL import Image
import io
import logging
from config import FOTOS_DIR, ENCODINGS_FILE, FACE_TOLERANCE, FACE_DETECTION_MODEL

logger = logging.getLogger(__name__)


class FaceProcessor:
    """Clase para procesar reconocimiento facial"""
    
    def __init__(self):
        self.known_encodings = []
        self.known_ids = []
        self.known_names = []
        self.encodings_loaded = False
        
        # Cargar encodings si existe el archivo
        if os.path.exists(ENCODINGS_FILE):
            self.cargar_encodings()
        else:
            logger.warning(f"Archivo de encodings no encontrado: {ENCODINGS_FILE}")
    
    def cargar_encodings(self):
        """
        Carga los encodings pre-calculados desde archivo pickle
        """
        try:
            with open(ENCODINGS_FILE, 'rb') as f:
                data = pickle.load(f)
            
            self.known_encodings = data['encodings']
            self.known_ids = data['ids']
            self.known_names = data['names']
            self.encodings_loaded = True
            
            logger.info(f"✅ Encodings cargados: {len(self.known_encodings)} rostros")
            
        except Exception as e:
            logger.error(f"Error al cargar encodings: {e}")
            self.encodings_loaded = False
    
    def generar_encodings_desde_fotos(self, estudiantes_db):
        """
        Genera encodings desde las fotos en la carpeta y los guarda
        
        Args:
            estudiantes_db (list): Lista de estudiantes desde la BD
        """
        logger.info("🔄 Generando encodings desde fotos...")
        
        encodings = []
        ids = []
        names = []
        
        for estudiante in estudiantes_db:
            id_estudiante = estudiante['id_estudiante']
            nombre = estudiante['nombre_completo']
            path_foto = estudiante['path_foto_referencia']
            
            # Construir ruta completa
            full_path = os.path.join(FOTOS_DIR, path_foto)
            
            if not os.path.exists(full_path):
                logger.warning(f"⚠️  Foto no encontrada: {full_path}")
                continue
            
            try:
                # Cargar imagen
                image = face_recognition.load_image_file(full_path)
                
                # Generar encoding
                face_encodings = face_recognition.face_encodings(image)
                
                if len(face_encodings) > 0:
                    encodings.append(face_encodings[0])
                    ids.append(id_estudiante)
                    names.append(nombre)
                    logger.info(f"✅ Encoding generado: {nombre}")
                else:
                    logger.warning(f"⚠️  No se detectó rostro en: {path_foto}")
                    
            except Exception as e:
                logger.error(f"❌ Error procesando {path_foto}: {e}")
        
        # Guardar encodings
        if len(encodings) > 0:
            data = {
                'encodings': encodings,
                'ids': ids,
                'names': names
            }
            
            with open(ENCODINGS_FILE, 'wb') as f:
                pickle.dump(data, f)
            
            self.known_encodings = encodings
            self.known_ids = ids
            self.known_names = names
            self.encodings_loaded = True
            
            logger.info(f"💾 Encodings guardados: {len(encodings)} rostros")
        else:
            logger.error("❌ No se generó ningún encoding")
    
    def procesar_frame(self, image_array):
        """
        Procesa un frame y busca rostros conocidos
        
        Args:
            image_array (numpy.ndarray): Frame en formato numpy array (RGB)
            
        Returns:
            dict: Resultado del procesamiento {
                'faces_found': int,
                'matches': [{'id': int, 'name': str, 'location': tuple}]
            }
        """
        if not self.encodings_loaded:
            return {
                'faces_found': 0,
                'matches': [],
                'error': 'Encodings no cargados'
            }
        
        try:
            # Detectar ubicaciones de rostros
            face_locations = face_recognition.face_locations(
                image_array, 
                model=FACE_DETECTION_MODEL
            )
            
            if len(face_locations) == 0:
                return {
                    'faces_found': 0,
                    'matches': []
                }
            
            # Generar encodings para los rostros detectados
            face_encodings = face_recognition.face_encodings(
                image_array, 
                face_locations
            )
            
            matches_result = []
            
            # Comparar cada rostro detectado con los conocidos
            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Comparar con todos los rostros conocidos
                matches = face_recognition.compare_faces(
                    self.known_encodings,
                    face_encoding,
                    tolerance=FACE_TOLERANCE
                )
                
                # Calcular distancias para encontrar la mejor coincidencia
                face_distances = face_recognition.face_distance(
                    self.known_encodings,
                    face_encoding
                )
                
                if True in matches:
                    # Encontrar la mejor coincidencia (menor distancia)
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        id_estudiante = self.known_ids[best_match_index]
                        nombre = self.known_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        
                        matches_result.append({
                            'id': id_estudiante,
                            'name': nombre,
                            'location': face_location,
                            'confidence': float(confidence)
                        })
            
            return {
                'faces_found': len(face_locations),
                'matches': matches_result
            }
            
        except Exception as e:
            logger.error(f"Error al procesar frame: {e}")
            return {
                'faces_found': 0,
                'matches': [],
                'error': str(e)
            }
    
    def decode_image_from_base64(self, base64_string):
        """
        Decodifica una imagen base64 a numpy array
        
        Args:
            base64_string (str): Imagen en base64
            
        Returns:
            numpy.ndarray: Imagen en formato RGB
        """
        try:
            import base64
            
            # Decodificar base64
            img_data = base64.b64decode(base64_string)
            
            # Convertir a PIL Image
            img = Image.open(io.BytesIO(img_data))
            
            # Convertir a RGB si es necesario
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convertir a numpy array
            img_array = np.array(img)
            
            return img_array
            
        except Exception as e:
            logger.error(f"Error al decodificar imagen: {e}")
            return None


# Instancia global
face_processor = FaceProcessor()