<template>
  <div :class="{ 
    'message': true,
    'message--has-choices': choices,
    'message--server': !client,
    'message--client': client,
  }">
    <div class="message__content">
      {{text}}
    </div>
    <div class="message__choices" v-if="choices && current">
      <button 
        class="message__choice"
        v-for="choice in choices"
        :key="choice"
        @click.prevent="$emit('choose', choice)">
        {{choice}}
      </button>
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
    choices: {
      type: Array,
      default: null,
    },
    current: Boolean,
    client: Boolean,
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.message {
  @include col();
  @include cell($grow: 0, $shrink: 0);
  transition: all 0.2s;
  
  &__content {
    background-color: color(background, 1);
    box-shadow: 0 0 10px color(shadow);
    border-radius: $border-radius;
    border-bottom-left-radius: 0;
    padding: baseline(0.5);
    position: relative;
    margin-bottom: baseline(0.5);
  }

  &__choices {
    @include row($wrap: nowrap);
    align-self: flex-end;
    margin-bottom: baseline(0.5);
    overflow-x: auto;
  }

  // TODO export it in its own file

  &__choice {
    @include cell($grow: 0, $shrink: 0);
    background: transparent;
    border: 1px solid color(brand);
    border-radius: $border-radius;
    cursor: pointer;
    color: color(brand);
    font-weight: bold;
    outline: none;
    padding: baseline(0.5);
    transition: all 0.2s;

    &:active,
    &:focus {
      box-shadow: 0 0 10px color(brand);
    }

    &:hover {
      background-color: color(brand);
      color: color(text-inverse);
    }

    &:active {
      transform: scale(0.8);
    }

    & + & {
      margin-left: baseline(0.5);
    }
  }

  &--server &__content {
    border: 1px solid color(divider);
  }

  &--client {
    .message__content {
      align-self: flex-end;
      background-color: color(brand);
      border-bottom-left-radius: $border-radius;
      border-bottom-right-radius: 0;
      color: color(text-inverse);
    }
  }

  &:last-child &__content,
  &:last-child &__choices {
    margin-bottom: baseline();
  }

  &:last-child.message--has-choices &__content {
    margin-bottom: baseline(0.5);
  }
}
</style>
