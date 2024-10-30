# **Historias de Usuario - Módulo de Usuarios y Empresas - Partner App**

## **1. Registro, Autenticación y Creación de Empresas (RAC)**

### **RAC-01**: Registro y Autenticación
1. Como **usuario**, quiero registrarme en la plataforma utilizando mi email y contraseña mediante Auth0, para acceder a la aplicación.
2. Como **usuario**, quiero poder recuperar mi contraseña en caso de haberla olvidado, mediante un flujo de recuperación en Auth0.
3. Como **usuario autenticado**, quiero iniciar sesión con mis credenciales para acceder a mis empresas asociadas o como persona natural.

### **RAC-02**: Creación de Empresa
4. Como **usuario registrado**, quiero crear una empresa a través de un formulario con los datos necesarios para revisión.
5. Como **equipo de revisión**, quiero validar y aprobar o rechazar la solicitud de creación de la empresa.
6. Como **usuario creador**, quiero ser asignado automáticamente como administrador de la empresa aprobada.

---

## **2. Asociación de Usuarios a Empresas (AUE)**

### **AUE-01**: Gestión de Asociaciones
7. Como **administrador**, quiero invitar a nuevos usuarios a unirse a mi empresa mediante email.
8. Como **usuario**, quiero aceptar una invitación para unirme a una empresa y comenzar a trabajar en ella.
9. Como **usuario**, quiero desvincularme de una empresa en cualquier momento para dejar de trabajar con ella.
10. Como **usuario**, quiero tener múltiples canales de operación: ser parte de varias empresas o gestionar mis actividades como persona natural.

---

## **3. Roles y Permisos de Usuarios (RPU)**

### **RPU-01**: Gestión de Roles y Permisos
11. Como **administrador**, quiero asignar roles específicos a los usuarios de mi empresa (Ej: Analista de Compras, Vendedor).
12. Como **administrador**, quiero editar los roles de los usuarios en cualquier momento para ajustar sus permisos.
13. Como **usuario**, quiero tener múltiples roles dentro de la misma empresa para realizar distintas funciones.
14. Como **administrador**, quiero transferir roles a otros usuarios, como el rol de administrador, para delegar responsabilidades.
15. Como **usuario**, quiero ver los permisos asociados a mis roles para saber qué acciones puedo realizar.

---

## **4. Gestión del Estado del Usuario (GEU)**

### **GEU-01**: Manejo de Estados
16. Como **usuario**, quiero poder cambiar mi estado entre activo e inactivo en una empresa específica.
17. Como **administrador**, quiero inactivar usuarios para restringir temporalmente su acceso.
18. Como **usuario sin empresa**, quiero ver un mensaje que me indique que debo unirme a una empresa o continuar operando como persona natural.
19. Como **administrador**, quiero recibir notificaciones cuando un usuario se asocie o desvincule de mi empresa.

---

## **5. Gestión de Empresas y Direcciones (GED)**

### **GED-01**: Gestión de Empresas
20. Como **administrador**, quiero registrar y editar los datos de la empresa, incluyendo nombre, RUT y tipo de empresa.
21. Como **usuario con permisos**, quiero consultar el listado de todas las empresas en las que estoy asociado.
22. Como **administrador**, quiero eliminar una empresa, lo que desvinculará automáticamente a todos los usuarios asociados.

### **GED-02**: Gestión de Dirección
23. Como **administrador**, quiero registrar la dirección de la casa matriz de la empresa (región, comuna, latitud, longitud).
24. Como **administrador**, quiero actualizar los datos de la dirección en cualquier momento.
25. Como **usuario**, quiero poder ver la dirección registrada de la casa matriz para conocer su ubicación.

---

## **6. Optimización y Accesibilidad (OA)**

### **OA-01**: Validaciones y Búsqueda
26. Como **usuario**, quiero que mi correo y RUT estén verificados y validados al momento de registrarme para evitar errores.
27. Como **administrador**, quiero buscar usuarios por nombre o correo para gestionar más fácilmente sus roles.

### **OA-02**: Restricciones y Exportaciones
28. Como **administrador**, quiero que los usuarios no puedan eliminar su propia cuenta si son los únicos administradores de una empresa.
29. Como **usuario**, quiero poder exportar un informe con todos los roles y permisos que tengo en cada empresa.
30. Como **administrador**, quiero recibir alertas si se intenta registrar un RUT duplicado en la plataforma.
31. Como **usuario inactivo**, quiero que se me informe si mi cuenta ha sido suspendida en alguna empresa.

