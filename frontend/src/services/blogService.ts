import api from './api';

// TypeScript interfaces matching backend schemas
export interface Author {
  id: number;
  name: string;
  bio?: string;
  profile_picture_url?: string;
  created_at: string;
}

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  excerpt?: string;
  author_id: number;
  publication_date?: string;
  created_at: string;
  updated_at?: string;
  author?: Author;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export const blogService = {
  /**
   * Get paginated list of blog posts
   * @param limit Number of posts to return (default: 10, max: 100)
   * @param offset Number of posts to skip (default: 0)
   * @returns Array of blog posts
   */
  async getPosts(limit: number = 10, offset: number = 0): Promise<BlogPost[]> {
    const response = await api.get<BlogPost[]>('/api/posts/', {
      params: { limit, offset },
    });
    return response.data;
  },

  /**
   * Get a single blog post by ID with full content
   * @param id Blog post ID
   * @returns Blog post with author information
   */
  async getPostById(id: number): Promise<BlogPost> {
    const response = await api.get<BlogPost>(`/api/posts/${id}`);
    return response.data;
  },

  /**
   * Get author details by ID
   * @param id Author ID
   * @returns Author information
   */
  async getAuthorById(id: number): Promise<Author> {
    const response = await api.get<Author>(`/api/posts/authors/${id}`);
    return response.data;
  },
};
