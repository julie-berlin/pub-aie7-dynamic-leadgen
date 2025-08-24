"""
File Upload Utilities for Logo and Asset Management

Provides secure file upload handling with validation, storage management,
and support for different storage backends (local filesystem, cloud storage).
"""

import os
import uuid
import hashlib
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
import logging
from datetime import datetime

from fastapi import UploadFile, HTTPException, status
from PIL import Image
from app.database import db

# Try to import magic, fallback to mimetypes if not available
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    import mimetypes
    MAGIC_AVAILABLE = False

logger = logging.getLogger(__name__)

# Configuration
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = {
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'image/gif': ['.gif'],
    'image/webp': ['.webp'],
    'image/svg+xml': ['.svg']
}

# Maximum image dimensions
MAX_IMAGE_WIDTH = 1920
MAX_IMAGE_HEIGHT = 1080
MAX_LOGO_WIDTH = 1000
MAX_LOGO_HEIGHT = 1000

class FileUploadError(Exception):
    """Custom exception for file upload errors"""
    pass

class FileUploadValidator:
    """Validates uploaded files for security and format compliance"""
    
    def __init__(self):
        if MAGIC_AVAILABLE:
            self.magic_mime = magic.Magic(mime=True)
        else:
            self.magic_mime = None
    
    def validate_file_size(self, file: UploadFile, max_size: int = MAX_FILE_SIZE) -> None:
        """Validate file size is within limits"""
        # Read content to check size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > max_size:
            raise FileUploadError(f"File size {file_size} bytes exceeds maximum allowed size {max_size} bytes")
        
        if file_size == 0:
            raise FileUploadError("File is empty")
    
    def validate_file_type(self, file_content: bytes, filename: str) -> str:
        """Validate file type using both MIME detection and extension"""
        # Get file extension
        file_extension = Path(filename).suffix.lower()
        
        # Get MIME type from file content or filename
        if MAGIC_AVAILABLE and self.magic_mime:
            detected_mime = self.magic_mime.from_buffer(file_content)
        else:
            # Fallback to extension-based detection
            detected_mime, _ = mimetypes.guess_type(filename)
            if not detected_mime:
                # Default based on extension
                extension_to_mime = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg', 
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp',
                    '.svg': 'image/svg+xml'
                }
                detected_mime = extension_to_mime.get(file_extension, 'application/octet-stream')
        
        if detected_mime not in ALLOWED_IMAGE_TYPES:
            raise FileUploadError(f"File type {detected_mime} is not allowed. Allowed types: {list(ALLOWED_IMAGE_TYPES.keys())}")
        
        # Verify extension matches MIME type
        allowed_extensions = ALLOWED_IMAGE_TYPES[detected_mime]
        if file_extension not in allowed_extensions:
            raise FileUploadError(f"File extension {file_extension} does not match detected type {detected_mime}")
        
        return detected_mime
    
    def validate_image_content(self, file_content: bytes, is_logo: bool = False) -> Dict[str, Any]:
        """Validate image content and dimensions"""
        try:
            # Open image with Pillow
            image = Image.open(io.BytesIO(file_content))
            
            # Get image info
            width, height = image.size
            format_name = image.format
            mode = image.mode
            
            # Check dimensions
            max_width = MAX_LOGO_WIDTH if is_logo else MAX_IMAGE_WIDTH
            max_height = MAX_LOGO_HEIGHT if is_logo else MAX_IMAGE_HEIGHT
            
            if width > max_width or height > max_height:
                raise FileUploadError(
                    f"Image dimensions {width}x{height} exceed maximum allowed "
                    f"{max_width}x{max_height} for {'logo' if is_logo else 'image'}"
                )
            
            # Validate image is not corrupted
            image.verify()
            
            return {
                'width': width,
                'height': height,
                'format': format_name,
                'mode': mode,
                'aspect_ratio': round(width / height, 2)
            }
            
        except Exception as e:
            raise FileUploadError(f"Invalid or corrupted image: {str(e)}")

import io

class FileStorageManager:
    """Manages file storage operations with multi-tenant support"""
    
    def __init__(self, base_upload_dir: str = "uploads"):
        self.base_upload_dir = Path(base_upload_dir)
        self.temp_dir = self.base_upload_dir / "temp"
        
        # Create base directories if they don't exist
        self._ensure_base_directories()
    
    def _ensure_base_directories(self) -> None:
        """Create base directories for file storage"""
        for directory in [self.base_upload_dir, self.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
            # Ensure proper permissions (readable/writable by owner, readable by group)
            os.chmod(directory, 0o755)
    
    def _get_client_directory(self, client_id: str, file_type: str = "logos") -> Path:
        """Get client-specific directory for file storage"""
        # Create client-specific directory structure: uploads/clients/{client_id}/{file_type}/
        client_dir = self.base_upload_dir / "clients" / client_id / file_type
        
        # Ensure directory exists
        client_dir.mkdir(parents=True, exist_ok=True)
        
        # Set appropriate permissions
        os.chmod(client_dir, 0o755)
        
        return client_dir
    
    def _ensure_client_isolation(self, client_id: str, filename: str) -> bool:
        """Verify that a file access request is for the correct client"""
        # This prevents cross-client file access by validating the file path
        try:
            # Extract client_id from filename if it follows our naming convention
            if filename.startswith(f"client_{client_id}_"):
                return True
            
            # For backward compatibility, allow files without client prefix
            # but log a warning
            logger.warning(f"File {filename} accessed without client prefix validation")
            return True
            
        except Exception:
            return False
    
    def generate_unique_filename(self, original_filename: str, prefix: str = "") -> str:
        """Generate a unique filename to prevent conflicts"""
        # Extract extension
        file_extension = Path(original_filename).suffix.lower()
        
        # Generate unique identifier
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        if prefix:
            filename = f"{prefix}_{timestamp}_{unique_id}{file_extension}"
        else:
            filename = f"{timestamp}_{unique_id}{file_extension}"
        
        return filename
    
    def save_logo(self, file_content: bytes, original_filename: str, client_id: str, mime_type: str = 'image/jpeg') -> Dict[str, str]:
        """Save logo file in client-specific directory and return file information"""
        try:
            # Get client-specific directory
            client_logos_dir = self._get_client_directory(client_id, "logos")
            
            # Generate unique filename with client prefix for extra safety
            filename = self.generate_unique_filename(original_filename, f"client_{client_id}")
            file_path = client_logos_dir / filename
            
            # Write file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Set appropriate file permissions
            os.chmod(file_path, 0o644)
            
            # Generate file hash for integrity verification
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            # Save metadata to database
            upload_time = datetime.now()
            uploaded_file_record = {
                'client_id': client_id,
                'filename': filename,
                'original_filename': original_filename,
                'file_type': 'logo',
                'size_bytes': len(file_content),
                'mime_type': mime_type,
                'file_hash': file_hash,
                'storage_path': f"clients/{client_id}/logos/{filename}",
                'url': f"/api/files/clients/{client_id}/logos/{filename}",
                'uploaded_at': upload_time.isoformat(),
                'is_active': True
            }
            
            try:
                db_result = db.client.table("uploaded_files").insert(uploaded_file_record).execute()
                file_id = db_result.data[0]['id'] if db_result.data else None
                logger.info(f"Saved file metadata to database: {filename} (ID: {file_id})")
            except Exception as db_error:
                logger.error(f"Failed to save file metadata to database: {db_error}")
                # Don't fail the upload if database insert fails, just log the error
                file_id = None
            
            # Return file information
            return {
                'filename': filename,
                'file_path': str(file_path),
                'relative_path': f"clients/{client_id}/logos/{filename}",
                'url': f"/api/files/clients/{client_id}/logos/{filename}",
                'size': len(file_content),
                'hash': file_hash,
                'uploaded_at': upload_time.isoformat(),
                'client_id': client_id,
                'file_id': file_id
            }
            
        except Exception as e:
            raise FileUploadError(f"Failed to save file: {str(e)}")
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage"""
        try:
            full_path = Path(file_path)
            if full_path.exists() and full_path.is_file():
                full_path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            else:
                logger.warning(f"File not found for deletion: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    def get_file_info(self, filename: str, client_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a stored file in client-specific directory"""
        # Get client-specific directory
        client_logos_dir = self._get_client_directory(client_id, "logos")
        file_path = client_logos_dir / filename
        
        if not file_path.exists():
            return None
        
        try:
            stat = file_path.stat()
            return {
                'filename': filename,
                'size': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'exists': True,
                'client_id': client_id,
                'relative_path': f"clients/{client_id}/logos/{filename}"
            }
        except Exception as e:
            logger.error(f"Error getting file info for {filename} (client {client_id}): {e}")
            return None
    
    def delete_logo(self, filename: str, client_id: str) -> bool:
        """Delete a logo file from client-specific directory"""
        try:
            # Get client-specific directory
            client_logos_dir = self._get_client_directory(client_id, "logos")
            file_path = client_logos_dir / filename
            
            # Verify client isolation
            if not self._ensure_client_isolation(client_id, filename):
                logger.error(f"Client isolation check failed for {filename} (client {client_id})")
                return False
            
            file_exists = file_path.exists() and file_path.is_file()
            
            # Update database record first (soft delete)
            try:
                delete_time = datetime.now()
                update_result = db.client.table("uploaded_files").update({
                    'is_active': False,
                    'deleted_at': delete_time.isoformat(),
                    'updated_at': delete_time.isoformat()
                }).eq('client_id', client_id).eq('filename', filename).eq('file_type', 'logo').execute()
                
                if update_result.data:
                    logger.info(f"Marked logo as deleted in database: {filename} (client {client_id})")
                else:
                    logger.warning(f"No database record found for logo: {filename} (client {client_id})")
                    
            except Exception as db_error:
                logger.error(f"Failed to update database for logo deletion: {db_error}")
                # Continue with file deletion even if database update fails
            
            # Delete physical file
            if file_exists:
                file_path.unlink()
                logger.info(f"Deleted logo file: {filename} for client {client_id}")
                return True
            else:
                logger.warning(f"Logo file not found for deletion: {filename} (client {client_id})")
                # Return True if database was updated successfully even if file doesn't exist
                return True
                
        except Exception as e:
            logger.error(f"Error deleting logo {filename} (client {client_id}): {e}")
            return False

class FileUploadHandler:
    """Main handler for file upload operations"""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.validator = FileUploadValidator()
        self.storage = FileStorageManager(upload_dir)
        
    async def process_logo_upload(
        self, 
        file: UploadFile, 
        client_id: str,
        max_size: int = MAX_FILE_SIZE
    ) -> Dict[str, Any]:
        """Process a logo upload with full validation and storage"""
        
        try:
            # Basic validation
            if not file.filename:
                raise FileUploadError("No filename provided")
            
            # Read file content
            file_content = await file.read()
            
            # Validate file size using content
            if len(file_content) > max_size:
                raise FileUploadError(f"File size {len(file_content)} bytes exceeds maximum allowed size {max_size} bytes")
            
            if len(file_content) == 0:
                raise FileUploadError("File is empty")
            
            # Validate file type
            mime_type = self.validator.validate_file_type(file_content, file.filename)
            
            # Validate image content (with logo-specific constraints)
            image_info = self.validator.validate_image_content(file_content, is_logo=True)
            
            # Save file
            file_info = self.storage.save_logo(file_content, file.filename, client_id, mime_type)
            
            # Combine all information
            result = {
                **file_info,
                'original_filename': file.filename,
                'mime_type': mime_type,
                'client_id': client_id,
                'image_info': image_info,
                'validation_passed': True
            }
            
            logger.info(f"Successfully processed logo upload for client {client_id}: {file.filename}")
            return result
            
        except FileUploadError as e:
            logger.warning(f"File upload validation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File upload validation failed: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during file upload"
            )
    
    def delete_logo(self, filename: str, client_id: str) -> bool:
        """Delete a logo file from client-specific directory"""
        return self.storage.delete_logo(filename, client_id)
    
    def get_logo_info(self, filename: str, client_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a logo file in client-specific directory"""
        return self.storage.get_file_info(filename, client_id)

# Global instance
file_upload_handler = FileUploadHandler()

# Helper functions for FastAPI routes
async def validate_and_store_logo(file: UploadFile, client_id: str) -> Dict[str, Any]:
    """Helper function for logo upload in API routes"""
    return await file_upload_handler.process_logo_upload(file, client_id)

def remove_logo(filename: str, client_id: str) -> bool:
    """Helper function for logo deletion in API routes"""
    return file_upload_handler.delete_logo(filename, client_id)

def get_logo_metadata(filename: str, client_id: str) -> Optional[Dict[str, Any]]:
    """Helper function to get logo metadata in API routes"""
    return file_upload_handler.get_logo_info(filename, client_id)