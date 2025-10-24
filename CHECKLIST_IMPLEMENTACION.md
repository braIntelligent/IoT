# ✅ Checklist de Implementación

## 📋 Lista de Verificación Completa

### Fase 1: Hardware ⚙️

#### Compras
- [ ] Raspberry Pi 4 (4GB RAM mínimo)
- [ ] Tarjeta MicroSD (32GB+, Clase 10)
- [ ] Fuente de poder USB-C 5V 3A
- [ ] Gabinete para Raspberry Pi
- [ ] Cámara Raspberry Pi (v2 o v3)
- [ ] 2x LEDs (verde y rojo, 5mm)
- [ ] 2x Resistencias 220Ω
- [ ] Protoboard
- [ ] Cables jumper macho-hembra
- [ ] Cable HDMI (para setup inicial)
- [ ] Teclado + Mouse USB (para setup inicial)

#### Ensamblaje
- [ ] Instalar disipadores en Raspberry Pi
- [ ] Colocar Pi en gabinete
- [ ] Conectar cámara al puerto CSI
- [ ] Conectar LED verde a GPIO 17 con resistencia
- [ ] Conectar LED rojo a GPIO 27 con resistencia
- [ ] Verificar polaridad de LEDs (+ hacia GPIO)
- [ ] Conectar ambos LEDs a GND
- [ ] Verificar conexiones con multímetro (opcional)

---

### Fase 2: Software Base 💻

#### Raspberry Pi
- [ ] Descargar Raspberry Pi OS (64-bit)
- [ ] Flashear tarjeta SD con Raspberry Pi Imager
- [ ] Habilitar SSH en boot
- [ ] Configurar WiFi en boot (wpa_supplicant.conf)
- [ ] Primera boot y actualizar sistema
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- [ ] Habilitar cámara con `raspi-config`
- [ ] Instalar Python 3 y pip
- [ ] Verificar GPIO con `gpio readall`

#### Servidor
- [ ] Preparar PC/VPS con Linux (Ubuntu 22.04 LTS recomendado)
- [ ] Actualizar sistema operativo
- [ ] Instalar Python 3.9+
- [ ] Instalar MySQL 8.0
- [ ] Instalar librerías del sistema:
  ```bash
  sudo apt install -y python3-dev libmysqlclient-dev build-essential cmake
  ```
- [ ] Configurar firewall (puertos 8000, 3306)

---

### Fase 3: Base de Datos 🗄️

- [ ] Iniciar servicio MySQL
- [ ] Crear usuario `asistencia_user`
- [ ] Asignar password seguro
- [ ] Dar permisos al usuario
- [ ] Ejecutar `schema.sql` para crear tablas
- [ ] Verificar creación de tablas:
  ```sql
  SHOW TABLES;
  ```
- [ ] Insertar estudiantes de prueba (opcional: `datos_ejemplo.sql`)
- [ ] Insertar dispositivos
- [ ] Verificar datos con queries de prueba

---

### Fase 4: Fotos de Referencia 📸

- [ ] Crear carpeta `servidor/fotos_conocidas/`
- [ ] Tomar fotos de cada estudiante:
  - [ ] Fondo neutro
  - [ ] Buena iluminación frontal
  - [ ] Rostro de frente
  - [ ] Sin lentes/sombrero (si es posible)
  - [ ] Resolución mínima 640x480
- [ ] Nombrar fotos: `nombre_apellido_rut.jpg`
- [ ] Copiar fotos a `servidor/fotos_conocidas/`
- [ ] Verificar que nombres coincidan con BD

---

### Fase 5: Configuración del Servidor 🖥️

- [ ] Clonar/copiar carpeta `servidor/`
- [ ] Crear entorno virtual:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Editar `config.py`:
  - [ ] Configurar credenciales MySQL
  - [ ] Ajustar `FACE_TOLERANCE` si es necesario
  - [ ] Configurar rutas de archivos
- [ ] Generar encodings faciales:
  ```bash
  python generate_encodings.py
  ```
- [ ] Verificar que se generaron todos los encodings
- [ ] Probar inicio del servidor:
  ```bash
  python main.py
  ```
- [ ] Verificar endpoint de health:
  ```bash
  curl http://localhost:8000/api/health
  ```

---

### Fase 6: Configuración de Raspberry Pi 📡

- [ ] Copiar carpeta `raspberry-pi/` a la Pi
- [ ] Instalar dependencias:
  ```bash
  pip3 install -r requirements.txt
  ```
- [ ] Editar `config.py`:
  - [ ] Configurar `SERVER_HOST` con IP del servidor
  - [ ] Ajustar `DEVICE_ID`
  - [ ] Verificar pines GPIO
- [ ] Probar API de control GPIO:
  ```bash
  python3 control_gpio_api.py
  ```
- [ ] En otra terminal, probar LEDs:
  ```bash
  curl -X POST http://localhost:5000/api/led \
    -H "Content-Type: application/json" \
    -d '{"color": "green", "duration": 2}'
  ```
- [ ] Verificar que LEDs se encienden
- [ ] Probar captura de video:
  ```bash
  python3 captura_cliente.py
  ```
- [ ] Verificar que no hay errores de cámara

---

### Fase 7: Cliente Web 🌐

- [ ] Copiar carpeta `cliente-web/`
- [ ] Editar `js/app.js`:
  - [ ] Configurar `API_URL` con IP del servidor
  - [ ] Ajustar `REFRESH_INTERVAL` si es necesario
- [ ] Iniciar servidor web:
  ```bash
  cd cliente-web/
  python3 -m http.server 8080
  ```
- [ ] Abrir navegador en `http://IP_SERVIDOR:8080`
- [ ] Verificar que se muestra la interfaz
- [ ] Verificar que carga lista de estudiantes
- [ ] Verificar conexión con API (indicador verde)

---

### Fase 8: Pruebas de Integración 🧪

- [ ] Ejecutar script de prueba:
  ```bash
  python3 test_sistema.py IP_SERVIDOR IP_RASPBERRY_PI
  ```
- [ ] Verificar que todos los tests pasan
- [ ] Probar flujo completo:
  - [ ] Persona se para frente a la cámara
  - [ ] Pi captura y envía frame
  - [ ] Servidor procesa y reconoce
  - [ ] LED se enciende
  - [ ] Registro aparece en BD
  - [ ] Web se actualiza (esperar hasta 10 seg)
- [ ] Probar con todos los estudiantes registrados
- [ ] Probar con persona no registrada (LED rojo)
- [ ] Verificar cooldown (no registrar 2 veces en 5 min)

---

### Fase 9: Optimización ⚡

#### Rendimiento
- [ ] Ajustar `FRAME_RESIZE_WIDTH` en servidor
- [ ] Ajustar `CAPTURE_INTERVAL` en Pi
- [ ] Ajustar `JPEG_QUALITY` en Pi
- [ ] Verificar latencia de red:
  ```bash
  ping -c 100 IP_SERVIDOR
  ```
- [ ] Monitorear uso de CPU/RAM en servidor
- [ ] Reducir `FACE_TOLERANCE` si hay falsos positivos

#### Confiabilidad
- [ ] Configurar auto-inicio en Pi (systemd)
- [ ] Configurar auto-inicio en servidor (systemd)
- [ ] Configurar logs rotativos
- [ ] Crear backup de base de datos
- [ ] Documentar configuración actual

---

### Fase 10: Producción 🚀

#### Seguridad
- [ ] Cambiar passwords por defecto
- [ ] Configurar firewall en servidor
- [ ] Habilitar solo IPs confiables para MySQL
- [ ] Considerar HTTPS para API (Let's Encrypt)
- [ ] Crear usuario limitado para servicios

#### Monitoreo
- [ ] Configurar logs en `/var/log/`
- [ ] Crear script de backup diario de BD
- [ ] Documentar procedimientos de mantenimiento
- [ ] Crear contactos de soporte

#### Documentación
- [ ] Documentar IPs de dispositivos
- [ ] Documentar credenciales (en lugar seguro)
- [ ] Crear manual de usuario para profesores
- [ ] Documentar procedimientos de emergencia

---

## 📊 Verificación Final

### Tests Funcionales
- [ ] ✅ Servidor responde en `/api/health`
- [ ] ✅ MySQL acepta conexiones
- [ ] ✅ Encodings cargados correctamente
- [ ] ✅ Pi puede capturar video
- [ ] ✅ LEDs funcionan correctamente
- [ ] ✅ Comunicación Pi ↔ Servidor funciona
- [ ] ✅ Reconocimiento facial funciona
- [ ] ✅ Registros se guardan en BD
- [ ] ✅ Cliente web muestra datos
- [ ] ✅ Actualizaciones en tiempo real funcionan

### Tests de Estrés
- [ ] Sistema funciona con múltiples personas
- [ ] Sistema funciona durante 1 hora continua
- [ ] Servidor soporta múltiples Pis (si aplica)
- [ ] Base de datos maneja 100+ registros

---

## 🎯 Métricas de Éxito

| Métrica | Objetivo | Estado |
|---------|----------|--------|
| Tasa de reconocimiento | >95% | ⬜ |
| Falsos positivos | <2% | ⬜ |
| Latencia (captura → LED) | <3 segundos | ⬜ |
| Disponibilidad | >99% | ⬜ |
| Tiempo de registro | <5 segundos | ⬜ |

---

## 📝 Notas de Implementación

### Fecha de inicio: __________

### Responsables:
- Hardware: __________
- Servidor: __________
- Base de datos: __________
- Frontend: __________

### Problemas encontrados:
_____________________________________________________
_____________________________________________________
_____________________________________________________

### Soluciones aplicadas:
_____________________________________________________
_____________________________________________________
_____________________________________________________

---

## 🎓 Próximos Pasos

Después de completar este checklist:

1. **Entrenar a usuarios:** Mostrar cómo usar el sistema
2. **Monitorear:** Primeros días revisar logs frecuentemente
3. **Iterar:** Ajustar según feedback de usuarios
4. **Escalar:** Si funciona bien, añadir más aulas
5. **Mejorar:** Implementar funcionalidades adicionales

---

## 📞 Soporte

Si tienes problemas en algún paso:

1. Revisar logs del componente con problemas
2. Consultar README.md correspondiente
3. Verificar conexiones y configuración
4. Ejecutar test_sistema.py para diagnóstico
5. Revisar sección de "Solución de Problemas" en documentación

**¡Éxito en tu implementación! 🚀**