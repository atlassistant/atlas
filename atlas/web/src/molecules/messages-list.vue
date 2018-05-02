<template>
  <pop-group class="messages-list">
    <message v-for="item in messages" :key="item.id" :text="item.text" :client="item.client" />
    <message v-if="showThinking" text="..." :key="0" />
  </pop-group>
</template>

<script>
import {
  PopGroup,
} from './../transitions';
import {
  Message,
} from './../atoms';

export default {
  name: 'MessagesList',
  components: { 
    Message,
    PopGroup,
  },
  mounted() {
    this.$el.addEventListener('DOMNodeInserted', 
      () => this.$el.scroll({ 
        top: this.$el.scrollHeight,
        behavior: 'smooth',
      }));
  },
  props: {
    messages: Array,
    showThinking: Boolean,
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.messages-list {
  @include col($x: flex-start);
  overflow: auto;
  padding: baseline(1);
  padding-bottom: 0;
}
</style>


