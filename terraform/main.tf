terraform {
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "2.1.0"
    }
  }
}

provider "openstack" {
  cloud = "5Net"
}

resource "openstack_objectstorage_container_v1" "adtech_bucket" {
  name           = "adtech"
  storage_policy = "<YOUR_SWIFT_POLICY>"    # Assigns the storage policy
  container_read = ".r:*,admin:admin"  # Makes the bucket public
  container_write = "admin:admin"
}

resource "openstack_objectstorage_object_v1" "adtech_images" {
  for_each       = fileset("${path.module}/images", "*")
  container_name = openstack_objectstorage_container_v1.adtech_bucket.name
  name           = each.value
  source         = "${path.module}/images/${each.value}"
  content_type   = "image/jpeg" # Adjust according to your image type
}