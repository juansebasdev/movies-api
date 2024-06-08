variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Project region"
  type        = string
}

variable "service_account_email" {
  description = "Service account email"
  type        = string
}

variable "service_name" {
  description = "Name of the service"
  type        = string
}

variable "image_url" {
  description = "Image URL"
  type        = string
}

variable "google_client_id" {
  description = "Google client ID"
  type        = string
}
variable "google_client_secret" {
  description = "Google client secret"
  type        = string
}
variable "sql_url" {
  description = "SQL connection string"
  type        = string
  default     = "sqlite:///movies.db"
}
variable "mongo_url" {
  description = "MongoDB connection string"
  type        = string
}
variable "data_repository" {
  description = "Use SQL or NoSQL data repository"
  type        = string
  default     = "NOSQL"
}

variable "host" {
  description = "Host"
  type        = string
  default     = "0.0.0.0"
}
