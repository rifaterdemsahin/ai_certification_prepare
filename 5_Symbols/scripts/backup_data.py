import os
import shutil
import subprocess
import sys
from datetime import datetime

try:
    from azure.storage.blob import BlobServiceClient
    azure_sdk_available = True
except ImportError:
    azure_sdk_available = False

def get_connection_string_from_key_vault():
    """Tries to retrieve the storage connection string from Azure Key Vault using Azure CLI"""
    print("🔑 Attempting to fetch connection string from Azure Key Vault (dp-kv-deliverypilot)...")
    try:
        # Check if az CLI is available
        subprocess.run(["az", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Azure CLI ('az') is not installed or not in PATH. Cannot query Key Vault automatically.")
        return None

    try:
        cmd = [
            "az", "keyvault", "secret", "show",
            "--vault-name", "dp-kv-deliverypilot",
            "--name", "AzureWebJobsStorage",
            "--query", "value",
            "-o", "tsv"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        connection_string = result.stdout.strip()
        if connection_string:
            print("✅ Successfully retrieved connection string from Azure Key Vault.")
            return connection_string
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Azure CLI command failed: {e.stderr.strip()}")
        print("   Make sure you are logged in using 'az login' and have access to the Key Vault.")
    
    return None

def download_azure_data(connection_string, temp_dir):
    """Downloads files from configured Azure Blob Storage containers to the backup folder"""
    if not azure_sdk_available:
        print("⚠️  Warning: azure-storage-blob library is not installed. Skipping Azure backup.")
        print("   Install it using: pip install azure-storage-blob")
        return

    print("🔗 Connecting to Azure Blob Storage...")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        containers = ['memory-cards', 'analyse-pages', 'concepts']
        
        for container_name in containers:
            print(f"📥 Checking container: {container_name}...")
            container_client = blob_service_client.get_container_client(container_name)
            
            try:
                # List blobs in container
                blobs = list(container_client.list_blobs())
                if not blobs:
                    print(f"   No blobs found in container: {container_name}")
                    continue
                
                # Create destination subdirectory
                dest_sub_dir = os.path.join(temp_dir, 'azure', container_name)
                os.makedirs(dest_sub_dir, exist_ok=True)
                
                print(f"   Found {len(blobs)} blobs. Downloading...")
                for blob in blobs:
                    blob_client = container_client.get_blob_client(blob.name)
                    # Resolve subfolders inside container if any
                    blob_dest_path = os.path.join(dest_sub_dir, blob.name)
                    os.makedirs(os.path.dirname(blob_dest_path), exist_ok=True)
                    
                    with open(blob_dest_path, "wb") as file:
                        download_stream = blob_client.download_blob()
                        file.write(download_stream.readall())
                
                print(f"   ✅ Finished downloading container: {container_name}")
            except Exception as e:
                print(f"   ⚠️  Could not backup container {container_name}: {e}")
                
    except Exception as e:
        print(f"❌ Azure Connection failed: {e}")

def run_backup():
    # Get project root (located 2 levels up from 5_Symbols/scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    data_dir = os.path.join(project_root, '5_Symbols', 'data')
    backups_dir = os.path.join(data_dir, 'backups')
    
    # Ensure backups directory exists
    os.makedirs(backups_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'backup_{timestamp}'
    backup_zip_path = os.path.join(backups_dir, backup_filename)
    
    # Files to backup (exclude the backups directory itself)
    files_to_backup = []
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        if os.path.isfile(item_path):
            files_to_backup.append(item)
            
    if not files_to_backup:
        print("❌ No local files found in data directory to backup.")
        return
        
    print(f"📦 Starting backup of data files from: {data_dir}")
    print(f"🗂 Local files found: {', '.join(files_to_backup)}")
    
    # Create temporary directory for zipping to avoid zipping the backups folder
    temp_dir = os.path.join(backups_dir, f'temp_{timestamp}')
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Copy local data files
        for file in files_to_backup:
            shutil.copy2(os.path.join(data_dir, file), os.path.join(temp_dir, file))
            
        # Get connection string from Env or Key Vault
        connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connection_string:
            connection_string = get_connection_string_from_key_vault()
            
        if connection_string:
            download_azure_data(connection_string, temp_dir)
        else:
            print("⚠️  Azure connection string unavailable. Skipping Azure download.")
            print("   Please login via 'az login' or export 'AZURE_STORAGE_CONNECTION_STRING'.")
            
        # Create zip archive
        shutil.make_archive(backup_zip_path, 'zip', temp_dir)
        print(f"✅ Backup created successfully: {backup_zip_path}.zip")
        
    except Exception as e:
        print(f"❌ Error during backup process: {e}")
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    run_backup()
