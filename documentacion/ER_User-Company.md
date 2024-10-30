# **Modelos y Entidades - Usuarios y Empresas - Partner App**

Este documento describe los modelos y las relaciones necesarias para implementar todas las historias de usuario definidas para el módulo de **Usuarios y Empresas**.

---

## **1. Modelos y Tablas**

### **1.1. Usuario (Auth0)**
**Tabla:** `usuario_auth0`  
Almacena la información esencial de los usuarios gestionada por Auth0.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | UUID PRIMARY KEY   | Identificador único del usuario. |
| email             | VARCHAR(255) UNIQUE | Correo electrónico del usuario. |
| estado            | BOOLEAN            | Activo/Inactivo.                 |
| creado_en         | TIMESTAMP          | Fecha de creación del usuario.   |
| password_hash     | TEXT               | Hash de la contraseña (opcional para Auth0). |

**Nota:** La gestión de contraseñas es delegada a **Auth0**. En caso de manejar contraseñas localmente, el **hash** se almacena en el campo `password_hash`.

---

### **1.2. Usuario (Datos Adicionales)**
**Tabla:** `usuarios`  
Almacena los datos adicionales no gestionados por Auth0.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | UUID PRIMARY KEY   | Mismo ID que en `usuario_auth0`. |
| nombre            | VARCHAR(100)       | Nombre del usuario.              |
| rut               | VARCHAR(12) UNIQUE | RUT del usuario validado.        |
| creado_en         | TIMESTAMP          | Fecha de creación del registro.  |

---

### **1.3. Empresa**
**Tabla:** `empresas`  
Almacena la información de las empresas registradas.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único de la empresa. |
| nombre            | VARCHAR(255)       | Nombre de la empresa.            |
| rut               | VARCHAR(12) UNIQUE | RUT único de la empresa.         |
| estado            | BOOLEAN            | Activo/Inactivo.                 |
| creado_en         | TIMESTAMP          | Fecha de creación de la empresa. |

---

### **1.4. Dirección de Empresa**
**Tabla:** `direcciones`  
Define la dirección de la casa matriz de las empresas.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único de la dirección. |
| empresa_id        | INTEGER            | FK hacia `empresas`.             |
| region            | VARCHAR(100)       | Región de la dirección.          |
| comuna            | VARCHAR(100)       | Comuna de la dirección.          |
| direccion         | VARCHAR(255)       | Dirección específica.            |
| latitud           | FLOAT              | Latitud geográfica.              |
| longitud          | FLOAT              | Longitud geográfica.             |

---

### **1.5. Usuario-Empresa**
**Tabla:** `usuarios_empresas`  
Gestión de la relación N:M entre usuarios y empresas.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único de la relación. |
| usuario_id        | UUID               | FK hacia `usuarios`.             |
| empresa_id        | INTEGER            | FK hacia `empresas`.             |
| estado            | BOOLEAN            | Activo/Inactivo en la empresa.   |
| creado_en         | TIMESTAMP          | Fecha de asociación.             |

---

### **1.6. Roles**
**Tabla:** `roles`  
Define los roles que pueden asignarse a los usuarios dentro de las empresas.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único del rol.     |
| nombre            | VARCHAR(100)       | Nombre del rol.                  |
| descripcion       | TEXT               | Descripción del rol.             |
| transferible      | BOOLEAN            | Indica si el rol es transferible.|

---

### **1.7. Permisos**
**Tabla:** `permisos`  
Define los permisos específicos que pueden ser asociados a los roles.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único del permiso. |
| nombre            | VARCHAR(100)       | Nombre del permiso.              |
| tipo              | VARCHAR(50)        | Visualizar / Operar.             |

---

### **1.8. Notificaciones**
**Tabla:** `notificaciones`  
Gestiona las notificaciones enviadas a los usuarios sobre eventos importantes.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único de la notificación. |
| usuario_id        | UUID               | FK hacia `usuarios`.             |
| mensaje           | TEXT               | Contenido de la notificación.    |
| leido             | BOOLEAN            | Indica si la notificación fue leída. |
| fecha_hora        | TIMESTAMP          | Fecha y hora de la notificación. |

---

## **2. Relaciones Clave**

1. **Usuario ↔ Empresa (N:M):**  
   - Un usuario puede estar asociado a varias empresas.
   - Una empresa puede tener múltiples usuarios.

2. **Usuario ↔ Rol (N:M):**  
   - Cada usuario puede tener varios roles en una empresa.
   - Los roles definen las acciones permitidas.

3. **Rol ↔ Permiso (1:N):**  
   - Un rol tiene múltiples permisos asignados.

4. **Empresa ↔ Dirección (1:1):**  
   - Cada empresa tiene una única dirección de casa matriz.

5. **Usuario ↔ Notificación (1:N):**  
   - Cada usuario puede tener múltiples notificaciones.

---

## **3. Reglas de Negocio y Funciones**

1. **Asignación de Roles Múltiples:**  
   - Los usuarios pueden tener varios roles dentro de una misma empresa.

2. **Gestión de Invitaciones:**  
   - Los administradores pueden invitar usuarios por email para unirse a la empresa.

3. **Validación de RUT:**  
   - Tanto los usuarios como las empresas deben tener un RUT válido y único.

4. **Estado de Usuario y Empresa:**  
   - Los usuarios pueden estar activos o inactivos en empresas específicas.
   - Las empresas pueden activarse o desactivarse según su estado.

5. **Notificaciones:**  
   - Las notificaciones se envían a los usuarios para eventos importantes, como cambios de estado o nuevas asociaciones.

---

## **4. Esquema en PostgreSQL**

Este diseño se implementará utilizando **PostgreSQL** como base de datos relacional. Las relaciones N:M se manejarán con tablas intermedias para mantener la flexibilidad del modelo.

---

Fin del documento.
