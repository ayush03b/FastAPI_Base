import { writable, derived } from 'svelte/store';
import type { LoginRequest, RegisterRequest, TokenResponse } from '../api/auth';
import { login as apiLogin, register as apiRegister } from '../api/auth';

const tokenStore = writable<string | null>(localStorage.getItem('access_token'));

tokenStore.subscribe((val) => {
  if (val) localStorage.setItem('access_token', val);
  else localStorage.removeItem('access_token');
});

export const token = tokenStore;
export const isAuthenticated = derived(tokenStore, ($t) => Boolean($t));

export async function login(payload: LoginRequest) {
  const res: TokenResponse = await apiLogin(payload);
  tokenStore.set(res.access_token);
}

export async function register(payload: RegisterRequest) {
  await apiRegister(payload);
}

export function logout() {
  tokenStore.set(null);
}


