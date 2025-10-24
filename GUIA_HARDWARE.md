# 🔧 Guía de Hardware y Componentes

## Lista de Materiales Completa (BOM)

### 🖥️ Computación

| Componente | Especificaciones | Cantidad | Precio Aprox. (CLP) |
|------------|-----------------|----------|---------------------|
| **Raspberry Pi 4 Model B** | 4GB RAM (mínimo), 64-bit | 1 | $60.000 - $80.000 |
| **Tarjeta MicroSD** | 32GB+, Clase 10, A1/A2 | 1 | $8.000 - $12.000 |
| **Fuente de Poder** | USB-C, 5V 3A oficial | 1 | $12.000 - $15.000 |
| **Gabinete para Pi** | Con ventilación/disipadores | 1 | $5.000 - $10.000 |

**Total Raspberry Pi: ~$85.000 - $117.000**

### 📷 Captura de Imagen

| Componente | Especificaciones | Cantidad | Precio Aprox. (CLP) |
|------------|-----------------|----------|---------------------|
| **Cámara Raspberry Pi** | v2.1 (8MP) o v3 (12MP) | 1 | $25.000 - $40.000 |
| **Cable Ribbon CSI** | 30cm (incluido con cámara) | 1 | Incluido |

**Alternativa económica:** Webcam USB compatible (~$10.000)

### 💡 Indicadores LED

| Componente | Especificaciones | Cantidad | Precio Aprox. (CLP) |
|------------|-----------------|----------|---------------------|
| **LED Verde** | 5mm, 20mA, difuso | 1 | $100 - $300 |
| **LED Rojo** | 5mm, 20mA, difuso | 1 | $100 - $300 |
| **Resistencias** | 220Ω, 1/4W | 2 | $50 c/u |
| **Protoboard** | 400 puntos mínimo | 1 | $1.500 - $3.000 |
| **Cables Jumper** | Macho-Hembra, 20cm | 10 | $2.000 - $4.000 |

**Total Electrónica: ~$4.000 - $8.000**

### 🖥️ Servidor (Opciones)

#### Opción 1: PC/Laptop Existente
- **CPU:** Intel i3/AMD Ryzen 3 o superior
- **RAM:** 4GB mínimo (8GB recomendado)
- **Storage:** 20GB libres
- **SO:** Linux (Ubuntu 22.04 LTS recomendado)
- **Costo:** $0 (reutilizar equipo existente)

#### Opción 2: Mini PC Nuevo
- **Ejemplo:** Intel NUC, Beelink, ASUS Mini PC
- **Specs:** i5/Ryzen 5, 8GB RAM, 256GB SSD
- **Costo:** $300.000 - $500.000

#### Opción 3: VPS en la Nube
- **Proveedor:** DigitalOcean, AWS, Google Cloud, Contabo
- **Specs:** 2 vCPU, 4GB RAM, 50GB Storage
- **Costo mensual:** $10.000 - $25.000 (USD $12-30)

### 🌐 Networking

| Componente | Especificaciones | Necesario | Precio Aprox. (CLP) |
|------------|-----------------|-----------|---------------------|
| **Router WiFi** | 2.4GHz/5GHz, WPA2/WPA3 | Sí | Ya disponible |
| **Cable Ethernet** | Cat 5e+ (opcional para servidor) | Opcional | $2.000 - $5.000 |

---

## 🔌 Diagrama de Conexión GPIO

```
RASPBERRY PI 4 - GPIO PINOUT

         3V3  (1) (2)  5V
       GPIO2  (3) (4)  5V
       GPIO3  (5) (6)  GND
       GPIO4  (7) (8)  GPIO14
         GND  (9) (10) GPIO15
      GPIO17 (11) (12) GPIO18  ← LED VERDE (Pin 11)
      GPIO27 (13) (14) GND     ← LED ROJO (Pin 13)
      GPIO22 (15) (16) GPIO23
         3V3 (17) (18) GPIO24
      GPIO10 (19) (20) GND
       GPIO9 (21) (22) GPIO25
      GPIO11 (23) (24) GPIO8
         GND (25) (26) GPIO7
       ... resto de pines ...
```

### Conexión de LEDs

**LED Verde:**
```
GPIO 17 (Pin 11) → Resistencia 220Ω → (+) LED (-) → GND (Pin 9)
```

**LED Rojo:**
```
GPIO 27 (Pin 13) → Resistencia 220Ω → (+) LED (-) → GND (Pin 14)
```

**Importante:** El lado más largo del LED es el ánodo (+)

---

## 🛠️ Herramientas Necesarias

- Destornillador (para gabinete)
- Alicate de corte (para cables, opcional)
- Multímetro (para verificar LEDs, opcional)
- Lector de tarjetas MicroSD

---

## 📦 Dónde Comprar en Chile

### Tiendas Online
- **Raspberry Pi y Accesorios:**
  - Unit Electronics (unit.cl)
  - HuinchaTech (huinchatech.cl)
  - Grupo VCI (grupovci.cl)

- **Componentes Electrónicos:**
  - Casa Royal (casaroyal.cl)
  - Vistronica (vistronica.cl)
  - Electronica Elemon

- **Tarjetas MicroSD:**
  - PC Factory (pcfactory.cl)
  - París (paris.cl)
  - Amazon.com (envío a Chile)

### Tiendas Físicas Santiago
- Patronato (Barrio comercial electrónico)
- San Diego con Santa Isabel

---

## ⚙️ Especificaciones Técnicas Detalladas

### Raspberry Pi 4 Model B - 4GB

**Procesador:**
- Broadcom BCM2711, Quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz

**Memoria:**
- 4GB LPDDR4-3200 SDRAM

**Conectividad:**
- WiFi 802.11ac (2.4/5GHz)
- Bluetooth 5.0, BLE
- Gigabit Ethernet
- 2x USB 3.0, 2x USB 2.0

**GPIO:**
- 40-pin GPIO header (backward compatible)

**Cámara:**
- 2-lane MIPI CSI camera port

**Alimentación:**
- 5V DC via USB-C (mínimo 3A)

**SO Compatible:**
- Raspberry Pi OS (64-bit)
- Ubuntu Server
- Manjaro ARM

### Cámara Raspberry Pi v2.1

**Sensor:**
- Sony IMX219
- 8 megapixels

**Resolución Video:**
- 1080p @ 30fps
- 720p @ 60fps

**FOV:**
- 62.2° diagonal

**Interfaz:**
- CSI (15-pin ribbon cable)

---

## 💡 Cálculo de Consumo Eléctrico

### Raspberry Pi + Cámara + LEDs

| Componente | Consumo | Costo Mensual* |
|------------|---------|----------------|
| Raspberry Pi 4 (idle) | ~3.5W | $840 |
| Raspberry Pi 4 (carga) | ~7W | $1.680 |
| Cámara activa | ~1.5W | $360 |
| LEDs (uso intermitente) | ~0.1W | $24 |
| **TOTAL (promedio)** | **~6W** | **~$1.440** |

*Basado en tarifa residencial promedio Chile: $150/kWh
*Cálculo: (W × 24h × 30 días / 1000) × $150

**Servidor (PC):** +$3.000-$8.000 mensuales dependiendo del equipo

---

## 🔐 Consideraciones de Seguridad

### Protección del Hardware

1. **Gabinete:** Protege contra polvo y contactos accidentales
2. **Ventilación:** Evita sobrecalentamiento (disipadores/ventilador)
3. **Fuente de calidad:** Previene daños por voltaje inestable
4. **UPS (opcional):** Protege contra cortes de energía (~$50.000)

### Montaje Físico

- **Altura recomendada:** 1.5-2m para captura facial óptima
- **Ángulo cámara:** Ligeramente hacia abajo (15-20°)
- **Distancia de captura:** 0.5-2 metros
- **Iluminación:** Evitar contraluz, preferir luz frontal/lateral

---

## 📈 Escalabilidad

### Sistema Pequeño (1 aula)
- 1 Raspberry Pi
- 1 Servidor local
- **Costo inicial:** ~$200.000
- **Capacidad:** 30-50 estudiantes

### Sistema Mediano (3-5 aulas)
- 3-5 Raspberry Pi
- 1 Servidor dedicado
- **Costo inicial:** ~$600.000 - $800.000
- **Capacidad:** 150-250 estudiantes

### Sistema Grande (10+ aulas)
- 10+ Raspberry Pi
- Servidor con GPU o VPS
- **Costo inicial:** ~$1.500.000+
- **Capacidad:** 500+ estudiantes

---

## ✅ Checklist de Compra

- [ ] Raspberry Pi 4 (4GB)
- [ ] Tarjeta MicroSD (32GB+)
- [ ] Fuente USB-C (3A)
- [ ] Gabinete con ventilación
- [ ] Cámara Raspberry Pi v2/v3
- [ ] 2x LEDs (verde y rojo)
- [ ] 2x Resistencias 220Ω
- [ ] Protoboard
- [ ] Cables jumper
- [ ] Cable HDMI (setup inicial)
- [ ] Teclado y mouse USB (setup inicial)

**¿Ya tienes un servidor/PC?** ¡Perfecto! Ahorra ~$300.000-$500.000

---

## 🎓 Recomendaciones Finales

1. **Comienza simple:** 1 Pi + PC existente como servidor
2. **Prueba primero:** Verifica el sistema antes de comprar múltiples unidades
3. **Fotos de calidad:** La precisión del reconocimiento depende de buenas fotos de referencia
4. **Backup:** Respalda la tarjeta SD regularmente
5. **Monitoreo:** Revisa logs para detectar problemas temprano

**Presupuesto mínimo funcional:** ~$100.000-$150.000 (reutilizando PC como servidor)