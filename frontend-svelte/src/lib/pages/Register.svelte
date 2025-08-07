<script lang="ts">
  import { register } from '../stores/auth';
  import { goto } from '../util/nav';
  let username = '';
  let email = '';
  let password = '';
  let error: string | null = null;
  let loading = false;

  async function onSubmit(e: Event) {
    e.preventDefault();
    error = null;
    loading = true;
    try {
      await register({ username, email, password });
      goto('#/login');
    } catch (err: any) {
      error = err?.response?.data?.detail || 'Registration failed';
    } finally {
      loading = false;
    }
  }
</script>

<div class="max-w-md mx-auto mt-12 p-6 border border-gray-200 rounded-lg">
  <h2 class="text-xl font-semibold mb-4">Register</h2>
  <form on:submit|preventDefault={onSubmit} class="space-y-4">
    <div class="space-y-1">
      <label class="block text-sm text-gray-700">Username</label>
      <input class="w-full border border-gray-300 rounded px-3 py-2" bind:value={username} required />
    </div>
    <div class="space-y-1">
      <label class="block text-sm text-gray-700">Email</label>
      <input class="w-full border border-gray-300 rounded px-3 py-2" type="email" bind:value={email} required />
    </div>
    <div class="space-y-1">
      <label class="block text-sm text-gray-700">Password</label>
      <input class="w-full border border-gray-300 rounded px-3 py-2" type="password" bind:value={password} required />
    </div>
    {#if error}
      <p class="text-red-600 text-sm">{error}</p>
    {/if}
    <button class="inline-flex items-center justify-center rounded bg-blue-600 text-white px-4 py-2 hover:bg-blue-700 disabled:opacity-50" type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Register'}</button>
  </form>
</div>


