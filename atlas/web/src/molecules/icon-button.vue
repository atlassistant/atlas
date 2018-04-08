<template>
  <button 
    :class="{ 
      'icon-button': true, 
      'icon-button--brand': brand,
      'icon-button--accent': accent,
      'icon-button--secondary': secondary,
    }"
    @click="$emit('click', $event)"
  >
    <icon :name="name" />
  </button>
</template>

<script>
import {
  Icon,
} from './../atoms';

export default {
  name: 'IconButton',
  components: {
    Icon,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
    brand: {
      type: Boolean,
      default: true,
    },
    accent: Boolean,
    secondary: Boolean,
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.icon-button {
  background-color: transparent;
  border: 0;
  cursor: pointer;
  outline: none;
  padding: baseline(0.5);
  transition: all 0.2s;

  &:active {
    transform: scale(0.8);
  }

  &--brand {
    color: color(brand);

    &:hover,
    &:focus {
      color: color(brand, -1);
    }
  }

  &--accent {
    color: color(accent);

    &:hover,
    &:focus {
      color: color(accent, -1);
    }
  }

  &--secondary {
    color: color(icon, 1);

    &:hover,
    &:focus {
      color: color(icon);
    }
  }
}

</style>

