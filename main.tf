provider "google" {
  project = var.project_id
  region = var.region
}

resource "google_kubernetes_engine_cluster" "default" {
  name = "my-cluster"
  location = var.region
}

resource "google_cloudbuild_trigger" "default" {
  name = "my-trigger"
  description = "Builds and deploys my application."
  trigger_template {
    filename = "cloudbuild.yaml"
  }
}