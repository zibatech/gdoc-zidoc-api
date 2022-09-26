# ZiDoc REST API
Servicio que integra los registros de *ZiDoc*, aplicativo de la entidad CRA, con terceros.
## Requisitos

 - Docker
 - Base de datos de *ZiDoc* montada

## Instalación
El servicio se encuentra dockerizado, por ende lo único que tenemos que hacer es cambiar los valores de las variables de entorno necesarias y ejecutar los comandos de ***[Docker](https://www.docker.com/)*** respectivos. A continuación, las variables de entorno a configurar:

 - ***`DB_URI`:*** string de conexión de la base de datos, definida con la estructura que aparece en **`.env.template`**.
 - **`HMAC_SECRET_KEY`:** llave usada para hashear el valor del header de autenticación (puedes generarla desde [aquí](https://randomkeygen.com/)).

Una vez configuradas las variables de entorno, tendremos algo como lo siguiente:
```env
# Database
DB_URI=mysql://zidocusuario:supersecretpwd@host.docker.internal:3306/zidoc_cra

# Secret keys
HMAC_SECRET_KEY=fR2i/-]qFP:%y=kE~mYq5=l@+z;T)
```
> **host.docker.internal**: este valor se usa para acceder a la red local del *host* desde el contenedor.

Hecho esto ya podremos continuar con la construcción de la imagen, ejecutando lo siguiente en la raíz del proyecto:
```bash
$ docker build . -t <nombre>
```
Construida la imagen, procedemos a correrla con:
```bash
$ docker run -d -p <puerto>:<puerto> --name <nombre_contenedor> <nombre>
```
En este punto ya tenemos nuestro servicio corriendo en el puerto que se especifique, ahora vamos con la generación de la llave que se usará para la autorización. Lo primero que tenemos que hacer es acceder a la terminal del contenedor, ejecutando:
```bash
$ docker exec -it <nombre_contenedor> bash
```
Una vez ahí, entramos a la **`shell`** que nos ofrece **[Flask](https://flask.palletsprojects.com/en/2.2.x/)**, esto ejecutando:
```bash
$ flask shell
```
Esto nos dará acceso a la terminal interna de nuestro servicio, donde procederemos a ejecutar lo siguiente:
```python
>>> from app import hmac
>>> hmac.make_hmac().decode('utf-8')
>>> <llave>
```
El valor reemplazado en **`<llave>`** es nuestra llave de autenticación, esta deberá ser incluida en los **`headers`** de las peticiones que hagamos bajo la llave **`Signature`**.

Ahora si empecemos con las peticiones, podremos consultar *expedientes* y *documentos*, esto proveyendo filtros en los parámetros **`GET`** de la petición. A continuación dichos parámetros, tipos en base de datos, etiquetas y equivalencia en formularios de **`html`**:

#### Expedientes

 - **`Fecha (DATE, 'Fecha')`**:  ``<input type="date" name="Fecha"/>``
 - **`Usuario (INT(11), 'Usuario')`**:  `<option value="<id>"><nombre></option>`
 - **`NumeroExpediente (VARCHAR(50), 'Numero de expediente')`**:  ``<input type="text" name="NumeroExpediente"/>``
 - **`Dependencia (INT(11), 'Dependencia')`** :  `<option value="<id>"><codigo> - <nombre></option>`
 - **`Serie (INT(11), 'Serie')`**:  `<option value="<id>"><codigo> - <nombre></option>`
 - **`SubSerie (INT(11), 'Subserie')`**:  `<option value="<id>"><codigo> - <nombre></option>`
 - **`FechaExtInicial (DATE, 'Fecha extrema inicial')`:**  ``<input type="date" name="FechaExtInicial"/>``
 - **`FechaExtFinal (DATE, 'Fecha extrema final')`**:  ``<input type="date" name="FechaExtFinal"/>``
 - **`Caja (VARCHAR(10), 'Caja')`**:  ``<input type="text" name="Caja"/>``
 - **`Carpeta (VARCHAR(50), 'Carpeta')`**:  ``<input type="text" name="Carpeta"/>``
 - **`Tomo (VARCHAR(50), 'Tomo')`**:  ``<input type="text" name="Tomo"/>``
 - **`Otro (VARCHAR(50), 'Otro')`**:  ``<input type="text" name="Otro"/>``
 - **`NumeroFolios (DATE, 'NumeroFolios')`**:  ``<input type="number" name="NumeroFolios"/>``
 - **`Soporte (VARCHAR(50), 'Soporte')`**:  ``<input type="text" name="Soporte"/>``
 - **`ReferenciaDoc (DATE, 'Referencia de documentos')`**:  ``<input type="text" name="ReferenciaDoc"/>``
 - **`ConsecutivoInicial (INT(20), 'Consecutivo inicial')`**:  ``<input type="number" name="ConsecutivoInicial"/>``
 - **`ConsecutivoFinal (INT(20), 'Consecutivo final')`**:  ``<input type="number" name="ConsecutivoFinal"/>``
 - **`cedula_NIT (TEXT, 'Cédula/NIT')`**:  ``<input type="text" name="cedula_NIT"/>``
 - **`nombre_expediente (TEXT, 'Nombre')`**:  ``<input type="text" name="nombre_expediente"/>``

#### Documentos
- **`Expediente (INT(11), 'Expediente')`**: -
- **`NumeroRadicado (VARCHAR(20), 'Radicado')`:** ``<input type="text" name="NumeroRadicado"/>``
- **`Dependencia (INT(11), 'Dependencia')`** :  `<option value="<id>"><codigo> - <nombre></option>`
 - **`Serie (INT(11), 'Serie')`**:  `<option value="<id>"><codigo> - <nombre></option>`
 - **`SubSerie (INT(11), 'Subserie')`**:  `<option value="<id>"><codigo> - <nombre></option>`
- **`TipoDoc (INT(11), 'Tipo documental')`**:  `<option value="<codigo>"><codigo> - <nombre></option>`
- **`TipoDoc (VARCHAR(5), 'Tipo documental')`:** `<option value="<codigo>"><codigo> - <nombre></option>`
- **`Asunto (VARCHAR(500), 'Asunto')`:** ``<input type="text" name="Asunto"/>``
- **`numero (TEXT, 'Número')`:** ``<input type="text" name="numero"/>``
- **`ConsecutivoIniDoc (VARCHAR(15), 'Consecutivo inicial')`** ``<input type="text" name="ConsecutivoIniDoc"/>``
- **`ConsecutivoFinDoc (VARCHAR(15), 'Consecutivo final')`** ``<input type="text" name="ConsecutivoFinDoc"/>``
- **`FechaDoc (DATE, 'Fecha')`:** ``<input type="date" name="FechaDoc"/>``

Estos serían todos los campos por los que podemos filtrar nuestras consultas. Dentro de estos tenemos casos especiales (**`Usuario`**, **`Dependencia`**, **`Serie`**, **`SubSerie`**), ya que la equivalencia en **`html`** de estos es una lista desplegable donde las opciones son generadas por la iteracion sobre los registros que nos retornan los **`endpoints`** respectivos para cada uno y el valor de cada una de estas tiene que ser el **`id`** de dichos registros retornados, a continuación un ejemplo con **`php`**:
```php
$dependencias = [...]; // dependencias retornadas
foreach ($dependencia as $dependencias) {
  echo "<option value='$dependencia[id]'>$dependencia[codigo] - $dependencia[nombre]</option>";
}
```
Esto con la finalidad de no estropear las relaciones definidad a nivel de base de datos. Entendido esto, procedemos con las peticiones:

## TRD

#### Respuesta general
```
HTTP/1.1 200 OK
Content-type: application/json
```
```json
{
  "ok": true,
  "data": [
    {
      "id": 1,
      "codigo": 100,
      "nombre": "Dirección General"
    }
  ]
}
```

### Dependencias
#### Todas
``POST /api/dependencias``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/dependencias
```

### Series
#### Todas
``POST /api/series``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/series
```
#### De la dependencia con id=1 y código=100
Ten en cuenta que cuando se hacen este tipo de filtros se debe especificar la *dependencia*, *serie* o *subserie* por el **`id`** obtenido del proceso previamente descrito y no por el código de esta.

``POST /api/series?dependencia=1``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/series?dependencia=1
```
### Subseries
#### Todas
``POST /api/subseries``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/subseries
```
#### De la dependencia con id=1 y código=100 y serie con id=5 y código=55

``POST /api/subseries?dependencia=1&serie=5``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/subseries?dependencia=1&serie=5
```

### Tipos documentales

#### Todos
``POST /api/tipos-documentales``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/tipos-documentales
```
#### De la dependencia con id=9 y código=140 y serie con id=11 y código=71

``POST /api/subseries?dependencia=9&serie=11``
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/subseries?dependencia=19&serie=11
```

### Expedientes

#### Respuesta general
```json
{
   "ok": true,
   "data": [
     {
       "Caja": ...,
	   "Carpeta": ...,
	   "ConsecutivoFinal": ...,
	   "ConsecutivoInicial": ...,
	   "Dependencia": ...,
	   "FUID": ...,
	   "Fecha": ....,
	   "FechaExtFinal": ...,
	   "FechaExtInicial": ...,
	   "Notas": ...,
	   "NumeroExpediente": ...,
	   "NumeroFolios": ...,
	   "Otro": ...,
	   "ReferenciaDoc": ...,
	   "Soporte": ...,
	   "SubSerie": ...,
	   "Tomo": ...,
	   "Usuario": ...,
	   "cedula_NIT": ...,
	   "id": ...,
	   "nombre_expediente": ...
     },
     ... // demás registros
  ]  
}  
```

### Todos

``POST /api/expedientes`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/expedientes
```

### De la dependencia con id=7 y código=130

``POST /api/expedientes?Dependencia=7`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/expedientes?Dependencia=7
```

### De la dependencia con id=7 y código=130 y subserie con id=4 y código=21

``POST /api/expedientes?Dependencia=7&Serie=4`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/expedientes?Dependencia=7&Serie=4
```
 ### De la dependencia 130, serie 55 y subserie 01

``POST /api/expedientes?Dependencia=130&Serie=55&SubSerie=01`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/expedientes?Dependencia=130&Serie=55&SubSerie=01
```

### Documentos
Debido a la gran cantidad de registros, la ausencia de relaciones a nivel de base de datos y la inexistencia de *"índices"* de una tabla en otra, no se pudo cambiar la estructura de la tablas **`documentos`** , por lo que la consulta de *documentos* por *dependencia*, *serie*, *subserie* y *tipos documentales*  sigue siendo por código.

#### Respuesta general
```json
{
   "ok": true,
   "data": [
     {
       "Archivo": ...,
       "Asunto": ...,
       "ConsecutivoFinDoc": ...,
       "ConsecutivoIniDoc": ...,
       "Expediente": ...,
       "Fecha": ...,
       "FechaDoc": ...,
       "Folio": ...,
       "NumeroRadicado": ...,
       "TipoDoc": ...,
       "TipoRadicado": ...,
       "folio_final": ...,
       "folio_inicial": ...,
       "id": ...,
       "numero": ...,
       "observaciones": ...
     },
     ... // demás registros
  ]
}
```

### Todos

``POST /api/documentos`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/documentos
```

### De la dependencia con código=130

``POST /api/documentos?Dependencia=130`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/documentos?Dependencia=7
```

### De la dependencia con código=160 y serie con código=11

``POST /api/documentos?Dependencia=160&Serie=11`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/documentos?Dependencia=160&Serie=11
```
 ### De la dependencia con código=120, serie con código=51 y subserie con código=01

``POST /api/documentos?Dependencia=120&Serie=51&SubSerie=01`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/documentos?Dependencia=120&Serie=51&SubSerie=01
```

### De la dependencia con código=190 y tipo documental con código=10

``POST /api/documentos?Dependencia=190&TipoDoc=10`` 
```bash
$ curl -H 'Signature: <llave>' <host>:<puerto>/api/documentos?Dependencia=190&TipoDoc=10
```

Ese sería el proceso a través del cuál podemos integral *ZiDoc* con terceros.

*[Gian López](https://gian-lopez.web.app/)*