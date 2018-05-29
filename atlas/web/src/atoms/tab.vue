<template>
  <router-link v-if="to" class="tab" :to="to" active-class="tab--active">
    <icon v-if="icon" class="tab__icon" :name="icon" />
    {{text}}
    <span v-if="count !== undefined" class="tab__badge">{{count}}</span>
  </router-link>
  <div v-else class="tab">
    {{text}}
    <span v-if="count !== undefined" class="tab__badge">{{count}}</span>
  </div>
</template>

<script>
import Icon from './icon.vue';

export default {
  name: 'Tab',
  components: {
    Icon,
  },
  props: {
    to: [Object, String],
    count: Number,
    icon: String,
    text: {
      type: String,
      required: true,
    },
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.tab {
  @include link(color(text));
  @include row($y: center);
  border: 1px solid transparent;
  border-top: 3px solid transparent;
  display: flex !important;
  cursor: pointer;
  padding: baseline(0.3) baseline(0.5);
  position: relative;
  top: 1px;

  &__badge {
    @include type(tiny);
    background-color: color(background, -1);
    border-radius: $border-radius;
    margin-left: baseline(0.25);
    display: block;
    padding: 0 baseline(0.25);
  }

  &__icon {
    @include type(body);
    color: color(icon, 1);
    margin-right: baseline(0.25);
  }

  &--active {
    background-color: color(background, 1);
    border: 1px solid color(divider);
    border-top: 3px solid color(accent);
    border-bottom-color: color(background, 1);
    border-radius: $border-radius;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;

    .tab__icon {
      color: color(text);
    }
  }
}
</style>

