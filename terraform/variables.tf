variable "aws_region" {
  description = "AWS region in which to deploy the lab."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name used to tag lab resources."
  type        = string
  default     = "cloudops-aws-web-lab"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,35}$", var.project_name))
    error_message = "Use 3-36 lowercase letters, digits or hyphens, starting with a letter."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the dedicated lab VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the public lab subnet; must be inside vpc_cidr."
  type        = string
  default     = "10.42.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance size; t3.micro is a paid resource outside eligible promotions."
  type        = string
  default     = "t3.micro"
}

variable "allowed_http_cidrs" {
  description = "IP CIDRs allowed to reach the demo web page on port 80. Restrict to your IP/32 where possible."
  type        = list(string)
  default     = ["0.0.0.0/0"]

  validation {
    condition     = length(var.allowed_http_cidrs) > 0 && alltrue([for cidr in var.allowed_http_cidrs : can(cidrnetmask(cidr))])
    error_message = "Provide one or more valid IPv4 CIDR blocks."
  }
}
