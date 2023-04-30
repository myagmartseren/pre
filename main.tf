provider "google" {
  project = var.project_id
  region = var.region
}

resource "google_kubernetes_engine_cluster" "default" {
  name = var.cluster_name
  location = var.region
  node_version = "1.19.10"
  node_count = 3
}