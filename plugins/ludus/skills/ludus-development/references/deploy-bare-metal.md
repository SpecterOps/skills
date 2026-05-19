# Bare Metal Deployment (Recommended)

Reference for deploying Ludus on bare metal hardware, including recommended mini PC configurations, RAM/NVMe options, and install steps.

## Overview

Ludus works best on a "bare metal" machine. This can be a rented cloud "bare metal" server or a local machine dedicated to Ludus.

Relatively inexpensive small form factor (SFF) computers excel as Ludus hosts (i.e. [Intel NUCs](https://www.intel.com/content/www/us/en/products/details/nuc.html), [Minisforums](https://store.minisforum.com/), [Beelink](https://www.bee-link.com/), [GMKTec](https://www.gmktec.com/), etc.)

Cloud providers also offer dedicated or "bare metal" servers (i.e. [Contabo](https://contabo.com/en/dedicated-servers/), [Hetzner](https://www.hetzner.com/dedicated-rootserver?country=us&ram_from=32), [Equinix](https://deploy.equinix.com/product/bare-metal/), [Vultr](https://www.vultr.com/products/bare-metal/), etc.)

When looking for a Ludus host, try to get as much RAM as possible, followed by as many fast cores as possible, and finally as much fast NVMe as you can.

## Current Recommendation

A sheet of powerful mini PC options is available [here](https://docs.google.com/spreadsheets/d/1zhh-F_U5_bBFd4Udyz5ZIW7-zPSXckX08bThQFqqI80/edit?usp=sharing).

We have been using the GMKTec NucBox K8 (AMD Ryzen 7 8845HS 8c/16t base 3.8Ghz boost 5.1Ghz), 96 GB of 5600MHz RAM, and 2x 2TB PCIe 4.0 NVMe in RAID0.

While the GMKTec K9 has more cores (14c/18t) it has a lower passmark score (21572) compared to the K8 (29242) due to 10 cores being efficiency cores.

2x 2TB is overkill, and 2x 1TB in RAID0 would likely be enough for most use cases.

## Buy

All Amazon links are affiliate links, thank you for supporting Ludus development.

### Hardware Base

- ~[Bare bones K8](https://www.gmktec.com/products/amd-ryzen-7-8845hs-mini-pc-nucbox-k8) - Will need RAM and NVMe from below~ No longer available from GMKTec

- [Bare bones K8 Plus](https://www.gmktec.com/products/amd-ryzen-7-8845hs-mini-pc-nucbox-k8-plus) - Will need RAM and NVMe from below

- [Bare bones K6](https://www.gmktec.com/products/amd-ryzen-7-7840hs-mini-pc-nucbox-k6) - Basically the same as the K8 but with a 7000 series GPU, will need RAM and NVMe from below

OR

- [Pre-Configured K8+ 64GB/1TB at Amazon](https://amzn.to/4ixCsih) - If you buy this variant you don't need anything else below but only have 64GB RAM and a single NVMe

### RAM Options

128GB

- [Crucial 128GB 5600MHz DDR5](https://amzn.to/4ijGeeQ)

96GB

- [Mushkin Redline 96GB 5600MHz DDR5](https://amzn.to/4dar7Cm)
- [Crucial 96GB 5600MHz DDR5](https://amzn.to/3UvXofE)

64GB

- [Silicon Power 64GB 5600MHz DDR5](https://amzn.to/3JAjXKc)
- [Crucial 64GB 5600MHz DDR5](https://amzn.to/3QhebAM)
- [Mushkin Redline 64GB 5600MHz DDR5](https://amzn.to/4b4uDgh)

### NVMe Options (Look for Gen4 with ~7,000MB/s speeds)

- [Samsung 990 Pro 1TB](https://amzn.to/3WeIH1P)
- [Crucial T500 1TB](https://amzn.to/49X3r1o)
- [WD Black 1TB](https://amzn.to/3xNpYAp)

### NVMe Heatsinks

- [Low profile copper heatsink](https://amzn.to/3WbxGhS)

## Install

1. Install Debian 12 or 13 - make note of the root and user passwords set during install. Set up RAID0 if you have multiple drives for greater speed.
2. Follow the Install Ludus quick-start guide.
