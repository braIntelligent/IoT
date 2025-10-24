"""
database.py - Módulo de conexión y operaciones con MySQL
"""

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from datetime import date, datetime
from config import DB_CONFIG
import logging

logger = logging.getLogger(__name__)


class Database:
    """Clase para manejar operaciones con MySQL"""
    
    def __init__(self):
        self.config = DB_CONFIG
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión a la base de datos
        
        Uso:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(...)
        """
        conn = None
        try:
            conn = mysql.connector.connect(**self.config)
            yield conn
            conn.commit()
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Error de base de datos: {e}")
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()
    
    def registrar_asistencia(self, id_estudiante, device_id=None):
        """
        Registra la asistencia de un estudiante
        
        Args:
            id_estudiante (int): ID del estudiante
            device_id (str): Identificador del dispositivo
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                fecha_hoy = date.today()
                
                # Insertar o actualizar (si ya existe para hoy)
                query = """
                INSERT INTO asistencia (id_estudiante, fecha_registro, dispositivo_id)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    hora_ingreso = CURRENT_TIMESTAMP,
                    dispositivo_id = VALUES(dispositivo_id)
                """
                
                cursor.execute(query, (id_estudiante, fecha_hoy, device_id))
                
                # Verificar si fue INSERT o UPDATE
                if cursor.rowcount == 1:
                    resultado = "nuevo_registro"
                elif cursor.rowcount == 2:
                    resultado = "actualizado"
                else:
                    resultado = "sin_cambios"
                
                cursor.close()
                
                return {
                    "success": True,
                    "resultado": resultado,
                    "id_estudiante": id_estudiante
                }
                
        except Error as e:
            logger.error(f"Error al registrar asistencia: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_estudiantes(self):
        """
        Obtiene la lista completa de estudiantes
        
        Returns:
            list: Lista de estudiantes
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                SELECT id_estudiante, nombre_completo, rut, path_foto_referencia
                FROM estudiantes
                ORDER BY nombre_completo
                """
                
                cursor.execute(query)
                estudiantes = cursor.fetchall()
                cursor.close()
                
                return estudiantes
                
        except Error as e:
            logger.error(f"Error al obtener estudiantes: {e}")
            return []
    
    def obtener_asistencia_hoy(self):
        """
        Obtiene los registros de asistencia del día actual
        
        Returns:
            list: Lista de asistencias
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                fecha_hoy = date.today()
                
                query = """
                SELECT 
                    a.id_asistencia,
                    a.id_estudiante,
                    e.nombre_completo,
                    e.rut,
                    a.hora_ingreso,
                    a.dispositivo_id
                FROM asistencia a
                INNER JOIN estudiantes e ON a.id_estudiante = e.id_estudiante
                WHERE a.fecha_registro = %s
                ORDER BY a.hora_ingreso DESC
                """
                
                cursor.execute(query, (fecha_hoy,))
                asistencias = cursor.fetchall()
                cursor.close()
                
                # Convertir datetime a string para JSON
                for asistencia in asistencias:
                    if isinstance(asistencia['hora_ingreso'], datetime):
                        asistencia['hora_ingreso'] = asistencia['hora_ingreso'].strftime('%H:%M:%S')
                
                return asistencias
                
        except Error as e:
            logger.error(f"Error al obtener asistencia: {e}")
            return []
    
    def obtener_estudiante_por_id(self, id_estudiante):
        """
        Obtiene información de un estudiante específico
        
        Args:
            id_estudiante (int): ID del estudiante
            
        Returns:
            dict: Información del estudiante o None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                SELECT id_estudiante, nombre_completo, rut, path_foto_referencia
                FROM estudiantes
                WHERE id_estudiante = %s
                """
                
                cursor.execute(query, (id_estudiante,))
                estudiante = cursor.fetchone()
                cursor.close()
                
                return estudiante
                
        except Error as e:
            logger.error(f"Error al obtener estudiante: {e}")
            return None
    
    def verificar_cooldown(self, id_estudiante, segundos=300):
        """
        Verifica si un estudiante ya fue registrado recientemente
        
        Args:
            id_estudiante (int): ID del estudiante
            segundos (int): Segundos de cooldown
            
        Returns:
            bool: True si está en cooldown, False si puede registrarse
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                SELECT hora_ingreso
                FROM asistencia
                WHERE id_estudiante = %s 
                  AND fecha_registro = CURDATE()
                  AND hora_ingreso > DATE_SUB(NOW(), INTERVAL %s SECOND)
                LIMIT 1
                """
                
                cursor.execute(query, (id_estudiante, segundos))
                resultado = cursor.fetchone()
                cursor.close()
                
                return resultado is not None
                
        except Error as e:
            logger.error(f"Error al verificar cooldown: {e}")
            return False


# Instancia global
db = Database()