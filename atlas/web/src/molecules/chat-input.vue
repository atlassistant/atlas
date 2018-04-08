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
  props: {
    lang: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isListening: false,
    };
  },
  mounted() {
    // this.speaker = new SpeechSynthesisUtterance();
    // this.speaker.lang = 'fr-FR';
    // this.speaker.text = 'Pour quelle ville voulez-vous la météo ?'
    
    // speechSynthesis.speak(this.speaker);

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
  },
  methods: {
    startListening() {
      this.isListening = true;
      this.recognition.start();
    },
    stopListening() {
      this.isListening = false;
      this.recognition.abort();
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

