terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>5.0"
    }
  }
  backend "gcs" {
    bucket = "bucket-infra-juansebasdev"
    prefix = "movies-api/terraform.tfstate"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repository" {
  provider      = google
  location      = var.region
  repository_id = "${var.service_name}-${terraform.workspace}-repository"
  description   = "Docker repository"
  format        = "DOCKER"
}

resource "google_cloud_run_service" "gc_run_service" {
  name     = "${var.service_name}-${terraform.workspace}-service"
  location = var.region
  template {
    spec {
      service_account_name = var.service_account_email
      containers {
        image = var.image_url
        env {
          name  = "GOOGLE_CLIENT_ID"
          value = var.google_client_id
        }
        env {
          name  = "GOOGLE_CLIENT_SECRET"
          value = var.google_client_secret
        }
        env {
          name  = "SQL_URL"
          value = var.sql_url
        }
        env {
          name  = "MONGO_URL"
          value = var.mongo_url
        }
        env {
          name  = "DATA_REPOSITORY"
          value = var.data_repository
        }
        env {
          name  = "HOST"
          value = var.host
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_artifact_registry_repository.repository]
}

resource "google_cloud_run_service_iam_binding" "default" {
  location = google_cloud_run_service.gc_run_service.location
  service  = google_cloud_run_service.gc_run_service.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]

  depends_on = [google_cloud_run_service.gc_run_service]
}
