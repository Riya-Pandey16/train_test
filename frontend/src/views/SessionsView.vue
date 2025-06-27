<template>
  <div class="session-container">
    <h2 class="title">📅 Upcoming Sessions</h2>

    <!-- Session Cards -->
    <div class="session-grid">
      <div v-for="session in sessions" :key="session.id" class="session-card">
        <div class="session-info">
          <h3 class="session-topic">🎓 {{ session.topic }}</h3>
          <p class="session-time">🕒 {{ formatDateTime(session.time) }}</p>
          <p class="session-link">
            🔗 <a :href="session.link" target="_blank">{{ session.link }}</a>
          </p>
        </div>
        <div class="session-actions">
          <button class="join-btn" @click="joinSession(session)">Join</button>
          <button
            class="delete-btn"
            v-if="session.user_id === currentUserId"
            @click="deleteSession(session.id)"
          >
            🗑️ Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Create New Session -->
    <div class="create-session-form">
      <h3 class="form-title">➕ Create New Session</h3>
      <form @submit.prevent="createSession">
        <div class="form-group">
          <label class="form-label">Topic</label>
          <input
            v-model="topic"
            type="text"
            placeholder="Enter session topic"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label class="form-label">Time</label>
          <input
            v-model="time"
            type="datetime-local"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label class="form-label">Session Link (Zoom / Jitsi / WebRTC)</label>
          <input
            v-model="link"
            type="url"
            placeholder="https://meet.jit.si/your-room"
            required
            class="form-input"
          />
        </div>
        <button type="submit" class="submit-btn">Create Session</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      topic: '',
      time: '',
      link: '',
      sessions: [],
      currentUserId: null
    };
  },
  mounted() {
    this.fetchCurrentUser();
    this.fetchSessions();
  },
  methods: {
    formatDateTime(datetime) {
      return new Date(datetime).toLocaleString();
    },
    async fetchCurrentUser() {
      try {
        const token = localStorage.getItem('token');
        if (!token) return;

        const res = await fetch('/profile/profile/me', {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (res.ok) {
          const data = await res.json();
          this.currentUserId = data.id;
        } else {
          console.error('❌ Failed to get current user');
        }
      } catch (err) {
        console.error('❌ Error fetching current user', err);
      }
    },
    async fetchSessions() {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch('/session/all', {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (res.ok) {
          this.sessions = await res.json();
        } else {
          console.error('❌ Failed to fetch sessions');
        }
      } catch (err) {
        console.error('❌ Error fetching sessions', err);
      }
    },
    async createSession() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('❌ You must be logged in to create a session');
          return;
        }

        const response = await fetch('/session/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            topic: this.topic,
            time: this.time,
            link: this.link
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Unknown error');
        }

        const result = await response.json();
        this.sessions.push(result); // Update UI instantly

        alert(`✅ Session created: "${result.topic}"`);

        // Clear form
        this.topic = '';
        this.time = '';
        this.link = '';
      } catch (err) {
        alert(`❌ Error: ${err.message}`);
        console.error(err);
      }
    },
    joinSession(session) {
      if (session.link) {
        window.open(session.link, '_blank');
      } else {
        alert('❌ No session link provided.');
      }
    },
    async deleteSession(sessionId) {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`/session/delete/${sessionId}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (res.ok) {
          this.sessions = this.sessions.filter((s) => s.id !== sessionId);
          alert('✅ Session deleted');
        } else {
          const data = await res.json();
          alert(`❌ Error: ${data.error}`);
        }
      } catch (err) {
        console.error('❌ Error deleting session:', err);
      }
    }
  }
};
</script>

<style scoped>
.session-container {
  max-width: 900px;
  margin: auto;
  padding: 2rem;
}

.title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(to right, #3b82f6, #6366f1);
  color: white;
  padding: 0.8rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);

}

.session-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  margin-bottom: 2.5rem;

}

.session-card {
  background-color: #fff;
  border: 2px solid #e0e7ff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

}

.session-info {
  margin-bottom: 1rem;
}

.session-topic {
  font-weight: bold;
  font-size: 1.2rem;
}

.session-time,
.session-link {
  font-size: 0.95rem;
}

.session-actions {
  display: flex;
  justify-content: space-between;
}

.join-btn,
.delete-btn {
  background: #4caf50;
  color: white;
  padding: 0.4rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.delete-btn {
  background: #e53935;
}

.create-session-form {
  margin-top: 3rem;
  background: #eef2f7;
  padding: 1.5rem;
  border-radius: 10px;
}

.form-title {
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.submit-btn {
  background-color: #1976d2;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
