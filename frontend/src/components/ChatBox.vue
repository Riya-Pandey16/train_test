<template>
  <div class="chatbox">
    <div class="chat-header">
      <h3>Chat with {{ toUser.name }}</h3>
      <button class="clear-chat-btn" @click="clearChat" title="Clear Entire Chat">🗑️ Clear Chat</button>
    </div>

    <div class="messages" ref="messagesContainer">
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['message', msg.sender_id === fromUser.id ? 'my-message' : 'their-message']"
      >
        <input
          v-if="msg.sender_id === fromUser.id"
          type="checkbox"
          v-model="selectedMessages"
          :value="msg.id"
          class="select-msg-checkbox"
          title="Select message to delete"
        />
        <div class="message-text">{{ msg.message }}</div>
        <button
          v-if="msg.sender_id === fromUser.id"
          class="delete-msg-btn"
          @click="deleteMessage(msg.id)"
          title="Delete this message"
        >
          ❌
        </button>
      </div>
    </div>

    <div class="message-input">
      <input
        type="text"
        v-model="messageText"
        placeholder="Type a message"
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">📨</button>
      <button
        v-if="selectedMessages.length"
        class="delete-selected-btn"
        @click="deleteSelectedMessages"
        title="Delete selected messages"
      >
        🗑️ Delete Selected
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatBox',
  props: ['toUser', 'fromUser', 'socket'],
  data() {
    return {
      messages: [],
      messageText: '',
      selectedMessages: [],
      roomId: '',
    };
  },
  methods: {
    getRoomId(id1, id2) {
      return [id1, id2].sort().join('_');
    },
    sendMessage() {
      if (!this.messageText.trim()) return;
      if (!this.socket || !this.toUser) return;

      this.socket.emit('send_message', {
        sender_id: this.fromUser.id,
        receiver_id: this.toUser.id,
        message: this.messageText,
        room: this.roomId,
      });

      this.messageText = '';
    },
    deleteMessage(messageId) {
      if (!confirm('Delete this message?')) return;
      this.socket.emit('delete_message', { message_id: messageId, room: this.roomId });
    },
    deleteSelectedMessages() {
      if (!this.selectedMessages.length) return;
      if (!confirm(`Delete ${this.selectedMessages.length} selected messages?`)) return;

      this.selectedMessages.forEach((msgId) => {
        this.socket.emit('delete_message', { message_id: msgId, room: this.roomId });
      });
      this.selectedMessages = [];
    },
    clearChat() {
      if (!confirm('Are you sure you want to clear this chat?')) return;
      this.socket.emit('clear_chat', {
        user1: this.fromUser.id,
        user2: this.toUser.id,
        room: this.roomId,
      });
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) container.scrollTop = container.scrollHeight;
      });
    },
  },
  mounted() {
    this.roomId = this.getRoomId(this.fromUser.id, this.toUser.id);

    // Join the room
    this.socket.emit('join', { room: this.roomId, username: this.fromUser.name });

    // Load initial chat history (you can fetch via API here if needed)
    this.socket.emit('load_messages', { room: this.roomId });

    // Listen for new messages
    this.socket.on('receive_message', (msg) => {
      this.messages.push(msg);
      this.scrollToBottom();
    });

    // Listen for message deleted event
    this.socket.on('message_deleted', (data) => {
      this.messages = this.messages.filter((m) => m.id !== data.message_id);
    });

    // Listen for chat cleared event
    this.socket.on('chat_cleared', (data) => {
      if (data.room === this.roomId) this.messages = [];
    });

    // Receive initial loaded messages
    this.socket.on('messages_loaded', (msgs) => {
      this.messages = msgs;
      this.scrollToBottom();
    });
  },
  watch: {
    toUser(newUser) {
      if (!newUser || !this.fromUser) return;
      this.roomId = this.getRoomId(this.fromUser.id, newUser.id);
      this.messages = [];
      this.selectedMessages = [];
      this.socket.emit('join', { room: this.roomId, username: this.fromUser.name });
      this.socket.emit('load_messages', { room: this.roomId });
    },
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.off('receive_message');
      this.socket.off('message_deleted');
      this.socket.off('chat_cleared');
      this.socket.off('messages_loaded');
    }
  },
};
</script>

<style scoped>
.chatbox {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.clear-chat-btn {
  background: #ff4d4f;
  border: none;
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  cursor: pointer;
}

.clear-chat-btn:hover {
  background: #d9363e;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fafafa;
  margin-bottom: 10px;
}

.message {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.my-message {
  justify-content: flex-end;
}

.their-message {
  justify-content: flex-start;
}

.select-msg-checkbox {
  margin-right: 8px;
  cursor: pointer;
}

.message-text {
  background: #d2eafd;
  padding: 8px 12px;
  border-radius: 15px;
  max-width: 60%;
  word-wrap: break-word;
}

.my-message .message-text {
  background: #007bff;
  color: white;
}

.delete-msg-btn {
  background: transparent;
  border: none;
  color: #ff4d4f;
  cursor: pointer;
  margin-left: 5px;
  font-size: 14px;
}

.message-input {
  display: flex;
  gap: 10px;
}

.message-input input {
  flex: 1;
  padding: 10px 15px;
  border-radius: 20px;
  border: 1px solid #ccc;
  outline: none;
}

.message-input button {
  border: none;
  background: #007bff;
  color: white;
  padding: 10px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 18px;
}

.message-input button:hover {
  background: #0056b3;
}

.delete-selected-btn {
  background: #ff4d4f;
  color: white;
  border-radius: 20px;
  border: none;
  padding: 10px 16px;
  cursor: pointer;
}

.delete-selected-btn:hover {
  background: #d9363e;
}
</style>
