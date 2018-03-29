<template>
  <div class="app">
      <div class="app__messages">
        <div class="app__message" v-for="message in messages" :key="message">
          <p>{{message}}</p>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="app__form">
        <input type="text" class="app__input" v-model="input" />
      </form>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  name: 'App',
  data() {
    return {
      messages: [],
      input: '',
    };
  },
  mounted() {
    this.socket = io('/ws');
    this.socket.on('ask', data => this.messages.push(data.text));
    this.socket.on('show', data => this.messages.push(data.text));
  },
  methods: {
    handleSubmit() {
      this.socket.emit('parse', this.input);
    }
  }
}
</script>


<style lang="scss">
@import "./_vars.scss";

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  height: 100%;
}

body {
  @include type(body);
  background-color: color(background);
  color: color(text);
  display: flex;
  flex-direction: column;
  font-family: $font-family;
}

.app {
  @include col($x: stretch);
  @include cell();

  &__messages {
    flex: 1;
    padding: baseline();
  }

  &__form {
    margin: baseline();
  }

  &__input {
    background-color: color(background, -1);
    box-shadow: 0 1px 10px rgba(0, 0, 0, 0.12);
    border: 0;
    color: color(text, 1);
    outline: none;
    padding: baseline(0.5) baseline();
    width: 100%;
  }
}

</style>

