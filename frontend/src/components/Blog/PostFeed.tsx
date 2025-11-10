import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { blogService, BlogPost } from '../../services/blogService';
import {
  DocumentTextIcon,
  UserCircleIcon,
  CalendarIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';

const PostFeed: React.FC = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      setLoading(true);
      setError(null);
      const postsData = await blogService.getPosts(20, 0);
      setPosts(postsData);
    } catch (err: any) {
      console.error('Error loading blog posts:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to load blog posts. Please try again later.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handlePostClick = (postId: number) => {
    navigate(`/blog/${postId}`);
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
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading blog posts...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-8">
        <div className="flex flex-col items-center justify-center text-center">
          <ExclamationCircleIcon className="h-16 w-16 text-red-500 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Unable to Load Posts
          </h3>
          <p className="text-gray-600 mb-6 max-w-md">{error}</p>
          <button
            onClick={loadPosts}
            className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Empty state
  if (posts.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8">
        <div className="text-center">
          <DocumentTextIcon className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No Blog Posts Yet
          </h3>
          <p className="text-gray-600">
            Check back later for new content!
          </p>
        </div>
      </div>
    );
  }

  // Posts list
  return (
    <div className="space-y-6">
      {posts.map((post) => (
        <div
          key={post.id}
          onClick={() => handlePostClick(post.id)}
          className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer group"
        >
          <div className="p-6">
            {/* Post Title */}
            <h2 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors">
              {post.title}
            </h2>

            {/* Post Excerpt */}
            {post.excerpt && (
              <p className="text-gray-700 mb-4 line-clamp-3">
                {post.excerpt}
              </p>
            )}

            {/* Post Metadata */}
            <div className="flex items-center space-x-6 text-sm text-gray-500">
              {/* Author */}
              <div className="flex items-center space-x-2">
                <UserCircleIcon className="h-5 w-5" />
                <span>
                  {post.author?.name || `Author ${post.author_id}`}
                </span>
              </div>

              {/* Publication Date */}
              <div className="flex items-center space-x-2">
                <CalendarIcon className="h-5 w-5" />
                <span>
                  {formatDate(post.publication_date || post.created_at)}
                </span>
              </div>
            </div>

            {/* Read More Indicator */}
            <div className="mt-4 text-primary-600 font-medium text-sm group-hover:text-primary-700 transition-colors">
              Read more →
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PostFeed;
