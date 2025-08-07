<script lang="ts">
  import { onMount } from 'svelte';
  import { isAuthenticated, logout } from '../stores/auth';
  import { createBook, deleteBook, listBooks, updateBook, voteBook } from '../api/books';
  
  let books: any[] = [];
  let loading = true;
  let error: string | null = null;
  let search = '';
  let form = { title: '', author: '', price: '' };

  async function fetchBooks() {
    loading = true;
    try {
      books = await listBooks({ search });
    } catch (err: any) {
      error = err?.response?.data?.detail || 'Failed to load books';
    } finally {
      loading = false;
    }
  }

  onMount(fetchBooks);

  async function handleCreate(e: Event) {
    e.preventDefault();
    try {
      await createBook({ title: form.title, author: form.author, price: Number(form.price) });
      form = { title: '', author: '', price: '' };
      fetchBooks();
    } catch (err: any) {
      error = err?.response?.data?.detail || 'Failed to create';
    }
  }

  async function handleUpdate(id: number) {
    const title = prompt('New title?') || undefined;
    const author = prompt('New author?') || undefined;
    const priceStr = prompt('New price?') || undefined;
    try {
      await updateBook(id, { title, author, price: priceStr ? Number(priceStr) : undefined });
      fetchBooks();
    } catch (err: any) {
      error = err?.response?.data?.detail || 'Failed to update';
    }
  }

  async function handleDelete(id: number) {
    if (!confirm('Delete this book?')) return;
    try {
      await deleteBook(id);
      books = books.filter((b) => b.id !== id);
    } catch (err: any) {
      error = err?.response?.data?.detail || 'Failed to delete';
    }
  }

  async function handleVote(id: number, direction: 1 | 0 | -1) {
    try {
      await voteBook(id, direction);
      fetchBooks();
    } catch (err: any) {
      error = err?.response?.data?.detail || 'Failed to vote';
    }
  }
</script>

<div class="max-w-5xl mx-auto p-4">
  <div class="flex items-center justify-between mb-4">
    <h2 class="text-2xl font-semibold">Books</h2>
    <div>
      {#if $isAuthenticated}
        <button class="px-3 py-1 rounded bg-gray-100 hover:bg-gray-200" on:click={logout}>Logout</button>
      {:else}
        <span class="text-gray-500">Guest</span>
      {/if}
    </div>
  </div>

  <div class="flex gap-2 mb-4">
    <input class="border border-gray-300 rounded px-3 py-2 flex-1" placeholder="Search by title" bind:value={search} />
    <button class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700" on:click={fetchBooks}>Search</button>
  </div>

  {#if $isAuthenticated}
    <form on:submit|preventDefault={handleCreate} class="grid grid-cols-1 sm:grid-cols-4 gap-2 mb-4">
      <input class="border border-gray-300 rounded px-3 py-2" placeholder="Title" bind:value={form.title} required />
      <input class="border border-gray-300 rounded px-3 py-2" placeholder="Author" bind:value={form.author} required />
      <input class="border border-gray-300 rounded px-3 py-2" type="number" step="0.01" placeholder="Price" bind:value={form.price} required />
      <button class="px-4 py-2 rounded bg-green-600 text-white hover:bg-green-700" type="submit">Add</button>
    </form>
  {/if}

  {#if loading}
    <p>Loading...</p>
  {:else if error}
    <p class="text-red-600">{error}</p>
  {:else}
    <div class="overflow-x-auto">
      <table class="w-full text-left border border-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="p-2 border-b">Title</th>
            <th class="p-2 border-b">Author</th>
            <th class="p-2 border-b">Price</th>
            <th class="p-2 border-b">Votes</th>
            <th class="p-2 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each books as b (b.id)}
            <tr class="odd:bg-white even:bg-gray-50">
              <td class="p-2 border-b">{b.title}</td>
              <td class="p-2 border-b">{b.author}</td>
              <td class="p-2 border-b">${b.price.toFixed(2)}</td>
              <td class="p-2 border-b">{b.votes ?? 0}</td>
              <td class="p-2 border-b flex flex-wrap gap-2">
                <button class="px-2 py-1 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50" on:click={() => handleVote(b.id, 1)} disabled={!$isAuthenticated}>Upvote</button>
                <button class="px-2 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50" on:click={() => handleVote(b.id, -1)} disabled={!$isAuthenticated}>Downvote</button>
                <button class="px-2 py-1 rounded bg-gray-600 text-white hover:bg-gray-700 disabled:opacity-50" on:click={() => handleVote(b.id, 0)} disabled={!$isAuthenticated}>Clear</button>
                <button class="px-2 py-1 rounded bg-amber-500 text-white hover:bg-amber-600 disabled:opacity-50" on:click={() => handleUpdate(b.id)} disabled={!$isAuthenticated}>Edit</button>
                <button class="px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700 disabled:opacity-50" on:click={() => handleDelete(b.id)} disabled={!$isAuthenticated}>Delete</button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>


