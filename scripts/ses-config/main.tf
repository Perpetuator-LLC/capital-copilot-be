# Copyright (c) 2024 Perpetuator LLC
variable "domain" {}
variable "zone_id" {}
variable "mail_subdomain" {}
variable "sender_email" {}

provider "aws" {
  region = "us-east-1"
}

resource "aws_ses_domain_identity" "example" {
  domain = var.domain
}

resource "aws_route53_record" "ses_verification_record" {
  zone_id = var.zone_id
  name    = aws_ses_domain_identity.example.domain
  type    = "TXT"
  ttl     = 300
  records = [aws_ses_domain_identity.example.verification_token]
}

resource "aws_ses_domain_dkim" "example" {
  domain = aws_ses_domain_identity.example.domain
}

resource "aws_route53_record" "ses_dkim_records" {
  count   = 3
  zone_id = var.zone_id
  name    = "${aws_ses_domain_dkim.example.dkim_tokens[count.index]}._domainkey.${aws_ses_domain_dkim.example.domain}"
  type    = "CNAME"
  ttl     = 300
  records = ["${aws_ses_domain_dkim.example.dkim_tokens[count.index]}.dkim.amazonses.com"]
}

resource "aws_ses_domain_mail_from" "example" {
  domain    = aws_ses_domain_identity.example.domain
  mail_from_domain = var.mail_subdomain
  behavior_on_mx_failure = "UseDefaultValue"
}

resource "aws_route53_record" "ses_mail_from_record" {
  zone_id = var.zone_id
  name    = aws_ses_domain_mail_from.example.mail_from_domain
  type    = "MX"
  ttl     = 300
  records = ["10 inbound-smtp.us-east-1.amazonaws.com"]
}

resource "aws_ses_email_identity" "example" {
  email = var.sender_email
}

output "ses_domain_identity_arn" {
  value = aws_ses_domain_identity.example.arn
}

