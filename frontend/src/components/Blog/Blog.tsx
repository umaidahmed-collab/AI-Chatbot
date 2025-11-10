import React from 'react';
import { Routes, Route } from 'react-router-dom';
import PostFeed from './PostFeed';
import PostDetail from './PostDetail';

const Blog: React.FC = () => {
  return (
    <div className="p-4 sm:p-6 lg:p-8">
      <Routes>
        {/* Blog post feed (default route) */}
        <Route index element={<PostFeed />} />

        {/* Individual post detail page */}
        <Route path=":id" element={<PostDetail />} />
      </Routes>
    </div>
  );
};

export default Blog;
