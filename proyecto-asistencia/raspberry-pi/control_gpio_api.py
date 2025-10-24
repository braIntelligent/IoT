"""
control_gpio_api.py - API Flask para control remoto de LEDs en Raspberry Pi
Servidor ligero que recibe comandos del servidor principal para encender LEDs
"""

from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import threading
import time
from config import LED_GREEN_PIN, LED_RED_PIN, GPIO_API_PORT

app = Flask(__name__)

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
GPIO.setup(LED_RED_PIN, GPIO.OUT)

# Asegurar que los LEDs estén apagados al inicio
GPIO.output(LED_GREEN_PIN, GPIO.LOW)
GPIO.output(LED_RED_PIN, GPIO.LOW)


def blink_led(pin, duration):
    """
    Enciende un LED por una duración específica en un thread separado
    """
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)


@app.route('/api/led', methods=['POST'])
def control_led():
    """
    Endpoint para controlar LEDs
    
    Body JSON:
    {
        "color": "green" o "red",
        "duration": 2  (segundos)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        color = data.get('color', '').lower()
        duration = data.get('duration', 2)
        
        # Validar color
        if color not in ['green', 'red']:
            return jsonify({"error": "Color debe ser 'green' o 'red'"}), 400
        
        # Validar duración
        if not isinstance(duration, (int, float)) or duration <= 0 or duration > 10:
            return jsonify({"error": "Duración debe ser entre 0 y 10 segundos"}), 400
        
        # Seleccionar pin según color
        pin = LED_GREEN_PIN if color == 'green' else LED_RED_PIN
        
        # Encender LED en thread separado para no bloquear
        led_thread = threading.Thread(target=blink_led, args=(pin, duration))
        led_thread.start()
        
        return jsonify({
            "status": "ok",
            "color": color,
            "duration": duration
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """
    Endpoint de health check
    """
    return jsonify({
        "status": "online",
        "device": "raspberry-pi-gpio",
        "green_pin": LED_GREEN_PIN,
        "red_pin": LED_RED_PIN
    }), 200


@app.route('/api/led/off', methods=['POST'])
def leds_off():
    """
    Apagar todos los LEDs inmediatamente
    """
    try:
        GPIO.output(LED_GREEN_PIN, GPIO.LOW)
        GPIO.output(LED_RED_PIN, GPIO.LOW)
        return jsonify({"status": "ok", "message": "LEDs apagados"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def cleanup():
    """
    Limpieza de GPIO al cerrar
    """
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        print(f"🚀 Iniciando API de control GPIO en puerto {GPIO_API_PORT}")
        print(f"   LED Verde: GPIO {LED_GREEN_PIN}")
        print(f"   LED Rojo: GPIO {LED_RED_PIN}")
        app.run(host='0.0.0.0', port=GPIO_API_PORT, debug=False)
    except KeyboardInterrupt:
        print("\n⚠️  Cerrando servidor...")
        cleanup()