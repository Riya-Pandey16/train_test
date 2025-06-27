<template>
  <div class="post-page">
    <h2>📢 Share Your Ideas / Notes / Videos</h2>

    <!-- Post submission form -->
    <form @submit.prevent="submitPost" class="post-form">
      <input
        v-model="newPost.title"
        type="text"
        placeholder="Enter post title"
        required
      />
      <textarea
        v-model="newPost.content"
        placeholder="Write your idea, note, or video link here..."
        required
      ></textarea>
      <input
        type="file"
        @change="handleFileUpload"
        accept="image/*,application/pdf,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation"
      />
      <button type="submit">Post</button>
    </form>

    <!-- Search bar -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="🔍 Search posts"
      />
    </div>

    <!-- Posts feed -->
    <div class="post-feed">
      <h3>📝 Recent Posts</h3>
      <div
        class="post-card"
        v-for="post in filteredPosts"
        :key="post.id"
      >
        <div class="post-header">
          <strong>{{ post.author.name }}</strong>
          <span class="meta">{{ post.author.branch }}, Year {{ post.author.year }}</span>

          <!-- Delete button -->
          <!-- DELETE button: show only to admin or post owner -->
          <button
            v-if="currentUser.id && (post.user_id === currentUser.id || currentUser.is_admin)"
            @click="deletePost(post.id)"
            class="delete-btn"
          >
            🗑️ Delete
          </button>


        </div>

        <div class="post-content">
          <h4>{{ post.title }}</h4>
          <p v-if="isYouTubeLink(post.content)">
            📹 <a :href="post.content" target="_blank">{{ post.content }}</a>
          </p>
          <p v-else>{{ post.content }}</p>

          <!-- Show attached file if any -->
          <div v-if="post.file_url">
            <p><strong>📎 Attachment:</strong></p>
            <div v-if="isImage(post.file_url)">
              <img :src="post.file_url" alt="Uploaded image" style="max-width: 100%; margin-top: 10px;" />
            </div>
            <div v-else>
              <a :href="post.file_url" target="_blank">📄 View File</a>
            </div>
          </div>

          <small>{{ formatTimestamp(post.timestamp) }}</small>
        </div>
      </div>

      <div v-if="filteredPosts.length === 0">
        <p>No posts found matching your search.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostView',
  data() {
    return {
      currentUser: {},
      searchQuery: '',
      newPost: {
        title: '',
        content: ''
      },
      selectedFile: null,
      posts: [],
      loading: false,
      error: null
    };
  },
  computed: {
    filteredPosts() {
      const q = this.searchQuery.toLowerCase();
      return this.posts.filter(post =>
        post.title.toLowerCase().includes(q) ||
        post.content.toLowerCase().includes(q) ||
        post.author.name.toLowerCase().includes(q)
      );
    }
  },
  methods: {
    getAuthHeader() {
      const token = localStorage.getItem('token');
      return { 'Authorization': `Bearer ${token}` };
    },
   


    async fetchPosts() {
      this.loading = true;
      this.error = null;
      try {
        const res = await fetch('/posts/', {
          method: 'GET',
          headers: this.getAuthHeader()
        });
        if (!res.ok) throw new Error('Failed to fetch posts');
        this.posts = await res.json();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async submitPost() {
      const formData = new FormData();
      formData.append('title', this.newPost.title);
      formData.append('content', this.newPost.content);
      if (this.selectedFile) {
        formData.append('file', this.selectedFile);
      }

      try {
        const res = await fetch('/posts/', {
          method: 'POST',
          headers: this.getAuthHeader(),
          body: formData
        });
        if (!res.ok) throw new Error('Failed to submit post');

        await this.fetchPosts();
        this.newPost.title = '';
        this.newPost.content = '';
        this.selectedFile = null;
      } catch (err) {
        console.error(err);
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      const maxSizeMB = 10;
      if (file && file.size > maxSizeMB * 1024 * 1024) {
        alert(`File exceeds ${maxSizeMB}MB limit.`);
        return;
      }
      this.selectedFile = file;
    },

    async deletePost(postId) {
      if (!confirm('Are you sure you want to delete this post?')) return;

      try {
        const res = await fetch(`/posts/${postId}`, {
          method: 'DELETE',
          headers: this.getAuthHeader()
        });
        if (!res.ok) throw new Error('Failed to delete post');
        this.posts = this.posts.filter(p => p.id !== postId);
      } catch (err) {
        console.error(err);
      }
    },

    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },

    isYouTubeLink(content) {
      return content.includes('youtube.com') || content.includes('youtu.be');
    },

    isImage(fileUrl) {
      return /\.(jpg|jpeg|png|gif|webp)$/i.test(fileUrl);
    }
  },
  async mounted() {
    try {
      const userRes = await fetch('/profile/profile/me', {
        headers: this.getAuthHeader()
      });
      if (!userRes.ok) throw new Error('Failed to fetch user');
      const user = await userRes.json();
      console.log('Current user:', user); // DEBUG
      this.currentUser = user;
    } catch (e) {
      console.error('Error fetching user profile:', e);
    }

    await this.fetchPosts();
  }
};
</script>


<style scoped>
.post-page {
  padding: 20px;
  max-width: 800px;
  margin: auto;
  font-family: Arial, sans-serif;
  background-color: hsl(0, 0%, 95%);
}
.post-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 30px;
  font-size: 12px;
  color: #0e0b0a;
}
.post-form input,
.post-form textarea {
  padding: 10px;
  font-size: 16px;
  font-size: 12px;
  color: #070403ce;
}
.post-form button {
  padding: 10px;
  font-size: 16px;
  background-color: #2d88ff;
  color: white;
  border: none;
  cursor: pointer;
}
.search-bar input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
}
.post-feed {
  margin-top: 20px;
}
.post-card {
  background: #dee8ed;
  border: 2px solid #27191915;
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 8px;
}
.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
 
}
.meta {
  font-size: 12px;
  color: #4630ea;
}
.delete-btn {
  background: none;
  border: none;
  color: #d11a2a;
  font-size: 16px;
  cursor: pointer;
}
.post-content h4 {
  margin: 10px 0;
  font-size: 16px;
  color: #d11a2a;

}
</style>
