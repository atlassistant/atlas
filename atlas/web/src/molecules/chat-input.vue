<template>
  <div class="chat-input">
    <icon-button name="keyboard" secondary />

    <icon-button v-if="!isListening" name="mic" @click.prevent="startListening" />
    <spinner v-else />

    <icon-button name="settings" secondary />
  </div>
</template>

<script>
import IconButton from './icon-button.vue';
import {
  Spinner,
} from './../atoms';

export default {
  name: 'ChatInput',
  components: {
    IconButton,
    Spinner,
  },
  data() {
    return {
      isListening: false,
    };
  },
  methods: {
    startListening() {
      this.isListening = true;
    },
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.chat-input {
  @include row($x: space-between);

  background-color: color(background, 1);
  box-shadow: 0 0 10px color(shadow);
  padding: baseline(0.5);
}
</style>

