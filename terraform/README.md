# OpenStack Object Storage Terraform Configuration

This Terraform configuration uses the OpenStack provider to create a container (bucket) in OpenStack Object Storage (Swift) and upload images into it. Below is a breakdown of each part of the file.

## Overview

- **Terraform Block**  
  Specifies the required provider (OpenStack), including its source and version.
- **Provider Configuration**  
  Defines how to connect to the OpenStack environment (in this case using the cloud named `"5Net"` from your local `clouds.yaml` or OpenStack configuration).
- **Object Storage Container (adtech_bucket)**  
  Creates a Swift container named `"adtech"` with a specific storage policy (`"<YOUR_SWIFT_POLICY>"`) and sets read/write permissions.
- **Object Storage Objects (adtech_images)**  
  Automatically uploads all files from a local `images` directory into the newly created Swift container. Each file is given a content type of `"image/jpeg"` by default.

## File Explanation

1. **Terraform Required Providers**
   ```hcl
   terraform {
     required_providers {
       openstack = {
         source  = "terraform-provider-openstack/openstack"
         version = "2.1.0"
       }
     }
   }
   ```
   - Declares that this configuration will use the `openstack` provider plugin from the specified source and version.

2. **Provider Configuration**
   ```hcl
   provider "openstack" {
     cloud = "5Net"
   }
   ```
   - Instructs Terraform to use the `5Net` cloud configuration (from local credentials or environment variables) to authenticate against OpenStack.

3. **Object Storage Container Resource**
   ```hcl
   resource "openstack_objectstorage_container_v1" "adtech_bucket" {
     name           = "adtech"
     storage_policy = "<YOUR_SWIFT_POLICY>"
     container_read = ".r:*,admin:admin"
     container_write = "admin:admin"
   }
   ```
   - **name**: Creates a container (similar to a bucket in other storage services) named `"adtech"`.
   - **storage_policy**: Assigns the `"<YOUR_SWIFT_POLICY>"` policy for high-performance storage if available in your cloud environment.
   - **container_read**: The permissions set here (`".r:*"`) make the container publicly readable; `"admin:admin"` allows admin-level read. 
   - **container_write**: Allows users with `"admin:admin"` credentials to write to the container.

4. **Object Storage Objects Resource**
   ```hcl
   resource "openstack_objectstorage_object_v1" "adtech_images" {
     for_each       = fileset("${path.module}/images", "*")
     container_name = openstack_objectstorage_container_v1.adtech_bucket.name
     name           = each.value
     source         = "${path.module}/images/${each.value}"
     content_type   = "image/jpeg"
   }
   ```
   - **for_each**: Dynamically iterates over all files in the `images` directory within the current module, creating a resource for each file.
   - **container_name**: References the `adtech_bucket` container resource (by name).
   - **name**: Uses the filename as the object name in Swift.
   - **source**: Specifies the path to the local file being uploaded.
   - **content_type**: Assigns a MIME type of `"image/jpeg"`. Adjust if your images differ.

## Usage

1. **Prerequisites**  
   - You have valid OpenStack credentials/configuration (e.g., `clouds.yaml`) referencing a cloud named `"5Net"`.
   - Terraform is installed and you have cloned/copied this configuration locally.

2. **Initialize Terraform**  
   ```bash
   terraform init
   ```
   This will download the OpenStack provider plugin.

3. **Plan the Configuration**  
   ```bash
   terraform plan
   ```
   Reviews your configuration and shows changes that will be made to your OpenStack environment.

4. **Apply the Configuration**  
   ```bash
   terraform apply
   ```
   Provisions the container and uploads each image from `./images` to the container in Swift.

5. **Verify**  
   - Log in to your OpenStack console or use the Swift CLI to confirm that the container named `"adtech"` is created and the images have been uploaded successfully.

## Notes

- **Storage Policies**: The `"<YOUR_SWIFT_POLICY>"` policy must exist in your OpenStack swift environment.
- **Permissions**: `container_read = ".r:*"` makes the container publicly readable. Adjust if you do not want public access.
- **Content Type**: Update `content_type` as needed if you’re uploading different file types.

## Cleanup

To remove the container and its objects:
```bash
terraform destroy
```
This removes all resources created by this Terraform configuration.

## License

This configuration is provided as-is. Feel free to modify it as needed for your own use cases.
