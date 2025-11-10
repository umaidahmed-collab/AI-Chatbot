import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { blogService, BlogPost } from '../../services/blogService';
import {
  DocumentTextIcon,
  UserCircleIcon,
  CalendarIcon,
  ExclamationCircleIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from '@heroicons/react/24/outline';

const POSTS_PER_PAGE = 10;

const PostFeed: React.FC = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMorePosts, setHasMorePosts] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  // Get current page from URL query parameters (default to 1)
  const currentPage = parseInt(searchParams.get('page') || '1', 10);

  useEffect(() => {
    loadPosts();
  }, [currentPage]);

  const loadPosts = async () => {
    try {
      setLoading(true);
      setError(null);
      const offset = (currentPage - 1) * POSTS_PER_PAGE;
      // Request one extra post to determine if there are more pages
      const postsData = await blogService.getPosts(POSTS_PER_PAGE + 1, offset);

      // Check if there are more posts
      if (postsData.length > POSTS_PER_PAGE) {
        setHasMorePosts(true);
        setPosts(postsData.slice(0, POSTS_PER_PAGE));
      } else {
        setHasMorePosts(false);
        setPosts(postsData);
      }
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

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setSearchParams({ page: String(currentPage - 1) });
      // Scroll to top when changing pages
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleNextPage = () => {
    if (hasMorePosts) {
      setSearchParams({ page: String(currentPage + 1) });
      // Scroll to top when changing pages
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
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
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600 text-sm sm:text-base">Loading blog posts...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8 lg:p-12">
        <div className="flex flex-col items-center justify-center text-center">
          <ExclamationCircleIcon className="h-12 w-12 sm:h-16 sm:w-16 text-red-500 mb-4" />
          <h3 className="text-base sm:text-lg lg:text-xl font-semibold text-gray-900 mb-2">
            Unable to Load Posts
          </h3>
          <p className="text-sm sm:text-base text-gray-600 mb-6 max-w-md px-4">{error}</p>
          <button
            onClick={loadPosts}
            className="px-4 sm:px-6 py-2 sm:py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-all hover:shadow-md text-sm sm:text-base"
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
      <div className="bg-white rounded-lg shadow-lg p-6 sm:p-8 lg:p-12">
        <div className="text-center">
          <DocumentTextIcon className="h-12 w-12 sm:h-16 sm:w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-base sm:text-lg lg:text-xl font-semibold text-gray-900 mb-2">
            No Blog Posts Yet
          </h3>
          <p className="text-sm sm:text-base text-gray-600">
            Check back later for new content!
          </p>
        </div>
      </div>
    );
  }

  // Posts list
  return (
    <div className="space-y-8">
      {/* Posts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        {posts.map((post) => (
          <div
            key={post.id}
            onClick={() => handlePostClick(post.id)}
            className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer group transform hover:-translate-y-1"
          >
            <div className="p-4 sm:p-6 flex flex-col h-full">
              {/* Post Title */}
              <h2 className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900 mb-2 sm:mb-3 group-hover:text-primary-600 transition-colors line-clamp-2">
                {post.title}
              </h2>

              {/* Post Excerpt */}
              {post.excerpt && (
                <p className="text-sm sm:text-base text-gray-700 mb-4 line-clamp-3 flex-grow">
                  {post.excerpt}
                </p>
              )}

              {/* Post Metadata */}
              <div className="space-y-3 mt-auto">
                {/* Author */}
                <div className="flex items-center space-x-3">
                  {post.author?.profile_picture_url ? (
                    <img
                      src={post.author.profile_picture_url}
                      alt={post.author.name}
                      className="w-8 h-8 sm:w-10 sm:h-10 rounded-full object-cover border-2 border-gray-200"
                    />
                  ) : (
                    <UserCircleIcon className="w-8 h-8 sm:w-10 sm:h-10 text-gray-400" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="text-xs sm:text-sm font-medium text-gray-900 truncate">
                      {post.author?.name || `Author ${post.author_id}`}
                    </p>
                    <div className="flex items-center text-xs text-gray-500">
                      <CalendarIcon className="h-3 w-3 sm:h-4 sm:w-4 mr-1 flex-shrink-0" />
                      <span className="truncate">
                        {formatDate(post.publication_date || post.created_at)}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Read More Indicator */}
                <div className="pt-2 border-t border-gray-100">
                  <span className="text-primary-600 font-medium text-xs sm:text-sm group-hover:text-primary-700 transition-colors inline-flex items-center">
                    Read more
                    <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination Controls */}
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6">
        <div className="flex items-center justify-between">
          {/* Previous Button */}
          <button
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
            className={`
              flex items-center space-x-1 sm:space-x-2 px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base
              ${
                currentPage === 1
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-500 text-white hover:bg-primary-600 hover:shadow-md'
              }
            `}
          >
            <ChevronLeftIcon className="h-4 w-4 sm:h-5 sm:w-5" />
            <span className="hidden xs:inline">Previous</span>
            <span className="xs:hidden">Prev</span>
          </button>

          {/* Page Indicator */}
          <div className="text-gray-700 font-medium text-sm sm:text-base">
            Page {currentPage}
          </div>

          {/* Next Button */}
          <button
            onClick={handleNextPage}
            disabled={!hasMorePosts}
            className={`
              flex items-center space-x-1 sm:space-x-2 px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base
              ${
                !hasMorePosts
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-500 text-white hover:bg-primary-600 hover:shadow-md'
              }
            `}
          >
            <span>Next</span>
            <ChevronRightIcon className="h-4 w-4 sm:h-5 sm:w-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostFeed;
