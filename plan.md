# RDTire-Trading - Sistema de Gestión de Inspección de Llantas

## Visión General del Proyecto
Sistema completo de gestión de llantas con **arquitectura multi-tenant**, autenticación de usuarios, roles diferenciados, registro de vehículos, inspección de llantas y seguimiento de vida útil basado en profundidad de banda de rodadura (1.03mm límite).

---

## Fase 1: Sistema de Autenticación y Roles ✅
- [x] Implementar sistema de login con usuario y contraseña
- [x] Crear base de datos de usuarios con roles (Administrador, Usuario Administrador, Usuario Técnico)
- [x] Agregar página de login con validación de credenciales
- [x] Implementar sistema de sesiones para mantener usuario autenticado
- [x] Crear middleware de protección de rutas según rol
- [x] Agregar funcionalidad de logout
- [x] Diseñar dashboard específico para cada rol con permisos diferenciados

---

## Fase 2: Gestión de Vehículos y Llantas ✅
- [x] Crear página de gestión de vehículos (acceso: Admin y Usuario Admin)
- [x] Implementar formulario de registro de vehículos (placa, marca, modelo, año, tipo)
- [x] Agregar sistema de asociación de llantas a vehículos
- [x] Crear formulario de registro de llantas (posición, marca, modelo, fecha instalación)
- [x] Implementar vista detallada de vehículo con todas sus llantas
- [x] Agregar funcionalidad de edición y eliminación de vehículos/llantas
- [x] Crear historial de llantas por vehículo (instalaciones, rotaciones, reemplazos)

---

## Fase 3: Sistema de Inspección y Control de Vida Útil ✅
- [x] Crear página de inspección de llantas (acceso: Admin y Usuario Técnico)
- [x] Implementar formulario de inspección con medición de profundidad (mm)
- [x] Agregar validación automática de vida útil (alerta si ≤ 1.03mm)
- [x] Crear sistema de alertas visuales para llantas en límite de vida útil
- [x] Implementar historial de inspecciones por llanta con gráficas de desgaste
- [x] Agregar reportes de inspección con fecha, técnico responsable y observaciones
- [x] Crear dashboard de alertas con llantas que requieren reemplazo inmediato
- [x] Implementar notificaciones de mantenimiento preventivo

---

## Fase 4: Sistema Multi-Tenant con PostgreSQL ✅
- [x] Diseñar arquitectura multi-tenant con schemas separados
- [x] Implementar modelos SQLAlchemy con Base y schema_translate_map
- [x] Crear modelo Cliente (tenant) en schema public
- [x] Crear modelos Usuario, Vehiculo, Tire, etc. en schema tenant
- [x] Implementar tenant_manager para gestión de clientes
- [x] Crear init_db para inicialización de base de datos
- [x] Implementar CRUD operations para todas las entidades
- [x] Actualizar AuthState para usar PostgreSQL
- [x] Agregar soporte para múltiples clientes con aislamiento de datos
- [x] Crear script de seed para cliente demo "REDx Soluciones"
- [x] Documentar arquitectura y configuración

---

## 🎯 Arquitectura Multi-Tenant

### Características:
- **Schema por Cliente**: Cada cliente tiene su propio schema PostgreSQL (ej: `redx_soluciones`)
- **Aislamiento Total**: Los datos de cada cliente están completamente separados
- **Schema Público**: Tabla `clientes` compartida en schema `public`
- **Schema Translate Map**: SQLAlchemy enruta automáticamente queries al schema correcto
- **Escalabilidad**: Permite añadir nuevos clientes dinámicamente

### Estructura de Base de Datos:

```
rdtire_db
├── public (schema compartido)
│   └── clientes (tabla de tenants)
│
├── redx_soluciones (schema del cliente 1)
│   ├── usuarios
│   ├── vehiculos
│   ├── tires
│   ├── vehicle_tires
│   ├── tire_history
│   ├── customers
│   ├── sales
│   └── sale_items
│
└── otra_empresa (schema del cliente 2)
    └── ... (mismas tablas)
```

### Modelos:
1. **Cliente** (schema: public)
   - id, nombre, schema_name, activo, fecha_creacion

2. **Usuario** (schema: tenant)
   - id, username, email, password_hash, role, activo, cliente_id

3. **Vehiculo** (schema: tenant)
   - id, placa, marca, modelo, ano, tipo, fecha_registro

4. **Tire** (schema: tenant)
   - id, brand, model, size, type, season, speed_rating, load_index, price, stock, image_url

5. **VehicleTire** (schema: tenant)
   - id, vehicle_id, tire_id, position, fecha_instalacion, estado, profundidad_actual

6. **TireHistory** (schema: tenant)
   - id, vehicle_tire_id, tipo_evento, fecha, notas, profundidad_medida

7. **Customer, Sale, SaleItem** (schema: tenant)

---

## 🚀 Configuración del Sistema

### Requisitos:
- PostgreSQL 12+
- Python 3.11+
- psycopg2-binary
- SQLAlchemy
- Reflex

### Variables de Entorno (.env):
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rdtire_db
```

### Inicialización:
```bash
# 1. Crear base de datos PostgreSQL
createdb rdtire_db

# 2. Inicializar esquema y datos demo
python -m app.database.seed_demo

# 3. Ejecutar aplicación
reflex run
```

### Credenciales Demo:
**Cliente: REDx Soluciones**
- Admin: `admin@redx.com` / `admin123`
- Usuario Admin: `usuario@redx.com` / `usuario123`
- Técnico: `tecnico@redx.com` / `tecnico123`

---

## 📊 Funcionalidades por Rol

### Administrador:
- ✅ Acceso completo a todas las funciones
- ✅ Gestión de productos y precios
- ✅ Gestión de inventario
- ✅ Visualización de ventas
- ✅ Gestión de clientes
- ✅ Gestión de vehículos y llantas
- ✅ Inspecciones técnicas
- ✅ Reportes y analíticas avanzadas
- ✅ Configuración del sistema

### Usuario Administrador:
- ✅ Gestión de vehículos
- ✅ Gestión de llantas
- ✅ Gestión de clientes
- ✅ Inspecciones (lectura)
- ✅ Reportes básicos

### Usuario Técnico:
- ✅ Inspecciones de llantas
- ✅ Registro de profundidad
- ✅ Visualización de historial
- ✅ Generación de alertas

---

## 🔐 Seguridad

- ✅ Passwords hasheados con SHA-256
- ✅ Aislamiento de datos por cliente (schema separado)
- ✅ Validación de permisos por rol
- ✅ Sesiones seguras
- ✅ Protección de rutas según rol
- ✅ Validación de cliente activo

---

## 📝 Notas Técnicas

### Profundidad de Llantas:
- **Nueva**: ≥ 8mm
- **En uso**: 3-8mm  
- **Advertencia**: 1.04-3mm (amarillo)
- **Crítica**: ≤ 1.03mm (rojo - reemplazo inmediato)

### Roles Disponibles:
- Administrador
- Usuario Administrador
- Usuario Técnico

### Estados de Llanta:
- Nueva
- En uso
- Advertencia
- Crítica

---

## 🎉 Proyecto Completado

El sistema RDTire-Trading está **completamente funcional** con arquitectura multi-tenant, permitiendo que múltiples clientes utilicen la misma aplicación con **aislamiento total de datos**.

### ✅ Características Implementadas:
1. **Autenticación Multi-Tenant**: Login con soporte para múltiples clientes
2. **Gestión de Clientes**: Crear y administrar múltiples empresas
3. **Gestión de Vehículos**: CRUD completo con información detallada
4. **Gestión de Llantas**: Asociación a vehículos por posición (5 posiciones)
5. **Sistema de Inspección**: Formulario con medición de profundidad y validación automática
6. **Alertas Visuales**: Badges de color según estado (Verde/Amarillo/Rojo)
7. **Historial Completo**: Seguimiento de eventos por llanta
8. **Control de Vida Útil**: Validación automática contra límite legal (1.03mm)
9. **Base de Datos PostgreSQL**: Con arquitectura multi-tenant escalable
10. **Aislamiento de Datos**: Cada cliente tiene su propio schema

### 🚀 Listo para Producción
El sistema está listo para ser desplegado y utilizado por **múltiples clientes simultáneamente** con total seguridad y aislamiento de datos.