# **Flujo de Operación - Partner App**

Este documento describe el flujo de operación en la plataforma, enfocándose en el rol de `Account` como la entidad operativa para usuarios y empresas.

---

## **1. Registro de Usuarios y Creación de Cuentas**

1. **Registro de Usuario**:
   - Un representante de una empresa se registra en la plataforma, proporcionando sus datos básicos como correo electrónico y contraseña.
   - Los datos iniciales se almacenan en la tabla `usuario_auth0` y luego en `user_profiles`, donde se guardan detalles adicionales como nombre, apellido y número de teléfono.

2. **Creación de la Cuenta (`Account`) y Vinculación con la Empresa (`Company`)**:
   - Una vez registrado, el usuario crea una `Account` vinculada a una `Company`.
   - Si la empresa ya está registrada, el usuario puede solicitar acceso o seleccionar la empresa.
   - Si la empresa no existe en la plataforma, el usuario puede crear un registro en `companies`, proporcionando datos clave como nombre legal y RUT (tax ID).
   
3. **Activación de la Cuenta**:
   - Cada `Account` tiene un campo `is_active` que indica si la cuenta está activa o inactiva. Solo cuentas activas permiten operar en la plataforma.

---

## **2. Configuración de la Empresa como `Supplier`, `Buyer`, o Ambos**

1. **Definición de Actividad**:
   - Al crear una `Company`, el usuario define si la empresa actuará como `Supplier`, `Buyer`, o ambos.
   - Las referencias a `Supplier` y `Buyer` se configuran en `companies` para indicar la actividad de la empresa en la plataforma.

2. **Perfil de Proveedor (`Supplier`)**:
   - Si la empresa se registra como `Supplier`, se crea un perfil en la tabla `suppliers`.
   - Este perfil incluye:
     - **Descripción de Servicios**: Explicación de los productos o servicios ofrecidos.
     - **Palabras Clave**: Términos para facilitar la búsqueda de sus servicios.
     - **Categoría**: Clasificación de productos o servicios.

3. **Perfil de Comprador (`Buyer`)**:
   - Si la empresa se registra como `Buyer`, se crea un perfil en la tabla `buyers`.
   - Esto permite que la empresa acceda a funcionalidades específicas para compradores, como la búsqueda de proveedores y la publicación de licitaciones.

---

## **3. Operación en la Plataforma con `Account`**

1. **Publicación de Ofertas (`Supplier`)**:
   - Si la `Account` del usuario está vinculada a una empresa con perfil de `Supplier`, el usuario puede publicar ofertas de servicios o productos en la plataforma.
   - Estas ofertas se vinculan al perfil de `Supplier`, facilitando la búsqueda y el acceso a compradores.

2. **Creación de Licitaciones (`Buyer`)**:
   - Si la `Account` está vinculada a una empresa con perfil de `Buyer`, el usuario puede crear licitaciones o solicitudes de servicio para recibir propuestas de proveedores.
   - La licitación detalla los requisitos de compra y permite que los proveedores respondan con propuestas personalizadas.

3. **Respuesta a Licitaciones**:
   - Las empresas registradas como `Supplier` pueden responder a licitaciones creadas por compradores, enviando propuestas que especifican precio, términos, y otros detalles relevantes.
   - Los compradores pueden revisar estas propuestas y seleccionar la que mejor se ajuste a sus necesidades.

---
