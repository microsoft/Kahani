variable "prefix" {
  type        = string
  sensitive   = false
  description = "dev or prod"
}

variable "OPENAI_API_KEY" {
  type        = string
  sensitive   = true
  description = "OpenAI API Key"
}

variable "SDAPI_HOST" {
  type        = string
  sensitive   = true
  description = "A1111 host"
}

variable "container_registry" {
  type        = string
  description = "Container Registry *.azurecr.io"
}

variable "container_registry_username" {
  type        = string
  description = "Container Registry Username"
}

variable "container_registry_password" {
  type        = string
  description = "Container Registry Password"
  sensitive   = true
}
