<template>
  <input type="text" :class="{ 
    'textinput': true,
    'textinput--borderless': borderless,
  }" 
    @input="$emit('input', $event.target.value)" :value="value" 
    @blur="$emit('blur', $event)"
  />
</template>

<script>
export default {
  name: 'TextInput',
  props: {
    borderless: Boolean,
    value: String,
  },
  methods: {
    focus() {
      this.$el.focus();
    },
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.textinput {
  @include type(body);

  color: color(text);
  outline: none;
  padding: baseline(0.5);
  width: 100%;

  &--borderless {
    border: 0;
  }
}
</style>


