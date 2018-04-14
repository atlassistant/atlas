<template>
  <div class="chat">
    <messages-list :show-thinking="isThinking" class="chat__list" :messages="messages" />
    <chat-input :lang="lang" ref="chatInput" class="chat__input" @input="onInput" />
  </div>
</template>

<script>
import {
  MessagesList,
} from './../molecules';
import {
  ChatInput,
} from './../organisms';
import io from 'socket.io-client';

export default {
  name: 'Chat',
  components: {
    ChatInput,
    MessagesList,
  },
  data() {
    return {
      isThinking: false,
      lang: window.LANG,
      messages: [],
    };
  },
  mounted() {
    this.speaker = new SpeechSynthesisUtterance();
    this.speaker.lang = this.lang;

    this.socket = io();
    this.socket.on('ask', (data) => this.processMessage(data, true));
    this.socket.on('show', (data) => this.processMessage(data));
    this.socket.on('terminate', () => this.onTerminate());
  },
  methods: {
    onInput(text) {
      this.messages.push({
        client: true,
        id: this.messages.length + 1,
        text,
      });
      this.isThinking = true;
      this.socket.emit('parse', text);
    },
    onTerminate() {
      this.$refs.chatInput.stopListening();
      this.isThinking = false;
    },
    processMessage(data, requiresUserInput) {
      this.messages.push({
        id: this.messages.length + 1,
        ...data,
      });

      if (data.text) {
        this.speaker.text = data.text;

        if (requiresUserInput) {
          this.isThinking = false;
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
  overflow: hidden;
  flex: 1;

  &__list {
    flex: 1;
  }
}
</style>
