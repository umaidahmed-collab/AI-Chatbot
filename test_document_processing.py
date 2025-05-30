#!/usr/bin/env python3
"""
Test script to verify document processing functionality.
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_document_processing():
    """Test document processing functionality."""
    print("🧪 Testing Document Processing\n")
    
    try:
        # Import after adding to path
        from app.services.document_processor import DocumentProcessor
        from app.utils.config import settings
        
        print("✅ Successfully imported document processor")
        
        # Create a test document processor
        processor = DocumentProcessor()
        print(f"✅ Document processor initialized")
        print(f"   - Upload directory: {processor.upload_dir}")
        print(f"   - ChromaDB path: {settings.CHROMA_DB_PATH}")
        print(f"   - OpenAI embeddings enabled: {processor.use_embeddings}")
        
        # Create a test text file
        test_content = """
        This is a test document for the AI chatbot.
        
        The chatbot can process various types of documents including:
        - PDF files
        - Word documents (DOCX)
        - Plain text files
        
        The system uses OpenAI embeddings for semantic search,
        allowing users to ask questions about their uploaded documents.
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            test_file_path = f.name
        
        print(f"✅ Created test file: {test_file_path}")
        
        # Test text extraction
        try:
            extracted_text = processor.extract_text(test_file_path)
            print(f"✅ Text extraction successful: {len(extracted_text)} characters")
        except Exception as e:
            print(f"❌ Text extraction failed: {e}")
            return False
        
        # Test document processing
        try:
            success = await processor.process_document(test_file_path, 999)
            if success:
                print("✅ Document processing successful")
            else:
                print("❌ Document processing failed")
                return False
        except Exception as e:
            print(f"❌ Document processing error: {e}")
            return False
        
        # Test document search
        try:
            results = await processor.search_documents("chatbot features", n_results=3)
            print(f"✅ Document search successful: {len(results)} results found")
            
            if results:
                print("   Sample result:")
                print(f"   - Content preview: {results[0]['content'][:100]}...")
                print(f"   - Metadata: {results[0]['metadata']}")
        except Exception as e:
            print(f"❌ Document search error: {e}")
            return False
        
        # Test statistics
        try:
            stats = processor.get_document_stats()
            print(f"✅ Document statistics: {stats}")
        except Exception as e:
            print(f"❌ Statistics error: {e}")
        
        # Cleanup
        try:
            processor.delete_document_chunks(999)
            os.unlink(test_file_path)
            print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
        
        print("\n🎉 All document processing tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_openai_integration():
    """Test OpenAI integration."""
    print("\n🧪 Testing OpenAI Integration\n")
    
    try:
        from app.services.chat_service import ChatService
        
        chat_service = ChatService()
        
        if chat_service.client:
            print("✅ OpenAI client initialized successfully")
            print(f"   - Model: {chat_service.model}")
        else:
            print("⚠️  OpenAI client not initialized (API key not provided)")
            print("   - This is expected if OPENAI_API_KEY is not set")
            print("   - The application will use fallback responses")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI integration error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 AI Chatbot Document Processing Test Suite\n")
    
    # Test document processing
    doc_test_passed = await test_document_processing()
    
    # Test OpenAI integration
    openai_test_passed = await test_openai_integration()
    
    print(f"\n📊 Test Results:")
    print(f"   - Document Processing: {'✅ PASSED' if doc_test_passed else '❌ FAILED'}")
    print(f"   - OpenAI Integration: {'✅ PASSED' if openai_test_passed else '❌ FAILED'}")
    
    if doc_test_passed and openai_test_passed:
        print("\n🎉 All tests passed! The document processing system is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
