<template>
  <div :class="{ 
    'message': true,
    'message--server': !client,
    'message--client': client,
  }">
    {{text}}
  </div>
</template>

<script>
export default {
  name: 'Message',
  props: {
    text: {
      type: String,
      required: true,
    },
    client: Boolean,
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.message {
  background-color: color(background, 1);
  box-shadow: 0 0 10px color(shadow);
  padding: baseline(0.5);
  position: relative;
  margin-bottom: baseline(1);
  transition: all 0.2s;

  &:after { 
    box-shadow: 0 0 10px color(shadow);
    content: '';
    position: absolute;
    bottom: 0;
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-top-color: color(background, 1);
    border-bottom: 0;
    border-left: 0;
    margin-bottom: -9px;
  }

  &--server {
    &:after {
      left: 0;
    }
  }

  &--client {
    align-self: flex-end;
    background-color: color(brand);
    color: color(text-inverse);

    &:after {
      border: 10px solid transparent;
      border-top-color: color(brand);
      border-bottom: 0;
      border-right: 0;
      right: 0;
    }
  }
}
</style>
