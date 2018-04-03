<template>
  <div class="chat">
    <messages-list class="chat__list" />
    <chat-input class="chat__input" />
  </div>
</template>

<script>
import {
  ChatInput,
  MessagesList,
} from './../molecules';

export default {
  name: 'Chat',
  components: { 
    ChatInput,
    MessagesList,
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
