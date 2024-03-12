resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-${random_string.uniq.result}-kahani-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "P1v2"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-${random_string.uniq.result}-kahani"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  app_settings = {
    OPENAI_API_KEY = var.OPENAI_API_KEY
    SDAPI_HOST     = var.SDAPI_HOST
    WEBSITES_PORT  = "8080"
  }

  https_only = true

  site_config {
    always_on = true

    application_stack {
      docker_image_name        = "kahani-streaming:SERVERVERSION"
      docker_registry_url      = var.container_registry
      docker_registry_username = var.container_registry_username
      docker_registry_password = var.container_registry_password
    }

  }

}

