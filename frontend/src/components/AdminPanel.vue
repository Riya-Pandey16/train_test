<template>
  <div class="admin-panel">
    <h2>👨‍💼 Admin Dashboard</h2>

    <section>
      <h3>All Users</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Is Admin</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.is_admin ? 'Yes' : 'No' }}</td>
            <td>
              <button @click="deleteUser(user.id)" :disabled="user.is_admin">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section>
      <h3>All Posts</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Content</th>
            <th>User ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.id">
            <td>{{ post.id }}</td>
            <td>{{ post.content }}</td>
            <td>{{ post.user_id }}</td>
            <td>
              <button @click="deletePost(post.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AdminPanel',
  data() {
    return {
      users: [],
      posts: []
    };
  },
  methods: {
    async fetchData() {
      const token = localStorage.getItem('token');
      try {
        const userRes = await fetch('http://localhost:5000/admin/users', {
          headers: { Authorization: `Bearer ${token}` }
        });
        const postRes = await fetch('http://localhost:5000/admin/posts', {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (userRes.status === 403 || postRes.status === 403) {
          alert('Access Denied: Admins only');
          this.$router.push('/home');
          return;
        }

        this.users = await userRes.json();
        this.posts = await postRes.json();
      } catch (error) {
        console.error('Error fetching admin data:', error);
      }
    },
    async deleteUser(userId) {
      if (!confirm('Are you sure you want to delete this user?')) return;
      const token = localStorage.getItem('token');
      await fetch(`http://localhost:5000/admin/user/${userId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      this.fetchData();
    },
    async deletePost(postId) {
      if (!confirm('Are you sure you want to delete this post?')) return;
      const token = localStorage.getItem('token');
      await fetch(`http://localhost:5000/admin/post/${postId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      this.fetchData();
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user?.is_admin) {
      alert('Access Denied: Admins only');
      this.$router.push('/home');
      return;
    }
    this.fetchData();
  }
};
</script>

<style scoped>
.admin-panel {
  padding: 20px;
}
h2, h3 {
  margin-top: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}
th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}
button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
}
button:hover {
  background-color: #c82333;
}
</style>
