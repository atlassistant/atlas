<template>
  <div class="chat-input">
    <form v-if="isTextInput" class="chat-input__form" @submit.prevent="sendParse">
      <text-input ref="input" borderless v-model="text" placeholder="What can I do for you?" />
    </form>
    <icon-button name="keyboard" secondary v-else @click.prevent="switchToTextInput" />

    <icon-button v-if="!isListening" name="mic" @click.prevent="startListening" />
    <spinner v-else />

    <icon-button name="settings" secondary v-if="!isTextInput" />
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
    lang: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      text: '',
      isListening: false,
      isTextInput: false,
    };
  },
  mounted() {
    // this.speaker = new SpeechSynthesisUtterance();
    // this.speaker.lang = 'fr-FR';
    // this.speaker.text = 'Pour quelle ville voulez-vous la météo ?'
    
    // speechSynthesis.speak(this.speaker);

    if ('webkitSpeechRecognition' in window) {
      this.recognition = new webkitSpeechRecognition();
      this.recognition.lang = this.lang;
      this.recognition.onresult = (evt) => {
        this.isListening = false;

        if (evt.results.length > 0) {
          const r = evt.results[0];

          if (r.length > 0 && r.isFinal) {
            this.$emit('input', r[0].transcript);
          }
        }
      }
    }
  },
  methods: {
    sendParse() {
      this.$emit('input', this.text);
      this.text = '';
    },
    switchToTextInput() {
      this.text = '';
      this.stopListening();
      this.isTextInput = true;
    },
    startListening() {
      this.isTextInput = false;
      this.isListening = true;

      if (this.recognition) {
        this.recognition.start();
      }
    },
    stopListening() {
      this.isListening = false;

      if (this.recognition) {
        this.recognition.abort();
      }
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

