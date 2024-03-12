terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.38"
    }
  }

  required_version = ">= 0.14.9"
}

provider "azurerm" {
  features {}
}

resource "random_string" "uniq" {
  length      = 4
  min_lower   = 4
  min_numeric = 0
  min_special = 0
  min_upper   = 0
  numeric     = false
  upper       = false
  special     = false
  lower       = true
}

resource "random_password" "db_password" {
  length           = 20
  special          = true
  override_special = "_%@"
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-${random_string.uniq.result}"
  location = "Central India"
  lifecycle {
    ignore_changes = [
      tags
    ]
  }
}

