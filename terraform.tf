terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.25.0"
    }
  }
}

provider "google" {
  credentials = "/home/cesar/cre.json" # credeciais
  project     = "data-energia-global"
  region      = "us-central1"
}