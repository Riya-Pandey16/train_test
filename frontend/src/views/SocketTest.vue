<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Socket.IO Test Page</h2>

    <!-- Token Input -->
    <input v-model="token" placeholder="JWT Token" class="border p-2 mb-2 w-full" />

    <!-- Room Join -->
    <div class="flex gap-2 mb-2">
      <input v-model="room" placeholder="Room ID" class="border p-2 flex-1" />
      <button @click="joinRoom" class="bg-blue-500 text-white px-4 py-2 rounded">Join</button>
    </div>

    <!-- Message Input -->
    <div class="flex gap-2 mb-2">
      <input v-model="message" placeholder="Type a message" class="border p-2 flex-1" />
      <button @click="sendMessage" class="bg-green-500 text-white px-4 py-2 rounded">Send</button>
    </div>

    <!-- File Upload -->
    <div class="mb-2">
      <input type="file" @change="uploadFile" />
    </div>

    <!-- Messages -->
    <div class="bg-gray-100 p-2 h-64 overflow-y-scroll border rounded">
      <div v-for="(msg, index) in messages" :key="index" class="mb-2">
        <pre class="text-sm">{{ msg }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { io } from 'socket.io-client'

const socket = ref(null)
const token = ref('')
const message = ref('')
const room = ref('')
const messages = ref([])

const addLog = (msg) => {
  messages.value.push(`[${new Date().toLocaleTimeString()}] ${msg}`)
}

const connectSocket = () => {
  if (socket.value) {
    socket.value.disconnect()
  }

  socket.value = io('http://localhost:5000', {
    transports: ['websocket'],
    auth: { token: token.value }
  })

  socket.value.on('connect', () => {
    addLog('✅ Connected to socket.io')
  })

  socket.value.on('disconnect', () => {
    addLog('❌ Disconnected')
  })

  socket.value.on('receive_message', (data) => {
    addLog(`📩 Message from ${data.sender_id || 'unknown'}: ${data.text || '[file]'}`)
  })

  socket.value.on('error', (err) => {
    addLog(`⚠️ Socket error: ${err}`)
  })

  socket.value.on('connect_error', (err) => {
    addLog(`❌ Connect error: ${err.message}`)
  })
}

const joinRoom = () => {
  if (!socket.value) connectSocket()
  socket.value.emit('join_room', { room: room.value })
  addLog(`➡️ Joined room ${room.value}`)
}

const sendMessage = () => {
  if (!socket.value) return
  socket.value.emit('send_message', {
    room: room.value,
    text: message.value
  })
  addLog(`📤 Sent message: ${message.value}`)
  message.value = ''
}

const uploadFile = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch('http://localhost:5000/api/chat/upload', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token.value}`
    },
    body: formData
  })

  const data = await res.json()
  if (data.url) {
    addLog(`📎 File uploaded: ${data.url}`)
    // Send as message
    socket.value.emit('send_message', {
      room: room.value,
      file_url: data.url,
      file_name: file.name
    })
  } else {
    addLog(`❌ Upload failed: ${data.error || 'Unknown error'}`)
  }
}

onBeforeUnmount(() => {
  if (socket.value) socket.value.disconnect()
})
</script>

<style scoped>
input[type="file"] {
  border: 1px solid #ccc;
  padding: 6px;
}
</style>
