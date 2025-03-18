terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.25.0"
    }
  }
}

provider "google" {
  credentials = /home/cesar/cre.txt
  project     = "my-project-id"
  region      = "us-central1"
}