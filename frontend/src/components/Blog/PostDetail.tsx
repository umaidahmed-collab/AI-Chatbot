import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { blogService, BlogPost, Author } from '../../services/blogService';
import {
  ArrowLeftIcon,
  UserCircleIcon,
  CalendarIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';

const PostDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [author, setAuthor] = useState<Author | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadPost(parseInt(id));
    }
  }, [id]);

  const loadPost = async (postId: number) => {
    try {
      setLoading(true);
      setError(null);

      // Fetch post details
      const postData = await blogService.getPostById(postId);
      setPost(postData);

      // Fetch author details separately if author_id exists
      if (postData.author_id) {
        try {
          const authorData = await blogService.getAuthorById(postData.author_id);
          setAuthor(authorData);
        } catch (authorErr) {
          console.error('Error loading author details:', authorErr);
          // Continue even if author fetch fails
        }
      }
    } catch (err: any) {
      console.error('Error loading blog post:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to load blog post. Please try again later.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleBackClick = () => {
    navigate('/blog');
  };

  const formatDate = (dateString?: string): string => {
    if (!dateString) return 'No date';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return 'Invalid date';
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading blog post...</p>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !post) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow p-8">
          <div className="flex flex-col items-center justify-center text-center">
            <ExclamationCircleIcon className="h-16 w-16 text-red-500 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Unable to Load Post
            </h3>
            <p className="text-gray-600 mb-6 max-w-md">
              {error || 'Post not found'}
            </p>
            <button
              onClick={handleBackClick}
              className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
            >
              Back to Feed
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Post content
  return (
    <div className="max-w-4xl mx-auto">
      {/* Back Navigation Button */}
      <button
        onClick={handleBackClick}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
      >
        <ArrowLeftIcon className="h-5 w-5" />
        <span>Back to Feed</span>
      </button>

      {/* Post Container */}
      <article className="bg-white rounded-lg shadow-lg">
        <div className="p-8">
          {/* Post Title */}
          <h1 className="text-4xl font-bold text-gray-900 mb-6">
            {post.title}
          </h1>

          {/* Post Metadata */}
          <div className="flex items-center space-x-6 text-sm text-gray-500 mb-8 pb-6 border-b border-gray-200">
            {/* Publication Date */}
            <div className="flex items-center space-x-2">
              <CalendarIcon className="h-5 w-5" />
              <span>
                {formatDate(post.publication_date || post.created_at)}
              </span>
            </div>

            {/* Author Name */}
            <div className="flex items-center space-x-2">
              <UserCircleIcon className="h-5 w-5" />
              <span>
                {author?.name || post.author?.name || `Author ${post.author_id}`}
              </span>
            </div>
          </div>

          {/* Post Content */}
          <div className="prose prose-lg max-w-none mb-8">
            <div className="text-gray-800 whitespace-pre-wrap leading-relaxed">
              {post.content}
            </div>
          </div>

          {/* Author Bio Section */}
          {author && (author.bio || author.profile_picture_url) && (
            <div className="mt-8 pt-8 border-t border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                About the Author
              </h2>
              <div className="flex items-start space-x-4">
                {/* Author Profile Picture */}
                {author.profile_picture_url ? (
                  <img
                    src={author.profile_picture_url}
                    alt={author.name}
                    className="w-16 h-16 rounded-full object-cover"
                  />
                ) : (
                  <UserCircleIcon className="w-16 h-16 text-gray-400" />
                )}

                {/* Author Info */}
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-2">
                    {author.name}
                  </h3>
                  {author.bio && (
                    <p className="text-gray-600 text-sm">
                      {author.bio}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </article>
    </div>
  );
};

export default PostDetail;
