# Historias de Usuario - Plataforma de Gestión de Proveedores

## Historia de Usuario 1: Crear modelo de proveedor con datos extendidos asociados a un Auth ID
**Como** proveedor,  
**quiero** que mi perfil en la plataforma esté vinculado con mi Auth ID,  
**para** gestionar mi información específica sin necesidad de almacenar datos sensibles como mi correo o contraseña.

### Criterios de Aceptación:
- El Auth ID será utilizado como identificador principal para el proveedor.
- La información extendida debe incluir:
  - Nombre comercial.
  - Dirección.
  - Rubros/actividades específicos.
  - Descripción general de la empresa.
- Debe existir un endpoint `/provider/profile` que devuelva esta información extendida.

---

## Historia de Usuario 2: Implementación de roles en Auth0
**Como** administrador,  
**quiero** gestionar los roles de los usuarios desde Auth0,  
**para** definir los permisos y accesos de proveedores, compradores y administradores.

### Criterios de Aceptación:
- Los roles disponibles deben incluir:
  - **Proveedor:** acceso a perfil extendido y gestión de servicios.
  - **Comprador:** acceso a la búsqueda y compra de servicios.
  - **Administrador:** acceso a todas las funcionalidades del sistema.
- Los roles deben estar presentes en el token JWT para ser verificados mediante middleware.
- El backend debe validar los roles antes de permitir el acceso a recursos específicos.

---

## Historia de Usuario 3: Endpoint para modificar datos de autenticación (Auth0)
**Como** proveedor,  
**quiero** modificar mi correo, contraseña y otros datos desde la plataforma,  
**para** mantener mi perfil de autenticación actualizado sin salir del sistema.

### Criterios de Aceptación:
- El backend debe exponer un endpoint `/auth/update` que permita:
  - Modificar correo y contraseña.
  - Actualizar el nombre del perfil.
- El frontend debe confirmar la identidad del usuario antes de permitir cambios sensibles (por ejemplo, pedir la contraseña actual).
- El feedback debe ser claro, indicando el éxito o error de la operación.

---

## Historia de Usuario 4: Endpoint para obtener información extendida del proveedor
**Como** proveedor,  
**quiero** obtener mi información extendida desde el backend,  
**para** asegurar que mi perfil está actualizado y visible para los compradores.

### Criterios de Aceptación:
- El endpoint `/provider/profile` debe devolver:
  - Información específica (nombre comercial, dirección).
  - Rubros/actividades en los que opera.
  - Descripción general.
- El frontend debe consumir este endpoint y mostrar la información en la interfaz del perfil del proveedor.

---

## Historia de Usuario 5: CRUD para publicaciones de productos y servicios de un proveedor
**Como** proveedor,  
**quiero** gestionar publicaciones de productos y servicios,  
**para** mantener mi oferta clara y actualizada para los compradores.

### Criterios de Aceptación:
- Cada publicación debe incluir:
  - Título.
  - Descripción.
  - Estado (activo/inactivo).
  - Rubro al que pertenece.
- El CRUD debe permitir:
  - Crear, leer, actualizar y eliminar publicaciones.
- Las publicaciones deben estar vinculadas al perfil del proveedor y visibles en la plataforma.

---

## Historia de Usuario 6: Feed de publicaciones para proveedores
**Como** proveedor,  
**quiero** publicar en un feed general,  
**para** compartir actualizaciones, novedades y promociones con otros usuarios y compradores.

### Criterios de Aceptación:
- El feed debe mostrar publicaciones ordenadas por fecha.
- Cada publicación debe incluir:
  - Título.
  - Descripción.
  - Fecha de creación.
  - Rubro al que pertenece.
- Los proveedores deben poder:
  - Editar o eliminar sus publicaciones.
- El feed debe ser visible para compradores y proveedores, similar a un muro de LinkedIn.

---

## Historia de Usuario 7: Panel de Administración para Proveedores
**Como** proveedor,  
**quiero** un panel que muestre estadísticas de mi actividad,  
**para** tener una visión clara de mi desempeño.

### Criterios de Aceptación:
- El panel debe mostrar:
  - Número de servicios activos.
  - Publicaciones realizadas.
  - Última actualización del perfil.
- Debe existir un acceso rápido desde el panel para gestionar publicaciones y servicios.
- El panel debe ser accesible solo para usuarios con el rol de proveedor.

---

## Historia de Usuario 8: Búsqueda avanzada de proveedores por rubros y palabras clave
**Como** comprador,  
**quiero** buscar proveedores por rubro o términos específicos,  
**para** encontrar la oferta más adecuada a mis necesidades.

### Criterios de Aceptación:
- La búsqueda debe permitir filtros por:
  - Rubro.
  - Nombre comercial.
  - Palabras clave.
- El backend debe proporcionar un endpoint `/providers/search` con resultados paginados.
- A futuro, se implementará una IA que optimice los resultados según el perfil del comprador y los rubros del proveedor.
ta