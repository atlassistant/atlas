<template>
  <div class="messages-list">
    <message v-for="item in messages" :key="item.id" :text="item.text" />
  </div>
</template>

<script>
import {
  Message,
} from './../atoms';

export default {
  name: 'MessagesList',
  components: { 
    Message,
  },
  props: {
    messages: Array,
  },
}
</script>

