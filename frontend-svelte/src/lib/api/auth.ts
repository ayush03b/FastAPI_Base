import { api } from './client';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function login(req: LoginRequest): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/login', req);
  return data;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export async function register(req: RegisterRequest) {
  const { data } = await api.post('/users', req);
  return data;
}


