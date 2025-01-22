Prueba_Tecnica_DevOps
=======
Prueba Técnica para DevOps Senior - Sistemas de IA en AWS
---

# 1. Infraestructura en la Nube
Configurar una arquitectura en AWS para soportar un modelo de transcripción basado en IA, requiere configurar credenciales AWS con `aws-cli` para gestionar recursos.
   ```bash
   terraform apply
   terraform validate
   terraform apply
   ```
Terraform mostrará los valores como el ID del bucket S3, el nombre del clúster EKS y el ID de la instancia EC2. `outputs.tf`
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
as

![cloud_infrastructure](assets\cloud_infrastructure.png)

Entrega esperada:
• Scripts Terraform o CloudFormation que implementen la infraestructura.
• Diagramas de arquitectura (pueden ser generados en herramientas como
Lucidchart o Diagramas de AWS).

# 2. Pipeline de CI/CD 

# 3. Gestión de Datos y Data Warehouse 


# 4. Monitoreo y Observabilidad 
