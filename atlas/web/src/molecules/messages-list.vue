<template>
  <pop class="messages-list">
    <message v-for="item in messages" :key="item.id" :text="item.text" :client="item.client" />
  </pop>
</template>

<script>
import {
  Pop,
} from './../transitions';
import {
  Message,
} from './../atoms';

export default {
  name: 'MessagesList',
  components: { 
    Message,
    Pop,
  },
  props: {
    messages: Array,
  },
  watch: {
    messages() {
      // TODO, scroll to bottom !
    }
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.messages-list {
  @include col($x: flex-start);
  overflow: auto;
  padding: baseline(1);
}
</style>


