#!/usr/bin/env python3
"""
test_sistema.py - Script de prueba para verificar todos los componentes
"""

import requests
import sys
import time

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(mensaje):
    print(f"{BLUE}[TEST]{RESET} {mensaje}")

def print_success(mensaje):
    print(f"{GREEN}[✓]{RESET} {mensaje}")

def print_error(mensaje):
    print(f"{RED}[✗]{RESET} {mensaje}")

def print_warning(mensaje):
    print(f"{YELLOW}[!]{RESET} {mensaje}")

def test_servidor(host, port=8000):
    """Probar conexión con el servidor"""
    print_test(f"Probando servidor en {host}:{port}")
    
    try:
        # Test 1: Health check
        response = requests.get(f"http://{host}:{port}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Servidor respondiendo: {data.get('status')}")
            print_success(f"Encodings cargados: {data.get('total_encodings')}")
            return True
        else:
            print_error(f"Servidor respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_warning("Verificar que el servidor esté corriendo: python main.py")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_mysql(host):
    """Probar endpoints de base de datos"""
    print_test("Probando conexión con MySQL")
    
    try:
        # Test estudiantes
        response = requests.get(f"http://{host}:8000/api/estudiantes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print_success(f"Base de datos accesible: {total} estudiantes registrados")
            
            if total == 0:
                print_warning("No hay estudiantes registrados en la BD")
                return False
            return True
        else:
            print_error("Error al consultar estudiantes")
            return False
    except Exception as e:
        print_error(f"Error de BD: {e}")
        return False

def test_raspberry_pi(host, port=5000):
    """Probar API de GPIO en Raspberry Pi"""
    print_test(f"Probando Raspberry Pi en {host}:{port}")
    
    try:
        response = requests.get(f"http://{host}:{port}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Raspberry Pi respondiendo: {data.get('status')}")
            print_success(f"Pines GPIO: Verde={data.get('green_pin')}, Rojo={data.get('red_pin')}")
            return True
        else:
            print_error("Raspberry Pi no responde correctamente")
            return False
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar a la Raspberry Pi")
        print_warning("Verificar que control_gpio_api.py esté corriendo")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_led_control(pi_host):
    """Probar control de LEDs"""
    print_test("Probando control de LEDs")
    
    try:
        # Test LED verde
        print("  Probando LED verde...")
        response = requests.post(
            f"http://{pi_host}:5000/api/led",
            json={"color": "green", "duration": 1},
            timeout=5
        )
        if response.status_code == 200:
            print_success("LED verde funciona")
            time.sleep(1.5)
        else:
            print_error("Error al controlar LED verde")
            return False
        
        # Test LED rojo
        print("  Probando LED rojo...")
        response = requests.post(
            f"http://{pi_host}:5000/api/led",
            json={"color": "red", "duration": 1},
            timeout=5
        )
        if response.status_code == 200:
            print_success("LED rojo funciona")
            return True
        else:
            print_error("Error al controlar LED rojo")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_flujo_completo(servidor_host, pi_host):
    """Probar flujo completo de reconocimiento"""
    print_test("Probando flujo completo (simulado)")
    
    try:
        import base64
        
        # Crear imagen de prueba simple (1x1 pixel negro)
        test_image = base64.b64encode(b'\x00\x00\x00').decode('utf-8')
        
        response = requests.post(
            f"http://{servidor_host}:8000/api/procesar-frame",
            json={"image": test_image, "device_id": "test"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Procesamiento de frames funciona: {data.get('status')}")
            return True
        else:
            print_warning(f"Respuesta no esperada: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    print("""
╔═══════════════════════════════════════════════════╗
║    TEST DEL SISTEMA DE ASISTENCIA IoT             ║
╚═══════════════════════════════════════════════════╝
    """)
    
    # Obtener IPs desde argumentos o usar localhost
    servidor_host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    pi_host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
    
    print(f"Servidor: {servidor_host}")
    print(f"Raspberry Pi: {pi_host}")
    print()
    
    resultados = {
        'servidor': False,
        'mysql': False,
        'raspberry': False,
        'leds': False,
        'flujo': False
    }
    
    # Ejecutar tests
    print("="*60)
    resultados['servidor'] = test_servidor(servidor_host)
    
    print("="*60)
    if resultados['servidor']:
        resultados['mysql'] = test_mysql(servidor_host)
    
    print("="*60)
    resultados['raspberry'] = test_raspberry_pi(pi_host)
    
    print("="*60)
    if resultados['raspberry']:
        resultados['leds'] = test_led_control(pi_host)
    
    print("="*60)
    if resultados['servidor'] and resultados['mysql']:
        resultados['flujo'] = test_flujo_completo(servidor_host, pi_host)
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    total = len(resultados)
    exitosos = sum(resultados.values())
    
    for nombre, resultado in resultados.items():
        simbolo = "✓" if resultado else "✗"
        color = GREEN if resultado else RED
        print(f"{color}{simbolo}{RESET} {nombre.upper()}")
    
    print(f"\nTotal: {exitosos}/{total} pruebas exitosas")
    
    if exitosos == total:
        print_success("¡Todos los componentes funcionan correctamente! ✨")
        return 0
    else:
        print_error("Algunos componentes tienen problemas. Revisar logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())