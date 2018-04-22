<template>
  <div class="chat">
    <messages-list v-if="messages.length" :show-thinking="isThinking" class="chat__list" :messages="messages" />
    <blankslate v-else icon="explore">
      Looks like you do not have an history yet!<br />Start chatting with your assistant!
    </blankslate>
    <chat-input :lang="lang" ref="chatInput" class="chat__input" @input="onInput" />
  </div>
</template>

<script>
import {
  MessagesList,
  Blankslate,
} from './../molecules';
import {
  ChatInput,
} from './../organisms';
import io from 'socket.io-client';

export default {
  name: 'Chat',
  components: {
    Blankslate,
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
    this.socket.on('work', () => this.onWork());
  },
  methods: {
    onInput(text) {
      this.messages.push({
        client: true,
        id: this.messages.length + 1,
        text,
      });

      this.socket.emit('parse', text);
    },
    onWork() {
      this.isThinking = true;
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
