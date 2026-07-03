# Content fix pack — copy-paste ready

Everything below is ready to paste into WP admin / Yoast fields.

---

## 1. New title tags & meta descriptions

Paste into **Yoast SEO box → "SEO title" / "Meta description"** on each page.
(Titles ≤ 60 chars, descriptions ≤ 155 chars.)

### Pages currently missing a meta description

| Page | Meta description |
|---|---|
| `/faq/` | Answers to common questions about VAPT, SOC monitoring, ISO 27001, SEBI, RBI & DPDPA compliance, pricing and timelines — from Selkey Cyber Security. |
| `/privacy-policy/` | How Selkey Cyber Security collects, uses and protects your personal data, and the rights you have under applicable data-protection law. |
| `/terms-and-conditions/` | The terms governing use of the Selkey Cyber Security website and engagement of our cybersecurity, compliance and training services. |

### Titles that truncate in Google (too long)

| Page | New title |
|---|---|
| `/about-us/` | About Selkey Cyber Security \| VAPT & Compliance Experts |
| Thick Client VAPT | Thick Client Application Pentesting \| Selkey |
| Network VAPT | Network Penetration Testing Services in India \| Selkey |
| Mobile VAPT | Mobile App Penetration Testing (Android & iOS) \| Selkey |
| Code IoT VAPT | IoT & Embedded Device Pentesting \| Selkey |

### Titles wasting keyword space (too short)

| Page | New title |
|---|---|
| `/service/compliance/` | Cyber Security Compliance Services in India \| Selkey |
| `/service/red-teaming/` | Red Teaming & Adversary Simulation Services \| Selkey |
| `/service/virtual-ciso/` | Virtual CISO (vCISO) Services in India \| Selkey |
| `/service/soc-as-a-services/`* | SOC as a Service — 24/7 Security Monitoring \| Selkey |

\* Rename slug to `soc-as-a-service` first (see redirects.htaccess).

### Corrected service names (fix in page title, H1 AND slug)

| Current | Corrected |
|---|---|
| Security **Assesment** Services & OT | Security **Assessment** Services & OT |
| GDPR Implementation & Readiness (`…-readness` slug) | slug: `gdpr-implementation-readiness` |
| SOC as a **Services** | SOC as a **Service** |
| Code **IOT** Vulnerability Assessment… | **IoT** & Embedded Device VAPT |
| WHY CHOOSE US..? | Why Choose Us? |

---

## 2. Homepage copy replacements

Replace the leftover theme demo copy (edit with Elementor):

| Current (theme filler) | Replacement |
|---|---|
| H2: "We Provide the best Information Technology Solutions service" | "End-to-End Cyber Security, From Assessment to Response" |
| H2: "Key Features Driving Excellence in IT Solutions" | "Why Businesses Across BFSI, Healthcare & Manufacturing Trust Selkey" |
| H2: "How To Work It!" | "How We Work: Our 4-Step Engagement Process" |
| H3 ×7: "From Encryption to Freedom" (all seven testimonials) | Use a short quote from each client as the heading, e.g. "Cleared our SEBI CSCRF audit on the first attempt" — Shreeji Dental & Multispecialist Hospital. Every heading must be unique. |

**Trust-number consistency:** the site currently claims "4.8★ by 144+ clients" (meta + schema) and "765+ More Happy Clients" (homepage counter). Pick the number you can prove and use it everywhere. If 765 is total engagements and 144 is reviews, label them distinctly: "765+ projects delivered · 4.8★ from 144 client reviews".

---

## 3. `/services/` hub page — draft content

Create a real page at `/services/` (Pages → Add New, slug `services`), point the main nav "Services" item at it, and build these sections:

**Title tag:** Cyber Security Services in India | Selkey Cyber Security
**Meta description:** Explore Selkey's cybersecurity services — VAPT, managed SOC, digital forensics, compliance (ISO 27001, SEBI, RBI, DPDPA) and specialized security consulting.
**H1:** Cyber Security Services in India

**Intro (2–3 sentences):** Selkey Cyber Security protects organisations across India with offensive testing, 24/7 defence and regulatory compliance. Every engagement is delivered by certified specialists and ends with clear, actionable reporting.

**Six H2 sections, each linking to its service-family page and its child services:**
1. Vulnerability Assessment & Penetration Testing — web, mobile, API, network, thick client, IoT, source code review, Active Directory, red teaming
2. Managed Cyber Security Services — SOC as a Service, MDR, vulnerability management, dark-web monitoring, phishing & ransomware simulation
3. Compliance — ISO 27001:2022, SEBI CSCRF, RBI, DPDPA, GDPR
4. Digital Forensics & Incident Response — incident response & malware analysis, ransomware investigation, data-breach response, compromise assessment, disk/endpoint forensics, eDiscovery
5. Specialized Services — virtual CISO, cyber insurance consulting, OT/ICS assessment, cloud security assessment, security awareness, talent augmentation
6. Training & Certification — SOC engineer, penetration testing expert, ethical hacker programs

**Close with:** an FAQ block (reuse 4–5 questions from `/faq/`, add FAQPage schema via Yoast blocks) and a contact CTA.

---

## 4. Replacement business schema (JSON-LD)

The current `aggregateRating` is self-serving (Google ignores or penalises star ratings a business marks up about itself unless the reviews are collected and displayed on that page). **Either** display the 144 reviews on the page, **or** use this version without the rating. Added: `geo`, `openingHours`, `priceRange`.

Paste via your schema plugin or an HTML widget in the footer template (replace the existing block, don't duplicate it). Fill in the correct coordinates and hours:

```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://selkeycybersecurity.com/#business",
  "name": "Selkey Cyber Security Pvt Ltd",
  "alternateName": "Selkey",
  "url": "https://selkeycybersecurity.com/",
  "image": "https://selkeycybersecurity.com/wp-content/uploads/2024/05/1600x365.png",
  "logo": "https://selkeycybersecurity.com/wp-content/uploads/2024/05/1600x365.png",
  "telephone": "+917777999564",
  "email": "Hello@selkeycybersecurity.com",
  "priceRange": "₹₹",
  "description": "Cybersecurity services in India: VAPT, SOC, incident response and compliance (ISO 27001, SEBI, RBI, DPDPA).",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "A-856, Money Plant High Street, Near BSNL House, Jagatpur",
    "addressLocality": "Ahmedabad",
    "addressRegion": "Gujarat",
    "postalCode": "382470",
    "addressCountry": "IN"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "23.1", 
    "longitude": "72.55"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "09:30",
    "closes": "18:30"
  },
  "areaServed": "IN",
  "sameAs": [
    "https://www.facebook.com/people/Selkey-Cyber-Security-Pvt-Ltd/61557019211306/",
    "https://www.instagram.com/cyberselkey/",
    "https://www.linkedin.com/company/selkey-cyber-security/",
    "https://x.com/cyberselkey"
  ]
}
```

---

## 5. Social share image (og:image) spec

Replace the 1.9 MB animated GIF with a static image:

- **Size:** 1200 × 630 px, JPG or PNG, under 300 KB
- **Content:** Selkey logo + tagline ("Cyber Security Services in India — VAPT · SOC · Compliance") on brand background; keep text inside the middle 1000×524 safe area
- **Where:** Yoast SEO → Settings → General → Site features → make sure Open Graph is on; then Settings → Site representation / Social sharing → set as default image. Also set it under Yoast's "Social" tab on the homepage itself.
- After changing, refresh caches: LinkedIn Post Inspector, Facebook Sharing Debugger.
