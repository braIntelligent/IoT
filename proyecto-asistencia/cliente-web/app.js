// app.js - Aplicación JavaScript para el Sistema de Asistencia

// Configuración
const CONFIG = {
    API_URL: 'http://localhost:8000',  // Cambiar por la IP del servidor
    REFRESH_INTERVAL: 10000,  // 10 segundos
    MAX_REGISTROS_RECIENTES: 10
};

// Estado de la aplicación
let state = {
    estudiantes: [],
    asistencias: [],
    filtroActivo: 'todos',
    busqueda: ''
};

// ==============================================
// INICIALIZACIÓN
// ==============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Iniciando aplicación...');
    
    // Configurar reloj
    actualizarReloj();
    setInterval(actualizarReloj, 1000);
    
    // Configurar event listeners
    configurarEventListeners();
    
    // Cargar datos iniciales
    cargarDatos();
    
    // Configurar actualización automática
    setInterval(cargarDatos, CONFIG.REFRESH_INTERVAL);
});

// ==============================================
// FUNCIONES DE DATOS
// ==============================================

async function cargarDatos() {
    try {
        // Cargar estudiantes y asistencias en paralelo
        const [estudiantesRes, asistenciasRes] = await Promise.all([
            fetch(`${CONFIG.API_URL}/api/estudiantes`),
            fetch(`${CONFIG.API_URL}/api/asistencia/hoy`)
        ]);
        
        if (!estudiantesRes.ok || !asistenciasRes.ok) {
            throw new Error('Error al cargar datos');
        }
        
        const estudiantesData = await estudiantesRes.json();
        const asistenciasData = await asistenciasRes.json();
        
        state.estudiantes = estudiantesData.estudiantes || [];
        state.asistencias = asistenciasData.asistencias || [];
        
        // Actualizar UI
        actualizarEstadisticas();
        renderizarListaAsistencia();
        renderizarUltimosRegistros();
        actualizarEstadoConexion(true);
        
        // Actualizar timestamp
        document.getElementById('ultima-actualizacion').textContent = 
            new Date().toLocaleTimeString('es-CL');
        
    } catch (error) {
        console.error('Error cargando datos:', error);
        actualizarEstadoConexion(false);
        mostrarToast('Error al conectar con el servidor', 'error');
    }
}

// ==============================================
// RENDERIZADO
// ==============================================

function renderizarListaAsistencia() {
    const tbody = document.getElementById('lista-estudiantes');
    
    if (state.estudiantes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="mensaje-vacio">No hay estudiantes registrados</td></tr>';
        return;
    }
    
    // Crear mapa de asistencias para búsqueda rápida
    const asistenciasMap = {};
    state.asistencias.forEach(asistencia => {
        asistenciasMap[asistencia.id_estudiante] = asistencia;
    });
    
    // Filtrar estudiantes según búsqueda
    let estudiantesFiltrados = state.estudiantes;
    
    if (state.busqueda) {
        const busqueda = state.busqueda.toLowerCase();
        estudiantesFiltrados = estudiantesFiltrados.filter(est => 
            est.nombre_completo.toLowerCase().includes(busqueda) ||
            (est.rut && est.rut.includes(busqueda))
        );
    }
    
    // Filtrar según estado
    if (state.filtroActivo === 'presentes') {
        estudiantesFiltrados = estudiantesFiltrados.filter(est => 
            asistenciasMap[est.id_estudiante]
        );
    } else if (state.filtroActivo === 'ausentes') {
        estudiantesFiltrados = estudiantesFiltrados.filter(est => 
            !asistenciasMap[est.id_estudiante]
        );
    }
    
    // Renderizar filas
    if (estudiantesFiltrados.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="mensaje-vacio">No se encontraron resultados</td></tr>';
        return;
    }
    
    tbody.innerHTML = estudiantesFiltrados.map(estudiante => {
        const asistencia = asistenciasMap[estudiante.id_estudiante];
        const presente = !!asistencia;
        
        return `
            <tr>
                <td>
                    <span class="estado-badge ${presente ? 'presente' : 'ausente'}">
                        ${presente ? '✅ Presente' : '❌ Ausente'}
                    </span>
                </td>
                <td>${estudiante.nombre_completo}</td>
                <td>${estudiante.rut || 'N/A'}</td>
                <td>
                    ${presente 
                        ? `<span class="hora-ingreso">${asistencia.hora_ingreso}</span>`
                        : '<span class="hora-ingreso">--</span>'
                    }
                </td>
            </tr>
        `;
    }).join('');
}

function renderizarUltimosRegistros() {
    const container = document.getElementById('ultimos-registros');
    
    if (state.asistencias.length === 0) {
        container.innerHTML = '<p class="mensaje-vacio">No hay registros hoy</p>';
        return;
    }
    
    // Tomar los últimos N registros
    const ultimosRegistros = state.asistencias
        .slice(0, CONFIG.MAX_REGISTROS_RECIENTES);
    
    container.innerHTML = ultimosRegistros.map(asistencia => `
        <div class="registro-item">
            <div>
                <div class="nombre">${asistencia.nombre_completo}</div>
                <div class="hora">${asistencia.dispositivo_id || 'Desconocido'}</div>
            </div>
            <div class="hora">${asistencia.hora_ingreso}</div>
        </div>
    `).join('');
}

function actualizarEstadisticas() {
    const totalEstudiantes = state.estudiantes.length;
    const totalPresentes = state.asistencias.length;
    const totalAusentes = totalEstudiantes - totalPresentes;
    
    document.getElementById('total-presentes').textContent = totalPresentes;
    document.getElementById('total-ausentes').textContent = totalAusentes;
}

function actualizarEstadoConexion(online) {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.getElementById('status-text');
    
    if (online) {
        statusIndicator.classList.add('online');
        statusIndicator.classList.remove('offline');
        statusText.textContent = 'Conectado al servidor';
    } else {
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('offline');
        statusText.textContent = 'Sin conexión';
    }
}

// ==============================================
// UTILIDADES
// ==============================================

function actualizarReloj() {
    const ahora = new Date();
    
    const fecha = ahora.toLocaleDateString('es-CL', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    const hora = ahora.toLocaleTimeString('es-CL');
    
    document.getElementById('fecha-actual').textContent = 
        fecha.charAt(0).toUpperCase() + fecha.slice(1);
    document.getElementById('hora-actual').textContent = hora;
}

function mostrarToast(mensaje, tipo = 'success') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    
    const icon = tipo === 'success' ? '✅' : '❌';
    
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <div class="toast-message">${mensaje}</div>
    `;
    
    container.appendChild(toast);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ==============================================
// EVENT LISTENERS
// ==============================================

function configurarEventListeners() {
    // Buscador
    const inputBuscar = document.getElementById('buscar-estudiante');
    inputBuscar.addEventListener('input', (e) => {
        state.busqueda = e.target.value;
        renderizarListaAsistencia();
    });
    
    // Filtros de estado
    const filtros = document.querySelectorAll('input[name="filtro"]');
    filtros.forEach(filtro => {
        filtro.addEventListener('change', (e) => {
            state.filtroActivo = e.target.value;
            renderizarListaAsistencia();
        });
    });
}

// ==============================================
// POLLING PARA NUEVOS REGISTROS
// ==============================================

let ultimaCantidadAsistencias = 0;

// Detectar nuevos registros
function verificarNuevosRegistros() {
    const cantidadActual = state.asistencias.length;
    
    if (cantidadActual > ultimaCantidadAsistencias && ultimaCantidadAsistencias > 0) {
        // Hay nuevos registros
        const nuevoRegistro = state.asistencias[0];
        mostrarToast(`${nuevoRegistro.nombre_completo} registrado`, 'success');
        
        // Reproducir sonido (opcional)
        reproducirSonidoRegistro();
    }
    
    ultimaCantidadAsistencias = cantidadActual;
}

function reproducirSonidoRegistro() {
    // Crear un beep corto (opcional)
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
    } catch (error) {
        // Ignorar errores de audio
    }
}

// Ejecutar verificación después de cada carga de datos
const originalCargarDatos = cargarDatos;
cargarDatos = async function() {
    await originalCargarDatos();
    verificarNuevosRegistros();
};

console.log('✅ Aplicación inicializada');