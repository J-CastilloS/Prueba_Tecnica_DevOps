# Prueba Técnica para DevOps Senior - Sistemas de IA en AWS
--------------
Configurar una arquitectura en AWS para soportar un modelo de transcripción basado en IA, requiere configurar credenciales AWS con `aws-cli` para gestionar recursos.

#### Requirements
- `Python`: 3.8.x and greater
- `Terraform`: 1.10.4 latest
- `Docker`: 

#### Getting Started
A continuación, presento los pasos principales con scripts `Terraform <https://www.terraform.io/>` (`/tf/main.tf`) que puedes replicar para implementar la misma arquitectura planteada.
```bash
    terraform init
    terraform validate
    terraform apply
```


## 1. Infraestructura en la Nube
--------------
Terraform mostrará los valores como el ID del bucket S3, el nombre del clúster EKS y el ID de la instancia EC2 creada. (`outputs.tf`)
```hcl
    output "s3_bucket_name" {
    value = aws_s3_bucket.data_bucket.id
    }
    output "eks_cluster_name" {
    value = module.eks.cluster_name
    }
    output "ec2_instance_id" {
    value = aws_instance.ml_ec2.id
    }
```
En general, la arquitectura planteada es la siguiente, `Diagrama Excalidraw <https://excalidraw.com/>`,
![cloud_infrastructure](assets\terraform.png)



## 2. Pipeline de CI/CD
--------------
Una solución basada en **GitHub Actions** que implementa un pipeline CI/CD para el despliegue de un modelo de transcripción en un clúster de EKS. Este pipeline incluye pruebas unitarias, construcción de imágenes Docker y despliegue automatizado.

#### Configuration

1. Secretos en GitHub:
   - `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`: Credenciales de AWS.
2. Manifiestos Kubernetes:
   - Actualizar los archivos `deployment.yaml` y `service.yaml` con las configuraciones necesarias.
3. Imagenes Docker:
   - Configurar un repositorio para almacenar las imágenes Docker del modelo.
4. Clúster EKS:
   - Tener configurado un clúster EKS con los permisos necesarios para el despliegue.



# 3. Gestión de Datos y Data Warehouse 
--------------
Diseñar un flujo para procesar grabaciones y almacenar resultados en un data warehouse. El pipeline propuesto consta de tres componentes principales:
1. Extracción de datos desde S3: Un evento en S3 (subida de un archivo) activa la función Lambda.
2. Procesamiento de datos mediante `Lambda`:
   - La función Lambda procesa la grabación (transcripción, extracción de metadatos, etc.).
   - Los resultados se formatean en `TABLE`, `JSON` o `CSV` para su carga.
3. Carga en Amazon Redshift: La función Lambda utiliza la funcionalidad de `COPY` de Redshift para cargar los datos procesados al data warehouse.

#### Amazon Redshift
Esquema de la base de datos con los campos `text` de la transcripción y `timestamp` para verificar la hora de subida y procesamiento,
```sql
CREATE TABLE transcription_results (
    id VARCHAR(50) PRIMARY KEY,
    text TEXT,
    timestamp TIMESTAMP
);
```

#### Permisos IAM
Roles y políticas necesarias para acceder a S3 y Redshift.
![IAM Polities](assets\iam.png)
1. VPC Lambda: Configurar Lambda para ejecutarse en la misma VPC con los subnets y security groups adecuados.
2. S3 Event Notification: Configura el bucket S3 para que active un evento cuando se suba un archivo:
    - **Evento:** `s3:ObjectCreated: *`.
    - **Destino:** `Lambda Function`.

#### Configuración de Amazon Redshift
Cargar directamente desde S3 a Redshift usando el comando `COPY`,
```sql
COPY transcription_results
FROM 's3://<S3_BUCKET_NAME>/<processed_file>'
CREDENTIALS 'aws_access_key_id=<ACCESS_KEY>;aws_secret_access_key=<SECRET_KEY>'
FORMAT AS JSON 'auto';
```
#### Variables de Entorno
- `S3_BUCKET`
- `REDSHIFT_HOST`
- `REDSHIFT_PORT`
- `REDSHIFT_DB`
- `REDSHIFT_USER`
- `REDSHIFT_PASSWORD`
- `REDSHIFT_TABLE`



# 4. Monitoreo y Observabilidad 
--------------
El sistema de monitoreo utiliza **CloudWatch** y **Grafana** para visualizar métricas, rastrear el rendimiento y configurar alertas para detectar fallos críticos.

#### Configuración del monitoreo en Amazon EKS
AWS proporciona un addon llamado **Container Insights** que integra métricas del clúster EKS en CloudWatch, siguiendo los siguientes pasos,
1. Instalar el agente de CloudWatch en EKS:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-cloudwatch-agent/main/kubernetes/cloudwatch-agent.yaml
   ```
2. Crea un rol IAM para el agente de CloudWatch que permita enviar métricas y logs a CloudWatch (`polities/cloudwatch.json`).
3. Verifica logs y métricas que envíen al namespace en CloudWatch.

#### Monioreo del clúster EKS y Lambda Functions
- Duración de la ejecución: Tiempo que toma la función en completarse.
- Tasa de invocación: Número de ejecuciones por minuto.
- Errores: Número de errores durante la ejecución.
- Utilización de CPU y memoria por nodo.
- Estado de los pods (running, pending, failed).
- Tasa de errores en servicios.

Ejemplo de consulta de logs para mostrar errores en aplicaciones:
```bash
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
```

#### **Integración con Grafana**
1. **Conectar Grafana a CloudWatch**:
   - Instala el plugin de CloudWatch en Grafana.
   - Configura una nueva fuente de datos con las credenciales de AWS.
   - Configura un intervalo de actualización (por ejemplo, cada 1 minuto).
2. **Crear dashboards personalizados en Grafana**:
   - **Panel EKS**:
     - CPU/Memory por nodo.
     - Estado de los pods por namespace.
     - Tráfico entrante/saliente de servicios (HTTP, gRPC).
   - **Panel Lambda**:
     - Duración, errores y tasa de invocación.
3. **Configuración del archivo `grafana-dashboard.json`**: Exporta el dashboard para compartirlo o reutilizarlo.

#### CloudWatch Alarms
- **Condición**: `Errors > 0` en un período de 5 minutos.
- **Acción**: Envía notificación a un SNS topic.
- **Configuración**:
  ```bash
  aws cloudwatch put-metric-alarm \
    --alarm-name "LambdaErrorAlarm" \
    --metric-name Errors \
    --namespace AWS/Lambda \
    --statistic Sum \
    --period 300 \
    --threshold 0 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:<region>:<account-id>:<sns-topic-name>
  ```
#### Configurar alertas en Grafana
- Define alertas en las métricas clave (CPU, errores Lambda, tráfico de red).
- Configura canales de notificación (Slack, email, PagerDuty).



# 5. Preguntas Teóricas 
--------------
#### **1. ¿Cómo garantizarías la seguridad de las credenciales almacenadas en los pipelines?**
Se pueden seguir las siguientes estrategias,
1. **Almacenamiento en gestores de secretos:**
   - Utilizar servicios como **AWS Secrets Manager** para almacenar credenciales sensibles (tokens, claves API, contraseñas).
   - Acceder a las credenciales directamente desde el pipeline mediante integraciones con estos gestores.
2. **Variables de entorno cifradas:**
   - Configurar las credenciales como variables de entorno en los sistemas CI/CD (GitHub Actions, Jenkins, GitLab).
   - Asegurarse de que estas variables estén cifradas y solo accesibles durante la ejecución del pipeline.
3. **Principio de menor privilegio:**
   - Asignar solo los permisos estrictamente necesarios para cada credencial.
   - Usar roles IAM temporales en lugar de credenciales estáticas para interactuar con servicios como AWS.
4. **Rotación automática de credenciales:**
   - Implementar mecanismos de rotación periódica para las credenciales.
   - Automatizar la actualización de los secretos almacenados.

#### 2. Explica una estrategia para escalar dinámicamente los microservicios según la carga de trabajo.
La escalabilidad dinámica permite ajustar los recursos asignados a los microservicios en función de la carga de trabajo, mejorando la eficiencia y reduciendo costos. Una estrategia típica incluye,
1. **Configurar un controlador de escalado automático (Horizontal Pod Autoscaler - HPA):** En un clúster Kubernetes, usar el **HPA** para ajustar el número de pods según las métricas observadas.
2. **Uso de escalado vertical automático (Vertical Pod Autoscaler - VPA):** Ajusta los recursos asignados (CPU/memoria) a los pods individuales en función de la carga.
3. **Escalado basado en eventos:**
   - Utilizar soluciones como **KEDA** (Kubernetes Event-Driven Autoscaler) para escalar microservicios según eventos, como mensajes en una cola (Amazon SQS, Kafka) o solicitudes HTTP.
4. **Pruebas de estrés y ajuste de límites:**
   - Realizar pruebas de carga para determinar los límites de cada servicio.
   - Configurar políticas de calidad de servicio (QoS) en Kubernetes para priorizar recursos.

Con esta estrategia, los microservicios pueden responder dinámicamente a la carga de trabajo, manteniendo la disponibilidad y optimizando el uso de recursos. 😊



# More Resources
--------------
-  `GitHub Actions <https://docs.github.com/es/actions/>`
-  `Grafana Documentation <https://grafana.com/docs/>`
-  `Cloudwatch Documentation <https://docs.aws.amazon.com/cloudwatch/>`
-  `AWS Documentation <https://docs.aws.amazon.com/>`
-  `AWS CLI Documentation <https://docs.aws.amazon.com/cli/index.html/>`
-  `AWS Support <https://console.aws.amazon.com/support/home#/>`