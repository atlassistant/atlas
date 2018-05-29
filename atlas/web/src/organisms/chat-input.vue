<template>
  <div class="chat-input">
    <form v-if="isTextInput" class="chat-input__form" @submit.prevent="sendParse">
      <text-input ref="input" borderless v-model="text" placeholder="What can I do for you?" />
    </form>
    <icon-button name="keyboard" secondary v-else @click.prevent="$emit('switch')" />

    <icon-button v-if="!isListening" name="mic" @click.prevent="$emit('listen')" />
    <spinner v-else />

    <icon-button name="settings" secondary v-if="!isTextInput" @click.prevent="$emit('settings')" />
  </div>
</template>

<script>
import {
  IconButton,
} from './../molecules';
import {
  Spinner,
  TextInput,
} from './../atoms';

export default {
  name: 'ChatInput',
  components: {
    IconButton,
    TextInput,
    Spinner,
  },
  props: {
    isListening: {
      type: Boolean,
      required: true,
    },
    isTextInput: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      text: '',
    };
  },
  methods: {
    sendParse() {
      if (!this.text) {
        return;
      }
      
      this.$emit('input', this.text);
      this.text = '';
    },
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.chat-input {
  @include row($x: space-between, $y: center);

  background-color: color(background, 1);
  border-top: 1px solid color(divider);
  box-shadow: 0 0 10px color(shadow);
  padding: baseline(0.5);

  &__form {
    flex: 1;
  }
}
</style>

