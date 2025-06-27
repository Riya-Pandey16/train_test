<!-- MsgView.vue -->
<!-- MsgView.vue -->
<template>
  <div class="msg-view-container" :class="{ dark: isDarkMode }">
    <!-- Sidebar -->
    <div class="sidebar">
      <button class="theme-toggle" @click="toggleTheme">{{ isDarkMode ? '🌙' : '☀️' }}</button>
      <input v-model="search" @input="fetchUsers" placeholder="Search users..." class="search-bar" />
      <ul>
        <li v-for="user in filteredUsers" :key="user.id" @click="selectUser(user)" :class="{ active: selectedUser?.id === user.id }">
          <img :src="user.profile_picture || defaultProfile" class="avatar" />
          <span>{{ user.name }}</span>
        </li>
      </ul>
    </div>

    <!-- Chat Area -->
    <div class="chat-area" v-if="selectedUser">
      <div class="chat-header">
        <img :src="selectedUser.profile_picture || defaultProfile" class="avatar" />
        <h3>{{ selectedUser.name }}</h3>
        <div class="status">{{ typing ? `${selectedUser.name} is typing...` : '' }}</div>
      </div>

      <div class="chat-messages" ref="chatMessages">
        <div v-for="msg in messages" :key="msg.id" class="message" :class="{ own: msg.sender_id === currentUser.id }">
          <div class="msg-content" @contextmenu.prevent="openMsgOptions(msg, $event)">
            <div v-if="msg.file">
              <a :href="msg.file" target="_blank">📎 File</a>
            </div>
            <div v-else>{{ msg.content }}</div>
            <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
            <div class="reactions">
              <span v-for="(emoji, i) in msg.reactions" :key="i">{{ emoji }}</span>

            </div>
          </div>
        </div>
      </div>

      <!-- Context Menu -->
      <div v-if="showMsgOptions" class="context-menu" :style="{ top: msgMenu.y + 'px', left: msgMenu.x + 'px' }">
        <div v-for="emoji in emojis" :key="emoji" @click="reactToMessage(msgMenu.msg.id, emoji)">React {{ emoji }}</div>
        <div @click="deleteMessage(msgMenu.msg.id, 'self')">Delete for Me</div>
        <div v-if="msgMenu.msg.sender_id === currentUser.id" @click="deleteMessage(msgMenu.msg.id, 'everyone')">Delete for Everyone</div>
      </div>

      <!-- Input Area -->
      <div class="chat-input">
        <textarea v-model="newMessage" @keyup.enter.exact.prevent="sendMessage" @input="emitTyping" placeholder="Type a message..." />
        <input
          type="file"
          ref="fileInput"
          @change="handleFileChange"
          style="display: none"
        />
        <button @click="sendMessage">Send</button>
        <button @click="toggleEmoji">😊</button>
        <button @click="triggerFileInput">📎</button>
      </div>

      <!-- Emoji Picker -->
      <div v-if="showEmoji" class="emoji-picker">
        <span v-for="emoji in emojis" :key="emoji" @click="addEmoji(emoji)">{{ emoji }}</span>
      </div>
    </div>

    <div v-else class="no-user">
      <p>Select a user to start chatting.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { io } from 'socket.io-client'

const socket = io(window.location.origin, {
  path: '/socket.io',
  transportOptions: {
    polling: {
      extraHeaders: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }
  }
})


// State
const users = ref([])
const messages = ref([])
const search = ref('')
const newMessage = ref('')
const selectedUser = ref(null)
const typing = ref(false)
const showEmoji = ref(false)
const chatMessages = ref(null)

const currentUser = reactive({ id: 0, name: '' })
const defaultProfile = '/default-avatar.png'
const emojis = ['😀', '😂', '😍', '😢', '😡', '👍', '👎', '❤️', '🎉', '🙏']

const showMsgOptions = ref(false)
const msgMenu = reactive({ msg: null, x: 0, y: 0 })
const isDarkMode = ref(false)

// Theme
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark-mode', isDarkMode.value)
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

const filteredUsers = computed(() =>
  users.value.filter((u) => u.name.toLowerCase().includes(search.value.toLowerCase()))
)

const fetchUsers = async () => {
  const res = await fetch('/chat/users', {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
  })
  users.value = await res.json()
}

const selectUser = async (user) => {
  selectedUser.value = user
  const res = await fetch(`/chat/messages/${user.id}`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
  })
  messages.value = await res.json()
  socket.emit('join_room', { user_id: currentUser.id, target_id: user.id })
  scrollToBottom()
}

// Send message
const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  const msg = { content: newMessage.value, receiver_id: selectedUser.value.id }
  const res = await fetch('/chat/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify(msg),
  })
  const saved = await res.json()
  messages.value.push(saved)
  socket.emit('send_message', saved)
  newMessage.value = ''
  scrollToBottom()
}

socket.on('message_sent', (msg) => {
  if (msg.receiver_id === currentUser.id || msg.sender_id === currentUser.id) {
    messages.value.push({
      id: msg.id,
      content: msg.content,
      file: msg.file,
      sender_id: msg.sender_id,
      receiver_id: msg.receiver_id,
      timestamp: msg.timestamp,
      reactions: msg.reactions || []
    })
    scrollToBottom()
  }
})


socket.on('receive_message', (msg) => {
  if (
    selectedUser.value &&
    (msg.sender_id === selectedUser.value.id || msg.receiver_id === selectedUser.value.id)
  ) {
    messages.value.push({
      id: msg.id,
      content: msg.content,
      file: msg.file,
      sender_id: msg.sender_id,
      receiver_id: msg.receiver_id,
      timestamp: msg.timestamp,
      reactions: msg.reactions || []
    })
    scrollToBottom()
  }
})

const emitTyping = () => {
  if (selectedUser.value) {
    socket.emit('typing', { to: selectedUser.value.id, from: currentUser.id })
  }
}

socket.on('user_typing', ({ from }) => {
  if (selectedUser.value?.id === from) {
    typing.value = true
    setTimeout(() => (typing.value = false), 1500)
  }
})

const scrollToBottom = () => {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight
    }
  })
}

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file || !selectedUser.value) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/chat/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) throw new Error(`Upload failed: ${JSON.stringify(data)}`);
    console.log("Uploaded:", data);

    // Now send the file as a message
    const msg = {
      file: data.file_url, // make sure your backend sends this field
      receiver_id: selectedUser.value.id,
    };

    const res2 = await fetch("/chat/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(msg),
    });

    const saved = await res2.json();
    messages.value.push(saved);
    socket.emit("send_message", saved);
    scrollToBottom();
  } catch (err) {
    console.error("Upload error:", err);
  }
};


const fileInput = ref(null);

const triggerFileInput = () => {
  if (fileInput.value) fileInput.value.click();
};

//const fileInput = ref(null)

const openMsgOptions = (msg, event) => {
  msgMenu.msg = msg
  msgMenu.x = event.clientX
  msgMenu.y = event.clientY
  showMsgOptions.value = true
  setTimeout(() => (showMsgOptions.value = false), 5000)
}

const reactToMessage = async (msgId, emoji) => {
  await fetch('/chat/react', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify({ message_id: msgId, reaction: emoji }),
  })
  const msg = messages.value.find((m) => m.id === msgId)
  if (msg && !msg.reactions.includes(emoji)) msg.reactions.push(emoji)
  showMsgOptions.value = false
}

const deleteMessage = async (msgId, mode) => {
  await fetch(`/chat/delete/${msgId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify({ mode }),
  })
  messages.value = messages.value.filter((m) => m.id !== msgId)
  showMsgOptions.value = false
}

const toggleEmoji = () => (showEmoji.value = !showEmoji.value)
const addEmoji = (emoji) => {
  newMessage.value += emoji
  showEmoji.value = false
}

const formatTime = (timestamp) => new Date(timestamp).toLocaleTimeString()

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.documentElement.classList.add('dark-mode')
  }

  const token = localStorage.getItem('token')
  const userData = JSON.parse(atob(token.split('.')[1]))
  currentUser.id = userData.id
  currentUser.name = userData.name
  fetchUsers()
})
</script>







<style scoped>
.context-menu {
  position: absolute;
  background: #fff;
  border: 1px solid #ccc;
  z-index: 10;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.context-menu div {
  padding: 5px;
  cursor: pointer;
}
.context-menu div:hover {
  background-color: #f0f0f0;
}

.msg-view-container {
  display: flex;
  height: 90vh;
  background-color: #d9f3d2;
  border-radius: 3px;
}
.sidebar {
  width: 25%;
  border-right: 1px solid #010101;
  overflow-y: auto;
}
.search-bar {
  width: 100%;
  padding: 10px;
  border: none;
  border-bottom: 1px solid #ccc;
}
.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar li {
  display: flex;
  align-items: center;
  padding: 10px;
  cursor: pointer;
}
.sidebar li.active {
  background-color: #e0e0e0;
}
.sidebar .avatar {
  width: 32px;
  height: 32px;
  margin-right: 10px;
  border-radius: 50%;
}
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.chat-header {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #d9f3d2;
  border-bottom: 1px solid #ccc;
}
.chat-header .avatar {
  width: 36px;
  height: 36px;
  margin-right: 10px;
  border-radius: 50%;
}
.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background: #e5ddd5;
}
.message {
  margin: 5px 0;
  max-width: 60%;
}
.message.own {
  margin-left: auto;
  background: #dcf8c6;
}
.message .msg-content {
  background: #fff;
  padding: 8px;
  border-radius: 8px;
  position: relative;
}
.timestamp {
  font-size: 0.7em;
  color: #999;
  margin-left: 5px;
}
.chat-input {
  display: flex;
  padding: 10px;
  background: #fff;
  align-items: center;
}
.chat-input textarea {
  flex: 1;
  resize: none;
  border: 1px solid #0a0707;
  padding: 8px;
  border-radius: 6px;
}
.chat-input button {
  background: #3f3673;
  border: 2px solid #0a0707;
  margin-left: 5px;
  font-size: 1.2em;
  cursor: pointer;
}
.chat-input button:first-child {
  background: #2f6c3d;
  color: white;
  border-radius: 6px;
  padding: 8px 12px;
}
.emoji-picker {
  background: #fff;
  padding: 10px;
  border-top: 1px solid #ccc;
  display: flex;
  flex-wrap: wrap;
}
.emoji-picker span {
  font-size: 1.5em;
  margin: 5px;
  cursor: pointer;
}
.no-user {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
}
.theme-toggle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f4f4f4;
  border: 1px solid #ccc;
  font-size: 18px;
  cursor: pointer;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}
.theme-toggle:hover {
  background-color: #ddd;
}
/* Dark mode global styles */
:global(.dark-mode) {
  background-color: #121212;
  color: #ffffff;
}
:global(.dark-mode input),
:global(.dark-mode textarea) {
  background-color: #2a2a2a;
  color: #fff;
  border-color: #444;
}
:global(.dark-mode .message-bubble) {
  background-color: #2e2e2e;
}
.theme-toggle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f4f4f4;
  border: 1px solid #ccc;
  font-size: 18px;
  cursor: pointer;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}
.theme-toggle:hover {
  background-color: #ddd;
}

.chat-input {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #f0f0f0;
  border-top: 1px solid #ccc;
}
.chat-input textarea {
  flex: 1;
  resize: none;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  height: 40px;
}
.chat-input button {
  margin-left: 8px;
  background: #4caf50;
  color: white;
  border: none;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
.chat-input button:hover {
  background: #45a049;
}
.emoji-picker {
  background: white;
  border: 1px solid #ccc;
  padding: 8px;
  position: absolute;
  bottom: 60px;
  right: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  z-index: 20;
}
.emoji-picker span {
  font-size: 20px;
  margin: 5px;
  cursor: pointer;
}
.no-user {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  color: #777;
  background: #e5ddd5;
}
.theme-toggle {
  margin: 10px;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
.dark-mode {
  background-color: #1e1e1e;
  color: white;
}
.dark-mode .sidebar {
  background-color: #2e2e2e;
}
.dark-mode .chat-header,
.dark-mode .chat-input,
.dark-mode .message .msg-content,
.dark-mode .chat-messages {
  background-color: #333 !important;
  color: white;
}
.dark-mode .context-menu {
  background-color: #444;
  color: white;
}
.dark-mode .emoji-picker {
  background-color: #555;
}

/* Global dark theme base */
:global(.dark-mode) {
  background-color: #121212;
  color: #f5f5f5;
}
/* Make sure inputs/textareas adapt */
:global(.dark-mode input),
:global(.dark-mode textarea) {
  background-color: #2a2a2a;
  color: #fff;
  border-color: #555;
}
/* Optional: override link styles */
:global(.dark-mode a) {
  color: #8ab4f8;
}
/* Chat area specific */
.chat-container {
  background-color: #ffffff;
  transition: background 0.3s ease, color 0.3s ease;
}
.chat-container.dark-chat {
  background-color: #1f1f1f;
  color: #e0e0e0;
}
/* Message bubbles */
.message-bubble {
  background-color: #e4e4e4;
  color: #251c1c84;
  padding: 8px 12px;
  border-radius: 8px;
  margin-bottom: 6px;
  max-width: 60%;
}
.dark-chat .message-bubble {
  background-color: #333;
  color: #fff;
}
.message.own {
  background: #dcf8c6;
  border-left: 4px solid #34b7f1;
  padding-left: 6px;
}
.message {
  background: #fff;
  padding: 6px;
  border-radius: 6px;
  margin-bottom: 5px;
}
.uploaded-image {
  max-width: 200px;
  max-height: 200px;
  display: block;
  margin-top: 5px;
}
.scroll-btn {
  position: absolute;
  bottom: 70px;
  right: 30px;
  padding: 10px;
  border-radius: 50%;
  background: #34b7f1;
  color: white;
  border: none;
}



</style>
