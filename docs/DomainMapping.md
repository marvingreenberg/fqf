# Custom Domain Setup: festschedule.org

## Overview

The app is deployed on Google Cloud Run and accessible via a default URL
(`fqf2026-<hash>.a.run.app`). A custom domain (`festschedule.org`) is mapped
to that service so the app is reachable at `https://festschedule.org/fq2026`.

## Components

| Component | What it does |
|-----------|-------------|
| **Cloud Domains** | Domain registration (festschedule.org, $12/yr) |
| **Cloud DNS** | Managed DNS zone hosting A/AAAA records |
| **Cloud Run domain mapping** | Binds the domain to the Cloud Run service; auto-provisions SSL |

## Steps performed (one-time setup)

### 1. Register the domain

```bash
gcloud domains registrations register festschedule.org
```

During registration, selected Cloud DNS managed zone `festschedule-org` for DNS hosting.

### 2. Create the DNS managed zone (if not created during registration)

```bash
gcloud dns managed-zones create festschedule-org \
    --dns-name=festschedule.org. \
    --description="FQF schedule builder"
```

### 3. Create the Cloud Run domain mapping

```bash
gcloud beta run domain-mappings create \
    --service=fqf2026 \
    --domain=festschedule.org \
    --region=us-central1 \
    --project=fqf2026
```

This outputs the required A and AAAA records.

### 4. Add DNS records

```bash
gcloud dns record-sets create festschedule.org. \
    --zone=festschedule-org --type=A --ttl=300 \
    --rrdatas="216.239.32.21,216.239.34.21,216.239.36.21,216.239.38.21"

gcloud dns record-sets create festschedule.org. \
    --zone=festschedule-org --type=AAAA --ttl=300 \
    --rrdatas="2001:4860:4802:32::15,2001:4860:4802:34::15,2001:4860:4802:36::15,2001:4860:4802:38::15"
```

### 5. Wait for SSL certificate provisioning

Google auto-provisions a managed SSL certificate. Takes 15-30 minutes after DNS propagates.

## Checking status

```bash
# Domain mapping status (look for CertificateProvisioned)
gcloud beta run domain-mappings describe \
    --domain=festschedule.org --region=us-central1

# DNS records
gcloud dns record-sets list --zone=festschedule-org

# DNS propagation (external check)
dig festschedule.org A +short
```

## URL structure

| URL | What it serves |
|-----|---------------|
| `festschedule.org/` | Landing page (disclaimer + link to schedule builder) |
| `festschedule.org/fq2026` | FQF 2026 schedule builder app |
| `festschedule.org/fq2026?share=<id>` | Shared schedule link |
| `fqf2026-<hash>.a.run.app/` | Same app via Cloud Run default URL |

## Billing

- Domain registration: $12/yr (via Cloud Domains / Squarespace reseller)
- Cloud DNS managed zone: ~$0.20/mo
- SSL certificate: free (Google-managed)
- Cloud Run: pay-per-use (scales to zero)
