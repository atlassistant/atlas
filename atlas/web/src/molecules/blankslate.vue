<template>
  <div class="blankslate">
    <div class="blankslate__content">
      <icon class="blankslate__icon" :name="icon" />
      <div class="blankslate__message">
        <slot />
      </div>
    </div>
  </div>
</template>

<script>
import {
  Icon,
} from './../atoms';

export default {
  name: 'Blankslate',
  props: {
    icon: {
      type: String,
      required: true,
    },
  },
  components: {
    Icon,
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.blankslate {
  @include col($x: center, $y: center);
  flex: 1;

  &__content {
    @include col($x: center);
    margin: baseline();
  }

  &__icon {
    color: color(icon, 1);
    font-size: 4rem;
  }

  &__message {
    color: color(text, 1);
    margin: baseline(0.5) 0;
    text-align: center;
  }
}
</style>


