# Inventory Automation System

A Python-based system that automates inventory tracking using Shopify’s API and stores data in AWS S3, demonstrating technical and project management expertise.

## Features
- **Inventory Tracking**: Retrieves inventory levels from Shopify’s REST Admin API.
- **Data Storage**: Saves inventory data as a CSV and uploads it to an AWS S3 bucket with timestamped filenames.
- **Automation**: Runs daily via GitHub Actions, ensuring consistent updates.
- **Error Handling**: Includes logging for debugging and reliability.

## Prerequisites
1. **Shopify Setup**:
   - Create a Shopify store or use an existing one via the [Shopify Partner Dashboard](https://partners.shopify.com/).
   - Create a private app with `read_inventory` and `write_inventory` permissions.
   - Note the **Shop Name** (e.g., `yourstore.myshopify.com`) and **Access Token**.

2. **AWS S3 Setup**:
   - Sign into the [AWS Management Console](https://aws.amazon.com/console/).
   - Create an S3 bucket (e.g., `shopify-inventory-data`).
   - Create an IAM user with `AmazonS3FullAccess` policy and note the **Access Key ID** and **Secret Access Key**.

## Setup Instructions
1. **Clone the Repository** (for local testing):
   ```bash
   git clone https://github.com/your-username/shopify-inventory-automation.git
   cd shopify-inventory-automation
