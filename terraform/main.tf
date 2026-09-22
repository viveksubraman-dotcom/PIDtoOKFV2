# Terraform Infrastructure for Extracter Agent Knowledge Storage
# Complies with Rule 9 (Infrastructure Manager) & Rule 10 (Zero allUsers)

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# GCS Bucket for OKF Knowledge Bundles
resource "google_storage_bucket" "okf_knowledge_bucket" {
  name                        = "${var.bucket_name}-${var.environment}"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      num_newer_versions = 5
      with_state         = "ARCHIVED"
    }
  }

  labels = {
    environment = var.environment
    managed_by  = "infrastructure-manager"
    app         = "extracter-agent"
  }
}

# Service Account for Extracter Agent Runtime
resource "google_service_account" "extracter_agent_sa" {
  account_id   = "extracter-agent-${var.environment}"
  display_name = "Extracter Agent Service Account (${var.environment})"
}

# Authorize Agent SA to write into GCS Bucket (Rule 10: Zero allUsers)
resource "google_storage_bucket_iam_member" "agent_bucket_admin" {
  bucket = google_storage_bucket.okf_knowledge_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.extracter_agent_sa.email}"
}
