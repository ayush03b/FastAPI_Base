<script lang="ts">
  import Login from './lib/pages/Login.svelte';
  import Register from './lib/pages/Register.svelte';
  import Books from './lib/pages/Books.svelte';
  import { isAuthenticated, logout } from './lib/stores/auth';
  import { readable } from 'svelte/store';

  const route = readable(window.location.hash || '#/', (set) => {
    const onHash = () => set(window.location.hash || '#/');
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  });
</script>

<nav class="border-b border-gray-200 px-4 py-3 flex gap-4 text-blue-600">
  <a href="#/">Books</a>
  <span class="text-gray-400">|</span>
  <a href="#/login">Login</a>
  <span class="text-gray-400">|</span>
  <a href="#/register">Register</a>
  <div class="ml-auto">
    {#if $isAuthenticated}
      <button class="px-3 py-1 rounded bg-gray-100 hover:bg-gray-200" on:click={logout}>Logout</button>
    {/if}
  </div>
</nav>

{#if $route === '#/' }
  <Books />
{:else if $route === '#/login'}
  <Login />
{:else if $route === '#/register'}
  <Register />
{:else}
  <Books />
{/if}
