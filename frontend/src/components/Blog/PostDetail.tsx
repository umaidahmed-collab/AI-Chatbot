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
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-2 border-primary-500 mx-auto mb-4"></div>
            <p className="text-gray-600 text-sm sm:text-base">Loading blog post...</p>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !post) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8 lg:p-12">
          <div className="flex flex-col items-center justify-center text-center">
            <ExclamationCircleIcon className="h-12 w-12 sm:h-16 sm:w-16 text-red-500 mb-4" />
            <h3 className="text-base sm:text-lg lg:text-xl font-semibold text-gray-900 mb-2">
              Unable to Load Post
            </h3>
            <p className="text-sm sm:text-base text-gray-600 mb-6 max-w-md px-4">
              {error || 'Post not found'}
            </p>
            <button
              onClick={handleBackClick}
              className="px-4 sm:px-6 py-2 sm:py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-all hover:shadow-md text-sm sm:text-base"
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
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Back Navigation Button */}
      <button
        onClick={handleBackClick}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4 sm:mb-6 transition-colors text-sm sm:text-base group"
      >
        <ArrowLeftIcon className="h-4 w-4 sm:h-5 sm:w-5 group-hover:-translate-x-1 transition-transform" />
        <span>Back to Feed</span>
      </button>

      {/* Post Container */}
      <article className="bg-white rounded-lg shadow-xl">
        <div className="p-4 sm:p-6 lg:p-8">
          {/* Post Title */}
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4 sm:mb-6 leading-tight">
            {post.title}
          </h1>

          {/* Post Metadata */}
          <div className="flex flex-wrap items-center gap-3 sm:gap-6 text-xs sm:text-sm text-gray-500 mb-6 sm:mb-8 pb-4 sm:pb-6 border-b border-gray-200">
            {/* Author with Profile Picture */}
            <div className="flex items-center space-x-2 sm:space-x-3">
              {author?.profile_picture_url ? (
                <img
                  src={author.profile_picture_url}
                  alt={author.name}
                  className="w-8 h-8 sm:w-10 sm:h-10 rounded-full object-cover border-2 border-gray-200"
                />
              ) : (
                <UserCircleIcon className="w-8 h-8 sm:w-10 sm:h-10 text-gray-400" />
              )}
              <span className="font-medium text-gray-700">
                {author?.name || post.author?.name || `Author ${post.author_id}`}
              </span>
            </div>

            {/* Publication Date */}
            <div className="flex items-center space-x-2">
              <CalendarIcon className="h-4 w-4 sm:h-5 sm:w-5 flex-shrink-0" />
              <span>
                {formatDate(post.publication_date || post.created_at)}
              </span>
            </div>
          </div>

          {/* Post Content */}
          <div className="prose prose-sm sm:prose-base lg:prose-lg max-w-none mb-6 sm:mb-8">
            <div className="text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base lg:text-lg">
              {post.content}
            </div>
          </div>

          {/* Author Bio Section */}
          {author && (author.bio || author.profile_picture_url) && (
            <div className="mt-6 sm:mt-8 pt-6 sm:pt-8 border-t border-gray-200">
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">
                About the Author
              </h2>
              <div className="flex items-start space-x-3 sm:space-x-4">
                {/* Author Profile Picture */}
                {author.profile_picture_url ? (
                  <img
                    src={author.profile_picture_url}
                    alt={author.name}
                    className="w-12 h-12 sm:w-16 sm:h-16 rounded-full object-cover border-2 border-gray-200 flex-shrink-0"
                  />
                ) : (
                  <UserCircleIcon className="w-12 h-12 sm:w-16 sm:h-16 text-gray-400 flex-shrink-0" />
                )}

                {/* Author Info */}
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 mb-1 sm:mb-2 text-base sm:text-lg">
                    {author.name}
                  </h3>
                  {author.bio && (
                    <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">
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
