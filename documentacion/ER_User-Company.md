# **Modelo de Usuarios y Empresas - Partner App**

Este archivo describe en detalle los modelos, tablas, relaciones y reglas de negocio para la gestión de **Usuarios** y **Empresas** en la plataforma.

---

## **1. Modelos y Tablas**

### **1.1. Usuario (Auth0)**  
**Tabla:** `usuario_auth0`  
Almacena la información esencial del usuario gestionada a través de Auth0.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | UUID PRIMARY KEY   | Identificador único del usuario. |
| email             | VARCHAR(255) UNIQUE | Correo del usuario.             |
| estado            | BOOLEAN            | Activo/Inactivo.                 |
| creado_en         | TIMESTAMP          | Fecha de creación.               |

---

### **1.2. Usuario (Datos Adicionales)**  
**Tabla:** `usuarios`  
Almacena la información adicional de los usuarios que no es manejada por Auth0.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | UUID PRIMARY KEY   | Mismo ID que en `usuario_auth0`. |
| nombre            | VARCHAR(100)       | Nombre completo del usuario.     |
| rut               | VARCHAR(12) UNIQUE | RUT del usuario (validación nacional). |
| creado_en         | TIMESTAMP          | Fecha de creación del registro.  |

---

### **1.3. Empresa**  
**Tabla:** `empresas`  
Contiene la información básica de las empresas registradas en la plataforma.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único de la empresa. |
| nombre            | VARCHAR(255)       | Nombre de la empresa.            |
| rut               | VARCHAR(12) UNIQUE | RUT de la empresa.               |
| estado            | BOOLEAN            | Activo/Inactivo.                 |
| creado_en         | TIMESTAMP          | Fecha de creación.               |

---

### **1.4. Dirección de Empresa (Matriz)**  
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

### **1.6. Rol**  
**Tabla:** `roles`  
Define los roles que pueden asignarse a los usuarios dentro de las empresas.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único del rol.     |
| nombre            | VARCHAR(100)       | Nombre del rol.                  |
| descripcion       | TEXT               | Descripción del rol.             |
| transferible      | BOOLEAN            | Indica si el rol puede ser transferido. |

---

### **1.7. Permiso**  
**Tabla:** `permisos`  
Define los permisos específicos asociados a los roles.

| Atributo          | Tipo de Dato       | Descripción                       |
|-------------------|--------------------|-----------------------------------|
| id                | SERIAL PRIMARY KEY | Identificador único del permiso. |
| nombre            | VARCHAR(100)       | Nombre del permiso.              |
| tipo              | VARCHAR(50)        | Visualizar / Operar.             |

---

## **2. Reglas de Negocio y Funciones**  

1. **Asignación de Roles Múltiples:**  
   - Un usuario puede tener varios roles dentro de una empresa.  
   - Los permisos asociados a esos roles se combinan para definir el acceso final.

2. **Usuarios en Múltiples Empresas:**  
   - Un usuario puede trabajar para varias empresas. Cada relación mantiene su estado y roles.

3. **Permisos por Tipo:**  
   - Los permisos se dividen en **Visualización** y **Operación**, permitiendo una configuración granular.

4. **Estado de Usuario:**  
   - Si un usuario pierde todas sus asociaciones con empresas, solo podrá operar como persona natural o buscar nuevas asociaciones.

5. **Índices:**  
   - Se deben crear índices en los campos `email` y `rut` para optimizar las consultas.

6. **Integridad Referencial:**  
   - Las relaciones entre tablas se asegurarán mediante **restricciones FOREIGN KEY**.

7. **Migraciones:**  
   - Todas las tablas deben ser gestionadas mediante migraciones para mantener la coherencia del esquema.

---

## **3. Esquema de Relaciones Clave**  

1. **Usuario ↔ Empresa (N:M):**  
   - Un usuario puede estar asociado a varias empresas.  
   - Una empresa puede tener múltiples usuarios.

2. **Usuario ↔ Rol (N:M):**  
   - Un usuario puede tener varios roles asignados dentro de una empresa.  
   - Los roles definen qué acciones puede realizar cada usuario.

3. **Rol ↔ Permiso (1:N):**  
   - Un rol tiene múltiples permisos asociados.

4. **Empresa ↔ Dirección (1:1):**  
   - Cada empresa tiene una única dirección de casa matriz.

---

## **4. Esquema en PostgreSQL**  
Este diseño será implementado utilizando **PostgreSQL** como base de datos relacional. Las relaciones **N:M** se manejarán mediante tablas intermedias para mantener la flexibilidad del modelo.

---

Fin del documento.
