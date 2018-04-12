<template>
  <pop-group class="messages-list">
    <message v-for="item in messages" :key="item.id" :text="item.text" :client="item.client" />
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
  props: {
    messages: Array,
  },
  watch: {
    messages() {
      setTimeout(() => this.$el.scrollTo(0, this.$el.scrollHeight), 50);
    },
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


