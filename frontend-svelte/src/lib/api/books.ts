import { api } from './client';

export interface Book {
  id: number;
  title: string;
  author: string;
  price: number;
  created_at: string;
  owner_id: number;
  votes?: number;
}

export interface CreateBookRequest {
  title: string;
  author: string;
  price: number;
}

export interface UpdateBookRequest {
  title?: string;
  author?: string;
  price?: number;
}

export async function listBooks(params?: { limit?: number; skip?: number; search?: string }) {
  const { data } = await api.get<Book[]>('/books', { params });
  return data;
}

export async function createBook(payload: CreateBookRequest) {
  const { data } = await api.post<Book>('/books', payload);
  return data;
}

export async function updateBook(id: number, payload: UpdateBookRequest) {
  const { data } = await api.put<Book>(`/books/${id}`, payload);
  return data;
}

export async function deleteBook(id: number) {
  await api.delete(`/books/${id}`);
}

export async function voteBook(bookId: number, direction: 1 | 0 | -1) {
  const { data } = await api.post(`/votes/`, { book_id: bookId, direction });
  return data as { message: string };
}


