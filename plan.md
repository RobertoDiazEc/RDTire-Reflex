# RDTire-Trading - Sistema de Gestión de Inspección de Llantas

## Visión General del Proyecto
Sistema completo de gestión de llantas con autenticación de usuarios, roles diferenciados, registro de vehículos, inspección de llantas y seguimiento de vida útil basado en profundidad de banda de rodadura (1.03mm límite).

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

## Fase 3: Sistema de Inspección y Control de Vida Útil ⏳
- [ ] Crear página de inspección de llantas (acceso: Admin y Usuario Técnico)
- [ ] Implementar formulario de inspección con medición de profundidad (mm)
- [ ] Agregar validación automática de vida útil (alerta si ≤ 1.03mm)
- [ ] Crear sistema de alertas visuales para llantas en límite de vida útil
- [ ] Implementar historial de inspecciones por llanta con gráficas de desgaste
- [ ] Agregar reportes de inspección con fecha, técnico responsable y observaciones
- [ ] Crear dashboard de alertas con llantas que requieren reemplazo inmediato
- [ ] Implementar notificaciones de mantenimiento preventivo

---

## Notas Técnicas
- **Profundidad mínima legal**: 1.03mm (alerta crítica)
- **Roles y Permisos**:
  - **Administrador**: Acceso total al sistema
  - **Usuario Administrador**: Gestión de vehículos y llantas
  - **Usuario Técnico**: Realización de inspecciones
- **Estados de llanta**: Nueva, En uso, Advertencia (< 2mm), Crítica (≤ 1.03mm), Reemplazada
- **Datos de inspección**: Profundidad (4 puntos por llanta), presión, daños visibles, fecha, técnico
