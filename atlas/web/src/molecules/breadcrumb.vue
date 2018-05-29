<template>
  <div class="breadcrumb">
    <content-wrapper>
      <router-link class="breadcrumb__link" v-for="(crumb, key) in $breadcrumbs.slice(0, -1)" :key="key" :to="crumb.path">
        <span class="breadcrumb__separator" v-if="key">/</span>{{crumb.meta.breadcrumb}}
      </router-link>
      <div class="breadcrumb__current">
        {{$breadcrumbs.slice(-1)[0].meta.breadcrumb}}
      </div>

    </content-wrapper>
  </div>
</template>

<script>
import {
  ContentWrapper,
} from './../atoms';
export default {
  name: 'Breadcrumb',
  components: {
    ContentWrapper,
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.breadcrumb {
  background-color: color(background);
  padding: baseline(0.5) 0 baseline(1) 0;

  &__link {
    @include type(small);
  }

  &__separator {
    @include type(small);
    color: color(text, 1);
    margin: 0 baseline(0.25);
  }

  &__current {
    font-weight: bold;
  }
}
</style>

