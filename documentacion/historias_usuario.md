# **Historias de Usuario - Módulo de Usuarios y Empresas - Partner App**

Este documento contiene todas las historias de usuario asociadas al módulo de **Usuarios y Empresas** para la Partner App, basadas en los modelos definidos. Cada historia sigue un formato claro para su implementación y está alineada con las funcionalidades previstas.

---

## **1. Historias de Usuario - Gestión de Usuarios**

### **1.1. Registro y Autenticación de Usuarios**
1. Como **usuario**, quiero registrarme en la plataforma utilizando mi email y contraseña mediante Auth0, para acceder a la aplicación.
2. Como **usuario autenticado**, quiero iniciar sesión con mis credenciales para acceder a mis empresas asociadas.
3. Como **usuario sin empresa**, quiero operar como persona natural para gestionar mis propias actividades comerciales.
4. Como **administrador**, quiero poder restablecer la contraseña de mis usuarios mediante Auth0, para garantizar el acceso.

### **1.2. Asociación de Usuarios a Empresas**
5. Como **administrador**, quiero invitar a nuevos usuarios a unirse a mi empresa mediante email.
6. Como **usuario**, quiero aceptar una invitación para unirme a una empresa y comenzar a trabajar en ella.
7. Como **usuario**, quiero desvincularme de una empresa en cualquier momento para dejar de trabajar con ella.
8. Como **usuario consultor**, quiero pertenecer a varias empresas para ofrecer servicios a múltiples clientes.

### **1.3. Roles y Permisos de Usuarios**
9. Como **administrador de empresa**, quiero asignar roles específicos a los usuarios de mi empresa (Ej: Analista de Compras, Vendedor).
10. Como **administrador**, quiero editar los roles de los usuarios en cualquier momento para ajustar sus permisos.
11. Como **usuario**, quiero tener múltiples roles dentro de la misma empresa, para realizar distintas funciones.
12. Como **administrador**, quiero transferir roles a otros usuarios, como el rol de administrador, para delegar responsabilidades.
13. Como **usuario**, quiero ver los permisos asociados a mis roles para saber qué acciones puedo realizar.

### **1.4. Manejo del Estado del Usuario**
14. Como **usuario**, quiero poder cambiar mi estado entre activo e inactivo en una empresa específica.
15. Como **administrador**, quiero inactivar a usuarios para restringir temporalmente su acceso.
16. Como **usuario sin empresa**, quiero ver un mensaje que me indique que debo unirme a una empresa o continuar operando como persona natural.

---

## **2. Historias de Usuario - Gestión de Empresas**

### **2.1. Registro y Gestión de Empresas**
17. Como **administrador**, quiero registrar una nueva empresa en la plataforma para comenzar a operar.
18. Como **administrador**, quiero editar los datos de la empresa, incluyendo nombre, RUT y tipo de empresa.
19. Como **usuario con permisos**, quiero poder consultar el listado de todas las empresas en las que estoy asociado.
20. Como **administrador**, quiero eliminar una empresa, lo que desvinculará automáticamente a todos los usuarios asociados.

### **2.2. Dirección de Empresa (Casa Matriz)**
21. Como **administrador**, quiero registrar la dirección de la casa matriz de la empresa para facilitar la gestión.
22. Como **administrador**, quiero actualizar la región, comuna, dirección, latitud y longitud de la empresa.
23. Como **usuario**, quiero poder ver la dirección registrada de la casa matriz para conocer su ubicación.

---

## **3. Historias de Usuario - Roles y Permisos Personalizados**

24. Como **administrador**, quiero crear roles personalizados para ajustar los permisos a las necesidades de mi empresa.
25. Como **administrador**, quiero habilitar o deshabilitar permisos específicos para cada rol (Ej: Ver módulo de compras, Operar licitaciones).
26. Como **usuario con permisos**, quiero poder ver un listado de todos los roles y sus permisos asociados.
27. Como **administrador**, quiero eliminar roles que ya no sean necesarios para mi empresa.

---

## **4. Historias de Usuario - Estados Especiales y Trazabilidad**

28. Como **administrador**, quiero ver un historial de los cambios de roles de los usuarios para mantener un registro de las modificaciones.
29. Como **usuario**, quiero ver un historial de las empresas en las que he trabajado para conocer mi trayectoria.
30. Como **administrador**, quiero recibir notificaciones cuando un usuario se asocie o desvincule de mi empresa.

---

## **5. Historias de Usuario - Optimización y Accesibilidad**

31. Como **usuario**, quiero que mi correo y RUT estén verificados y validados al momento de registrarme para evitar errores.
32. Como **administrador**, quiero buscar usuarios por nombre o correo para gestionar más fácilmente sus roles.
33. Como **usuario sin empresa**, quiero recibir sugerencias para unirme a empresas activas según mi historial y habilidades.
34. Como **usuario con varios roles**, quiero cambiar rápidamente entre empresas en la UI para agilizar mi flujo de trabajo.

---

## **6. Consideraciones Técnicas y Restricciones**

35. Como **administrador**, quiero que los usuarios no puedan eliminar su propia cuenta si son los únicos administradores de una empresa.
36. Como **usuario**, quiero poder exportar un informe con todos los roles y permisos que tengo en cada empresa.
37. Como **administrador**, quiero recibir alertas si se intenta registrar un RUT duplicado en la plataforma.
38. Como **usuario inactivo**, quiero que se me informe si mi cuenta ha sido suspendida en alguna empresa.

---

## **Esquema en PostgreSQL**  
Este diseño se implementará utilizando **PostgreSQL** como base de datos relacional. Cada historia de usuario está alineada con los modelos previamente definidos para garantizar coherencia entre la lógica de la app y la base de datos.

---

Fin del documento.
