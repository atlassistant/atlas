<template>
  <div class="topbar">
    <content-wrapper class="topbar__content">
      <router-link to="/" class="topbar__brand">
        <img class="topbar__logo" src="/public/favicon-32x32.png" alt="atlas logo" />
        atlas
        <span class="topbar__version">v{{version}}</span>
      </router-link>

      <div class="topbar__links">
        <router-link :to="{ name: 'intents' }" class="topbar__link">comprehension</router-link>
        <router-link :to="{ name: 'skills' }" class="topbar__link">execution</router-link>
        <router-link :to="{ name: 'intents' }" class="topbar__link">settings</router-link>
      </div>
    </content-wrapper>
  </div>
</template>

<script>
import {
  ContentWrapper,
} from './../atoms';

export default {
  name: 'Topbar',
  components: {
    ContentWrapper,
  },
  data() {
    return {
      version: window.VERSION,
    };
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.topbar {
  background-color: color(brand);

  &__content {
    @include row($y: center);
  }

  &__brand {
    @include row($y: center);
    @include link(color(text-inverse));
    display: inherit !important;
    font-weight: bold;
    margin-right: baseline();
    padding: baseline(0.5) 0;
  }

  &__version {
    @include type(tiny);
    background-color: color(brand, 1);
    border-radius: $border-radius;
    display: block;
    margin-left: baseline(0.25);
    padding: 0 baseline(0.25);
  }

  &__logo {
    margin-right: baseline(0.5);
  }

  &__link {
    @include link(color(text-inverse, 1), color(text-inverse));
    padding: baseline(0.5) baseline(0.25);
  }
}

</style>

