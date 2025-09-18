"""
Unit tests for chat_service.py
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from sqlalchemy.orm import Session

from app.services.chat_service import ChatService, chat_service
from app.models.database import User, ChatSession, ChatMessage
from app.models.schemas import ChatRequest, ChatResponse


class TestChatService:
    """Test cases for ChatService class."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def mock_user(self):
        """Mock user object."""
        user = Mock(spec=User)
        user.id = 1
        user.username = "testuser"
        user.email = "test@example.com"
        return user

    @pytest.fixture
    def chat_service_instance(self):
        """Chat service instance for testing."""
        return ChatService()

    def test_create_session(self, chat_service_instance, mock_db, mock_user):
        """Test creating a new chat session."""
        # Mock database operations
        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1
        mock_session.user_id = 1
        mock_session.title = "Test Chat"

        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Mock the ChatSession constructor
        with patch('app.services.chat_service.ChatSession', return_value=mock_session):
            result = chat_service_instance.create_session(mock_db, mock_user, "Test Chat")

        # Assertions
        mock_db.add.assert_called_once_with(mock_session)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_session)
        assert result == mock_session

    def test_create_session_default_title(self, chat_service_instance, mock_db, mock_user):
        """Test creating a session with default title."""
        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1
        mock_session.user_id = 1
        mock_session.title = "New Chat"

        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        with patch('app.services.chat_service.ChatSession', return_value=mock_session):
            result = chat_service_instance.create_session(mock_db, mock_user)

        assert result == mock_session

    def test_get_session(self, chat_service_instance, mock_db, mock_user):
        """Test getting a chat session by ID."""
        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1
        mock_session.user_id = 1

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_session
        mock_db.query.return_value = mock_query

        result = chat_service_instance.get_session(mock_db, 1, mock_user)

        mock_db.query.assert_called_once_with(ChatSession)
        assert result == mock_session

    def test_get_session_not_found(self, chat_service_instance, mock_db, mock_user):
        """Test getting a non-existent session."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query

        result = chat_service_instance.get_session(mock_db, 999, mock_user)

        assert result is None

    def test_get_user_sessions(self, chat_service_instance, mock_db, mock_user):
        """Test getting all user sessions."""
        mock_sessions = [Mock(spec=ChatSession), Mock(spec=ChatSession)]

        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = mock_sessions
        mock_db.query.return_value = mock_query

        result = chat_service_instance.get_user_sessions(mock_db, mock_user)

        mock_db.query.assert_called_once_with(ChatSession)
        assert result == mock_sessions

    def test_add_message(self, chat_service_instance, mock_db):
        """Test adding a message to a chat session."""
        mock_message = Mock(spec=ChatMessage)
        mock_message.id = 1
        mock_message.session_id = 1
        mock_message.content = "Test message"
        mock_message.role = "user"

        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        with patch('app.services.chat_service.ChatMessage', return_value=mock_message):
            result = chat_service_instance.add_message(mock_db, 1, "Test message", "user")

        mock_db.add.assert_called_once_with(mock_message)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_message)
        assert result == mock_message

    def test_get_session_messages(self, chat_service_instance, mock_db):
        """Test getting messages for a session."""
        mock_messages = [Mock(spec=ChatMessage), Mock(spec=ChatMessage)]

        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = mock_messages
        mock_db.query.return_value = mock_query

        result = chat_service_instance.get_session_messages(mock_db, 1)

        mock_db.query.assert_called_once_with(ChatMessage)
        assert result == mock_messages

    @pytest.mark.asyncio
    async def test_generate_response_new_session(self, chat_service_instance, mock_db, mock_user):
        """Test generating response with new session."""
        # Mock request
        request = ChatRequest(message="Hello", use_documents=False)

        # Mock session creation
        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1

        # Mock methods
        chat_service_instance.create_session = Mock(return_value=mock_session)
        chat_service_instance.get_session_messages = Mock(return_value=[])
        chat_service_instance.add_message = Mock()
        chat_service_instance._call_openai = AsyncMock(return_value="Hello! How can I help you?")

        with patch('app.services.chat_service.document_processor'):
            result = await chat_service_instance.generate_response(mock_db, request, mock_user)

        # Assertions
        chat_service_instance.create_session.assert_called_once_with(mock_db, mock_user)
        assert isinstance(result, ChatResponse)
        assert result.message == "Hello! How can I help you?"
        assert result.session_id == 1
        assert result.sources is None

    @pytest.mark.asyncio
    async def test_generate_response_existing_session(self, chat_service_instance, mock_db, mock_user):
        """Test generating response with existing session."""
        # Mock request
        request = ChatRequest(message="Hello", session_id=1, use_documents=False)

        # Mock session
        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1

        # Mock methods
        chat_service_instance.get_session = Mock(return_value=mock_session)
        chat_service_instance.get_session_messages = Mock(return_value=[])
        chat_service_instance.add_message = Mock()
        chat_service_instance._call_openai = AsyncMock(return_value="Hello! How can I help you?")

        with patch('app.services.chat_service.document_processor'):
            result = await chat_service_instance.generate_response(mock_db, request, mock_user)

        # Assertions
        chat_service_instance.get_session.assert_called_once_with(mock_db, 1, mock_user)
        assert isinstance(result, ChatResponse)
        assert result.message == "Hello! How can I help you?"
        assert result.session_id == 1

    @pytest.mark.asyncio
    async def test_generate_response_session_not_found(self, chat_service_instance, mock_db, mock_user):
        """Test generating response with non-existent session."""
        request = ChatRequest(message="Hello", session_id=999, use_documents=False)

        # Mock get_session to return None
        chat_service_instance.get_session = Mock(return_value=None)

        with pytest.raises(ValueError, match="Session not found"):
            await chat_service_instance.generate_response(mock_db, request, mock_user)

    @pytest.mark.asyncio
    async def test_generate_response_with_documents(self, chat_service_instance, mock_db, mock_user):
        """Test generating response with document context."""
        request = ChatRequest(message="What is the document about?", use_documents=True)

        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1

        # Mock document search results
        mock_doc_results = [
            {"content": "This is document content", "metadata": {"document_id": "doc1"}},
            {"content": "More document content", "metadata": {"document_id": "doc2"}}
        ]

        chat_service_instance.create_session = Mock(return_value=mock_session)
        chat_service_instance.get_session_messages = Mock(return_value=[])
        chat_service_instance.add_message = Mock()
        chat_service_instance._call_openai = AsyncMock(return_value="Based on the documents...")

        with patch('app.services.chat_service.document_processor') as mock_doc_processor:
            mock_doc_processor.search_documents.return_value = mock_doc_results
            result = await chat_service_instance.generate_response(mock_db, request, mock_user)

        mock_doc_processor.search_documents.assert_called_once_with("What is the document about?")
        assert result.sources == ["Document doc1", "Document doc2"]

    @pytest.mark.asyncio
    async def test_generate_response_with_conversation_history(self, chat_service_instance, mock_db, mock_user):
        """Test generating response with conversation history."""
        request = ChatRequest(message="Continue the conversation", use_documents=False)

        mock_session = Mock(spec=ChatSession)
        mock_session.id = 1

        # Mock conversation history
        mock_messages = []
        for i in range(15):  # More than 10 to test limit
            msg = Mock(spec=ChatMessage)
            msg.role = "user" if i % 2 == 0 else "assistant"
            msg.content = f"Message {i}"
            mock_messages.append(msg)

        chat_service_instance.create_session = Mock(return_value=mock_session)
        chat_service_instance.get_session_messages = Mock(return_value=mock_messages)
        chat_service_instance.add_message = Mock()

        # Mock _call_openai to capture the conversation history passed
        async def mock_call_openai(message, context, history):
            # Should only include last 10 messages
            assert len(history) == 10
            return "Response with history"

        chat_service_instance._call_openai = AsyncMock(side_effect=mock_call_openai)

        with patch('app.services.chat_service.document_processor'):
            result = await chat_service_instance.generate_response(mock_db, request, mock_user)

        assert result.message == "Response with history"

    @pytest.mark.asyncio
    async def test_call_openai_success(self, chat_service_instance):
        """Test successful OpenAI API call."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "AI response"

        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        chat_service_instance.client = mock_client

        with patch('app.services.chat_service.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-key"
            result = await chat_service_instance._call_openai(
                "Hello", "", [{"role": "user", "content": "Previous message"}]
            )

        assert result == "AI response"
        mock_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_openai_no_api_key(self, chat_service_instance):
        """Test OpenAI call without API key."""
        with patch('app.services.chat_service.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = None
            result = await chat_service_instance._call_openai("Hello", "", [])

        assert "I need an OpenAI API key" in result
        assert "Hello" in result

    @pytest.mark.asyncio
    async def test_call_openai_api_error(self, chat_service_instance):
        """Test OpenAI API error handling."""
        mock_client = AsyncMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        chat_service_instance.client = mock_client

        with patch('app.services.chat_service.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-key"
            result = await chat_service_instance._call_openai("Hello", "", [])

        assert "I need an OpenAI API key" in result
        assert "Hello" in result

    @pytest.mark.asyncio
    async def test_call_openai_with_context(self, chat_service_instance):
        """Test OpenAI call with document context."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response with context"

        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        chat_service_instance.client = mock_client

        with patch('app.services.chat_service.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-key"
            result = await chat_service_instance._call_openai(
                "Question", "Document context", []
            )

        # Verify system message includes context
        call_args = mock_client.chat.completions.create.call_args[1]
        messages = call_args['messages']
        system_message = messages[0]['content']
        assert "Document context" in system_message
        assert result == "Response with context"

    def test_fallback_response_with_context(self, chat_service_instance):
        """Test fallback response with document context."""
        result = chat_service_instance._fallback_response("Test question", "Document content")

        assert "Based on the uploaded documents" in result
        assert "Test question" in result
        assert "OpenAI API key" in result

    def test_fallback_response_without_context(self, chat_service_instance):
        """Test fallback response without document context."""
        result = chat_service_instance._fallback_response("Test question", "")

        assert "Test question" in result
        assert "OpenAI API key" in result
        assert "uploaded documents" not in result

    def test_global_chat_service_instance(self):
        """Test that global chat_service instance exists."""
        assert chat_service is not None
        assert isinstance(chat_service, ChatService)