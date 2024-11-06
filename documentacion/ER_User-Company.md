# **Modelos y Entidades - Partner App**

Este documento describe los modelos y las relaciones necesarias para implementar las historias de usuario definidas para el módulo de **Usuarios y Empresas** en la aplicación.

---

## **1. Modelos y Tablas**

### **Módulo `Accounts`**

Este módulo contiene toda la gestión de usuarios, empresas y cuentas, que son las entidades base para el sistema.

#### **1.1. Usuario (Auth0)**
**Tabla:** `usuario_auth0`  
Almacena la información esencial de los usuarios gestionada por Auth0.

| Atributo | Tipo de Dato          | Descripción                                      |
|----------|------------------------|--------------------------------------------------|
| id       | UUID PRIMARY KEY       | Identificador único del usuario.                 |
| email    | VARCHAR(255) UNIQUE    | Correo electrónico del usuario (identificador).  |

---

#### **1.2. Usuario (Datos Adicionales)**
**Tabla:** `user_profiles`  
Almacena los datos adicionales no gestionados por Auth0.

| Atributo       | Tipo de Dato       | Descripción                       |
|----------------|--------------------|-----------------------------------|
| id             | UUID PRIMARY KEY   | Mismo ID que en `usuario_auth0`.  |
| first_name     | VARCHAR(100)       | Nombre del usuario.               |
| last_name      | VARCHAR(100)       | Apellido del usuario.             |
| phone          | VARCHAR(15)        | Número de teléfono del usuario.   |

---

#### **1.3. Empresa**
**Tabla:** `companies`  
Almacena la información de las empresas registradas.

| Atributo      | Tipo de Dato        | Descripción                        |
|---------------|---------------------|------------------------------------|
| id            | SERIAL PRIMARY KEY  | Identificador único de la empresa. |
| legal_name    | VARCHAR(255)        | Nombre de la empresa.              |
| tax_id        | VARCHAR(12) UNIQUE  | RUT único de la empresa.           |
| is_active     | BOOLEAN             | Activo/Inactivo.                   |
| created_at    | TIMESTAMP           | Fecha de creación de la empresa.   |
| supplier_id   | INTEGER             | FK hacia `suppliers`, NULL si no es proveedor |
| buyer_id      | INTEGER             | FK hacia `buyers`, NULL si no es comprador    |

---

#### **1.4. Cuenta**
**Tabla:** `accounts`  
Gestiona la relación de cada usuario con una empresa. Si no hay empresa asociada, la cuenta representa una operación como persona natural.

| Atributo        | Tipo de Dato         | Descripción                                     |
|-----------------|----------------------|-------------------------------------------------|
| id              | SERIAL PRIMARY KEY   | Identificador único de la cuenta.               |
| user_profile_id | UUID                 | FK hacia `user_profiles`.                       |
| company_id      | INTEGER              | FK hacia `companies`, NULL si es cuenta personal|
| is_active       | BOOLEAN              | Activo/Inactivo.                                |

---

### **Módulo `Supplier`**

Este módulo gestiona los datos específicos y funcionalidades de los proveedores.

#### **2.1. Proveedor**
**Tabla:** `suppliers`  
Define el perfil de proveedor asociado a una empresa que actúa como vendedora en la plataforma.

| Atributo      | Tipo de Dato        | Descripción                                    |
|---------------|---------------------|------------------------------------------------|
| id            | SERIAL PRIMARY KEY  | Identificador único del perfil de proveedor.   |
| company_id    | INTEGER             | FK hacia `companies`, vínculo con empresa.     |
| description   | TEXT                | Descripción de los servicios del proveedor.    |
| keywords      | VARCHAR(255)        | Palabras clave para búsqueda.                  |
| category      | VARCHAR(50)         | Categoría de productos o servicios.            |

---

### **Módulo `Buyer`**

Este módulo gestiona los datos específicos de los compradores.

#### **3.1. Comprador**
**Tabla:** `buyers`  
Define el perfil de comprador asociado a una empresa que actúa como compradora en la plataforma.

| Atributo      | Tipo de Dato        | Descripción                                    |
|---------------|---------------------|------------------------------------------------|
| id            | SERIAL PRIMARY KEY  | Identificador único del perfil de comprador.   |
| company_id    | INTEGER             | FK hacia `companies`, vínculo con empresa.     |

---

## **2. Relaciones Clave**

1. **Company ↔ Supplier/Buyer (1:1)**:
   - **`Company` tiene FK opcional hacia `Supplier` y `Buyer`**: Esto permite identificar si una empresa actúa como proveedor, comprador o ambos.
   - **`Supplier` y `Buyer` también tienen FK a `Company`**: Esto permite que ambas entidades estén vinculadas a la misma empresa y facilita el acceso a información general de `Company`.

2. **Usuario ↔ Empresa (1:N a través de Cuenta)**:
   - Un usuario puede tener múltiples cuentas asociadas a diferentes empresas.
   - Una empresa puede tener múltiples usuarios (cuentas) vinculados a través de `Account`.

---

## **3. Reglas de Negocio y Funciones**

1. **Gestión de Acceso por Estado**:  
   - Las cuentas pueden activarse o desactivarse; un usuario solo podrá operar en la empresa donde tenga una cuenta activa.

2. **Validación de RUT de Empresas**:  
   - Las empresas deben tener un RUT único y válido para registrarse en la plataforma.

---

Este diseño asegura que cada usuario pueda operar en distintos contextos, según las actividades específicas de su empresa (`Supplier` o `Buyer`), manteniendo la integridad en la gestión de acceso y relación entre entidades.
