<template>
  <div class="chat">
    <messages-list class="chat__list" :messages="messages" />
    <chat-input lang="en-US" ref="chatInput" class="chat__input" @input="onInput" />
  </div>
</template>

<script>
import {
  ChatInput,
  MessagesList,
} from './../molecules';
import io from 'socket.io-client';

export default {
  name: 'Chat',
  components: { 
    ChatInput,
    MessagesList,
  },
  data() {
    return {
      messages: [],
    };
  },
  mounted() {
    this.speaker = new SpeechSynthesisUtterance();
    this.speaker.lang = 'fr-FR';

    this.socket = io();
    this.socket.on('ask', (data) => this.processMessage(data, true));
    this.socket.on('show', (data) => this.processMessage(data));
    this.socket.on('terminate', () => this.$refs.chatInput.stopListening());
  },
  methods: {
    onInput(text) {
      this.messages.push({
        client: true,
        id: this.messages.length,
        text,
      });
      this.socket.emit('parse', text);
    },
    processMessage(data, requiresUserInput) {
      this.messages.push({
        id: this.messages.length,
        ...data,
      });

      if (data.text) {
        this.speaker.text = data.text;

        if (requiresUserInput) {
          this.speaker.onend = () => {
            this.$refs.chatInput.startListening();
            this.speaker.onend = null;
          };
        }
        speechSynthesis.speak(this.speaker);
      }
    },
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

// Inspired by https://dribbble.com/shots/4026475--Exploration-Online-Learning-for-Student-Chat/attachments/922446

.chat {
  @include col($x: stretch);
  flex: 1;

  &__list {
    flex: 1;
  }
}
</style>
