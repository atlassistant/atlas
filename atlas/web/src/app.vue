<template>
  <div class="app">
      <div class="app__messages">
        <div v-if="connected" class="app__messages-wrapper">
          <div :class="{ 'app__message': true, 'app__message--self': message.type === 'self', 'app__message--server': message.type !== 'self' }" 
            v-for="message in messages" 
            :key="message.id">
            <p>{{message.text}}</p>
          </div>

          <div class="app__message app__message--server" v-if="working">
            <p>...</p>
          </div>
        </div>
        <p v-else>Disconnected</p>
      </div>

      <form @submit.prevent="handleSubmit" class="app__form">
        <button type="button" class="app__speak-button"><i class="material-icons">mic</i></button>
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
      connected: false,
      working: false,
    };
  },
  mounted() {
    this.socket = io('/');

    this.socket.on('connect', () => {
      this.connected = true;

      this.socket.on('ask', data => {
        this.addMessage({ 
          ...data, 
          type: 'ask',
        });
        this.stopWorking();
      });

      this.socket.on('show', data => this.addMessage({
        ...data, 
        type: 'show',
      }));

      this.socket.on('terminate', this.stopWorking);
    });

    this.socket.on('disconnect', () => this.connected = false);
  },
  methods: {
    updateScroll() {
      setTimeout(() => window.scrollTo(0, document.body.scrollHeight), 50);
    },
    addMessage(msg) {
      this.messages.push({
        ...msg,
        id: this.messages.length,
      });

      this.updateScroll();
    },
    startWorking() {
      this.working = true;

      this.updateScroll();
    },
    stopWorking() {
      this.working = false;

      this.updateScroll();
    },
    handleSubmit() {
      this.addMessage({
        type: 'self',
        text: this.input,
      });
      this.startWorking();
      this.socket.emit('parse', this.input);
      this.input = '';
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
  @include cell();

  &__messages {
    display: flex;
    flex-direction: column;
    padding: baseline();
  }

  &__messages-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: baseline(2.25);
  }

  &__message {
    box-shadow: 0 1px 10px rgba(0,0,0,0.04);
    display: inline-block;
    padding: baseline(0.25) baseline(0.5);
    position: relative;
    margin-bottom: baseline(0.5);
    min-width: 50px;

    &:after {
      content: '';
      position: absolute;
    }

    &--server {
      align-self: flex-end;
      background-color: color(background, 1);
      text-align: right;

      &:after {
        border-top: 10px solid color(background, 1);
        border-left: 50px solid transparent;
        border-right: 0 solid transparent;
        right: 0;
      }
    }

    &--self {
      align-self: flex-start;
      background-color: color(brand);
      color: color(background, 1);

      &:after {
        left: 0;
        border-top: 10px solid color(brand);
        border-left: 0 solid transparent;
        border-right: 50px solid transparent;
      }
    }
  }

  &__form {
    bottom: 0;
    left: 0;
    right: 0;
    margin: baseline();
    margin-left: baseline(2);
    position: fixed;
  }

  &__speak-button {
    background-color: color(brand);
    border: 2px solid color(background, 1);
    border-radius: 50%;
    box-shadow: 0 1px 5px color(brand);
    animation: pulse 2s infinite;
    color: color(background, 1);
    cursor: pointer;
    padding: baseline(0.7);
    position: absolute;
    left: 0;
    top: 50%;
    transition: transform 0.2s;
    transform: translateX(-50%) translateY(-50%);

    &:hover {
      animation: none;
      transform: translateX(-50%) translateY(-50%) scale(1.1);
    }

    & > * {
      position: relative;
      top: 2px;
    }

    &:active {
      transform: translateX(-50%) translateY(-50%);
    }
  }

  &__input {
    background-color: color(background, 1);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12);
    border: 0;
    color: color(text, 1);
    outline: none;
    padding: baseline(0.5) baseline() baseline(0.5) baseline(2);
    width: 100%;
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(color(brand), 0.4);
  }
  70% {
      box-shadow: 0 0 0 10px rgba(color(brand), 0);
  }
  100% {
      box-shadow: 0 0 0 0 rgba(color(brand), 0);
  }
}

</style>

