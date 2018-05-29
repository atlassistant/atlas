<template>
  <div v-if="isConnected" class="chat">
    <messages-list 
      @choose="parse" 
      v-if="messages.length" 
      :show-thinking="isThinking" 
      class="chat__list" 
      :messages="messages" />
    <blankslate v-else icon="explore">
      Looks like you do not have an history yet!<br />Start chatting with your assistant!
    </blankslate>
    <chat-input
      ref="chatInput"
      class="chat__input"
      @input="parse"
      @listen="listen"
      @settings="$router.push({ name: 'intents' })"
      @switch="switchToTextInput"
      :is-text-input="isTextInput"
      :is-listening="isListening" />
  </div>
  <blankslate v-else icon="network_check">
    Connecting to your assistant
  </blankslate>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { actions } from './../store';
import {
  MessagesList,
  Blankslate,
} from './../molecules';
import {
  ChatInput,
} from './../organisms';

export default {
  name: 'Chat',
  components: {
    Blankslate,
    ChatInput,
    MessagesList,
  },
  computed: {
    ...mapGetters([
        'messages', 'isConnected', 'isListening', 'isTextInput', 'isThinking',
    ]),
  },
  methods: {
    ...mapActions([actions.parse.name, actions.listen.name, actions.switchToTextInput.name]),
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

  &__notice {
    @include type(tiny);
    background-color: color(info);
    color: color(text-inverse);
    padding: baseline(0.5);
    text-align: center;
  }
}
</style>
