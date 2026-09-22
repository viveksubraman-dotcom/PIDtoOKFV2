variable "project_id" {
  description = "Target Google Cloud project ID"
  type        = string
  default     = "cs-poc-y03r7kmfyov4kilzg50fd7s"
}

variable "region" {
  description = "Target Google Cloud region"
  type        = string
  default     = "asia-southeast1"
}

variable "environment" {
  description = "Deployment environment name (nonprod or prod)"
  type        = string
  default     = "nonprod"
}

variable "bucket_name" {
  description = "GCS bucket name for OKF knowledge bundles"
  type        = string
  default     = "cs-poc-y03r7kmfyov4kilzg50fd7s-okf-knowledge"
}
