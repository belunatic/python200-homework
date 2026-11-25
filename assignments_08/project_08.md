# Project

Supabase is setup and the tables have been confirmed

# Amazon Calculator

## Scenario A — Lightweight compute: A t3.micro EC2 instance (1 vCPU, 1 GB RAM), on-demand pricing, running 8 hours per day, 5 days per week (approximately 160 hours per month). Use the US East (N. Virginia) region.

- Cost is $1.66 per month and 12 months is 19.92
- The price surprise me, it is very low and affordable

## Scenario B — Heavy analytics workload: A p3.2xlarge EC2 instance (8 vCPU, 1 V100 GPU), running 24/7 for the full month (730 hours); an RDS db.m5.large instance (2 vCPU, 8 GB RAM); and an S3 Standard storage bucket with 1 TB of data. Use US East (N. Virginia).

- Cost is 2,438.94 per month and 12 months is $29,267.28
- Now this is out of hand, and a lot it make sense for the amount of service you are using.

## what does the cost difference tell you about when a GPU instance is or isn't worth it?

- The more GPU you use the higher the cost; Therefore, before starting a project asking " Does this workload need a GPU? " then moving from GPU instance to general-purpose insatnce can save thousands of dollars per month.

## The recording

- [The video](https://youtu.be/xUs-lq85VOo)
