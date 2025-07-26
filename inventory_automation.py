import os
import shopify
import csv
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Shopify configuration
SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
API_VERSION = '2025-01'

# AWS S3 configuration
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

def initialize_shopify():
    """Initialize Shopify API session."""
    try:
        shopify.ShopifyResource.set_site(f'https://{SHOP_NAME}/admin/api/{API_VERSION}')
        shopify.ShopifyResource.set_access_token(ACCESS_TOKEN)
        logger.info("Shopify API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Shopify API: {e}")
        raise

def get_inventory():
    """Retrieve inventory levels from Shopify."""
    try:
        initialize_shopify()
        inventory_levels = shopify.InventoryLevel.find()
        logger.info(f"Retrieved {len(inventory_levels)} inventory levels")
        return inventory_levels
    except Exception as e:
        logger.error(f"Error retrieving inventory levels: {e}")
        return []

def save_inventory_to_csv(inventory_levels, file_name='inventory.csv'):
    """Save inventory data to a CSV file."""
    try:
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['location_id', 'inventory_item_id', 'available', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for level in inventory_levels:
                writer.writerow({
                    'location_id': level.location_id,
                    'inventory_item_id': level.inventory_item_id,
                    'available': level.available,
                    'updated_at': level.updated_at
                })
        logger.info(f"Inventory data saved to {file_name}")
        return file_name
    except Exception as e:
        logger.error(f"Error saving inventory to CSV: {e}")
        raise

def upload_to_s3(file_name, bucket):
    """Upload the CSV file to S3."""
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        # Use timestamped filename to avoid overwriting
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f'inventory_{timestamp}.csv'
        s3.upload_file(file_name, bucket, s3_key)
        logger.info(f"Uploaded {file_name} to S3 bucket {bucket} as {s3_key}")
    except FileNotFoundError:
        logger.error(f"The file was not found: {file_name}")
        raise
    except NoCredentialsError:
        logger.error("AWS credentials not available")
        raise
    except ClientError as e:
        logger.error(f"Error uploading to S3: {e}")
        raise

def main():
    """Main function to run the inventory automation."""
    try:
        inventory_levels = get_inventory()
        if not inventory_levels:
            logger.warning("No inventory levels retrieved")
            return
        file_name = save_inventory_to_csv(inventory_levels)
        upload_to_s3(file_name, S3_BUCKET_NAME)
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        raise

if __name__ == '__main__':
    main()
