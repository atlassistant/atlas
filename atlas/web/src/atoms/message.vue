<template>
  <div :class="{ 
    'message': true,
    'message--server': !client,
    'message--client': client,
  }">
    <div class="message__content">
      {{text}}
    </div>
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
  &__content {
    background-color: color(background, 1);
    box-shadow: 0 0 10px color(shadow);
    border-radius: $border-radius;
    border-bottom-left-radius: 0;
    padding: baseline(0.5);
    position: relative;
    margin-bottom: baseline(0.5);
    transition: all 0.2s;
  }

  &--server &__content {
    border: 1px solid color(divider);
  }

  &--client {
    align-self: flex-end;

    .message__content {
      background-color: color(brand);
      border-bottom-left-radius: $border-radius;
      border-bottom-right-radius: 0;
      color: color(text-inverse);
    }
  }

  &:last-child &__content {
    margin-bottom: baseline();
  }
}
</style>
