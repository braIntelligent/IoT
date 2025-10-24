# Diagrama de Arquitectura del Sistema

## Flujo de Datos

```mermaid
graph TB
    subgraph "RASPBERRY PI (Edge Device)"
        CAM[📷 Cámara]
        CAPTURE[Captura Video<br/>picamera2]
        COMPRESS[Compresión JPEG<br/>base64]
        GPIO_API[API Flask<br/>Control GPIO]
        LED_G[💚 LED Verde]
        LED_R[❤️ LED Rojo]
    end
    
    subgraph "SERVIDOR (Procesamiento Central)"
        API[FastAPI<br/>Puerto 8000]
        FACE_PROC[Face Recognition<br/>face_recognition lib]
        ENCODE[Comparación<br/>Encodings]
        DB_CONN[MySQL Connector]
        LED_CMD[Comandos LED]
    end
    
    subgraph "BASE DE DATOS"
        MYSQL[(MySQL 8.0<br/>asistencia_db)]
        ESTUDIANTES[Tabla<br/>estudiantes]
        ASISTENCIA[Tabla<br/>asistencia]
        DISPOSITIVOS[Tabla<br/>dispositivos]
    end
    
    subgraph "CLIENTE WEB"
        BROWSER[🌐 Navegador]
        HTML[HTML/CSS/JS]
        FETCH[Fetch API]
    end
    
    CAM -->|Video Stream| CAPTURE
    CAPTURE -->|Frame| COMPRESS
    COMPRESS -->|HTTP POST<br/>base64 JPEG| API
    API -->|Decodificar| FACE_PROC
    FACE_PROC -->|Detectar Rostros| ENCODE
    ENCODE -->|Comparar| ENCODE
    
    ENCODE -->|Match| DB_CONN
    ENCODE -->|No Match| LED_CMD
    
    DB_CONN --> MYSQL
    MYSQL --> ESTUDIANTES
    MYSQL --> ASISTENCIA
    MYSQL --> DISPOSITIVOS
    
    LED_CMD -->|HTTP POST| GPIO_API
    GPIO_API --> LED_G
    GPIO_API --> LED_R
    
    DB_CONN -->|Success| LED_CMD
    
    BROWSER --> HTML
    HTML -->|GET /estudiantes| FETCH
    HTML -->|GET /asistencia/hoy| FETCH
    FETCH -->|HTTP| API
    API -->|JSON| FETCH
    
    style CAM fill:#e1f5e1
    style API fill:#e1e5f5
    style MYSQL fill:#f5e1e1
    style BROWSER fill:#f5f5e1
```

## Secuencia de Reconocimiento

```mermaid
sequenceDiagram
    participant Pi as 🎥 Raspberry Pi
    participant Srv as 🖥️ Servidor
    participant DB as 💾 MySQL
    participant LED as 💡 LED
    
    loop Cada 0.5s
        Pi->>Pi: Capturar frame
        Pi->>Pi: Comprimir a JPEG
        Pi->>Srv: POST /api/procesar-frame<br/>{image: base64}
        
        Srv->>Srv: Decodificar imagen
        Srv->>Srv: Detectar rostros
        Srv->>Srv: Generar encodings
        Srv->>Srv: Comparar con BD
        
        alt Rostro Reconocido
            Srv->>DB: Verificar cooldown
            alt No está en cooldown
                Srv->>DB: INSERT asistencia
                DB-->>Srv: OK
                Srv->>Pi: POST /api/led {green, 2s}
                Pi->>LED: Encender LED Verde
                Srv-->>Pi: {status: "recognized", nombre: "Juan"}
            else En cooldown
                Srv-->>Pi: {status: "recognized", registrado: false}
            end
        else Rostro No Reconocido
            Srv->>Pi: POST /api/led {red, 1s}
            Pi->>LED: Encender LED Rojo
            Srv-->>Pi: {status: "unknown"}
        else Sin Rostro
            Srv-->>Pi: {status: "no_face"}
        end
    end
```

## Arquitectura de Red

```mermaid
graph LR
    subgraph "Red Local 192.168.1.0/24"
        subgraph "Raspberry Pi<br/>192.168.1.50"
            PI_CAP[Captura<br/>Puerto N/A]
            PI_GPIO[GPIO API<br/>Puerto 5000]
        end
        
        subgraph "Servidor<br/>192.168.1.100"
            SRV_API[FastAPI<br/>Puerto 8000]
            SRV_WEB[Web Server<br/>Puerto 8080]
            SRV_DB[MySQL<br/>Puerto 3306]
        end
        
        subgraph "Cliente Web<br/>Cualquier dispositivo"
            CLIENT[Navegador]
        end
    end
    
    PI_CAP -->|WiFi| SRV_API
    SRV_API -->|Local| PI_GPIO
    CLIENT -->|HTTP| SRV_WEB
    CLIENT -->|HTTP| SRV_API
    SRV_API -->|SQL| SRV_DB
    
    style PI_CAP fill:#a8e6cf
    style PI_GPIO fill:#a8e6cf
    style SRV_API fill:#ffd3b6
    style SRV_WEB fill:#ffd3b6
    style SRV_DB fill:#ffaaa5
    style CLIENT fill:#dcedc1
```

## Modelo de Datos

```mermaid
erDiagram
    ESTUDIANTES ||--o{ ASISTENCIA : tiene
    DISPOSITIVOS ||--o{ ASISTENCIA : registra
    
    ESTUDIANTES {
        int id_estudiante PK
        varchar nombre_completo
        varchar rut UK
        varchar path_foto_referencia
        varchar email
        timestamp fecha_creacion
        boolean activo
    }
    
    ASISTENCIA {
        int id_asistencia PK
        int id_estudiante FK
        timestamp hora_ingreso
        date fecha_registro
        varchar dispositivo_id FK
        text notas
    }
    
    DISPOSITIVOS {
        int id_dispositivo PK
        varchar nombre UK
        varchar descripcion
        varchar ip_address
        varchar ubicacion
        timestamp ultimo_ping
        boolean activo
    }
```

## Estados del Sistema

```mermaid
stateDiagram-v2
    [*] --> Esperando
    
    Esperando --> Capturando: Frame disponible
    Capturando --> Enviando: Comprimir
    Enviando --> Procesando: POST exitoso
    
    Procesando --> Reconocido: Match encontrado
    Procesando --> Desconocido: Sin match
    Procesando --> SinRostro: Sin detección
    
    Reconocido --> VerificarCooldown: Validar
    VerificarCooldown --> Registrando: No cooldown
    VerificarCooldown --> EnCooldown: Ya registrado
    
    Registrando --> LEDVerde: Insertar BD
    LEDVerde --> Esperando: Timeout LED
    
    EnCooldown --> Esperando: Skip registro
    
    Desconocido --> LEDRojo: Alerta
    LEDRojo --> Esperando: Timeout LED
    
    SinRostro --> Esperando: Continue
    
    Enviando --> Error: Connection failed
    Error --> Esperando: Retry
```

## Componentes y Tecnologías

```mermaid
mindmap
  root((Sistema IoT<br/>Asistencia))
    Edge
      Raspberry Pi 4
        Cámara Pi
        2x LEDs
        Python 3
        Flask
        GPIO
      Captura
        picamera2
        Pillow
        base64
    Servidor
      Procesamiento
        FastAPI
        face_recognition
        OpenCV
      Base de Datos
        MySQL 8.0
        mysql-connector
      Control
        requests
        asyncio
    Cliente
      Frontend
        HTML5
        CSS3
        JavaScript
      Comunicación
        Fetch API
        REST
      UI/UX
        Tiempo real
        Responsive
```

---

## Notas sobre el Diagrama

1. **Flujo Principal**: La Raspberry Pi captura → Comprime → Envía al servidor vía WiFi
2. **Procesamiento**: El servidor ejecuta face_recognition y registra en MySQL
3. **Feedback**: Servidor envía comandos de vuelta a la Pi para controlar LEDs
4. **Visualización**: Cliente web consulta API REST para mostrar asistencia
5. **Optimización**: Todo el procesamiento pesado está en el servidor, no en la Pi