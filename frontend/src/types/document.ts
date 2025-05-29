export interface Document {
  id: number;
  filename: string;
  original_filename: string;
  file_path: string;
  file_size: number;
  content_type: string;
  processed: boolean;
  owner_id: number;
  created_at: string;
  updated_at?: string;
}
