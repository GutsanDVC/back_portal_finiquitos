# Resumen del Proyecto

### 🎯Objetivos

- Automatizar el cálculo de finiquitos individuales y masivos.
- Usar listas desplegables y datos automáticos para evitar errores manuales.
- Validar causales según tipo de contrato con alertas en tiempo real.
- Generar Excel detallado por trabajador.
- Adaptar el sistema para uso escalable (más de 30 usuarios).
- Reutilizar motor de cálculo existente y centrar desarrollo en integración, interfaz y validaciones.

---

### 📥 Inputs

- **NP (Número de Personal)** – dato maestro clave.
- **Datos personales** – nombre, RUT, cargo, centro de costo.
- **Fechas** – ingreso y término.
- **Días de vacaciones pendientes** – sistema RRHH.
- **Años de servicio** – cálculo por fechas.
- **Tipo de contrato y causal de término** – desplegables validados.
- **Descuento AFC** – ingreso numérico manual obligatorio si aplica.
- **Perfil del usuario** – determina acceso a centros y personas.

---

### 📤 Outputs

- Cálculo detallado (vacaciones, indemnización, AFC, total).
- Excel exportable con todos los campos requeridos.
- Alertas de validación por causal incorrecta, fechas o falta de AFC.

---

### ⚙️ Reglas clave

- Causal incompatible con tipo de contrato → bloquea el cálculo.
- Descuento AFC no ingresado → alerta (no bloquea).
- Simulación de finiquito posible sin generar documento final.

---

### 👥 Perfiles

- **RRHH Obras**: acceso limitado por centro de costo.
- **Oficina Central**: acceso total, con trazabilidad de acciones.

---

### 🛠️ Stack Tecnológico

- **Backend:** Django Rest Framework - Framework Python para APIs REST
- **Frontend:** Vue.js con TypeScript - Framework JavaScript para interfaces de usuario
- **Base de Datos:** PostgreSQL - Sistema de gestión de bases de datos relacional
- **Auth:** Google OAuth 2.0 - Autenticación segura con cuentas corporativas Google Workspace